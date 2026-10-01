from products.models import Product


def resolve_product(product_name: str):
    """
    Resolve an active product by name.

    Returns a structured result instead of guessing when
    multiple products match.
    """

    product_name = (product_name or "").strip()

    if not product_name:
        return {
            "success": False,
            "status": "missing",
            "message": "Please specify a product.",
        }

    products = Product.objects.filter(
        name__icontains=product_name,
        is_active=True,
    )

    if not products.exists():
        return {
            "success": False,
            "status": "not_found",
            "message": f'No product found matching "{product_name}".',
        }

    # Prefer an exact name match.
    exact_matches = [
        product
        for product in products
        if product.name.lower() == product_name.lower()
    ]

    if len(exact_matches) == 1:
        product = exact_matches[0]

        return {
            "success": True,
            "status": "resolved",
            "product": product,
            "product_id": product.id,
            "product_name": product.name,
        }

    # Don't guess when multiple products match.
    if products.count() > 1:
        return {
            "success": False,
            "status": "multiple_matches",
            "message": f'Multiple products match "{product_name}".',
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                }
                for product in products[:10]
            ],
        }

    product = products.first()

    return {
        "success": True,
        "status": "resolved",
        "product": product,
        "product_id": product.id,
        "product_name": product.name,
    }