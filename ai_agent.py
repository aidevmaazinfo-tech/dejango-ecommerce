# import json
# import logging
# import traceback

# from django.conf import settings

# from groq import (
#     Groq,
#     APIError,
#     RateLimitError,
#     APIConnectionError,
# )

# from products.tools import (
#     search_products_tool,
#     get_product_description_tool,
# )

# from orders.tools import (
#     get_user_orders_tool,
#     execute_get_user_orders,
# )

# from cart.tools import (
#     get_cart_tool,
#     add_to_cart_tool,
#     remove_from_cart_tool,
#     clear_cart_tool,
#     update_cart_quantity_tool,
# )

# from cart.cart import Cart


# logger = logging.getLogger(__name__)


# # ============================================================
# # GROQ TOOL SCHEMAS
# # ============================================================

# TOOLS_SCHEMA = [

#     # ========================================================
#     # PRODUCT SEARCH
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "search_products_tool",

#             "description": (
#                 "ONLY use this tool when the user is actually "
#                 "searching, browsing, comparing, or asking to "
#                 "find products available in the store. "
#                 "DO NOT use this tool when the user is asking "
#                 "for the description or details of one specific "
#                 "product."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "The product search terms.",
#                     },

#                     "min_price": {
#                         "type": ["number", "null"],
#                         "description": "Minimum price if specified.",
#                     },

#                     "max_price": {
#                         "type": ["number", "null"],
#                         "description": "Maximum price if specified.",
#                     },
#                 },

#                 "required": ["query"],
#             },
#         },
#     },

#     # ========================================================
#     # PRODUCT DESCRIPTION
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "get_product_description_tool",

#             "description": (
#                 "Use this tool when the user wants the description, "
#                 "details, information, features, specifications, "
#                 "overview, or page of ONE specific product. "
#                 "The user may provide either a product ID or a "
#                 "product name. "
#                 "When this tool succeeds, the APPLICATION/UI will "
#                 "open the product detail page. "
#                 "The AI does NOT need to describe or announce the "
#                 "navigation. "
#                 "Do NOT use this tool for general product browsing "
#                 "or product discovery."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "product_id": {
#                         "type": ["integer", "null"],
#                         "description": (
#                             "Database ID of the product if the "
#                             "user provided a product ID."
#                         ),
#                     },

#                     "product_name": {
#                         "type": ["string", "null"],
#                         "description": (
#                             "Name of the specific product mentioned "
#                             "by the user."
#                         ),
#                     },
#                 },

#                 "required": [],
#             },
#         },
#     },

#     # ========================================================
#     # FIND PRODUCT FOR CART OPERATION
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "find_cart_product_tool",

#             "description": (
#                 "Find a product by name for a cart operation. "
#                 "Use ONLY when the user wants to add, remove, "
#                 "delete, or update a product in their cart "
#                 "but provided a product name instead of a product ID. "
#                 "This is NOT a general product search."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "product_name": {
#                         "type": "string",
#                         "description": (
#                             "The product name mentioned by the user."
#                         ),
#                     },

#                     "operation": {
#                         "type": "string",
#                         "enum": [
#                             "add",
#                             "remove",
#                             "update",
#                         ],
#                         "description": (
#                             "The cart operation that needs "
#                             "the product ID."
#                         ),
#                     },

#                     "quantity": {
#                         "type": ["integer", "null"],
#                         "description": (
#                             "Quantity for add or update operations."
#                         ),
#                     },
#                 },

#                 "required": [
#                     "product_name",
#                     "operation",
#                 ],
#             },
#         },
#     },

#     # ========================================================
#     # ORDER TOOL
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "get_user_orders_tool",

#             "description": (
#                 "Handle the authenticated user's orders. "
#                 "Use this when the user wants to see orders, "
#                 "view a specific order, track an order, "
#                 "or cancel an order."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "cancel_order_id": {
#                         "type": ["integer", "null"],
#                         "description": (
#                             "Order ID to cancel."
#                         ),
#                     },

#                     "order_id": {
#                         "type": ["integer", "null"],
#                         "description": "Specific order ID.",
#                     },

#                     "action": {
#                         "type": ["string", "null"],
#                         "enum": [
#                             "list",
#                             "track",
#                             "cancel",
#                             "specific",
#                             "null",
#                         ],
#                         "description": "Order action.",
#                     },
#                 },

#                 "required": [],
#             },
#         },
#     },

#     # ========================================================
#     # OPEN CART
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "open_cart_tool",

#             "description": (
#                 "Open the authenticated user's shopping cart. "
#                 "Use this when the user wants to view or open "
#                 "their cart, shopping bag, basket, cart contents, "
#                 "cart items, cart total, subtotal, or proceed "
#                 "to checkout."
#             ),

#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             },
#         },
#     },

#     # ========================================================
#     # ADD TO CART
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "add_to_cart_tool",

#             "description": (
#                 "Add a product to the authenticated user's cart. "
#                 "Use this after the product ID is known."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "product_id": {
#                         "type": "integer",
#                         "description": "Database ID of the product.",
#                     },

#                     "quantity": {
#                         "type": "integer",
#                         "description": (
#                             "Number of units to add. "
#                             "Defaults to 1."
#                         ),
#                     },
#                 },

#                 "required": [
#                     "product_id",
#                 ],
#             },
#         },
#     },

#     # ========================================================
#     # REMOVE FROM CART
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "remove_from_cart_tool",

#             "description": (
#                 "Remove a specific product completely "
#                 "from the authenticated user's cart. "
#                 "Use this after the product ID is known."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "product_id": {
#                         "type": "integer",
#                         "description": (
#                             "Database ID of the product "
#                             "to remove."
#                         ),
#                     },
#                 },

#                 "required": [
#                     "product_id",
#                 ],
#             },
#         },
#     },

#     # ========================================================
#     # CLEAR CART
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "clear_cart_tool",

#             "description": (
#                 "Remove every product from the authenticated "
#                 "user's shopping cart."
#             ),

#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             },
#         },
#     },

#     # ========================================================
#     # UPDATE CART QUANTITY
#     # ========================================================

#     {
#         "type": "function",
#         "function": {
#             "name": "update_cart_quantity_tool",

#             "description": (
#                 "Change the exact quantity of a specific "
#                 "product already in the user's cart. "
#                 "Use quantity 0 to remove the product."
#             ),

#             "parameters": {
#                 "type": "object",

#                 "properties": {
#                     "product_id": {
#                         "type": "integer",
#                         "description": "Database ID of the product.",
#                     },

#                     "quantity": {
#                         "type": "integer",
#                         "description": "The new exact quantity.",
#                     },
#                 },

#                 "required": [
#                     "product_id",
#                     "quantity",
#                 ],
#             },
#         },
#     },
# ]


# # ============================================================
# # CLEAN TOOL ARGUMENTS
# # ============================================================

# def clean_tool_arguments(raw_arguments):

#     try:

#         raw_args = (
#             json.loads(raw_arguments)
#             if raw_arguments
#             else {}
#         )

#     except json.JSONDecodeError as parse_err:

#         logger.error(
#             "[GROQ AI AGENT JSON ERROR] "
#             f"{parse_err}"
#         )

#         raise ValueError(
#             "The AI generated invalid tool arguments."
#         )

#     if not isinstance(raw_args, dict):

#         raise ValueError(
#             "The AI generated invalid tool arguments."
#         )

#     cleaned_args = {
#         key: value
#         for key, value in raw_args.items()
#         if value is not None
#     }

#     return cleaned_args


# # ============================================================
# # PRODUCT DESCRIPTION
# # ============================================================

# def handle_product_description_tool(
#     cleaned_args,
# ):

#     logger.info(
#         "[PRODUCT DESCRIPTION TOOL] "
#         f"Args={cleaned_args}"
#     )

#     product_id = cleaned_args.get(
#         "product_id"
#     )

#     product_name = cleaned_args.get(
#         "product_name"
#     )

#     if not product_id and not product_name:

#         return {
#             "status": "error",
#             "error_type": "MissingProduct",
#             "tool_called": (
#                 "get_product_description_tool"
#             ),
#             "message": (
#                 "Please specify the product ID "
#                 "or product name."
#             ),
#         }

#     try:

#         result = get_product_description_tool(
#             product_id=product_id,
#             product_name=product_name,
#         )

#     except Exception as exc:

#         logger.error(
#             "[PRODUCT DESCRIPTION ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": (
#                 "get_product_description_tool"
#             ),
#             "message": (
#                 "Unable to retrieve the product "
#                 f"description: {str(exc)}"
#             ),
#         }

#     # ========================================================
#     # PRODUCT NOT FOUND
#     # ========================================================

#     if not result.get("success"):

#         return {
#             "status": "success",
#             "tool_called": (
#                 "get_product_description_tool"
#             ),
#             "arguments": cleaned_args,
#             "action": "product_description",
#             "navigation": None,
#             "redirect": False,
#             "redirect_url": None,
#             "data": result,

#             # IMPORTANT:
#             # This is only an actual error/info message.
#             # No fake navigation message is generated.
#             "message": result.get(
#                 "message",
#                 "Product description not found.",
#             ),
#         }

#     # ========================================================
#     # PRODUCT FOUND
#     # ========================================================

#     product_data = result.get(
#         "product",
#         {}
#     )

#     product_url = product_data.get(
#         "url"
#     )

#     if not product_url:

#         logger.error(
#             "[PRODUCT DESCRIPTION ERROR] "
#             "Product has no URL."
#         )

#         return {
#             "status": "success",
#             "tool_called": (
#                 "get_product_description_tool"
#             ),
#             "arguments": cleaned_args,
#             "action": "product_description",
#             "navigation": "product_detail",
#             "redirect": False,
#             "redirect_url": None,
#             "data": result,
#             "message": (
#                 "Product found, but the product page "
#                 "URL is unavailable."
#             ),
#         }

#     # ========================================================
#     # SUCCESSFUL PRODUCT PAGE NAVIGATION
#     # ========================================================
#     #
#     # IMPORTANT:
#     #
#     # The UI/frontend is responsible for opening the page.
#     #
#     # DO NOT return:
#     #
#     #     "Opening HP Pavilion 15."
#     #
#     # The AI should NOT announce navigation.
#     #
#     # The frontend should simply use redirect_url.
#     #
#     # ========================================================

#     return {
#         "status": "success",

#         "tool_called": (
#             "get_product_description_tool"
#         ),

#         "arguments": cleaned_args,

#         "action": "product_description",

#         "navigation": "product_detail",

#         "redirect": True,

#         "redirect_url": product_url,

#         "data": result,

#         # EMPTY MESSAGE:
#         # Navigation is UI behavior, not AI conversation.
#         "message": "",
#     }


# # ============================================================
# # CART PRODUCT RESOLUTION
# # ============================================================

# def handle_find_cart_product_tool(
#     cleaned_args,
#     request=None,
# ):

#     logger.info(
#         "[FIND CART PRODUCT] "
#         f"Args={cleaned_args}"
#     )

#     product_name = (
#         cleaned_args.get(
#             "product_name",
#             ""
#         )
#         .strip()
#     )

#     operation = cleaned_args.get(
#         "operation"
#     )

#     quantity = cleaned_args.get(
#         "quantity"
#     )

#     if not product_name:

#         return {
#             "status": "error",
#             "error_type": "InvalidArguments",
#             "tool_called": "find_cart_product_tool",
#             "message": "Product name is required.",
#         }

#     try:

#         from products.models import Product

#         # ====================================================
#         # ADD
#         # ====================================================

#         if operation == "add":

#             products = (
#                 Product.objects
#                 .filter(
#                     is_active=True,
#                     name__icontains=product_name,
#                 )
#                 .order_by("id")
#             )

#         # ====================================================
#         # REMOVE / UPDATE
#         # ====================================================

#         elif operation in [
#             "remove",
#             "update",
#         ]:

#             if (
#                 not request
#                 or not request.user.is_authenticated
#             ):

#                 return {
#                     "status": "error",
#                     "error_type": "AuthenticationError",
#                     "tool_called": "find_cart_product_tool",
#                     "message": (
#                         "Please log in to manage your cart."
#                     ),
#                 }

#             cart = Cart(request)

#             cart_product_ids = list(
#                 cart.cart.keys()
#             )

#             if not cart_product_ids:

#                 return {
#                     "status": "success",
#                     "tool_called": "find_cart_product_tool",
#                     "arguments": cleaned_args,
#                     "action": "resolve_cart_product",
#                     "data": {
#                         "success": False,
#                         "found": False,
#                         "product_id": None,
#                         "product_name": product_name,
#                         "operation": operation,
#                         "message": (
#                             "Your cart is currently empty."
#                         ),
#                     },
#                 }

#             products = list(
#                 Product.objects
#                 .filter(
#                     id__in=cart_product_ids,
#                     is_active=True,
#                     name__icontains=product_name,
#                 )
#                 .order_by("id")
#             )

#         else:

#             return {
#                 "status": "error",
#                 "error_type": "InvalidOperation",
#                 "tool_called": "find_cart_product_tool",
#                 "message": (
#                     "Invalid cart operation."
#                 ),
#             }

#         # ====================================================
#         # NO PRODUCT
#         # ====================================================

#         if not products:

#             return {
#                 "status": "success",
#                 "tool_called": "find_cart_product_tool",
#                 "arguments": cleaned_args,
#                 "action": "resolve_cart_product",
#                 "data": {
#                     "success": False,
#                     "found": False,
#                     "product_id": None,
#                     "product_name": product_name,
#                     "operation": operation,
#                     "message": (
#                         f"No matching product found for "
#                         f"'{product_name}'."
#                     ),
#                 },
#             }

#         # ====================================================
#         # MULTIPLE PRODUCTS
#         # ====================================================

#         if len(products) > 1:

#             matches = []

#             for product in products[:10]:

#                 matches.append({
#                     "id": product.id,
#                     "name": product.name,
#                 })

#             return {
#                 "status": "success",
#                 "tool_called": "find_cart_product_tool",
#                 "arguments": cleaned_args,
#                 "action": "resolve_cart_product",
#                 "data": {
#                     "success": False,
#                     "found": True,
#                     "multiple_matches": True,
#                     "product_id": None,
#                     "product_name": product_name,
#                     "operation": operation,
#                     "matches": matches,
#                     "message": (
#                         f"Multiple products match "
#                         f"'{product_name}'."
#                     ),
#                 },
#             }

#         # ====================================================
#         # EXACT ONE PRODUCT
#         # ====================================================

#         product = products[0]

#         return {
#             "status": "success",
#             "tool_called": "find_cart_product_tool",
#             "arguments": cleaned_args,
#             "action": "resolve_cart_product",
#             "data": {
#                 "success": True,
#                 "found": True,
#                 "multiple_matches": False,
#                 "product_id": product.id,
#                 "product_name": product.name,
#                 "operation": operation,
#                 "quantity": quantity,
#             },
#         }

#     except Exception as exc:

#         logger.error(
#             "[FIND CART PRODUCT ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": "find_cart_product_tool",
#             "message": (
#                 "Unable to find the product: "
#                 f"{str(exc)}"
#             ),
#         }


# # ============================================================
# # OPEN CART
# # ============================================================

# def handle_cart_tool(
#     request=None,
# ):

#     logger.info(
#         "[CART TOOL] Opening cart."
#     )

#     try:

#         result = get_cart_tool(
#             request=request
#         )

#     except Exception:

#         logger.error(
#             "[CART TOOL ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": "open_cart_tool",
#             "message": "Cart operation failed.",
#         }

#     if not result.get("success"):

#         return {
#             "status": "error",
#             "error_type": "AuthenticationError",
#             "tool_called": "open_cart_tool",
#             "action": "cart",
#             "data": result,
#             "message": result.get(
#                 "message",
#                 "Please log in to view your cart.",
#             ),
#         }

#     return {
#         "status": "success",
#         "tool_called": "open_cart_tool",
#         "arguments": {},
#         "action": "cart",
#         "navigation": "cart_detail",
#         "redirect": True,
#         "redirect_url": result.get(
#             "redirect_url"
#         ),
#         "data": result,

#         # UI handles navigation.
#         "message": "",
#     }


# # ============================================================
# # ADD TO CART
# # ============================================================

# def handle_add_to_cart_tool(
#     cleaned_args,
#     request=None,
# ):

#     logger.info(
#         "[CART ADD TOOL] "
#         f"Args={cleaned_args}"
#     )

#     try:

#         result = add_to_cart_tool(
#             request=request,
#             **cleaned_args,
#         )

#     except Exception:

#         logger.error(
#             "[CART ADD ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": "add_to_cart_tool",
#             "message": (
#                 "Unable to add the product to your cart."
#             ),
#         }

#     if not result.get("success"):

#         return {
#             "status": "error",
#             "tool_called": "add_to_cart_tool",
#             "action": "add_to_cart",
#             "data": result,
#             "message": result.get(
#                 "message",
#                 "Unable to add product to cart.",
#             ),
#         }

#     return {
#         "status": "success",
#         "tool_called": "add_to_cart_tool",
#         "arguments": cleaned_args,
#         "action": "add_to_cart",
#         "navigation": "cart_detail",
#         "redirect": True,
#         "redirect_url": result.get(
#             "redirect_url"
#         ),
#         "data": result,
#         "message": "",
#     }


# # ============================================================
# # REMOVE FROM CART
# # ============================================================

# def handle_remove_from_cart_tool(
#     cleaned_args,
#     request=None,
# ):

#     logger.info(
#         "[CART REMOVE TOOL] "
#         f"Args={cleaned_args}"
#     )

#     try:

#         result = remove_from_cart_tool(
#             request=request,
#             **cleaned_args,
#         )

#     except Exception:

#         logger.error(
#             "[CART REMOVE ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": "remove_from_cart_tool",
#             "message": (
#                 "Unable to remove the product "
#                 "from your cart."
#             ),
#         }

#     if not result.get("success"):

#         return {
#             "status": "error",
#             "tool_called": "remove_from_cart_tool",
#             "action": "remove_from_cart",
#             "data": result,
#             "message": result.get(
#                 "message",
#                 "Unable to remove product.",
#             ),
#         }

#     return {
#         "status": "success",
#         "tool_called": "remove_from_cart_tool",
#         "arguments": cleaned_args,
#         "action": "remove_from_cart",
#         "navigation": "cart_detail",
#         "redirect": True,
#         "redirect_url": result.get(
#             "redirect_url"
#         ),
#         "data": result,
#         "message": "",
#     }


# # ============================================================
# # CLEAR CART
# # ============================================================

# def handle_clear_cart_tool(
#     request=None,
# ):

#     logger.info(
#         "[CART CLEAR TOOL] Clearing cart."
#     )

#     try:

#         result = clear_cart_tool(
#             request=request
#         )

#     except Exception:

#         logger.error(
#             "[CART CLEAR ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": "clear_cart_tool",
#             "message": (
#                 "Unable to clear your cart."
#             ),
#         }

#     if not result.get("success"):

#         return {
#             "status": "error",
#             "tool_called": "clear_cart_tool",
#             "action": "clear_cart",
#             "data": result,
#             "message": result.get(
#                 "message",
#                 "Unable to clear cart.",
#             ),
#         }

#     return {
#         "status": "success",
#         "tool_called": "clear_cart_tool",
#         "arguments": {},
#         "action": "clear_cart",
#         "navigation": "cart_detail",
#         "redirect": True,
#         "redirect_url": result.get(
#             "redirect_url"
#         ),
#         "data": result,
#         "message": "",
#     }


# # ============================================================
# # UPDATE CART QUANTITY
# # ============================================================

# def handle_update_cart_quantity_tool(
#     cleaned_args,
#     request=None,
# ):

#     logger.info(
#         "[CART UPDATE TOOL] "
#         f"Args={cleaned_args}"
#     )

#     try:

#         result = update_cart_quantity_tool(
#             request=request,
#             **cleaned_args,
#         )

#     except Exception:

#         logger.error(
#             "[CART UPDATE ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "tool_called": (
#                 "update_cart_quantity_tool"
#             ),
#             "message": (
#                 "Unable to update the cart quantity."
#             ),
#         }

#     if not result.get("success"):

#         return {
#             "status": "error",
#             "tool_called": (
#                 "update_cart_quantity_tool"
#             ),
#             "action": "update_cart_quantity",
#             "data": result,
#             "message": result.get(
#                 "message",
#                 "Unable to update cart quantity.",
#             ),
#         }

#     return {
#         "status": "success",
#         "tool_called": (
#             "update_cart_quantity_tool"
#         ),
#         "arguments": cleaned_args,
#         "action": "update_cart_quantity",
#         "navigation": "cart_detail",
#         "redirect": True,
#         "redirect_url": result.get(
#             "redirect_url"
#         ),
#         "data": result,
#         "message": "",
#     }


# # ============================================================
# # ORDER CANCELLATION
# # ============================================================

# def handle_cancel_order(
#     cleaned_args,
#     user,
#     tool_name,
# ):

#     order_id = cleaned_args.get(
#         "cancel_order_id"
#     )

#     if not order_id:

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "cancel",
#             "confirmation_required": False,
#             "data": {
#                 "success": False,
#                 "message": (
#                     "Please specify which "
#                     "order you want to cancel."
#                 ),
#             },
#         }

#     from orders.models import Order

#     order = (
#         Order.objects
#         .filter(
#             id=order_id,
#             user=user,
#         )
#         .first()
#     )

#     if not order:

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "cancel",
#             "confirmation_required": False,
#             "data": {
#                 "success": False,
#                 "message": "Order not found.",
#             },
#         }

#     if order.order_status == "CANCELLED":

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "cancel",
#             "confirmation_required": False,
#             "data": {
#                 "success": False,
#                 "message": (
#                     "This order is already cancelled."
#                 ),
#             },
#         }

#     if order.order_status in [
#         "SHIPPED",
#         "DELIVERED",
#     ]:

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "cancel",
#             "confirmation_required": False,
#             "data": {
#                 "success": False,
#                 "message": (
#                     f"Order #{order.id} can no longer "
#                     f"be cancelled because it is already "
#                     f"{order.order_status.lower()}."
#                 ),
#             },
#         }

#     redirect_url = (
#         f"/orders/orders/{order.id}/?cancel=1"
#     )

#     return {
#         "status": "success",
#         "tool_called": tool_name,
#         "arguments": cleaned_args,
#         "action": "cancel",
#         "confirmation_required": True,
#         "order_id": order.id,
#         "navigation": "order_detail",
#         "redirect": True,
#         "redirect_url": redirect_url,
#         "data": {
#             "success": True,
#             "action": "cancel",
#             "confirmation_required": True,
#             "order_id": order.id,
#             "navigation": "order_detail",
#             "redirect": True,
#             "redirect_url": redirect_url,
#             "order": {
#                 "id": order.id,
#                 "status": order.order_status,
#                 "total_price": str(
#                     order.total_price
#                 ),
#                 "created_at": (
#                     order.created_at.strftime(
#                         "%Y-%m-%d %H:%M"
#                     )
#                 ),
#                 "url": redirect_url,
#             },
#             "message": (
#                 f"Opening Order #{order.id} "
#                 f"to confirm cancellation."
#             ),
#         },
#     }


# # ============================================================
# # ORDER TOOL
# # ============================================================

# def handle_order_tool(
#     cleaned_args,
#     user,
#     tool_name,
# ):

#     if not user or not user.is_authenticated:

#         return {
#             "status": "error",
#             "error_type": "AuthenticationError",
#             "message": (
#                 "Please log in to view "
#                 "or manage your orders."
#             ),
#         }

#     action = cleaned_args.get(
#         "action"
#     )

#     if action == "cancel":

#         return handle_cancel_order(
#             cleaned_args=cleaned_args,
#             user=user,
#             tool_name=tool_name,
#         )

#     try:

#         result = execute_get_user_orders(
#             user=user,
#             **cleaned_args
#         )

#     except Exception as tool_err:

#         logger.error(
#             "[ORDER TOOL ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "ToolExecutionError",
#             "message": (
#                 "Order operation failed: "
#                 f"{str(tool_err)}"
#             ),
#         }

#     if action == "list":

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "list",
#             "navigation": "order_list",
#             "data": result,
#         }

#     if action == "specific":

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "specific",
#             "navigation": "order_detail",
#             "data": result,
#         }

#     if action == "track":

#         return {
#             "status": "success",
#             "tool_called": tool_name,
#             "arguments": cleaned_args,
#             "action": "track",
#             "navigation": "order_detail",
#             "data": result,
#         }

#     return {
#         "status": "success",
#         "tool_called": tool_name,
#         "arguments": cleaned_args,
#         "action": action,
#         "data": result,
#     }


# # ============================================================
# # AGENT
# # ============================================================

# def run_agent(
#     user_prompt: str,
#     user=None,
#     request=None,
# ):

#     logger.info(
#         "--- [GROQ AI AGENT START] "
#         f"Prompt: '{user_prompt}' | "
#         f"User: {user} ---"
#     )

#     # ========================================================
#     # API KEY
#     # ========================================================

#     api_key = getattr(
#         settings,
#         "GROQ_API_KEY",
#         None,
#     )

#     if not api_key:

#         return {
#             "status": "error",
#             "error_type": "ConfigurationError",
#             "message": (
#                 "GROQ_API_KEY is not configured "
#                 "in Django settings."
#             ),
#         }

#     try:

#         client = Groq(
#             api_key=api_key
#         )

#         # ====================================================
#         # SYSTEM INSTRUCTIONS
#         # ====================================================

#         system_instruction = (

#             "You are an e-commerce assistant.\n\n"

#             "==================================================\n"
#             "CRITICAL UI / NAVIGATION RULE\n"
#             "==================================================\n"

#             "The application UI is responsible for navigation.\n\n"

#             "When a tool returns a redirect URL or navigation "
#             "instruction, DO NOT verbally announce the navigation.\n\n"

#             "NEVER generate messages such as:\n"
#             "- Opening HP Pavilion\n"
#             "- Opening HP Pavilion 15\n"
#             "- Opening the product page\n"
#             "- I'm opening the product page\n"
#             "- Taking you to the product page\n"
#             "- Redirecting you to the product page\n"
#             "- Here is the product page\n"
#             "- Let me open that page\n\n"

#             "DO NOT describe UI actions as conversational answers.\n\n"

#             "If the user's request requires opening a page, "
#             "call the appropriate tool and let the APPLICATION/UI "
#             "perform the navigation.\n\n"

#             "The tool result contains the navigation information. "
#             "The frontend will use that information to open the page.\n\n"

#             "IMPORTANT: Opening a page is UI work, NOT an AI response.\n\n"

#             "For example:\n"
#             "User: open HP Pavilion 15\n"
#             "Correct behavior: call "
#             "get_product_description_tool with "
#             "product_name='HP Pavilion 15'.\n"
#             "Then stop. Do NOT respond with "
#             "'Opening HP Pavilion 15'.\n\n"

#             "User: show me the details of iPhone 15\n"
#             "Correct behavior: call "
#             "get_product_description_tool.\n"
#             "Then let the UI navigate to the product page.\n"
#             "Do NOT generate a navigation announcement.\n\n"

#             "==================================================\n"
#             "IMPORTANT TOOL ROUTING RULE\n"
#             "==================================================\n"

#             "Choose the tool based on the USER'S INTENT.\n\n"

#             "A cart command is NOT a product search.\n"
#             "A product description request is NOT a product search.\n\n"

#             "==================================================\n"
#             "PRODUCT SEARCH\n"
#             "==================================================\n"

#             "Use `search_products_tool` ONLY for actual "
#             "product discovery, browsing, searching, or "
#             "comparing products.\n\n"

#             "Examples:\n"
#             "- show me laptops -> search_products_tool\n"
#             "- find HP laptops -> search_products_tool\n"
#             "- search for smartwatches -> search_products_tool\n"
#             "- products under $500 -> search_products_tool\n"
#             "- compare laptops -> search_products_tool\n\n"

#             "Do NOT use search_products_tool when the user "
#             "asks for the description/details of ONE specific "
#             "product.\n\n"

#             "==================================================\n"
#             "PRODUCT DESCRIPTION / PRODUCT PAGE\n"
#             "==================================================\n"

#             "Use `get_product_description_tool` when the user "
#             "asks about the description, details, features, "
#             "information, overview, specifications, or page "
#             "of ONE specific product.\n\n"

#             "If the user gives a PRODUCT ID, pass it as "
#             "`product_id`.\n\n"

#             "If the user gives a PRODUCT NAME, pass it as "
#             "`product_name`.\n\n"

#             "Never invent a product ID.\n\n"

#             "Examples:\n"

#             "- describe product 5 -> "
#             "get_product_description_tool with product_id=5\n"

#             "- tell me about product 10 -> "
#             "get_product_description_tool with product_id=10\n"

#             "- what is the description of HP Pavilion 15 -> "
#             "get_product_description_tool with "
#             "product_name='HP Pavilion 15'\n"

#             "- show me the details of iPhone 15 -> "
#             "get_product_description_tool with "
#             "product_name='iPhone 15'\n"

#             "- open the iPhone 15 page -> "
#             "get_product_description_tool with "
#             "product_name='iPhone 15'\n\n"

#             "When the product description tool succeeds, "
#             "the APPLICATION/UI automatically navigates "
#             "to the product detail page.\n\n"

#             "DO NOT send a conversational message announcing "
#             "that navigation.\n\n"

#             "Do NOT say 'Opening [product name]'.\n"
#             "Do NOT say 'Opening the product page'.\n"
#             "Do NOT say 'Redirecting'.\n"
#             "Do NOT say 'Taking you to'.\n\n"

#             "The frontend handles the page transition.\n\n"

#             "If multiple products match the name, do not guess. "
#             "Return the available matches and ask the user "
#             "which product they mean.\n\n"

#             "==================================================\n"
#             "CART OPERATIONS\n"
#             "==================================================\n"

#             "Use `open_cart_tool` when the user wants to "
#             "view or open their cart.\n\n"

#             "Use `add_to_cart_tool` when the user wants "
#             "to add a product to their cart.\n\n"

#             "Use `remove_from_cart_tool` when the user wants "
#             "to remove a product from their cart.\n\n"

#             "Use `clear_cart_tool` when the user wants "
#             "to empty or clear the entire cart.\n\n"

#             "Use `update_cart_quantity_tool` when the user "
#             "wants to change quantity.\n\n"

#             "==================================================\n"
#             "PRODUCT NAME VS PRODUCT ID\n"
#             "==================================================\n"

#             "Cart execution tools require product_id.\n\n"

#             "If the user gives a PRODUCT ID, directly use "
#             "the appropriate cart execution tool.\n\n"

#             "If the user gives a PRODUCT NAME instead of "
#             "a product ID, use `find_cart_product_tool`.\n\n"

#             "For ADD:\n"
#             "operation='add'.\n\n"

#             "For REMOVE or DELETE:\n"
#             "operation='remove'.\n\n"

#             "For quantity changes:\n"
#             "operation='update'.\n\n"

#             "Never invent a product ID.\n\n"

#             "==================================================\n"
#             "CART EXAMPLES\n"
#             "==================================================\n"

#             "User: show my cart\n"
#             "Tool: open_cart_tool\n\n"

#             "User: add product 5 to cart\n"
#             "Tool: add_to_cart_tool with product_id=5\n\n"

#             "User: add 3 of product 5\n"
#             "Tool: add_to_cart_tool with "
#             "product_id=5, quantity=3\n\n"

#             "User: add smartwatch to my cart\n"
#             "Tool: find_cart_product_tool with "
#             "product_name='smartwatch', operation='add'\n\n"

#             "User: remove product 5 from my cart\n"
#             "Tool: remove_from_cart_tool with product_id=5\n\n"

#             "User: delete laptop from my cart\n"
#             "Tool: find_cart_product_tool with "
#             "product_name='laptop', operation='remove'\n\n"

#             "User: delete HP Pavilion 15 from my cart\n"
#             "Tool: find_cart_product_tool with "
#             "product_name='HP Pavilion 15', operation='remove'\n\n"

#             "User: change product 5 quantity to 3\n"
#             "Tool: update_cart_quantity_tool with "
#             "product_id=5, quantity=3\n\n"

#             "User: change smartwatch quantity to 3\n"
#             "Tool: find_cart_product_tool with "
#             "product_name='smartwatch', operation='update', "
#             "quantity=3\n\n"

#             "==================================================\n"
#             "ORDERS\n"
#             "==================================================\n"

#             "For order-related requests, use "
#             "`get_user_orders_tool`.\n\n"

#             "==================================================\n"
#             "SECURITY\n"
#             "==================================================\n"

#             "Never invent product IDs.\n"
#             "Never invent order IDs.\n"
#             "Only operate on the authenticated user's cart "
#             "and orders.\n"
#             "Never expose another user's order data.\n"
#             "Never directly cancel an order without "
#             "the application confirmation step.\n"
#         )

#         # ====================================================
#         # FIRST GROQ CALL
#         # ====================================================

#         response = client.chat.completions.create(

#             model="openai/gpt-oss-120b",

#             messages=[
#                 {
#                     "role": "system",
#                     "content": system_instruction,
#                 },

#                 {
#                     "role": "user",
#                     "content": user_prompt,
#                 },
#             ],

#             tools=TOOLS_SCHEMA,

#             tool_choice="auto",

#             temperature=0.0,
#         )

#         response_message = (
#             response.choices[0].message
#         )

#         tool_calls = (
#             response_message.tool_calls
#         )

#         # ====================================================
#         # NO TOOL
#         # ====================================================

#         if not tool_calls:

#             logger.info(
#                 "[GROQ AI AGENT] No tool executed."
#             )

#             return {
#                 "status": "text_response",
#                 "tool_called": None,
#                 "message": (
#                     response_message.content
#                     or "No response generated."
#                 ),
#             }

#         # ====================================================
#         # FIRST TOOL CALL
#         # ====================================================

#         call = tool_calls[0]

#         tool_name = (
#             call.function.name
#         )

#         raw_arguments_str = (
#             call.function.arguments
#         )

#         logger.info(
#             "[LLM TOOL CALL] "
#             f"Tool={tool_name} "
#             f"Args={raw_arguments_str}"
#         )

#         try:

#             cleaned_args = clean_tool_arguments(
#                 raw_arguments_str
#             )

#         except ValueError as parse_err:

#             return {
#                 "status": "error",
#                 "error_type": (
#                     "ToolArgumentsError"
#                 ),
#                 "message": str(parse_err),
#             }

#         # ====================================================
#         # PRODUCT DESCRIPTION
#         # ====================================================

#         if tool_name == "get_product_description_tool":

#             return handle_product_description_tool(
#                 cleaned_args=cleaned_args,
#             )

#         # ====================================================
#         # FIND CART PRODUCT
#         # ====================================================

#         if tool_name == "find_cart_product_tool":

#             resolved = handle_find_cart_product_tool(
#                 cleaned_args=cleaned_args,
#                 request=request,
#             )

#             data = resolved.get(
#                 "data",
#                 {}
#             )

#             if not data.get("success"):

#                 return resolved

#             product_id = data.get(
#                 "product_id"
#             )

#             operation = data.get(
#                 "operation"
#             )

#             # ------------------------------------------------
#             # ADD
#             # ------------------------------------------------

#             if operation == "add":

#                 quantity = (
#                     cleaned_args.get(
#                         "quantity",
#                         1
#                     )
#                 )

#                 return handle_add_to_cart_tool(
#                     cleaned_args={
#                         "product_id": product_id,
#                         "quantity": quantity,
#                     },
#                     request=request,
#                 )

#             # ------------------------------------------------
#             # REMOVE
#             # ------------------------------------------------

#             if operation == "remove":

#                 return handle_remove_from_cart_tool(
#                     cleaned_args={
#                         "product_id": product_id,
#                     },
#                     request=request,
#                 )

#             # ------------------------------------------------
#             # UPDATE
#             # ------------------------------------------------

#             if operation == "update":

#                 quantity = cleaned_args.get(
#                     "quantity"
#                 )

#                 if quantity is None:

#                     return {
#                         "status": "error",
#                         "error_type": "MissingQuantity",
#                         "tool_called": (
#                             "find_cart_product_tool"
#                         ),
#                         "message": (
#                             "Please specify the new "
#                             "quantity."
#                         ),
#                     }

#                 return handle_update_cart_quantity_tool(
#                     cleaned_args={
#                         "product_id": product_id,
#                         "quantity": quantity,
#                     },
#                     request=request,
#                 )

#         # ====================================================
#         # OPEN CART
#         # ====================================================

#         if tool_name == "open_cart_tool":

#             return handle_cart_tool(
#                 request=request
#             )

#         # ====================================================
#         # ADD CART
#         # ====================================================

#         if tool_name == "add_to_cart_tool":

#             return handle_add_to_cart_tool(
#                 cleaned_args=cleaned_args,
#                 request=request,
#             )

#         # ====================================================
#         # REMOVE CART
#         # ====================================================

#         if tool_name == "remove_from_cart_tool":

#             return handle_remove_from_cart_tool(
#                 cleaned_args=cleaned_args,
#                 request=request,
#             )

#         # ====================================================
#         # CLEAR CART
#         # ====================================================

#         if tool_name == "clear_cart_tool":

#             return handle_clear_cart_tool(
#                 request=request
#             )

#         # ====================================================
#         # UPDATE CART
#         # ====================================================

#         if tool_name == "update_cart_quantity_tool":

#             return handle_update_cart_quantity_tool(
#                 cleaned_args=cleaned_args,
#                 request=request,
#             )

#         # ====================================================
#         # PRODUCT SEARCH
#         # ====================================================

#         if tool_name == "search_products_tool":

#             if (
#                 "query" not in cleaned_args
#                 or not cleaned_args["query"]
#             ):

#                 cleaned_args["query"] = (
#                     user_prompt
#                 )

#             try:

#                 result = search_products_tool(
#                     **cleaned_args
#                 )

#             except Exception as tool_err:

#                 logger.error(
#                     "[PRODUCT TOOL ERROR]\n"
#                     f"{traceback.format_exc()}"
#                 )

#                 return {
#                     "status": "error",
#                     "error_type": (
#                         "ToolExecutionError"
#                     ),
#                     "message": (
#                         "Product search failed: "
#                         f"{str(tool_err)}"
#                     ),
#                 }

#             return {
#                 "status": "success",
#                 "tool_called": tool_name,
#                 "arguments": cleaned_args,
#                 "action": "product_search",
#                 "navigation": "home",
#                 "redirect": False,
#                 "data": result,
#             }

#         # ====================================================
#         # ORDER TOOL
#         # ====================================================

#         if tool_name == "get_user_orders_tool":

#             return handle_order_tool(
#                 cleaned_args=cleaned_args,
#                 user=user,
#                 tool_name=tool_name,
#             )

#         # ====================================================
#         # UNKNOWN TOOL
#         # ====================================================

#         return {
#             "status": "error",
#             "error_type": "UnknownTool",
#             "message": (
#                 f"Tool '{tool_name}' "
#                 "is not recognized."
#             ),
#         }

#     # ========================================================
#     # RATE LIMIT
#     # ========================================================

#     except RateLimitError:

#         logger.error(
#             "[GROQ RATE LIMIT]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "QuotaExceededError",
#             "code": 429,
#             "message": (
#                 "Groq API rate limit or token "
#                 "limit reached. Please try again later."
#             ),
#         }

#     # ========================================================
#     # CONNECTION ERROR
#     # ========================================================

#     except APIConnectionError:

#         logger.error(
#             "[GROQ CONNECTION ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "NetworkError",
#             "message": (
#                 "Unable to connect to Groq API."
#             ),
#         }

#     # ========================================================
#     # API ERROR
#     # ========================================================

#     except APIError as api_err:

#         status_code = getattr(
#             api_err,
#             "status_code",
#             None
#         )

#         logger.error(
#             "[GROQ API ERROR] "
#             f"Code={status_code}\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": "GroqAPIError",
#             "code": status_code,
#             "message": (
#                 f"Groq API Error: {str(api_err)}"
#             ),
#         }

#     # ========================================================
#     # UNEXPECTED ERROR
#     # ========================================================

#     except Exception as exc:

#         logger.error(
#             "[GROQ UNEXPECTED ERROR]\n"
#             f"{traceback.format_exc()}"
#         )

#         return {
#             "status": "error",
#             "error_type": type(exc).__name__,
#             "message": (
#                 f"Unexpected error: {str(exc)}"
#             ),
#         }