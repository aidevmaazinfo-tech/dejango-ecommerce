import re
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher

from products.models import Product, Category
from orders.models import Order


class ChatService:
    """
    Ecommerce chatbot search service.

    Search flow:

        Message
            ↓
        Intent detection
            ↓
        Order detection
            ↓
        Filter extraction
            ↓
        Category search
            ↓
        Product search
            ↓
        Product scoring
            ↓
        Response
    """
    
    # =========================================================
    # INTENT RESPONSES
    # =========================================================

    INTENT_RESPONSES = {
        "hello": (
            "Hello! 👋 What are you looking for today?"
        ),

        "bye": (
            "Goodbye! 👋 Thanks for shopping with us!"
        ),

        "thanks": (
            "You're welcome! 😊 Happy shopping!"
        ),

        "help": (
            "I can help you find products, check prices, "
            "availability, categories, product details, "
            "and your orders.\n\n"

            "Try asking:\n"
            "• Show me laptops\n"
            "• Do you have headphones?\n"
            "• Wireless headphones under $100\n"
            "• Show products under $500\n"
            "• Show me products in stock\n"
            "• Tell me about UltraBook Pro 15\n"
            "• Where is my order?\n"
            "• Show my orders\n"
            "• What is the status of order 15"
        ),
    }

    # =========================================================
    # STOP WORDS
    # =========================================================

    STOP_WORDS = {
        # General
        "the",
        "a",
        "an",
        "and",
        "or",
        "for",
        "you",
        "have",
        "has",
        "does",
        "this",
        "that",
        "these",
        "those",
        "what",
        "tell",
        "about",
        "show",
        "give",
        "with",
        "from",
        "are",
        "is",
        "can",
        "could",
        "please",
        "want",
        "need",
        "me",
        "do",
        "there",
        "any",
        "your",
        "i",
        "am",
        "looking",
        "find",
        "product",
        "products",
        "available",
        "price",
        "prices",
        "cost",
        "much",
        "many",
        "get",
        "buy",
        "purchase",
        "search",
        "searching",
        "some",

        # Location / relation
        "in",
        "on",
        "at",
        "to",
        "of",

        # Price
        "under",
        "below",
        "less",
        "than",
        "over",
        "above",
        "more",
        "between",
        "cheap",
        "cheapest",
        "expensive",
        "lowest",
        "highest",
        "maximum",
        "minimum",
        "max",
        "min",

        # Stock
        "currently",
        "stock",

        # Order
        "my",
        "order",
        "orders",
        "ordered",
        "status",
        "tracking",
        "track",
        "delivery",
        "delivered",
        "shipped",
        "shipping",
        "processing",
        "payment",
    }

    # =========================================================
    # SYNONYMS
    # =========================================================

    SYNONYMS = {
        # Phones
        "mobile": "phone",
        "mobiles": "phone",
        "smartphone": "phone",
        "smartphones": "phone",
        "cellphone": "phone",
        "cellphones": "phone",
        "cell": "phone",


        # Computers
        "notebook": "laptop",
        "notebooks": "laptop",
        "laptops": "laptop",

        # TV
        "television": "tv",
        "televisions": "tv",
        "tvs": "tv",

        # Audio
        "earphones": "earphone",
        "headphones": "headphone",
        "headsets": "headset",

        # Accessories
        "bags": "bag",
        "watches": "watch",

        # Display
        "monitors": "monitor",

        # Gaming
        "controllers": "controller",
        "gamepads": "gamepad",

        # Storage
        "ssds": "ssd",

        # Lights
        "lights": "light",

        # Smart home
        "smartwatches": "smartwatch",
    }

    # =========================================================
    # MAIN PROCESSOR
    # =========================================================

    def process_message(self, message, user=None):

        message = (message or "").strip()

        if not message:
            return self.error_response(
                "Please enter a message."
            )

        # -----------------------------------------------------
        # 1. CONVERSATION INTENT
        # -----------------------------------------------------

        intent = self.detect_intent(message)

        if intent:
            return self.intent_response(intent)

        # -----------------------------------------------------
        # 2. ORDER SEARCH
        # -----------------------------------------------------

        if self.is_order_query(message):
            return self.handle_order_query(
                message,
                user,
            )

        # -----------------------------------------------------
        # 3. EXTRACT FILTERS
        # -----------------------------------------------------

        filters = self.extract_filters(message)

        # -----------------------------------------------------
        # 4. CATEGORY SEARCH
        # -----------------------------------------------------

        category_result = self.find_category(message)

        if category_result:

            category, products = category_result

            products = self.apply_product_filters(
                products,
                filters,
            )

            products = self.sort_products(
                products,
                filters,
            )

            if products:
                return self.category_response(
                    category,
                    products,
                    filters=filters,
                )

        # -----------------------------------------------------
        # 5. PRODUCT SEARCH
        # -----------------------------------------------------

        products = self.find_products(
            message,
            filters=filters,
        )

        if products:

            if len(products) == 1:
                return self.product_response(
                    products[0]
                )

            return self.products_response(
                products,
                filters=filters,
            )

        # -----------------------------------------------------
        # 6. NOTHING FOUND
        # -----------------------------------------------------

        return self.normal_response(message)

    # =========================================================
    # INTENT DETECTION
    # =========================================================

    def detect_intent(self, message):

        text = self.normalize_text(message)

        hello_words = {
            "hi",
            "hello",
            "hey",
            "hi there",
            "hello there",
            "hey there",
            "good morning",
            "good afternoon",
            "good evening",
        }

        bye_words = {
            "bye",
            "goodbye",
            "see you",
            "see you later",
            "good night",
        }

        thanks_words = {
            "thanks",
            "thank you",
            "thankyou",
            "thanks a lot",
            "thank you very much",
        }

        help_words = {
            "help",
            "i need help",
            "can you help me",
            "what can you do",
        }

        if text in hello_words:
            return "hello"

        if text in bye_words:
            return "bye"

        if text in thanks_words:
            return "thanks"

        if text in help_words:
            return "help"

        return None

    # =========================================================
    # INTENT RESPONSE
    # =========================================================

    def intent_response(self, intent):

        return {
            "answer": self.INTENT_RESPONSES[intent],
            "type": "intent",
            "intent": intent,
            "document": None,
            "product": None,
            "products": [],
            "category": None,
            "orders": [],
            "order": None,
            "product_name": None,
            "product_url": None,
            "price": None,
            "stock_count": None,
            "score": None,
        }

    # =========================================================
    # ORDER QUERY
    # =========================================================

    def is_order_query(self, message):

        text = self.normalize_text(message)

        order_words = {
            "order",
            "orders",
            "ordered",
            "delivery",
            "delivered",
            "shipping",
            "shipped",
            "tracking",
            "track",
            "payment",
        }

        words = set(text.split())

        return bool(
            words.intersection(order_words)
        )

    # =========================================================
    # HANDLE ORDER QUERY
    # =========================================================

    def handle_order_query(self, message, user):

        if not user or not getattr(
            user,
            "is_authenticated",
            False,
        ):

            return {
                "answer": (
                    "Please log in to view your orders."
                ),
                "type": "order",
                "intent": "order_search",
                "document": None,
                "product": None,
                "products": [],
                "category": None,
                "orders": [],
                "order": None,
                "product_name": None,
                "product_url": None,
                "price": None,
                "stock_count": None,
                "score": None,
            }

        order_id = self.extract_order_number(
            message
        )

        # -----------------------------------------------------
        # Specific order
        # -----------------------------------------------------

        if order_id:

            order = (
                Order.objects
                .filter(
                    id=order_id,
                    user=user,
                )
                .prefetch_related(
                    "items__product"
                )
                .first()
            )

            if not order:

                return {
                    "answer": (
                        f"I couldn't find order "
                        f"#{order_id} in your account."
                    ),
                    "type": "order",
                    "intent": "order_search",
                    "document": None,
                    "product": None,
                    "products": [],
                    "category": None,
                    "orders": [],
                    "order": None,
                    "product_name": None,
                    "product_url": None,
                    "price": None,
                    "stock_count": None,
                    "score": None,
                }

            return self.order_response(order)

        # -----------------------------------------------------
        # Latest orders
        # -----------------------------------------------------

        orders = list(
            Order.objects
            .filter(user=user)
            .prefetch_related(
                "items__product"
            )
            .order_by("-created_at")[:10]
        )

        if not orders:

            return {
                "answer": (
                    "You don't have any orders yet."
                ),
                "type": "order",
                "intent": "order_search",
                "document": None,
                "product": None,
                "products": [],
                "category": None,
                "orders": [],
                "order": None,
                "product_name": None,
                "product_url": None,
                "price": None,
                "stock_count": None,
                "score": None,
            }

        if len(orders) == 1:
            return self.order_response(
                orders[0]
            )

        return self.orders_response(
            orders
        )

    # =========================================================
    # EXTRACT ORDER NUMBER
    # =========================================================

    def extract_order_number(self, message):

        patterns = [
            r"\border\s*#?\s*(\d+)\b",
            r"\border\s+number\s*#?\s*(\d+)\b",
            r"\border\s+no\.?\s*#?\s*(\d+)\b",
            r"\border\s+id\s*#?\s*(\d+)\b",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                message,
                re.IGNORECASE,
            )

            if match:

                try:
                    return int(
                        match.group(1)
                    )

                except (
                    ValueError,
                    TypeError,
                ):
                    return None

        return None

    # =========================================================
    # ORDER DATA
    # =========================================================

    def order_data(self, order):

        items = []

        for item in order.items.all():

            items.append({
                "id": item.id,

                "product_id": (
                    item.product.id
                    if item.product
                    else None
                ),

                "product_name": (
                    item.product.name
                    if item.product
                    else "Product"
                ),

                "quantity": item.quantity,

                "price": str(item.price),

                "cost": str(item.get_cost()),
            })

        return {
            "id": order.id,

            "order_number": order.id,

            "first_name": order.first_name,

            "last_name": order.last_name,

            "email": order.email,

            "address": order.address,

            "postal_code": order.postal_code,

            "city": order.city,

            "created_at": (
                order.created_at.isoformat()
                if order.created_at
                else None
            ),

            "updated_at": (
                order.updated_at.isoformat()
                if order.updated_at
                else None
            ),

            "total_price": str(
                order.total_price
            ),

            "payment_status": (
                order.get_payment_status_display()
            ),

            "payment_status_code": (
                order.payment_status
            ),

            "order_status": (
                order.get_order_status_display()
            ),

            "order_status_code": (
                order.order_status
            ),

            "transaction_id": (
                order.transaction_id
            ),

            "items": items,
        }

    # =========================================================
    # SINGLE ORDER RESPONSE
    # =========================================================

    def order_response(self, order):

        data = self.order_data(order)

        lines = [
            f"📦 Order #{order.id}",
            "",
            (
                f"Status: "
                f"{order.get_order_status_display()}"
            ),
            (
                f"Payment: "
                f"{order.get_payment_status_display()}"
            ),
            f"Total: ${order.total_price}",
            "",
            "Items:",
        ]

        for item in order.items.all():

            product_name = (
                item.product.name
                if item.product
                else "Product"
            )

            lines.append(
                f"• {product_name} "
                f"x{item.quantity} "
                f"— ${item.get_cost()}"
            )

        lines.extend([
            "",
            f"Delivery city: {order.city}",
        ])

        return {
            "answer": "\n".join(lines),
            "type": "order",
            "intent": "order_search",
            "document": None,
            "product": None,
            "products": [],
            "orders": [data],
            "order": data,
            "category": None,
            "product_name": None,
            "product_url": None,
            "price": str(order.total_price),
            "stock_count": None,
            "score": 1.0,
        }

    # =========================================================
    # MULTIPLE ORDERS RESPONSE
    # =========================================================

    def orders_response(self, orders):

        lines = [
            "Here are your recent orders:",
            "",
        ]

        order_list = []

        for order in orders:

            data = self.order_data(order)

            order_list.append(data)

            lines.append(
                f"📦 Order #{order.id}"
            )

            lines.append(
                f"   Status: "
                f"{order.get_order_status_display()}"
            )

            lines.append(
                f"   Payment: "
                f"{order.get_payment_status_display()}"
            )

            lines.append(
                f"   Total: "
                f"${order.total_price}"
            )

            lines.append("")

        return {
            "answer": "\n".join(lines),
            "type": "orders",
            "intent": "order_search",
            "document": None,
            "product": None,
            "products": [],
            "orders": order_list,
            "order": None,
            "category": None,
            "product_name": None,
            "product_url": None,
            "price": None,
            "stock_count": None,
            "score": 1.0,
        }

    # =========================================================
    # FILTER EXTRACTION
    # =========================================================

    def extract_filters(self, message):

        text = self.normalize_text(message)

        filters = {
            "min_price": None,
            "max_price": None,
            "in_stock": False,
            "out_of_stock": False,
            "sort": None,
        }

        # -----------------------------------------------------
        # STOCK
        # -----------------------------------------------------

        if any(
            phrase in text
            for phrase in [
                "in stock",
                "available",
                "have stock",
                "with stock",
            ]
        ):
            filters["in_stock"] = True

        if any(
            phrase in text
            for phrase in [
                "out of stock",
                "not in stock",
                "unavailable",
            ]
        ):
            filters["out_of_stock"] = True

        # -----------------------------------------------------
        # BETWEEN
        # -----------------------------------------------------

        between_pattern = (
            r"\bbetween\s+\$?"
            r"(\d+(?:\.\d+)?)"
            r"\s+and\s+\$?"
            r"(\d+(?:\.\d+)?)"
        )

        match = re.search(
            between_pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            try:

                first = Decimal(
                    match.group(1)
                )

                second = Decimal(
                    match.group(2)
                )

                filters["min_price"] = min(
                    first,
                    second,
                )

                filters["max_price"] = max(
                    first,
                    second,
                )

            except InvalidOperation:
                pass

        # -----------------------------------------------------
        # MAX PRICE
        # -----------------------------------------------------

        max_patterns = [
            r"\bunder\s+\$?(\d+(?:\.\d+)?)",
            r"\bbelow\s+\$?(\d+(?:\.\d+)?)",
            r"\bless\s+than\s+\$?(\d+(?:\.\d+)?)",
            r"\bmaximum\s+\$?(\d+(?:\.\d+)?)",
            r"\bmax\s+\$?(\d+(?:\.\d+)?)",
        ]

        for pattern in max_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                try:

                    filters["max_price"] = Decimal(
                        match.group(1)
                    )

                    break

                except InvalidOperation:
                    pass

        # -----------------------------------------------------
        # MIN PRICE
        # -----------------------------------------------------

        min_patterns = [
            r"\bover\s+\$?(\d+(?:\.\d+)?)",
            r"\babove\s+\$?(\d+(?:\.\d+)?)",
            r"\bmore\s+than\s+\$?(\d+(?:\.\d+)?)",
            r"\bminimum\s+\$?(\d+(?:\.\d+)?)",
            r"\bmin\s+\$?(\d+(?:\.\d+)?)",
        ]

        for pattern in min_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                try:

                    filters["min_price"] = Decimal(
                        match.group(1)
                    )

                    break

                except InvalidOperation:
                    pass

        # -----------------------------------------------------
        # SORT
        # -----------------------------------------------------

        if any(
            word in text.split()
            for word in [
                "cheap",
                "cheapest",
                "lowest",
            ]
        ):
            filters["sort"] = "price_asc"

        if any(
            word in text.split()
            for word in [
                "expensive",
                "highest",
            ]
        ):
            filters["sort"] = "price_desc"

        return filters

    # =========================================================
    # EXTRACT SEARCH WORDS
    # =========================================================

    def extract_search_words(self, message):

        text = self.normalize_text(message)

        # Remove BETWEEN price expression
        text = re.sub(
            r"\bbetween\s+\$?\d+(?:\.\d+)?"
            r"\s+and\s+\$?\d+(?:\.\d+)?\b",
            " ",
            text,
        )

        # Remove price expressions
        text = re.sub(
            r"\b(?:under|below|over|above|max|min|"
            r"maximum|minimum|less than|more than)"
            r"\s+\$?\d+(?:\.\d+)?\b",
            " ",
            text,
        )

        # Remove standalone numbers
        text = re.sub(
            r"\b\d+(?:\.\d+)?\b",
            " ",
            text,
        )

        words = []

        for word in text.split():

            if len(word) < 2:
                continue

            if word in self.STOP_WORDS:
                continue

            words.append(word)

        return words

    # =========================================================
    # APPLY FILTERS
    # =========================================================

    def apply_product_filters(
        self,
        products,
        filters,
    ):

        results = []

        for product in products:

            if not self.product_passes_filters(
                product,
                filters,
            ):
                continue

            results.append(product)

        return results

    # =========================================================
    # FILTER CHECK
    # =========================================================

    def product_passes_filters(
        self,
        product,
        filters,
    ):

        try:

            price = Decimal(
                str(product.price)
            )

        except (
            InvalidOperation,
            TypeError,
        ):

            return False

        min_price = filters.get(
            "min_price"
        )

        max_price = filters.get(
            "max_price"
        )

        # Minimum price
        if (
            min_price is not None
            and price < min_price
        ):
            return False

        # Maximum price
        if (
            max_price is not None
            and price > max_price
        ):
            return False

        # In stock
        if (
            filters.get("in_stock")
            and product.stock_count <= 0
        ):
            return False

        # Out of stock
        if (
            filters.get("out_of_stock")
            and product.stock_count > 0
        ):
            return False

        return True

    # =========================================================
    # SORT PRODUCTS
    # =========================================================

    def sort_products(
        self,
        products,
        filters,
    ):

        sort_type = filters.get(
            "sort"
        )

        if sort_type == "price_asc":

            return sorted(
                products,
                key=lambda product: Decimal(
                    str(product.price)
                ),
            )

        if sort_type == "price_desc":

            return sorted(
                products,
                key=lambda product: Decimal(
                    str(product.price)
                ),
                reverse=True,
            )

        return products

    # =========================================================
    # CATEGORY SEARCH
    # =========================================================

    def find_category(self, message):

        query_words = self.extract_search_words(
            message
        )

        if not query_words:
            return None

        query = " ".join(query_words)

        categories = Category.objects.all()

        best_category = None
        best_score = 0

        for category in categories:

            category_name = self.normalize_text(
                category.name
            )

            category_words = (
                self.extract_search_words(
                    category_name
                )
            )

            if not category_words:
                continue

            category_word_set = set(
                category_words
            )

            matched_words = 0

            for word in query_words:

                if word in category_word_set:
                    matched_words += 1

                elif self.word_in_text(
                    word,
                    category_name,
                ):
                    matched_words += 1

            if matched_words == 0:
                continue

            # =================================================
            # IMPORTANT FIX
            # =================================================
            #
            # A category should NOT match if only one word
            # from a multi-word query matches.
            #
            # Example:
            #
            # "gaming laptop"
            #
            # Category:
            # "Gaming Gear"
            #
            # "gaming" matches, but "laptop" doesn't.
            #
            # Therefore this category must NOT be selected.
            # =================================================

            if len(query_words) > 1:

                if matched_words < len(query_words):
                    continue

            query_ratio = (
                matched_words
                / len(query_words)
            )

            category_ratio = (
                matched_words
                / len(category_words)
            )

            score = 0

            # Exact category query
            if query == category_name:

                score = 300

            # Category is fully represented
            elif (
                category_ratio == 1
                and query_ratio == 1
            ):

                score = 220

            # Query contains complete category
            elif (
                category_name in query
                and category_ratio == 1
            ):

                score = 200

            if score > best_score:

                best_score = score
                best_category = category

        if (
            best_category
            and best_score >= 200
        ):

            products = list(
                best_category.products
                .filter(
                    is_active=True
                )
                .select_related("category")
            )

            if products:

                return (
                    best_category,
                    products,
                )

        return None

    # =========================================================
    # CATEGORY RESPONSE
    # =========================================================

    def category_response(
        self,
        category,
        products,
        filters=None,
    ):

        product_list = [
            self.product_data(product)
            for product in products
        ]

        answer = (
            f"Here are the products in "
            f"{category.name}:"
        )

        if filters:

            if filters.get(
                "max_price"
            ) is not None:

                answer += (
                    f"\n\nShowing products up to "
                    f"${filters['max_price']}."
                )

            if filters.get(
                "min_price"
            ) is not None:

                answer += (
                    f"\n\nShowing products from "
                    f"${filters['min_price']}."
                )

            if filters.get("in_stock"):

                answer += (
                    "\n\nShowing only products "
                    "that are in stock."
                )

            if filters.get("out_of_stock"):

                answer += (
                    "\n\nShowing only products "
                    "that are out of stock."
                )

            if filters.get("sort") == "price_asc":

                answer += (
                    "\n\nSorted from cheapest "
                    "to most expensive."
                )

            elif filters.get("sort") == "price_desc":

                answer += (
                    "\n\nSorted from most expensive "
                    "to cheapest."
                )

        return {
            "answer": answer,
            "type": "category",
            "intent": "category_search",

            "category": {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
            },

            "document": None,
            "product": None,
            "products": product_list,

            "orders": [],
            "order": None,

            "product_name": None,
            "product_url": None,
            "price": None,
            "stock_count": None,
            "score": 1.0,
        }

    # =========================================================
    # PRODUCT SEARCH
    # =========================================================

    def find_products(
        self,
        message,
        filters=None,
    ):

        if filters is None:

            filters = self.extract_filters(
                message
            )

        query_words = self.extract_search_words(
            message
        )

        query = " ".join(query_words)

        products = (
            Product.objects
            .filter(
                is_active=True
            )
            .select_related("category")
        )

        scored_products = []

        for product in products:

            # -------------------------------------------------
            # FILTER FIRST
            # -------------------------------------------------

            if not self.product_passes_filters(
                product,
                filters,
            ):
                continue

            # -------------------------------------------------
            # NO SEARCH WORDS
            # -------------------------------------------------

            if not query_words:

                score = 1
                matched_all_words = True

            else:

                score, matched_all_words = (
                    self.score_product(
                        product,
                        query,
                        query_words,
                    )
                )

            # =================================================
            # IMPORTANT SEARCH RULE
            # =================================================
            #
            # For a multi-word query, all meaningful words
            # should match.
            #
            # Example:
            #
            # "gaming laptop"
            #
            # Gaming Chair:
            # gaming = yes
            # laptop = no
            #
            # => reject
            #
            # Gaming Laptop:
            # gaming = yes
            # laptop = yes
            #
            # => accept
            # =================================================

            if query_words:

                if len(query_words) > 1:

                    if not matched_all_words:
                        continue

                    if score < 100:
                        continue

                else:

                    if score < 35:
                        continue

            scored_products.append(
                (
                    product,
                    score,
                )
            )

        if not scored_products:
            return []

        # -----------------------------------------------------
        # SCORE FIRST
        # -----------------------------------------------------

        scored_products.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        # -----------------------------------------------------
        # PRICE SORT
        # -----------------------------------------------------

        if filters.get("sort") == "price_asc":

            scored_products.sort(
                key=lambda item: Decimal(
                    str(item[0].price)
                )
            )

        elif filters.get("sort") == "price_desc":

            scored_products.sort(
                key=lambda item: Decimal(
                    str(item[0].price)
                ),
                reverse=True,
            )

        # -----------------------------------------------------
        # EXACT PRODUCT
        # -----------------------------------------------------

        top_product, top_score = (
            scored_products[0]
        )

        normalized_top_name = (
            self.normalize_text(
                top_product.name
            )
        )

        if query == normalized_top_name:

            return [
                top_product
            ]

        # -----------------------------------------------------
        # QUERY IS INSIDE PRODUCT NAME
        # -----------------------------------------------------

        if (
            query
            and query in normalized_top_name
        ):

            return [
                top_product
            ]

        # -----------------------------------------------------
        # STRONG UNIQUE MATCH
        # -----------------------------------------------------

        if (
            len(scored_products) > 1
            and query_words
        ):

            second_score = (
                scored_products[1][1]
            )

            if (
                top_score >= 100
                and top_score - second_score >= 25
            ):

                return [
                    top_product
                ]

        # -----------------------------------------------------
        # RETURN TOP 10
        # -----------------------------------------------------

        return [
            product
            for product, score
            in scored_products[:10]
        ]

    # =========================================================
    # PRODUCT SCORING
    # =========================================================

    def score_product(
        self,
        product,
        query,
        query_words,
    ):

        product_name = self.normalize_text(
            product.name or ""
        )

        description = self.normalize_text(
            product.description or ""
        )

        category_name = ""

        if product.category:

            category_name = self.normalize_text(
                product.category.name or ""
            )

        score = 0

        # -----------------------------------------------------
        # EXACT PRODUCT NAME
        # -----------------------------------------------------

        if query == product_name:

            return 1000, True

        # -----------------------------------------------------
        # COMPLETE QUERY IN NAME
        # -----------------------------------------------------

        if query and query in product_name:

            score += 300

        # -----------------------------------------------------
        # NAME IN QUERY
        # -----------------------------------------------------

        if (
            product_name
            and product_name in query
        ):

            score += 250

        matched_name_words = 0
        matched_category_words = 0
        matched_description_words = 0

        matched_query_words = set()

        # -----------------------------------------------------
        # WORD MATCHING
        # -----------------------------------------------------

        for word in query_words:

            if not word:
                continue

            # ---------------------------------------------
            # Product name exact word
            # ---------------------------------------------

            if word in product_name.split():

                score += 100
                matched_name_words += 1
                matched_query_words.add(word)

                continue

            # ---------------------------------------------
            # Product name partial word
            # ---------------------------------------------

            if self.word_in_text(
                word,
                product_name,
            ):

                score += 70
                matched_name_words += 1
                matched_query_words.add(word)

                continue

            # ---------------------------------------------
            # Category
            # ---------------------------------------------

            if self.word_in_text(
                word,
                category_name,
            ):

                score += 35
                matched_category_words += 1
                matched_query_words.add(word)

                continue

            # ---------------------------------------------
            # Description
            # ---------------------------------------------

            if self.word_in_text(
                word,
                description,
            ):

                score += 20
                matched_description_words += 1
                matched_query_words.add(word)

                continue

            # ---------------------------------------------
            # Fuzzy name matching
            # ---------------------------------------------

            fuzzy_score = (
                self.best_fuzzy_word_score(
                    word,
                    product_name,
                )
            )

            if fuzzy_score >= 0.88:

                score += 50
                matched_query_words.add(word)

            elif fuzzy_score >= 0.78:

                score += 25
                matched_query_words.add(word)

        # -----------------------------------------------------
        # MATCH RATIO
        # -----------------------------------------------------

        total_words = len(query_words)

        matched_words = len(
            matched_query_words
        )

        matched_all_words = (
            matched_words == total_words
            if total_words
            else True
        )

        if total_words:

            match_ratio = (
                matched_words
                / total_words
            )

            if match_ratio == 1:

                score += 150

            elif match_ratio >= 0.75:

                score += 60

            elif match_ratio >= 0.50:

                score += 25

        # -----------------------------------------------------
        # MULTIPLE NAME WORD BONUS
        # -----------------------------------------------------

        if matched_name_words >= 2:

            score += 100

        # -----------------------------------------------------
        # ALL NAME WORDS BONUS
        # -----------------------------------------------------

        if (
            matched_name_words == total_words
            and total_words > 1
        ):

            score += 100

        # -----------------------------------------------------
        # STOCK BONUS
        # -----------------------------------------------------

        if product.stock_count > 0:

            score += 5

        return score, matched_all_words

    # =========================================================
    # FUZZY SEARCH
    # =========================================================

    def best_fuzzy_word_score(
        self,
        query_word,
        text,
    ):

        text_words = text.split()

        best = 0

        for word in text_words:

            similarity = SequenceMatcher(
                None,
                query_word,
                word,
            ).ratio()

            if similarity > best:

                best = similarity

        return best

    # =========================================================
    # NORMALIZE TEXT
    # =========================================================

    def normalize_text(self, text):

        text = (
            text or ""
        ).lower().strip()

        # Remove punctuation
        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        # Remove duplicate spaces
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        words = text.split()

        normalized_words = []

        for word in words:

            word = self.SYNONYMS.get(
                word,
                word,
            )

            normalized_words.append(
                word
            )

        return " ".join(
            normalized_words
        )

    # =========================================================
    # WORD IN TEXT
    # =========================================================

    def word_in_text(
        self,
        word,
        text,
    ):

        if not text:
            return False

        text_words = text.split()

        # Exact
        if word in text_words:
            return True

        # Partial
        for text_word in text_words:

            if (
                len(word) >= 4
                and word in text_word
            ):
                return True

        return False

    # =========================================================
    # PRODUCT DATA
    # =========================================================

    def product_data(
        self,
        product,
    ):

        category_name = ""

        if product.category:

            category_name = (
                product.category.name
            )

        product_url = (
            product.get_absolute_url()
        )

        return {
            "id": product.id,

            "name": product.name,

            "url": product_url,

            "price": str(
                product.price
            ),

            "stock_count": (
                product.stock_count
            ),

            "category": category_name,
        }

    # =========================================================
    # SINGLE PRODUCT RESPONSE
    # =========================================================

    def product_response(
        self,
        product,
    ):

        if product.stock_count > 0:

            stock_text = (
                f"{product.stock_count} "
                f"available in stock"
            )

        else:

            stock_text = (
                "Currently out of stock"
            )

        category_name = ""

        if product.category:

            category_name = (
                product.category.name
            )

        product_url = (
            product.get_absolute_url()
        )

        answer = (
            f"I found this for you:\n\n"
            f"{product.name}\n\n"
            f"{product.description or ''}\n\n"
            f"Price: ${product.price}\n"
            f"Stock: {stock_text}\n"
            f"Category: {category_name}"
        )

        data = self.product_data(
            product
        )

        return {
            "answer": answer,

            "type": "product",

            "intent": None,

            "document": None,

            "product": data,

            "products": [
                data
            ],

            "category": None,

            "orders": [],
            "order": None,

            "product_name": product.name,

            "product_url": product_url,

            "price": str(
                product.price
            ),

            "stock_count": (
                product.stock_count
            ),

            "score": 1.0,
        }

    # =========================================================
    # MULTIPLE PRODUCTS RESPONSE
    # =========================================================

    def products_response(
        self,
        products,
        filters=None,
    ):

        product_list = [
            self.product_data(product)
            for product in products
        ]

        answer = (
            "I found these products "
            "for you:"
        )

        if filters:

            if filters.get(
                "max_price"
            ) is not None:

                answer += (
                    f"\n\nUnder "
                    f"${filters['max_price']}:"
                )

            if filters.get(
                "min_price"
            ) is not None:

                answer += (
                    f"\n\nAbove "
                    f"${filters['min_price']}:"
                )

            if filters.get("in_stock"):

                answer += (
                    "\n\nOnly showing "
                    "products in stock."
                )

            if filters.get("out_of_stock"):

                answer += (
                    "\n\nOnly showing "
                    "products out of stock."
                )

            if filters.get("sort") == "price_asc":

                answer += (
                    "\n\nSorted from cheapest "
                    "to most expensive."
                )

            elif filters.get("sort") == "price_desc":

                answer += (
                    "\n\nSorted from most expensive "
                    "to cheapest."
                )

        return {
            "answer": answer,

            "type": "products",

            "intent": None,

            "document": None,

            "product": None,

            "products": product_list,

            "category": None,

            "orders": [],
            "order": None,

            "product_name": None,

            "product_url": None,

            "price": None,

            "stock_count": None,

            "score": 1.0,
        }

    # =========================================================
    # NORMAL RESPONSE
    # =========================================================

    def normal_response(
        self,
        message,
    ):

        return {
            "answer": (
                "I couldn't find a matching product.\n\n"

                "Try searching by:\n"
                "• Product name\n"
                "• Category\n"
                "• Feature\n"
                "• Price\n"
                "• Stock availability\n\n"

                "For example:\n"
                "\"Gaming Chair\"\n"
                "\"wireless headphones\"\n"
                "\"wireless headphones under $100\"\n"
                "\"Doorbell in stock\"\n"
                "\"LED lights below $50\""
            ),

            "type": "general",

            "intent": None,

            "document": None,

            "product": None,

            "products": [],

            "orders": [],
            "order": None,

            "category": None,

            "product_name": None,

            "product_url": None,

            "price": None,

            "stock_count": None,

            "score": None,
        }

    # =========================================================
    # ERROR RESPONSE
    # =========================================================

    def error_response(
        self,
        message,
    ):

        return {
            "answer": message,

            "type": "error",

            "intent": None,

            "document": None,

            "product": None,

            "products": [],

            "orders": [],
            "order": None,

            "category": None,

            "product_name": None,

            "product_url": None,

            "price": None,

            "stock_count": None,

            "score": None,
        }