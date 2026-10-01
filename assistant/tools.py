from dataclasses import dataclass, field
from typing import Any, Callable

from cart.tools import (
    get_cart_tool,
    add_to_cart_tool,
    remove_from_cart_tool,
    clear_cart_tool,
    update_cart_quantity_tool,
    reorder_tool,
    get_customer_profile_tool,
    update_customer_profile_tool,
)

from products.tools import (
    search_products_tool,
    get_product_description_tool,
    search_delivered_products_tool,
)

from orders.tools import (
    delete_order_tool,
    get_user_orders_tool,
)

from .product_resolver import resolve_product


def help_tool():
    return {"success": True, "action": "help", "message": "I can help with products, cart operations, orders, delivery, account details, recommendations, and store FAQs."}


def get_recommendations_tool(request=None, limit=6):
    if request is None:
        return {"success": False, "message": "A Django request is required."}
    from recommendations.views import get_recommended_products
    products = get_recommended_products(request, limit=int(limit))
    return {
        "success": True,
        "action": "recommend_products",
        "recommendations": [{"id": p.id, "name": p.name, "price": str(p.price), "category": p.category.name if p.category else None, "image": p.image.url if p.image else None, "url": p.get_absolute_url(), "stock_count": p.stock_count} for p in products],
        "message": f"Here are {len(products)} recommendations for you.",
    }


# =========================================================
# FAQ TOOL FUNCTION
# =========================================================

def faq_tool(message):
    from intents.models import Intent

    FAQ_ALIASES = {
        "FAQ_SHIPPING": ("shipping", "delivery time", "delivery times", "how long", "shipping kitni der", "delivery kitni der"),
        "FAQ_RETURNS": ("return", "returns", "send back"),
        "FAQ_REFUNDS": ("refund", "money back", "paise wapas"),
        "FAQ_PAYMENT": ("payment", "pay", "card", "cash on delivery"),
        "FAQ_CANCELLATION": ("cancel order", "cancellation", "cancel karna"),
        "FAQ_TRACKING": ("track order", "order tracking", "where is my order"),
        "FAQ_ACCOUNT": ("account", "profile", "address", "mera address"),
    }

    DEFAULT_FAQ = {
        "FAQ_SHIPPING": "Standard delivery usually takes 5 to 7 days.",
        "FAQ_RETURNS": "Returns are handled through customer support after reviewing the order.",
        "FAQ_REFUNDS": "Refunds are reviewed after an eligible return is accepted.",
        "FAQ_PAYMENT": "Payments are currently recorded through the checkout payment flow.",
        "FAQ_CANCELLATION": "Processing orders can be cancelled before they are shipped.",
        "FAQ_TRACKING": "You can track an order by providing its order number.",
        "FAQ_ACCOUNT": "You can view and update your profile and shipping address after logging in.",
    }

    text = (message or "").lower().strip()
    for intent_name, aliases in FAQ_ALIASES.items():
        if any(alias in text for alias in aliases):
            database_intent = Intent.objects.filter(intent_name=intent_name, is_active=True).first()
            answer = database_intent.response if database_intent else DEFAULT_FAQ[intent_name]
            return {"success": True, "tool": "faq_tool", "intent": intent_name, "message": answer, "data": {"faq": answer}}
    return {"success": True, "tool": "faq_tool", "message": "I can help answer your questions about shipping, returns, refunds, payments, and account details.", "data": {"faq": None}}


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(
        default_factory=dict
    )


TOOL_REGISTRY: dict[str, Callable] = {
    # =========================================================
    # CART TOOLS
    # =========================================================

    "get_cart_tool": get_cart_tool,
    "add_to_cart_tool": add_to_cart_tool,
    "remove_from_cart_tool": remove_from_cart_tool,
    "clear_cart_tool": clear_cart_tool,
    "update_cart_quantity_tool": update_cart_quantity_tool,
    "reorder_tool": reorder_tool,

    # =========================================================
    # CUSTOMER PROFILE TOOLS
    # =========================================================

    "get_customer_profile_tool": get_customer_profile_tool,
    "update_customer_profile_tool": update_customer_profile_tool,

    # =========================================================
    # PRODUCT TOOLS
    # =========================================================

    "search_products_tool": search_products_tool,
    "get_product_description_tool": get_product_description_tool,
    "resolve_product": resolve_product,
    "search_delivered_products_tool": search_delivered_products_tool,

    # =========================================================
    # ORDER TOOLS & OTHERS
    # =========================================================

    "get_user_orders_tool": get_user_orders_tool,
    "delete_order_tool": delete_order_tool,
    "help_tool": help_tool,
    "get_recommendations_tool": get_recommendations_tool,
    "faq_tool": faq_tool,
}


def execute_tool(
    tool_call: ToolCall,
    *,
    request,
    user,
):
    """
    Execute a deterministic tool call.

    No external LLM is involved.

    Product tools operate independently from
    the Django request.

    Cart and profile tools receive the request because the
    underlying implementation depends on the
    authenticated request/session.

    Order tools receive the authenticated user
    because the existing order implementation
    restricts access to that user's orders.
    """

    tool = TOOL_REGISTRY.get(
        tool_call.name
    )

    if tool is None:
        return {
            "success": False,
            "message": (
                f"Unknown tool: {tool_call.name}"
            ),
        }

    arguments = dict(
        tool_call.arguments
    )

    # =========================================================
    # ADD TO CART
    # =========================================================

    if tool_call.name == "add_to_cart_tool":

        product_name = arguments.pop(
            "product_name",
            None,
        )

        if product_name:

            resolved = resolve_product(
                product_name
            )

            if not resolved["success"]:
                return resolved

            arguments["product_id"] = (
                resolved["product_id"]
            )

    # =========================================================
    # PRODUCT TOOLS
    # =========================================================

    if tool_call.name in {
        "search_products_tool",
        "get_product_description_tool",
        "resolve_product",
    }:

        return tool(
            **arguments
        )

    # =========================================================
    # ORDER TOOLS & USER-SPECIFIC TOOLS
    # =========================================================

    if tool_call.name == "get_user_orders_tool":

        return tool(
            user=user,
            **arguments
        )

    if tool_call.name == "delete_order_tool":
        return tool(user=user, **arguments)

    if tool_call.name == "search_delivered_products_tool":
        return tool(user=user, **arguments)

    if tool_call.name == "help_tool":
        return tool()

    if tool_call.name == "get_recommendations_tool":
        return tool(request=request, **arguments)

    if tool_call.name == "faq_tool":
        # faq_tool expects a message string; we pass arguments.get("message") or arguments.get("intent")
        message = arguments.get("message") or arguments.get("intent", "")
        return tool(message=message)

    # =========================================================
    # CART & PROFILE TOOLS
    # =========================================================

    return tool(
        request=request,
        **arguments,
    )