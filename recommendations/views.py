from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, Case, When, FloatField
from products.models import Product
from .models import UserInteraction, CachedRecommendation


class RecommendationEngine:
    """
    Scoring-based recommendation engine that evaluates category affinity,
    action weights, and novelty preferences via database-level annotations.
    Serves as an immediate calculation fallback when agent cache is missing.
    """

    def __init__(self, request, limit=8):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        self.session_key = request.session.session_key
        self.limit = limit

    def get_user_interactions(self):
        """Fetch user or session interactions."""
        if self.user:
            return UserInteraction.objects.filter(user=self.user)
        elif self.session_key:
            return UserInteraction.objects.filter(session_key=self.session_key)
        return UserInteraction.objects.none()

    def get_recommendations(self):
        interactions = self.get_user_interactions()

        # Base active product QuerySet with safety filter guards
        products = Product.objects.all()
        if hasattr(Product, "is_active"):
            products = products.filter(is_active=True)
        if hasattr(Product, "stock_count"):
            products = products.filter(stock_count__gt=0)

        # Fallback for guest users with no session history
        if not interactions.exists():
            return list(products[:self.limit])

        # Extract interacted product IDs and category weights
        interacted_product_ids = interactions.values_list("product_id", flat=True).distinct()

        # Aggregate weighted scores per category
        category_weights = (
            interactions.filter(product__category__isnull=False)
            .values("product__category_id")
            .annotate(total_weight=Sum("weight"))
            .order_by("-total_weight")
        )

        category_scores = {
            item["product__category_id"]: item["total_weight"] or 1.0 
            for item in category_weights
        }

        top_category_id = (
            max(category_scores, key=category_scores.get) if category_scores else None
        )

        # Build dynamic scoring cases for ORM evaluation
        whens = []
        if top_category_id:
            whens.append(When(category_id=top_category_id, then=10.0))

        for cat_id in category_scores:
            if cat_id != top_category_id:
                whens.append(When(category_id=cat_id, then=5.0))

        if whens:
            score_expression = Case(
                *whens,
                default=0.0,
                output_field=FloatField(),
            )
            # Annotate category score and apply penalty for already-interacted items
            products = products.annotate(category_score=score_expression)
            products = products.annotate(
                final_score=Case(
                    When(id__in=interacted_product_ids, then=score_expression - 2.0),
                    default=score_expression,
                    output_field=FloatField(),
                )
            ).order_by("-final_score", "-id")
        else:
            # Fallback if no categories were recorded: prioritize unseen products
            products = products.annotate(
                final_score=Case(
                    When(id__in=interacted_product_ids, then=-2.0),
                    default=0.0,
                    output_field=FloatField(),
                )
            ).order_by("-final_score", "-id")

        return list(products[:self.limit])


# =========================================================
# HELPER & VIEW FUNCTIONS
# =========================================================

def get_recommended_products(request, limit=8):
    """
    1. Reads pre-calculated recommendations from CachedRecommendation (Autonomous Agent).
    2. Dynamically calculates scores via RecommendationEngine if cache is not available.
    """
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key

    cache_obj = None
    if user:
        cache_obj = CachedRecommendation.objects.filter(user=user).first()
    elif session_key:
        cache_obj = CachedRecommendation.objects.filter(session_key=session_key).first()

    if cache_obj and cache_obj.recommended_products.exists():
        qs = cache_obj.recommended_products.all()
        if hasattr(Product, "is_active"):
            qs = qs.filter(is_active=True)
        if hasattr(Product, "stock_count"):
            qs = qs.filter(stock_count__gt=0)
        return list(qs[:limit])

    # Dynamic fallback calculation
    engine = RecommendationEngine(request=request, limit=limit)
    return engine.get_recommendations()


def recommendation_api_view(request):
    """
    REST API Endpoint: GET /recommendations/api/v1/recommendations/
    Returns JSON formatted recommendations derived from the Autonomous Agent Cache.
    """
    products = get_recommended_products(request, limit=8)

    data = []
    for product in products:
        prod_data = {
            "id": product.id,
            "name": getattr(product, "name", getattr(product, "title", f"Product #{product.id}")),
            "price": str(getattr(product, "price", "0.00")),
            "category": product.category.name if getattr(product, "category", None) else None,
        }

        if hasattr(product, "slug"):
            prod_data["slug"] = product.slug
        if hasattr(product, "get_absolute_url"):
            prod_data["url"] = product.get_absolute_url()
        elif hasattr(product, "id"):
            prod_data["url"] = f"/products/{product.id}/"

        if hasattr(product, "image") and getattr(product.image, "url", None):
            prod_data["image_url"] = product.image.url
        else:
            prod_data["image_url"] = None

        data.append(prod_data)

    return JsonResponse(
        {
            "status": "success",
            "count": len(data),
            "recommendations": data,
        },
        status=200,
    )


def recommendation_section_view(request):
    """
    View to render automatic recommended products directly on an HTML template fragment.
    """
    recommended_products = get_recommended_products(request, limit=6)
    return render(
        request,
        "recommendations/recommended_list.html",
        {"recommended_products": recommended_products},
    )