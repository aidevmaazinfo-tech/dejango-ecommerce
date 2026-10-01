import logging

from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Category, Product

from recommendations.models import UserInteraction
from recommendations.views import get_recommended_products


logger = logging.getLogger(__name__)


# =========================================================
# HOME
# =========================================================

def home_view(request):
    """
    Render the home page with featured products,
    categories and recommended products.
    """

    logger.info(
        "[HOME VIEW] Render requested | User=%s",
        request.user,
    )

    # Shuffles featured products randomly on every page load
    featured_products = (
        Product.objects
        .filter(
            is_active=True,
            stock_count__gt=0,
        )
        .select_related("category")
        .order_by('?')[:8]
    )

    categories = Category.objects.all()

    recommended_products = get_recommended_products(
        request,
        limit=6,
    )

    return render(
        request,
        "products/home.html",
        {
            "featured_products": featured_products,
            "categories": categories,
            "recommended_products": recommended_products,
        },
    )


# =========================================================
# PRODUCT LIST
# =========================================================

def product_list_view(request, category_slug=None):
    """
    Display products with optional category and
    text search filtering.
    """

    query = request.GET.get(
        "q",
        "",
    ).strip()

    logger.info(
        "[PRODUCT LIST VIEW] "
        "Category='%s' | Query='%s' | User=%s",
        category_slug,
        query,
        request.user,
    )

    category = None

    categories = Category.objects.all()

    products = (
        Product.objects
        .filter(
            is_active=True,
        )
        .select_related("category")
    )

    # =====================================================
    # CATEGORY FILTER
    # =====================================================

    if category_slug:

        category = get_object_or_404(
            Category,
            slug=category_slug,
        )

        products = products.filter(
            category=category,
        )

    # =====================================================
    # SEARCH FILTER
    # =====================================================

    if query:

        products = products.filter(
            Q(name__icontains=query)
            |
            Q(description__icontains=query)
        )

    # Shuffles product catalog items randomly on every page load/search
    products = products.order_by('?')

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    recommended_products = get_recommended_products(
        request,
        limit=4,
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "products/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "query": query,
            "recommended_products": recommended_products,
        },
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail_view(request, id, slug):
    """
    Display a single product detail page.

    URL example:

        /product/1084/hp-pavilion-15/
    """

    logger.info(
        "[PRODUCT DETAIL VIEW] "
        "Fetching Product ID=%s | Slug='%s' | User=%s",
        id,
        slug,
        request.user,
    )

    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        is_active=True,
    )

    # =====================================================
    # RECORD PRODUCT VIEW
    # =====================================================

    try:

        UserInteraction.log(
            request=request,
            product=product,
            action_type="VIEW",
        )

    except Exception:

        logger.exception(
            "[PRODUCT DETAIL VIEW] "
            "Unable to record product view."
        )

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    recommended_products = get_recommended_products(
        request,
        limit=4,
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "recommended_products": recommended_products,
        },
    )