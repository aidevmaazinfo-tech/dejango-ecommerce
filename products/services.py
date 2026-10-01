from django.db.models import Q

from .models import Product


class ProductSearchService:
    """
    Searches the ecommerce product database.

    Search behavior:
    - Each meaningful keyword must match.
    - A keyword can match name, description, brand, SKU, or category.
    - Price filters are applied independently.
    - Only active and in-stock products are returned.
    """

    # Words that should not affect product matching.
    STOP_WORDS = {
        "a",
        "an",
        "the",
        "in",
        "of",
        "to",
        "for",
        "with",
        "and",
        "or",
        "on",
        "at",
        "from",
        "between",
        "range",
        "show",
        "find",
        "search",
        "get",
        "look",
        "looking",
        "me",
        "please",
    }

    def search(
        self,
        query=None,
        min_price=None,
        max_price=None,
        limit=20,
    ):
        products = Product.objects.filter(
            is_active=True,
            stock_count__gt=0,
        )

        # --------------------------------------------------
        # PRODUCT KEYWORD SEARCH
        # --------------------------------------------------
        if query and query.strip():

            clean_query = query.strip().lower()

            keywords = [
                word
                for word in clean_query.split()
                if word not in self.STOP_WORDS
            ]

            # Each keyword must match at least one field.
            #
            # Example:
            # "gaming laptop"
            #
            # becomes:
            #
            # gaming -> name OR description OR brand OR SKU OR category
            # AND
            # laptop -> name OR description OR brand OR SKU OR category
            #
            # This prevents unrelated products from appearing.
            if keywords:
                query_filter = Q()

                for word in keywords:
                    word_filter = (
                        Q(name__icontains=word)
                        | Q(description__icontains=word)
                        | Q(brand__icontains=word)
                        | Q(sku__icontains=word)
                        | Q(category__name__icontains=word)
                    )

                    query_filter &= word_filter

                products = products.filter(query_filter)

        # --------------------------------------------------
        # MINIMUM PRICE
        # --------------------------------------------------
        if min_price is not None:
            products = products.filter(
                price__gte=min_price
            )

        # --------------------------------------------------
        # MAXIMUM PRICE
        # --------------------------------------------------
        if max_price is not None:
            products = products.filter(
                price__lte=max_price
            )

        # --------------------------------------------------
        # RETURN RESULTS
        # --------------------------------------------------
        return (
            products
            .select_related("category")
            .distinct()
            .order_by(
                "-stock_count",
                "-created_at",
            )[:limit]
        )

    def get_product_response(self, product):
        if not product:
            return None

        return {
            "id": product.id,
            "name": product.name,
            "brand": (
                product.brand
                if getattr(product, "brand", None)
                else ""
            ),
            "description": product.description,
            "price": str(product.price),
            "stock_count": product.stock_count,
            "in_stock": product.stock_count > 0,
            "category": (
                product.category.name
                if product.category
                else "General"
            ),
            "image_url": (
                product.image.url
                if getattr(product, "image", None)
                else None
            ),
            "url": (
                product.get_absolute_url()
                if hasattr(product, "get_absolute_url")
                else f"/products/{product.id}/"
            ),
        }

    def search_products_tool(
        self,
        query=None,
        min_price=None,
        max_price=None,
        limit=20,
    ):
        products = self.search(
            query=query,
            min_price=min_price,
            max_price=max_price,
            limit=limit,
        )

        return [
            self.get_product_response(product)
            for product in products
        ]