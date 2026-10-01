from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from search.models import SearchLog
from search.services.chat import ChatService

from products.models import Product
from intents.models import Intent


# =========================================================
# CHAT PAGE
# =========================================================

@require_http_methods(["GET"])
def chat_page(request):

    history = (
        SearchLog.objects
        .select_related(
            "matched_intent",
            "matched_product",
        )
        .order_by("-created_at")[:50]
    )

    return render(
        request,
        "chat/index.html",
        {
            "history": history,
        },
    )


# =========================================================
# NEW CHAT
# =========================================================

@require_http_methods(["GET"])
def new_chat(request):

    return redirect("search:chat")


# =========================================================
# CHAT MESSAGE
# =========================================================

@require_http_methods(["POST"])
def message(request):

    try:

        # -------------------------------------------------
        # GET USER MESSAGE
        # -------------------------------------------------

        query = (
            request.POST.get("message", "")
            .strip()
        )

        if not query:

            return JsonResponse(
                {
                    "answer": "Please enter a message.",
                    "type": "error",
                    "intent": None,
                    "document": None,
                    "product": None,
                    "products": [],
                    "category": None,
                    "product_name": None,
                    "product_url": None,
                    "price": None,
                    "stock_count": None,
                    "score": None,
                },
                status=400,
            )

        # -------------------------------------------------
        # CHAT SERVICE
        # -------------------------------------------------

        service = ChatService()

        result = service.process_message(
            query,
            user=request.user,
        )

        # -------------------------------------------------
        # MATCHED PRODUCT
        # -------------------------------------------------

        matched_product = None

        # For a single product result.
        if result.get("product"):

            product_id = (
                result["product"].get("id")
            )

            if product_id:

                matched_product = (
                    Product.objects
                    .filter(
                        id=product_id,
                        is_active=True,
                    )
                    .first()
                )

        # -------------------------------------------------
        # MATCHED INTENT
        # -------------------------------------------------

        matched_intent = None

        if result.get("intent"):

            matched_intent = (
                Intent.objects
                .filter(
                    intent_name=result["intent"],
                    is_active=True,
                )
                .first()
            )

        # -------------------------------------------------
        # SAVE SEARCH LOG
        # -------------------------------------------------

        SearchLog.objects.create(
            query=query,
            matched_intent=matched_intent,
            matched_product=matched_product,
        )

        # -------------------------------------------------
        # RETURN CHAT RESPONSE
        # -------------------------------------------------

        return JsonResponse(
            result,
            status=200,
        )

    except Exception as error:

        print("=================================")
        print("CHAT ERROR:")
        print(repr(error))
        print("=================================")

        return JsonResponse(
            {
                "answer": (
                    "Sorry, something went wrong "
                    "while processing your message."
                ),
                "type": "error",
                "intent": None,
                "document": None,
                "product": None,
                "products": [],
                "category": None,
                "product_name": None,
                "product_url": None,
                "price": None,
                "stock_count": None,
                "score": None,
            },
            status=500,
        )


# =========================================================
# CLEAR HISTORY
# =========================================================

@require_http_methods(["POST"])
def clear_history(request):

    try:

        SearchLog.objects.all().delete()

        return JsonResponse(
            {
                "success": True
            }
        )

    except Exception as error:

        print(
            "CLEAR HISTORY ERROR:",
            repr(error)
        )

        return JsonResponse(
            {
                "success": False,
                "error": "Unable to clear history.",
            },
            status=500,
        )


# =========================================================
# ADMIN GLOBAL SEARCH
# =========================================================

@require_http_methods(["GET"])
def admin_global_search(request):
    """
    Admin panel ka global smart search view.
    URL: /admin/global-search/?q=search_term
    """

    # Sirf staff members ke liye
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Access denied. Staff only.")

    from .services.global_search import GlobalSearchService

    query = request.GET.get('q', '').strip()
    results = None
    error_message = None
    execution_time = None

    if query:
        import time
        start_time = time.time()

        try:
            # Global search service call karo
            results = GlobalSearchService.search_all(query)

            # Search log mein save karo (existing model use karke)
            SearchLog.objects.create(query=query)

            execution_time = round(time.time() - start_time, 3)
        except Exception as e:
            error_message = f"Search error: {str(e)}"
            print(f"GLOBAL SEARCH ERROR: {repr(e)}")

    context = {
        'query': query,
        'results': results,
        'error_message': error_message,
        'execution_time': execution_time,
        'title': 'Global Smart Search',
        'is_nav_sidebar_enabled': True,
    }

    return render(request, 'admin/global_search.html', context)


# =========================================================
# ADMIN DASHBOARD (Custom View)
# =========================================================

@require_http_methods(["GET"])
def admin_dashboard(request):
    """
    Custom admin dashboard with global search and stats.
    URL: /admin/dashboard/
    """
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Access denied. Staff only.")

    from django.contrib.admin.sites import site
    from django.contrib.auth import get_user_model
    from orders.models import Order
    from products.models import Product
    from django.db.models import Sum

    User = get_user_model()

    # Basic stats
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()

    # Order status counts
    pending_orders_count = Order.objects.filter(order_status='PROCESSING').count()
    shipped_orders_count = Order.objects.filter(order_status='SHIPPED').count()
    delivered_orders_count = Order.objects.filter(order_status='DELIVERED').count()
    cancelled_orders_count = Order.objects.filter(order_status='CANCELLED').count()

    # Stock counts
    low_stock_count = Product.objects.filter(stock_count__lte=5, is_active=True).count()
    out_of_stock_count = Product.objects.filter(stock_count=0, is_active=True).count()

    # Revenue
    total_revenue = Order.objects.filter(payment_status='COMPLETED').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    # Recent orders (latest 5)
    recent_orders = Order.objects.order_by('-created_at')[:5]

    # Low stock products
    low_stock_list = Product.objects.filter(
        stock_count__lte=5,
        is_active=True
    ).order_by('stock_count')[:5]

    # Pending orders list
    pending_orders_list = Order.objects.filter(
        order_status='PROCESSING'
    ).order_by('-created_at')[:5]

    # App list
    app_list = site.get_app_list(request)

    context = {
        'title': 'Dashboard',
        'app_list': app_list,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'pending_orders_count': pending_orders_count,
        'shipped_orders_count': shipped_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_list': low_stock_list,
        'pending_orders_list': pending_orders_list,
        'site_header': 'E-commerce Admin',
        'site_title': 'E-commerce Admin',
        'index_title': 'Welcome to Admin Panel',
        'has_permission': True,
    }

    return render(request, 'admin/index.html', context)


# =========================================================
# LIVE STATS API (For Dashboard Auto-Refresh)
# =========================================================

@require_http_methods(["GET"])
def live_stats_api(request):
    """
    Dashboard ke liye live stats return karta hai.
    Ye API har 30 seconds mein call hogi bina page reload ke.
    """

    # Sirf staff members ke liye
    if not request.user.is_staff:
        return JsonResponse({"error": "Access denied"}, status=403)

    from django.contrib.auth import get_user_model
    from orders.models import Order
    from products.models import Product
    from django.db.models import Sum

    User = get_user_model()

    stats = {
        'total_users': User.objects.count(),
        'total_orders': Order.objects.count(),
        'total_products': Product.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'pending_orders': Order.objects.filter(order_status__icontains='PENDING').count(),
        'delivered_orders': Order.objects.filter(order_status__icontains='DELIVERED').count(),
        'total_revenue': Order.objects.aggregate(total=Sum('total_price'))['total'] or 0,
        'out_of_stock': Product.objects.filter(stock_count=0).count(),
    }

    return JsonResponse(stats)