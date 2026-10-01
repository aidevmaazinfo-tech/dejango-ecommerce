from datetime import timedelta
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from .models import Order
from products.models import Product


# ============================================================
# DELIVERY ESTIMATION
# ============================================================

def get_delivery_estimate(order):
    """
    Calculate estimated delivery information based on
    the current order status.

    PROCESSING:
        5-7 days from order creation

    SHIPPED:
        2-4 days from the current date

    DELIVERED:
        Already delivered

    CANCELLED:
        Will not be delivered
    """

    # =========================================================
    # DELIVERED
    # =========================================================

    if order.order_status == Order.OrderStatus.DELIVERED:

        delivered_date = (
            order.updated_at.date()
            if order.updated_at
            else timezone.localdate()
        )

        return {
            "estimated_days_min": 0,
            "estimated_days_max": 0,
            "days_remaining": 0,
            "estimated_delivery_date": delivered_date.isoformat(),
            "delivery_status": "DELIVERED",
            "delivery_message": (
                f"Order #{order.id} has already been delivered."
            ),
        }

    # =========================================================
    # CANCELLED
    # =========================================================

    if order.order_status == Order.OrderStatus.CANCELLED:

        return {
            "estimated_days_min": None,
            "estimated_days_max": None,
            "days_remaining": None,
            "estimated_delivery_date": None,
            "delivery_status": "CANCELLED",
            "delivery_message": (
                f"Order #{order.id} was cancelled and "
                f"will not be delivered."
            ),
        }

    # =========================================================
    # PROCESSING
    # =========================================================

    if order.order_status == Order.OrderStatus.PROCESSING:

        min_days = 5
        max_days = 7

        estimated_delivery_date = (
            order.created_at +
            timedelta(days=max_days)
        ).date()

    # =========================================================
    # SHIPPED
    # =========================================================

    elif order.order_status == Order.OrderStatus.SHIPPED:

        min_days = 2
        max_days = 4

        estimated_delivery_date = (
            timezone.localdate() +
            timedelta(days=max_days)
        )

    # =========================================================
    # FALLBACK
    # =========================================================

    else:

        min_days = 5
        max_days = 7

        estimated_delivery_date = (
            order.created_at +
            timedelta(days=max_days)
        ).date()

    # =========================================================
    # DAYS REMAINING
    # =========================================================

    today = timezone.localdate()

    days_remaining = (
        estimated_delivery_date - today
    ).days

    days_remaining = max(
        days_remaining,
        0
    )

    # =========================================================
    # HUMAN READABLE MESSAGE
    # =========================================================

    status = order.get_order_status_display()

    delivery_message = (
        f"Order #{order.id} is currently "
        f"{status.lower()}. "
        f"Estimated delivery is within "
        f"{min_days} to {max_days} days. "
        f"Expected delivery date is "
        f"{estimated_delivery_date.strftime('%B %d, %Y')}. "
        f"Approximately {days_remaining} day(s) remaining."
    )

    return {
        "estimated_days_min": min_days,
        "estimated_days_max": max_days,
        "days_remaining": days_remaining,
        "estimated_delivery_date": (
            estimated_delivery_date.isoformat()
        ),
        "delivery_status": order.order_status,
        "delivery_message": delivery_message,
    }


# ============================================================
# SERIALIZE ORDER
# ============================================================

def serialize_order(order, include_delivery=True):
    """
    Convert an Order object into a JSON-friendly dictionary.
    """

    payment_status = getattr(order, "payment_status", "Unknown")
    payment_status_display = (
        order.get_payment_status_display()
        if hasattr(order, "get_payment_status_display")
        else str(payment_status).title()
    )
    
    payment_method = getattr(order, "payment_method", "Unknown")
    payment_method_display = (
        order.get_payment_method_display()
        if hasattr(order, "get_payment_method_display")
        else str(payment_method).title()
    )

    data = {
        "id": order.id,
        "status": order.order_status,
        "status_display": (
            order.get_order_status_display()
        ),
        "total_price": str(order.total_price),
        "payment_status": payment_status,
        "payment_status_display": payment_status_display,
        "payment_method": payment_method,
        "payment_method_display": payment_method_display,
        "created_at": (
            order.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )
        ),
        "url": f"/orders/{order.id}/",
    }

    if include_delivery:

        delivery = get_delivery_estimate(order)

        data.update({
            "estimated_delivery_date": (
                delivery["estimated_delivery_date"]
            ),
            "estimated_days_min": (
                delivery["estimated_days_min"]
            ),
            "estimated_days_max": (
                delivery["estimated_days_max"]
            ),
            "days_remaining": (
                delivery["days_remaining"]
            ),
            "delivery_status": (
                delivery["delivery_status"]
            ),
            "delivery_message": (
                delivery["delivery_message"]
            ),
        })

    return data


# ============================================================
# GET USER ORDERS TOOL
# ============================================================

def get_user_orders_tool(
    user,
    order_id=None,
    cancel_order_id=None,
    action="list",
    confirmed=False,
):
    """
    Tool used by the AI assistant to retrieve and manage
    the authenticated user's orders.
    """

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    if not user or not user.is_authenticated:

        return {
            "success": False,
            "message": "Please log in to view your orders.",
        }

    # =========================================================
    # BASE QUERY
    # =========================================================

    orders = (
        Order.objects
        .filter(user=user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    # =========================================================
    # SPECIFIC ORDER
    # =========================================================

    if action == "specific":

        if not order_id:

            return {
                "success": False,
                "action": "specific",
                "message": "Please provide an order ID.",
            }

        order = (
            orders
            .filter(id=order_id)
            .first()
        )

        if not order:

            return {
                "success": False,
                "action": "specific",
                "message": "Order not found.",
            }

        delivery = get_delivery_estimate(order)

        return {
            "success": True,
            "action": "specific",
            "redirect": True,
            "redirect_url": (
                f"/orders/{order.id}/"
            ),
            "navigation": "order_detail",
            "arguments": {
                "order_id": order.id,
            },
            "order": serialize_order(
                order,
                include_delivery=True,
            ),
        }

    # =========================================================
    # TRACK ORDER
    # =========================================================

    if action == "track":

        if not order_id:
            return {
                "success": False,
                "action": "track",
                "redirect": False,
                "message": "Please provide an order ID.",
            }

        order = orders.filter(id=order_id).first()
        if not order:
            return {
                "success": False,
                "action": "track",
                "redirect": False,
                "message": "Order not found.",
            }

        delivery = get_delivery_estimate(order)

        return {

            "success": True,

            "action": "track",

            "redirect": False,

            "redirect_url": None,

            "navigation": "order_tracking",

            "arguments": {
                "order_id": order.id,
            },

            "tracking": {

                "order_id": order.id,

                "status": order.order_status,

                "status_display": (
                    order.get_order_status_display()
                ),

                "created_at": (
                    order.created_at.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                ),

                "estimated_delivery_date": (
                    delivery[
                        "estimated_delivery_date"
                    ]
                ),

                "estimated_days_min": (
                    delivery[
                        "estimated_days_min"
                    ]
                ),

                "estimated_days_max": (
                    delivery[
                        "estimated_days_max"
                    ]
                ),

                "days_remaining": (
                    delivery[
                        "days_remaining"
                    ]
                ),

                "delivery_status": (
                    delivery[
                        "delivery_status"
                    ]
                ),

                "delivery_message": (
                    delivery[
                        "delivery_message"
                    ]
                ),
            },

            "order": serialize_order(order, include_delivery=True),

            "message": (
                delivery[
                    "delivery_message"
                ]
            ),
        }

    # =========================================================
    # DELIVERY ESTIMATE ACTION
    # =========================================================

    if action == "delivery":

        if not order_id:

            order = orders.first()

            if not order:

                return {
                    "success": False,
                    "action": "delivery",
                    "redirect": False,
                    "message": "You do not have any orders to check delivery for.",
                }

        else:

            order = (
                orders
                .filter(id=order_id)
                .first()
            )

            if not order:

                return {
                    "success": False,
                    "action": "delivery",
                    "redirect": False,
                    "message": "Order not found.",
                }

        delivery = get_delivery_estimate(order)

        return {
            "success": True,
            "action": "delivery",
            "redirect": False,
            "redirect_url": None,
            "navigation": "order_delivery",
            "arguments": {
                "order_id": order.id,
            },
            "delivery": {
                "order_id": order.id,
                "status": order.order_status,
                "status_display": order.get_order_status_display(),
                "estimated_delivery_date": delivery["estimated_delivery_date"],
                "days_remaining": delivery["days_remaining"],
                "delivery_status": delivery["delivery_status"],
                "delivery_message": delivery["delivery_message"],
            },
            "order": serialize_order(order, include_delivery=True),
            "message": delivery["delivery_message"],
        }

    # =========================================================
    # CANCEL ORDER
    # =========================================================

    if action == "cancel":

        if not cancel_order_id:

            return {
                "success": False,
                "action": "cancel",
                "message": (
                    "Please provide an order ID to cancel."
                ),
            }

        order = (
            orders
            .filter(id=cancel_order_id)
            .first()
        )

        if not order:

            return {
                "success": False,
                "action": "cancel",
                "message": "Order not found.",
            }

        if (
            order.order_status
            == Order.OrderStatus.CANCELLED
        ):

            return {
                "success": False,
                "action": "cancel",
                "message": (
                    f"Order #{order.id} is already cancelled."
                ),
            }

        if order.order_status in [
            Order.OrderStatus.SHIPPED,
            Order.OrderStatus.DELIVERED,
        ]:

            return {
                "success": False,
                "action": "cancel",
                "message": (
                    f"Order #{order.id} can no longer be "
                    f"cancelled because it is already "
                    f"{order.get_order_status_display().lower()}."
                ),
            }

        if not confirmed:
            return {
                "success": True,
                "action": "cancel",
                "confirmation_required": True,
                "auto_open_cancel": True,
                "redirect": True,
                "redirect_url": reverse("orders:order_detail", args=[order.id]) + "?cancel=1",
                "order_id": order.id,
                "order": serialize_order(order, include_delivery=True),
                "message": f"Are you sure you want to cancel Order #{order.id}?",
            }

        # --------------------------------------------------------
        # ACTUAL CANCELLATION & STOCK RESTORATION
        # --------------------------------------------------------
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order.id, user=user)
            if order.order_status != Order.OrderStatus.PROCESSING:
                return {
                    "success": False,
                    "action": "cancel",
                    "message": "This order can no longer be cancelled.",
                }
            order.order_status = Order.OrderStatus.CANCELLED
            order.save(update_fields=["order_status", "updated_at"])
            for item in order.items.select_related("product"):
                product = Product.objects.select_for_update().get(id=item.product_id)
                product.stock_count += item.quantity
                product.save(update_fields=["stock_count", "updated_at"])

        redirect_url = reverse("orders:order_detail", args=[order.id])

        return {

            "success": True,

            "action": "cancel",

            "navigation": "order_detail",

            "redirect": True,

            "redirect_url": redirect_url,

            "arguments": {
                "order_id": order.id,
            },

            "order_id": order.id,

            "order": serialize_order(order, include_delivery=True),

            "message": f"Order #{order.id} has been cancelled successfully.",
        }

    # =========================================================
    # LIST ORDERS
    # =========================================================

    if action == "list":

        result_orders = []

        for order in orders:

            result_orders.append(
                serialize_order(
                    order,
                    include_delivery=True,
                )
            )

        return {

            "success": True,

            "action": "list",

            "navigation": "order_list",

            "redirect": True,

            "redirect_url": "/orders/",

            "orders": result_orders,

            "message": (
                f"Found {len(result_orders)} "
                f"order(s)."
            ),
        }

    # =========================================================
    # UNKNOWN ACTION
    # =========================================================

    return {
        "success": False,
        "action": action,
        "message": (
            f"Unknown order action: {action}"
        ),
    }


# ============================================================
# EXECUTE TOOL
# ============================================================

def execute_get_user_orders(
    user,
    order_id=None,
    cancel_order_id=None,
    action="list",
    confirmed=False,
):
    """
    Wrapper used by the AI agent and Django views.
    """

    return get_user_orders_tool(
        user=user,
        order_id=order_id,
        cancel_order_id=cancel_order_id,
        action=action,
        confirmed=confirmed,
    )


def delete_order_tool(user, order_id=None):
    if not user or not user.is_authenticated:
        return {"success": False, "message": "Please log in to continue."}
    order = Order.objects.filter(id=order_id, user=user).first()
    if not order:
        return {"success": False, "message": "Order not found."}
    if order.order_status != Order.OrderStatus.CANCELLED:
        return {"success": False, "message": f"Order #{order.id} cannot be deleted because it has not been cancelled."}
    order.delete()
    return {"success": True, "action": "delete_order", "order_id": order_id, "message": f"Order #{order_id} was removed from your order history."}