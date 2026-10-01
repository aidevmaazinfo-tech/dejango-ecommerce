from .faq import faq_tool
from .normalizer import normalize_command
from .parser import parse_command
from .tools import ToolCall, execute_tool

STATE_KEY = "deterministic_customer_agent"


def _standard_result(tool_name, result, intent=None):
    result = result if isinstance(result, dict) else {}
    data = dict(result)
    message = data.pop("message", "")
    success = bool(data.pop("success", False))

    if not message and success:
        if data.get("products"):
            message = f"I found {len(data['products'])} product(s) for you."
        elif data.get("product"):
            message = "Here are the product details."
        elif data.get("cart"):
            message = "Here is what is currently in your cart."
        elif data.get("orders"):
            message = f"Here are your {len(data['orders'])} order(s)."
        elif data.get("order"):
            message = "Here are the details for your order."
        elif data.get("recommendations"):
            message = "Here are some products you may like."
        else:
            message = "Your request was completed."
    return {
        "success": success,
        "tool": tool_name,
        "intent": intent,
        "message": message,
        "data": data,
        "requires_confirmation": bool(data.get("confirmation_required", False)),
        "navigation": result.get("navigation"),
        "redirect_url": result.get("redirect_url"),
    }


def _payload(result):
    data = result["data"]
    return {
        "answer": result["message"],
        "type": "assistant",
        "intent": result["intent"],
        "tool": result["tool"],
        "success": result["success"],
        "requires_confirmation": result.get("requires_confirmation", False),
        "data": data,
        "products": data.get("products", []),
        "product": data.get("product"),
        "orders": data.get("orders", []),
        "order": data.get("order"),
        "cart": data.get("cart"),
        "recommendations": data.get("recommendations", []),
        "navigation": result.get("navigation"),
        "redirect_url": result.get("redirect_url"),
    }


def process_customer_message(request, message):
    text = normalize_command(message)
    state = request.session.get(STATE_KEY, {})

    # ==========================================
    # 1. HANDLE CONFIRMATION STATE (YES / NO)
    # ==========================================
    if state.get("kind") == "cancel_confirmation":
        if text in {"yes", "y", "haan", "ji haan", "confirm", "yes cancel", "yes cancel it"}:
            order_id = state["order_id"]
            request.session.pop(STATE_KEY, None)
            
            # Execute tool with confirmed=True to trigger actual cancellation & stock restoration
            result = execute_tool(
                ToolCall("get_user_orders_tool", {"action": "cancel", "cancel_order_id": order_id, "confirmed": True}), 
                request=request, 
                user=request.user
            )
            return _payload(_standard_result("cancel_order", result, "ORDER_CANCEL"))
        
        if text in {"no", "n", "nahin", "cancel nahi", "keep it", "no keep it"}:
            request.session.pop(STATE_KEY, None)
            return {
                "answer": "Okay, I will keep the order unchanged.", 
                "type": "assistant", 
                "intent": "ORDER_CANCEL", 
                "success": True, 
                "requires_confirmation": False, 
                "data": {}, "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
            }
            
        return {
            "answer": "Please answer yes to cancel the order or no to keep it.", 
            "type": "confirmation", 
            "intent": "ORDER_CANCEL", 
            "success": True, 
            "requires_confirmation": True, 
            "data": {"order_id": state["order_id"]}, 
            "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
        }

    # ==========================================
    # 2. HANDLE ORDER ID INPUT FOR CANCELLATION
    # ==========================================
    if state.get("kind") == "cancel_awaiting_id":
        digits = "".join([char for char in text if char.isdigit()])
        if digits:
            order_id = int(digits)
            
            # Call tool with action='cancel' and confirmed=False to check validity & fetch order details
            result = execute_tool(
                ToolCall("get_user_orders_tool", {"action": "cancel", "cancel_order_id": order_id, "confirmed": False}), 
                request=request, 
                user=request.user
            )
            
            if not result.get("success"):
                # Order not found, already cancelled, or already shipped/delivered
                request.session.pop(STATE_KEY, None)
                return {
                    "answer": result.get("message", "This order cannot be cancelled."),
                    "type": "assistant",
                    "intent": "ORDER_CANCEL",
                    "success": False,
                    "requires_confirmation": False,
                    "data": result,
                    "products": [], "orders": [], "order": result.get("order"), "cart": None, "recommendations": []
                }
            
            # If valid and confirmation required, display order card and confirmation buttons
            if result.get("confirmation_required"):
                request.session[STATE_KEY] = {"kind": "cancel_confirmation", "order_id": order_id}
                order = result.get("order")
                return {
                    "answer": result.get("message", f"Are you sure you want to cancel Order #{order_id}?"), 
                    "type": "confirmation", 
                    "intent": "ORDER_CANCEL", 
                    "success": True, 
                    "requires_confirmation": True, 
                    "data": result, 
                    "products": [], "orders": [order] if order else [], "order": order, "cart": None, "recommendations": []
                }
        
        return {
            "answer": "I couldn't find an order with that ID. Please provide a valid order ID/number you wish to cancel.", 
            "type": "order_selection", 
            "intent": "ORDER_CANCEL", 
            "success": True, 
            "requires_confirmation": False, 
            "data": {}, 
            "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
        }

    # ==========================================
    # 3. HANDLE "SHOW DELIVERED PRODUCTS" INTENT
    # ==========================================
    delivered_phrases = {"delivered product", "delivered items", "products delivered", "what was delivered", "delivered products"}
    if any(phrase in text for phrase in delivered_phrases):
        if not request.user.is_authenticated:
            return {
                "answer": "Please log in to view your delivered products.",
                "type": "assistant",
                "intent": "DELIVERED_PRODUCTS",
                "success": False,
                "requires_confirmation": False,
                "data": {}, "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
            }
            
        result = execute_tool(ToolCall("search_delivered_products_tool", {}), request=request, user=request.user)
        return _payload(_standard_result("search_delivered_products_tool", result, "DELIVERED_PRODUCTS"))

    # ==========================================
    # 4. INITIAL PARSE WITH SESSION CONTEXT (FIXED)
    # ==========================================
    context = {
        "last_search_results": request.session.get("last_search_results", [])
    }
    tool_call = parse_command(text, context=context)
    
    # User wants to cancel, ask them to provide the order ID directly without buttons
    if tool_call.name == "get_user_orders_tool" and tool_call.arguments.get("action") == "cancel" and not tool_call.arguments.get("cancel_order_id"):
        request.session[STATE_KEY] = {"kind": "cancel_awaiting_id"}
        return {
            "answer": "Please provide the order ID/number you would like to cancel.",
            "type": "order_selection",
            "intent": "ORDER_CANCEL",
            "success": True,
            "requires_confirmation": False,
            "data": {},
            "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
        }

    # ==========================================
    # 5. FALLBACK TO STANDARD TOOL EXECUTION
    # ==========================================
    if tool_call.name == "unknown":
        faq_result = faq_tool(text)
        if faq_result:
            return {
                "answer": faq_result["message"], 
                "type": "faq", 
                "intent": faq_result["intent"], 
                "tool": "faq_tool", 
                "success": True, 
                "requires_confirmation": False, 
                "data": faq_result["data"], 
                "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
            }
        return {
            "answer": "I can help with products, your cart, orders, delivery, account details, recommendations, and store FAQs.", 
            "type": "unknown", 
            "intent": "UNKNOWN", 
            "success": False, 
            "requires_confirmation": False, 
            "data": {}, "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
        }

    result = execute_tool(tool_call, request=request, user=request.user)
    
    # Save search results in session so subsequent context turns ("add the first one") work in the chatbot
    if tool_call.name == "search_products_tool" and result.get("success"):
        request.session["last_search_results"] = result.get("products", [])
    
    if tool_call.name == "get_user_orders_tool" and tool_call.arguments.get("action") == "cancel" and result.get("confirmation_required"):
        request.session[STATE_KEY] = {"kind": "cancel_confirmation", "order_id": result["order_id"]}
        
    if tool_call.name == "search_products_tool" and not result.get("success"):
        faq_result = faq_tool(text)
        if faq_result:
            return {
                "answer": faq_result["message"], 
                "type": "faq", 
                "intent": faq_result["intent"], 
                "tool": "faq_tool", 
                "success": True, 
                "requires_confirmation": False, 
                "data": faq_result["data"], 
                "products": [], "orders": [], "order": None, "cart": None, "recommendations": []
            }
            
    return _payload(_standard_result(tool_call.name, result, tool_call.name.upper().replace("_TOOL", "")))