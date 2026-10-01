from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Ye imports add karo top pe
from search.views import admin_global_search, admin_dashboard


urlpatterns = [

    # ==========================
    # PRODUCTS
    # ==========================

    path(
        "",
        include(("products.urls", "products"), namespace="products"),
    ),

    # ==========================
    # ADMIN DASHBOARD (CUSTOM)
    # ==========================

    path(
        "admin/dashboard/",
        admin_dashboard,
        name="admin-dashboard",
    ),

    # ==========================
    # ADMIN GLOBAL SEARCH
    # ==========================

    path(
        "admin/global-search/",
        admin_global_search,
        name="admin-global-search",
    ),

    # ==========================
    # ADMIN
    # ==========================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==========================
    # ACCOUNTS
    # ==========================

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    # ==========================
    # CART
    # ==========================

    path(
        "cart/",
        include("cart.urls"),
    ),

    # ==========================
    # ORDERS
    # ==========================

    path(
        "orders/",
        include("orders.urls"),
    ),

    # ==========================
    # CHATBOT
    # ==========================

    path(
        "chat/",
        include("search.urls"),
    ),

    # ==========================
    # RECOMMENDATIONS
    # ==========================

    path(
        "recommendations/",
        include("recommendations.urls")
    ),

    # ==========================
    # ASSISTANT
    # ==========================

    path(
        "assistant/",
        include("assistant.urls"),
    ),
]


# ==========================
# MEDIA + STATIC FILES
# ==========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )