from decimal import Decimal

from django.conf import settings

from products.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(
            settings.CART_SESSION_ID
        )

        if cart is None:
            cart = {}
            self.session[settings.CART_SESSION_ID] = cart

        self.cart = cart

    # =========================================================
    # ADD PRODUCT
    # =========================================================

    def add(
        self,
        product,
        quantity=1,
        override_quantity=False,
    ):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.cart[product_id]["price"] = str(
            self.cart[product_id]["price"]
        )

        self.save()

    # =========================================================
    # SAVE SESSION
    # =========================================================

    def save(self):
        self.session.modified = True

    # =========================================================
    # REMOVE ONE PRODUCT
    # =========================================================

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # =========================================================
    # CLEAR ENTIRE CART
    # =========================================================

    def clear(self):
        """
        Remove every product from the cart.
        """

        self.cart.clear()

        self.save()

    # =========================================================
    # ITERATE CART
    # =========================================================

    def __iter__(self):

        product_ids = list(
            self.cart.keys()
        )

        products = Product.objects.filter(
            id__in=product_ids
        )

        product_map = {
            str(product.id): product
            for product in products
        }

        changed = False

        for product_id in product_ids:

            product = product_map.get(
                str(product_id)
            )

            # Product no longer exists.
            if product is None:

                del self.cart[product_id]

                changed = True

                continue

            item = self.cart[product_id]

            stored_price = item.get(
                "price",
                str(product.price),
            )

            price = Decimal(
                str(stored_price)
            )

            quantity = int(
                item.get(
                    "quantity",
                    1
                )
            )

            yield {
                "product": product,
                "quantity": quantity,
                "price": price,
                "total_price": price * quantity,
            }

        if changed:
            self.save()

    # =========================================================
    # CART LENGTH
    # =========================================================

    def __len__(self):

        return sum(
            int(
                item.get(
                    "quantity",
                    0
                )
            )
            for item in self.cart.values()
        )

    # =========================================================
    # TOTAL PRICE
    # =========================================================

    def get_total_price(self):

        total = Decimal("0.00")

        for item in self.cart.values():

            price = Decimal(
                str(item["price"])
            )

            quantity = int(
                item["quantity"]
            )

            total += price * quantity

        return total