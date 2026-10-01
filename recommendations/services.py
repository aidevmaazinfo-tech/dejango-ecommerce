import logging
from collections import Counter
from django.db.models import Count
from products.models import Product
from .models import UserInteraction

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Multi-strategy recommendation engine that evaluates user activity context
    and returns tailored product recommendations.
    """

    def __init__(self, request, limit=4):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        self.session_key = request.session.session_key
        self.limit = limit

    def get_user_interactions(self, limit=20):
        """Fetch recent interactions for current session or user account."""
        if not self.session_key and not self.user:
            return UserInteraction.objects.none()

        query = UserInteraction.objects.all()
        if self.user:
            query = query.filter(user=self.user)
        elif self.session_key:
            query = query.filter(session_key=self.session_key)

        return query.select_related("product", "product__category").order_by("-created_at")[:limit]

    def strategy_cart_complements(self):
        """Recommend items related to products recently added to cart."""
        cart_interactions = self.get_user_interactions().filter(action_type="CART_ADD")
        if not cart_interactions.exists():
            return Product.objects.none()

        cart_categories = [i.product.category_id for i in cart_interactions if i.product and i.product.category_id]
        cart_product_ids = [i.product_id for i in cart_interactions if i.product_id]

        if not cart_categories:
            return Product.objects.none()

        return (
            Product.objects.filter(is_active=True, stock_count__gt=0, category_id__in=cart_categories)
            .exclude(id__in=cart_product_ids)
            .distinct()[:self.limit]
        )

    def strategy_category_affinity(self):
        """Recommend products from the category the user views most frequently."""
        recent_views = self.get_user_interactions().filter(action_type="VIEW")
        if not recent_views.exists():
            return Product.objects.none()

        categories = [i.product.category_id for i in recent_views if i.product and i.product.category_id]
        if not categories:
            return Product.objects.none()

        most_frequent_cat = Counter(categories).most_common(1)[0][0]
        viewed_product_ids = [i.product_id for i in recent_views if i.product_id]

        return (
            Product.objects.filter(is_active=True, stock_count__gt=0, category_id=most_frequent_cat)
            .exclude(id__in=viewed_product_ids)
            .distinct()[:self.limit]
        )

    def strategy_popular_fallback(self):
        """Fallback strategy: Return active products with the highest view counts."""
        return (
            Product.objects.filter(is_active=True, stock_count__gt=0)
            .annotate(interaction_count=Count("userinteraction"))
            .order_by("-interaction_count", "-created_at")[:self.limit]
        )

    def get_recommendations(self):
        """
        Decision Matrix: Chooses the optimal strategy based on context depth.
        """
        # 1. High intent: Cart activity present -> Complementary items
        recommendations = list(self.strategy_cart_complements())
        if len(recommendations) >= self.limit:
            return recommendations[:self.limit]

        # 2. Medium intent: Category affinity from views
        affinity_recs = list(self.strategy_category_affinity())
        for prod in affinity_recs:
            if prod not in recommendations:
                recommendations.append(prod)
            if len(recommendations) >= self.limit:
                return recommendations[:self.limit]

        # 3. Cold start / Fallback: Popular items
        popular_recs = list(self.strategy_popular_fallback())
        for prod in popular_recs:
            if prod not in recommendations:
                recommendations.append(prod)
            if len(recommendations) >= self.limit:
                break

        return recommendations[:self.limit]