from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # ---------------------------------------------------------
    # STANDARD PRODUCT VIEWS
    # ---------------------------------------------------------
    path('', views.home_view, name='home'),

    path(
        'shop/',
        views.product_list_view,
        name='product_list'
    ),

    path(
        'category/<slug:category_slug>/',
        views.product_list_view,
        name='product_list_by_category'
    ),

    path(
        'product/<int:id>/<slug:slug>/',
        views.product_detail_view,
        name='product_detail'
    ),
]