from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # ========================================================
    # ORDER LIST -> /orders/
    # ========================================================
    path(
        "",
        views.order_list,
        name="order_list"
    ),

    # ========================================================
    # CREATE ORDER -> /orders/create/
    # ========================================================
    path(
        "create/",
        views.order_create,
        name="order_create"
    ),

    # ========================================================
    # ORDER DETAIL -> /orders/<id>/
    # ========================================================
    path(
        "<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    # ========================================================
    # CANCEL ORDER -> /orders/<id>/cancel/
    # ========================================================
    path(
        "<int:order_id>/cancel/",
        views.order_cancel,
        name="order_cancel"
    ),

    # ========================================================
    # DELETE CANCELLED ORDER -> /orders/<id>/delete/
    # ========================================================
    path(
        "<int:order_id>/delete/",
        views.order_delete,
        name="order_delete"
    ),
]