import uuid
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Order, OrderItem
from .forms import OrderCreateForm

from cart.cart import Cart
from .tools import execute_get_user_orders


def mock_payment_gateway(order_total, card_details):
    """
    Placeholder Integration Point for Stripe/PayPal.
    Returns transaction_id upon success.
    """
    return f"TXN-{uuid.uuid4().hex[:10].upper()}"


# ============================================================
# CREATE ORDER
# ============================================================

def order_create(request):

    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(
            request,
            "Your cart is empty."
        )
        return redirect(
            "products:product_list"
        )

    if request.method == "POST":

        form = OrderCreateForm(
            request.POST
        )

        if form.is_valid():

            order = form.save(
                commit=False
            )

            if request.user.is_authenticated:
                order.user = request.user

            order.total_price = cart.get_total_price()

            # =================================================
            # ESTIMATED DELIVERY
            # =================================================

            order.estimated_delivery_date = (
                timezone.localdate() + timedelta(days=5)
            )

            try:
                with transaction.atomic():
                    order.save()
                    for item in cart:
                        product = item["product"].__class__.objects.select_for_update().get(id=item["product"].id)
                        if product.stock_count < item["quantity"]:
                            raise ValidationError(f"{product.name} does not have enough stock.")
                        OrderItem.objects.create(order=order, product=product, price=item["price"], quantity=item["quantity"])
                        product.stock_count -= item["quantity"]
                        product.save(update_fields=["stock_count", "updated_at"])
            except ValidationError as error:
                messages.error(request, error.message)
                return render(request, "orders/checkout.html", {"cart": cart, "form": form})

            # =================================================
            # PAYMENT & METHOD HANDLING
            # =================================================

            if order.payment_method == Order.PaymentMethod.COD:
                order.payment_status = Order.PaymentStatus.PENDING
                order.transaction_id = ""
            else:
                txn_id = mock_payment_gateway(
                    order.total_price,
                    request.POST.get("payment_token")
                )
                order.payment_status = Order.PaymentStatus.COMPLETED
                order.transaction_id = txn_id

            order.save()

            # =================================================
            # CLEAR CART
            # =================================================

            cart.clear()

            return render(
                request,
                "orders/created.html",
                {
                    "order": order
                }
            )

    else:

        initial_data = {}

        if request.user.is_authenticated:
            initial_data = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "address": getattr(request.user, "shipping_address", ""),
            }

        form = OrderCreateForm(
            initial=initial_data
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "cart": cart,
            "form": form
        }
    )


# ============================================================
# ORDER LIST
# ============================================================

@login_required
def order_list(request):

    orders = (
        Order.objects
        .filter(
            user=request.user
        )
        .prefetch_related(
            "items__product"
        )
        .order_by(
            "-created_at"
        )
    )

    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders,
        }
    )


# ============================================================
# ORDER DETAIL
# ============================================================

@login_required
def order_detail(
    request,
    order_id
):

    order = (
        Order.objects
        .prefetch_related(
            "items__product"
        )
        .filter(
            id=order_id,
            user=request.user
        )
        .first()
    )

    if not order:
        messages.error(
            request,
            "Order not found."
        )
        return redirect(
            "orders:order_list"
        )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
        }
    )


# ============================================================
# CANCEL ORDER
# ============================================================

@login_required
def order_cancel(
    request,
    order_id
):
    """
    Actually cancels the order.

    This endpoint is only reached after the user
    confirms the cancellation popup.
    """

    if request.method != "POST":
        return redirect(
            "orders:order_detail",
            order_id=order_id
        )

    result = execute_get_user_orders(
        user=request.user,
        cancel_order_id=order_id,
        action="cancel",
        confirmed=True,
    )

    if result.get("success"):
        messages.success(
            request,
            result.get(
                "message",
                "Your order has been cancelled successfully."
            )
        )
    else:
        messages.error(
            request,
            result.get(
                "error",
                result.get(
                    "message",
                    "Unable to cancel this order."
                )
            )
        )

    return redirect(
        "orders:order_detail",
        order_id=order_id
    )


# ============================================================
# DELETE CANCELLED ORDER
# ============================================================

@login_required
def order_delete(request, order_id):

    if request.method != "POST":
        return redirect(
            "orders:order_list"
        )

    order = (
        Order.objects
        .filter(
            id=order_id,
            user=request.user
        )
        .first()
    )

    if not order:
        messages.error(
            request,
            "Order not found."
        )
        return redirect(
            "orders:order_list"
        )

    if order.order_status != Order.OrderStatus.CANCELLED:
        messages.error(
            request,
            "Only cancelled orders can be deleted."
        )
        return redirect(
            "orders:order_list"
        )

    order.delete()

    messages.success(
        request,
        f"Order #{order_id} has been removed from your order history."
    )

    return redirect(
        "orders:order_list"
    )