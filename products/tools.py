# products/tools.py

from typing import Optional, Dict, Any

from .models import Product
from .services import ProductSearchService


search_service = ProductSearchService()


# ============================================================
# SEARCH PRODUCTS TOOL
# ============================================================

def search_products_tool(
    query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Search active products using flexible OR keyword logic
    and optional price bounds.
    """

    # --------------------------------------------------------
    # SANITIZE PRICE INPUTS
    # --------------------------------------------------------

    try:

        parsed_min = (
            float(min_price)
            if min_price is not None
            else None
        )

        parsed_max = (
            float(max_price)
            if max_price is not None
            else None
        )

    except (TypeError, ValueError):

        return {
            "success": False,
            "message": "Invalid price filter.",
        }

    # --------------------------------------------------------
    # CLEAN QUERY
    # --------------------------------------------------------

    clean_query = query

    if query:

        clean_query = (
            query
            .strip()
            .lower()
            .replace("laptops", "laptop")
            .replace("shoes", "shoe")
        )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    results = search_service.search_products_tool(
        query=clean_query,
        min_price=parsed_min,
        max_price=parsed_max,
        limit=10,
    )

    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if not results:

        search_term = (
            query
            if query
            else "specified filters"
        )

        return {
            "success": False,
            "message": (
                "No active products matched your "
                f"search for: '{search_term}'."
            ),
        }

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    return {
        "success": True,
        "products": results,
    }


# ============================================================
# GET PRODUCT DETAILS TOOL
# ============================================================

def get_product_description_tool(
    product_id: Optional[int] = None,
    product_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get detailed information about a specific active product.

    The product can be identified by product ID or exact
    product name.
    """

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not product_id and not product_name:

        return {
            "success": False,
            "message": (
                "Please provide a product ID or product name."
            ),
        }

    product = None

    # --------------------------------------------------------
    # FIND BY PRODUCT ID
    # --------------------------------------------------------

    if product_id is not None:

        try:

            product = (
                Product.objects
                .select_related("category")
                .filter(
                    id=product_id,
                    is_active=True,
                )
                .first()
            )

        except Exception:

            return {
                "success": False,
                "message": (
                    "Unable to retrieve product details."
                ),
            }

    # --------------------------------------------------------
    # FIND BY PRODUCT NAME
    # --------------------------------------------------------

    elif product_name:

        product = (
            Product.objects
            .select_related("category")
            .filter(
                name__iexact=product_name.strip(),
                is_active=True,
            )
            .first()
        )

    # --------------------------------------------------------
    # PRODUCT NOT FOUND
    # --------------------------------------------------------

    if not product:

        return {
            "success": False,
            "message": (
                "The requested product was not found."
            ),
        }

    # --------------------------------------------------------
    # IMAGE URL
    # --------------------------------------------------------

    image_url = None

    if product.image:

        try:
            image_url = product.image.url
        except ValueError:
            image_url = None

    # --------------------------------------------------------
    # STOCK STATUS
    # --------------------------------------------------------

    if product.stock_count <= 0:

        stock_status = "out_of_stock"

    elif product.stock_count <= 5:

        stock_status = "low_stock"

    else:

        stock_status = "in_stock"

    # --------------------------------------------------------
    # PRODUCT DETAILS
    # --------------------------------------------------------

    product_data = {

        "id": product.id,

        "name": product.name,

        "brand": product.brand,

        "sku": product.sku,

        "description": product.description,

        "price": str(product.price),

        "stock_count": product.stock_count,

        "stock_status": stock_status,

        "is_active": product.is_active,

        # ✅ Flat string category name matching search/frontend expectations
        "category": product.category.name if product.category else None,

        "image": image_url,

        "url": product.get_absolute_url(),

        "created_at": (
            product.created_at.isoformat()
            if product.created_at
            else None
        ),

        "updated_at": (
            product.updated_at.isoformat()
            if product.updated_at
            else None
        ),
    }

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    return {
        "success": True,
        "product": product_data,
    }

# ============================================================
# SEARCH DELIVERED PRODUCTS TOOL
# ============================================================

def search_delivered_products_tool(user) -> Dict[str, Any]:
    """
    Retrieve products from the authenticated user's delivered orders.
    """
    if not user or not user.is_authenticated:
        return {
            "success": False,
            "message": "Please log in to view your delivered products.",
        }

    # Avoid circular imports by importing Order locally inside the function
    try:
        from orders.models import Order
    except ImportError:
        return {
            "success": False,
            "message": "Unable to access order records.",
        }

    # Find all product IDs from DELIVERED orders for this user
    delivered_product_ids = (
        Order.objects.filter(
            user=user, 
            order_status=Order.OrderStatus.DELIVERED
        )
        .values_list("items__product_id", flat=True)
    )

    products = Product.objects.filter(id__in=delivered_product_ids, is_active=True).select_related("category")

    if not products.exists():
        return {
            "success": False,
            "message": "You don't have any delivered products yet.",
        }

    serialized_products = []
    for product in products:
        image_url = None
        if product.image:
            try:
                image_url = product.image.url
            except ValueError:
                image_url = None

        serialized_products.append({
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "sku": product.sku,
            "description": product.description,
            "price": str(product.price),
            "stock_count": product.stock_count,
            "category": product.category.name if product.category else None,
            "image": image_url,
            "url": product.get_absolute_url(),
        })

    return {
        "success": True,
        "products": serialized_products,
        "message": f"Found {len(serialized_products)} delivered product(s).",
    }