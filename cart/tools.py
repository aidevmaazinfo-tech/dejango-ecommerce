from decimal import Decimal
from django.urls import reverse
from products.models import Product
from orders.models import Order
from .cart import Cart


# ============================================================
# AUTHENTICATION HELPER
# ============================================================

def _authentication_error():
    return {
        "success": False,
        "message": "Please log in to continue.",
    }


# ============================================================
# REQUEST VALIDATION
# ============================================================

def _validate_request(request):
    """
    Operations require the Django request for session/user access.
    """
    if request is None:
        return {
            "success": False,
            "message": "A Django request is required.",
        }

    user = getattr(request, "user", None)

    if not user or not user.is_authenticated:
        return _authentication_error()

    return None


# ============================================================
# CART URL
# ============================================================

def _cart_url():
    return reverse("cart:cart_detail")


# ============================================================
# PRODUCT LOOKUP INSIDE CURRENT CART
# ============================================================

def _find_cart_product(cart, product_name=None, product_id=None):
    if product_id is not None:
        try:
            product_id = int(product_id)
        except (TypeError, ValueError):
            return None, {
                "success": False,
                "message": "Product ID must be a valid number.",
            }

        product_key = str(product_id)

        if product_key not in cart.cart:
            return None, {
                "success": False,
                "message": f"Product #{product_id} is not currently in your cart.",
            }

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return None, {
                "success": False,
                "message": f"Product #{product_id} no longer exists.",
            }

        return product, None

    if not product_name:
        return None, {
            "success": False,
            "message": "Please specify which product.",
        }

    search_name = product_name.strip().lower()
    cart_product_ids = list(cart.cart.keys())

    if not cart_product_ids:
        return None, {
            "success": False,
            "message": "Your cart is currently empty.",
        }

    products = Product.objects.filter(id__in=cart_product_ids)

    for product in products:
        if product.name.strip().lower() == search_name:
            return product, None

    matches = [product for product in products if search_name in product.name.strip().lower()]

    if len(matches) == 1:
        return matches[0], None

    if len(matches) > 1:
        names = [product.name for product in matches]
        return None, {
            "success": False,
            "message": "I found multiple matching products in your cart: " + ", ".join(names) + ". Please specify which one.",
        }

    return None, {
        "success": False,
        "message": f"I couldn't find '{product_name}' in your cart.",
    }


# ============================================================
# GET / OPEN CART
# ============================================================

def get_cart_tool(request=None):
    error = _validate_request(request)
    if error:
        return error

    cart = Cart(request)
    items = []
    for item in cart:
        product = item["product"]
        items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item["quantity"],
            "price": str(item["price"]),
            "total_price": str(item["total_price"]),
            "image": product.image.url if product.image else None,
            "url": product.get_absolute_url(),
        })

    return {
        "success": True,
        "action": "view_cart",
        "navigation": "cart",
        "redirect": True,
        "redirect_url": _cart_url(),
        "cart": {"items": items, "item_count": len(cart), "total_price": str(cart.get_total_price())},
        "message": "Opening your shopping cart.",
    }


# ============================================================
# ADD TO CART
# ============================================================

def add_to_cart_tool(request=None, product_id=None, quantity=1):
    error = _validate_request(request)
    if error:
        return error

    if product_id is None:
        return {
            "success": False,
            "message": "Please specify which product to add.",
        }

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Quantity must be a valid number.",
        }

    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than zero.",
        }

    product = Product.objects.filter(id=product_id).first()
    if not product:
        return {
            "success": False,
            "message": f"Product #{product_id} was not found.",
        }

    cart = Cart(request)
    cart.add(product=product, quantity=quantity)

    return {
        "success": True,
        "action": "add_to_cart",
        "navigation": "cart_detail",
        "redirect": True,
        "redirect_url": _cart_url(),
        "product_id": product.id,
        "product_name": product.name,
        "quantity_added": quantity,
        "message": f"Added {quantity} × {product.name} to your cart.",
    }


# ============================================================
# REMOVE FROM CART
# ============================================================

def remove_from_cart_tool(request=None, product_id=None, product_name=None):
    error = _validate_request(request)
    if error:
        return error

    cart = Cart(request)
    product, lookup_error = _find_cart_product(
        cart=cart, product_name=product_name, product_id=product_id
    )

    if lookup_error:
        return lookup_error

    cart.remove(product)

    return {
        "success": True,
        "action": "remove_from_cart",
        "navigation": "cart_detail",
        "redirect": True,
        "redirect_url": _cart_url(),
        "product_id": product.id,
        "product_name": product.name,
        "message": f"Removed {product.name} from your cart.",
    }


# ============================================================
# CLEAR CART
# ============================================================

def clear_cart_tool(request=None):
    error = _validate_request(request)
    if error:
        return error

    cart = Cart(request)
    cart.clear()

    return {
        "success": True,
        "action": "clear_cart",
        "navigation": "cart_detail",
        "redirect": True,
        "redirect_url": _cart_url(),
        "message": "Your shopping cart has been cleared.",
    }


# ============================================================
# UPDATE CART QUANTITY
# ============================================================

def update_cart_quantity_tool(request=None, product_id=None, product_name=None, quantity=None):
    error = _validate_request(request)
    if error:
        return error

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Quantity must be a valid number.",
        }

    if quantity < 0:
        return {
            "success": False,
            "message": "Quantity cannot be negative.",
        }

    cart = Cart(request)
    product, lookup_error = _find_cart_product(
        cart=cart, product_name=product_name, product_id=product_id
    )

    if lookup_error:
        return lookup_error

    if quantity == 0:
        cart.remove(product)
        return {
            "success": True,
            "action": "update_cart_quantity",
            "navigation": "cart_detail",
            "redirect": True,
            "redirect_url": _cart_url(),
            "product_id": product.id,
            "product_name": product.name,
            "quantity": 0,
            "message": f"Removed {product.name} from your cart because quantity was set to zero.",
        }

    cart.add(product=product, quantity=quantity, override_quantity=True)

    return {
        "success": True,
        "action": "update_cart_quantity",
        "navigation": "cart_detail",
        "redirect": True,
        "redirect_url": _cart_url(),
        "product_id": product.id,
        "product_name": product.name,
        "quantity": quantity,
        "message": f"Updated {product.name} quantity to {quantity}.",
    }


# ============================================================
# REORDER TOOL (Add previous order items back to cart)
# ============================================================

def reorder_tool(request=None, order_id=None):
    error = _validate_request(request)
    if error:
        return error

    if order_id is None:
        return {
            "success": False,
            "message": "Please specify which order you want to reorder.",
        }

    try:
        order_id = int(order_id)
    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Order ID must be a valid number.",
        }

    order = Order.objects.filter(id=order_id, user=request.user).first()
    if not order:
        return {
            "success": False,
            "message": f"Order #{order_id} was not found in your order history.",
        }

    cart = Cart(request)
    added_items = []

    for item in order.items.all():
        if item.product:
            cart.add(product=item.product, quantity=item.quantity)
            added_items.append(f"{item.quantity}× {item.product.name}")

    return {
        "success": True,
        "action": "reorder",
        "navigation": "cart_detail",
        "redirect": True,
        "redirect_url": _cart_url(),
        "order_id": order.id,
        "message": f"Successfully added items from Order #{order.id} to your cart: " + ", ".join(added_items) + ".",
    }


# ============================================================
# CUSTOMER PROFILE & ADDRESS TOOLS
# ============================================================

def get_customer_profile_tool(request=None):
    error = _validate_request(request)
    if error:
        return error

    user = request.user

    profile_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_number": getattr(user, "phone_number", ""),
        "address": getattr(user, "shipping_address", ""),
    }

    # Fallback to latest order address if shipping_address is blank
    if not profile_data["address"]:
        latest_order = Order.objects.filter(user=user).first()
        if latest_order:
            profile_data["address"] = getattr(latest_order, "address", "")

    return {
        "success": True,
        "action": "get_profile",
        "profile": profile_data,
        "message": "Retrieved your customer profile and shipping information.",
    }


def update_customer_profile_tool(
    request=None,
    first_name=None,
    last_name=None,
    email=None,
    address=None,
    phone_number=None,
):
    error = _validate_request(request)
    if error:
        return error

    user = request.user

    if first_name is not None:
        user.first_name = first_name.strip()
    if last_name is not None:
        user.last_name = last_name.strip()
    if email is not None:
        user.email = email.strip()
    if phone_number is not None:
        user.phone_number = phone_number.strip()
    if address is not None:
        user.shipping_address = address.strip()

    user.save()

    return {
        "success": True,
        "action": "update_profile",
        "profile": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "address": user.shipping_address,
        },
        "message": "Your profile and shipping details have been successfully updated.",
    }