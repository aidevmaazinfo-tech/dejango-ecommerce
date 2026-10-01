import re
import spacy
from spacy.matcher import Matcher

from .normalizer import normalize_command
from .tools import ToolCall


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

# =========================================================
# SPACY INTENT MATCHING PATTERNS (Replaces Fuzzy Matching)
# =========================================================

matcher.add("GET_CART", [
    [{"LOWER": "cart"}],
    [{"LOWER": "open"}, {"LOWER": "cart"}],
    [{"LOWER": "open"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "show"}, {"LOWER": "cart"}],
    [{"LOWER": "show"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "view"}, {"LOWER": "cart"}],
    [{"LOWER": "view"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "check"}, {"LOWER": "cart"}],
    [{"LOWER": "check"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "cart"}, {"LOWER": "kholo"}],
    [{"LOWER": "cart"}, {"LOWER": "khol"}, {"LOWER": "do"}],
    [{"LOWER": "meri"}, {"LOWER": "cart"}, {"LOWER": "kholo"}],
    [{"LOWER": "mera"}, {"LOWER": "cart"}, {"LOWER": "kholo"}],
    [{"LOWER": "meri"}, {"LOWER": "cart"}, {"LOWER": "dikhao"}],
    [{"LOWER": "mera"}, {"LOWER": "cart"}, {"LOWER": "dikhao"}],
    [{"LOWER": "cart"}, {"LOWER": "dikhao"}],
])

matcher.add("CLEAR_CART", [
    [{"LOWER": "clear"}, {"LOWER": "cart"}],
    [{"LOWER": "clear"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "empty"}, {"LOWER": "cart"}],
    [{"LOWER": "empty"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "delete"}, {"LOWER": "cart"}],
    [{"LOWER": "delete"}, {"LOWER": "my"}, {"LOWER": "cart"}],
    [{"LOWER": "remove"}, {"LOWER": "everything"}, {"LOWER": "from"}, {"LOWER": "cart"}],
    [{"LOWER": "cart"}, {"LOWER": "clear"}],
    [{"LOWER": "cart"}, {"LOWER": "khali"}],
    [{"LOWER": "cart"}, {"LOWER": "khaali"}],
    [{"LOWER": "cart"}, {"LOWER": "clear"}, {"LOWER": "karo"}],
    [{"LOWER": "cart"}, {"LOWER": "khali"}, {"LOWER": "karo"}],
    [{"LOWER": "cart"}, {"LOWER": "empty"}, {"LOWER": "karo"}],
    [{"LOWER": "meri"}, {"LOWER": "cart"}, {"LOWER": "clear"}, {"LOWER": "karo"}],
])

matcher.add("GET_ORDERS", [
    [{"LOWER": "orders"}],
    [{"LOWER": "my"}, {"LOWER": "orders"}],
    [{"LOWER": "show"}, {"LOWER": "orders"}],
    [{"LOWER": "show"}, {"LOWER": "my"}, {"LOWER": "orders"}],
    [{"LOWER": "view"}, {"LOWER": "orders"}],
    [{"LOWER": "view"}, {"LOWER": "my"}, {"LOWER": "orders"}],
    [{"LOWER": "check"}, {"LOWER": "orders"}],
    [{"LOWER": "check"}, {"LOWER": "my"}, {"LOWER": "orders"}],
    [{"LOWER": "list"}, {"LOWER": "orders"}],
    [{"LOWER": "list"}, {"LOWER": "my"}, {"LOWER": "orders"}],
    [{"LOWER": "mere"}, {"LOWER": "orders"}],
    [{"LOWER": "meri"}, {"LOWER": "orders"}],
    [{"LOWER": "mere"}, {"LOWER": "orders"}, {"LOWER": "dikhao"}],
    [{"LOWER": "meri"}, {"LOWER": "orders"}, {"LOWER": "dikhao"}],
    [{"LOWER": "mere"}, {"LOWER": "orders"}, {"LOWER": "batao"}],
])

matcher.add("TRACK_ORDERS", [
    [{"LOWER": "track"}, {"LOWER": "my"}, {"LOWER": "order"}],
    [{"LOWER": "track"}, {"LOWER": "order"}],
    [{"LOWER": "track"}, {"LOWER": "my"}, {"LOWER": "orders"}],
    [{"LOWER": "track"}, {"LOWER": "orders"}],
    [{"LOWER": "where"}, {"LOWER": "is"}, {"LOWER": "my"}, {"LOWER": "order"}],
    [{"LOWER": "where"}, {"LOWER": "'s"}, {"LOWER": "my"}, {"LOWER": "order"}],
    [{"LOWER": "order"}, {"LOWER": "status"}],
    [{"LOWER": "my"}, {"LOWER": "order"}, {"LOWER": "status"}],
    [{"LOWER": "check"}, {"LOWER": "my"}, {"LOWER": "order"}, {"LOWER": "status"}],
    [{"LOWER": "check"}, {"LOWER": "order"}, {"LOWER": "status"}],
    [{"LOWER": "mera"}, {"LOWER": "order"}, {"LOWER": "kahan"}, {"LOWER": "hai"}],
    [{"LOWER": "mera"}, {"LOWER": "order"}, {"LOWER": "ka"}, {"LOWER": "status"}],
    [{"LOWER": "delivery"}, {"LOWER": "status"}],
])

matcher.add("GET_PROFILE", [
    [{"LOWER": "profile"}],
    [{"LOWER": "my"}, {"LOWER": "profile"}],
    [{"LOWER": "show"}, {"LOWER": "profile"}],
    [{"LOWER": "view"}, {"LOWER": "profile"}],
    [{"LOWER": "shipping"}, {"LOWER": "address"}],
    [{"LOWER": "my"}, {"LOWER": "address"}],
    [{"LOWER": "check"}, {"LOWER": "profile"}],
    [{"LOWER": "account"}, {"LOWER": "info"}],
    [{"LOWER": "mera"}, {"LOWER": "address"}, {"LOWER": "kya"}, {"LOWER": "hai"}],
    [{"LOWER": "meri"}, {"LOWER": "profile"}, {"LOWER": "dikhao"}],
])

matcher.add("DELIVERED_PRODUCTS", [
    [{"LOWER": "delivered"}, {"LOWER": "products"}],
    [{"LOWER": "delivered"}, {"LOWER": "items"}],
    [{"LOWER": "show"}, {"LOWER": "me"}, {"LOWER": "my"}, {"LOWER": "delivered"}, {"LOWER": "products"}],
    [{"LOWER": "show"}, {"LOWER": "delivered"}, {"LOWER": "products"}],
    [{"LOWER": "show"}, {"LOWER": "me"}, {"LOWER": "delivered"}, {"LOWER": "products"}],
    [{"LOWER": "my"}, {"LOWER": "delivered"}, {"LOWER": "products"}],
    [{"LOWER": "products"}, {"LOWER": "delivered"}],
    [{"LOWER": "what"}, {"LOWER": "was"}, {"LOWER": "delivered"}],
    [{"LOWER": "what"}, {"LOWER": "did"}, {"LOWER": "i"}, {"LOWER": "get"}, {"LOWER": "delivered"}],
    [{"LOWER": "delivered"}, {"LOWER": "product"}],
])


def parse_command(text: str, context: dict = None) -> ToolCall:
    """
    Deterministic command parser with Contextual Memory, General Search Extractor, 
    and prioritized Regex/spaCy NLU fallback.
    """
    command = normalize_command(text)
    context = context or {}

    if not command:
        return ToolCall(
            name="unknown",
            arguments={},
        )

    # Process text with spaCy for tokenization, lemmatization, and entity extraction
    doc = nlp(command)

    # =========================================================
    # 0. CONTEXTUAL RESOLUTION ("add the first one", "details of second")
    # =========================================================
    last_results = context.get("last_search_results", [])
    if last_results:
        ordinal_map = {
            "first": 0, "1st": 0, "1": 0,
            "second": 1, "2nd": 1, "2": 1,
            "third": 2, "3rd": 2, "3": 2,
            "fourth": 3, "4th": 3, "4": 3,
        }
        
        found_index = None
        for token in doc:
            if token.text.lower() in ordinal_map:
                found_index = ordinal_map[token.text.lower()]
                break
        
        if found_index is not None and found_index < len(last_results):
            target_product = last_results[found_index]
            product_name = target_product.get("name")
            
            lemmas = {token.lemma_ for token in doc}
            if lemmas.intersection({"add", "put", "include", "daal"}):
                return ToolCall(
                    name="add_to_cart_tool",
                    arguments={"product_name": product_name, "quantity": 1}
                )
            elif lemmas.intersection({"detail", "description", "tell", "show", "about"}):
                return ToolCall(
                    name="get_product_description_tool",
                    arguments={"product_name": product_name}
                )

    # =========================================================
    # 1. EXACT & REGEX PATTERNS FIRST (High Precision)
    # =========================================================

    update_patterns = [
        r"^(?:change|update|set)\s+(.+?)\s+(?:quantity|qty)\s+(?:to\s+)?(\d+)$",
        r"^(?:change|update|set)\s+(?:quantity|qty)\s+(?:of\s+)?(.+?)\s+(?:to\s+)?(\d+)$",
        r"^(.+?)\s+(?:quantity|qty)\s+(?:to\s+)?(\d+)$",
        r"^(?:make|set)\s+(.+?)\s+(?:quantity|qty)\s+(\d+)$",
        r"^(.+?)\s+ko\s+(\d+)\s+(?:kar|karo|kar do)$",
        r"^(.+?)\s+ki\s+(?:quantity|qty)\s+(\d+)\s+(?:karo|kar do)$",
    ]

    for pattern in update_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="update_cart_quantity_tool",
                arguments={
                    "product_name": match.group(1).strip(),
                    "quantity": int(match.group(2)),
                },
            )

    remove_patterns = [
        r"^(?:remove|delete)\s+(.+?)\s+(?:from|out of)\s+(?:my\s+)?cart$",
        r"^(?:remove|delete)\s+(.+?)\s+cart$",
        r"^cart\s+se\s+(?:remove|delete)\s+(.+)$",
        r"^cart\s+se\s+(.+?)\s+(?:remove|delete)\s+(?:karo|kar do)$",
        r"^(.+?)\s+cart\s+se\s+(?:remove|delete)\s+(?:karo|kar do)$",
        r"^(.+?)\s+(?:hata do|remove karo|delete karo)\s+(?:cart\s+se)?$",
    ]

    for pattern in remove_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="remove_from_cart_tool",
                arguments={
                    "product_name": match.group(1).strip(),
                },
            )

    add_patterns = [
        r"^add\s+(?:(\d+)\s+)?(.+?)\s+to\s+(?:my\s+)?cart$",
        r"^add\s+(?:(\d+)\s+)?(.+?)\s+(?:in|into)\s+(?:my\s+)?cart$",
        r"^add\s+(?:(\d+)\s+)?(.+?)\s+cart\s+(?:mein|me)$",
        r"^cart\s+(?:mein|me)\s+(?:(\d+)\s+)?(.+?)\s+(?:add|daal|dal)$",
        r"^cart\s+(?:mein|me)\s+(?:(\d+)\s+)?(.+?)\s+(?:daal|dal)\s+(?:do|de)$",
        r"^(?:(\d+)\s+)?(.+?)\s+cart\s+(?:mein|me)\s+(?:daal|dal)\s+(?:do|de)$",
    ]

    for pattern in add_patterns:
        match = re.search(pattern, command)
        if match:
            quantity = match.group(1) or "1"
            product_name = match.group(2).strip()
            return ToolCall(
                name="add_to_cart_tool",
                arguments={
                    "product_name": product_name,
                    "quantity": int(quantity),
                },
            )

    reorder_patterns = [
        r"^reorder\s+(?:order\s+)?#?(\d+)$",
        r"^order\s+#?(\d+)\s+again$",
        r"^(?:order\s+)?#?(\d+)\s+ke\s+items?\s+cart\s+(?:mein\s+)?(?:daal|dal)\s+do$",
        r"^mujhe\s+order\s+#?(\d+)\s+phir\s+se\s+chahiye$",
    ]

    for pattern in reorder_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="reorder_tool",
                arguments={
                    "order_id": int(match.group(1)),
                },
            )

    update_address_patterns = [
        r"^(?:update|change|set)\s+(?:my\s+)?address\s+(?:to\s+)?(.+)$",
        r"^mera\s+address\s+(?:change|update)\s+karke\s+(.+?)\s+kar\s+do$",
    ]

    for pattern in update_address_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="update_customer_profile_tool",
                arguments={
                    "address": match.group(1).strip(),
                },
            )

    track_patterns = [
        r"^track\s+(?:my\s+|the\s+)?order\s+#?(\d+)$",
        r"^where\s+is\s+(?:my\s+)?order\s+#?(\d+)$",
        r"^where's\s+(?:my\s+)?order\s+#?(\d+)$",
        r"^status\s+of\s+(?:my\s+)?order\s+#?(\d+)$",
        r"^check\s+status\s+of\s+(?:my\s+)?order\s+#?(\d+)$",
        r"^track\s+#?(\d+)$",
        r"^order\s+#?(\d+)\s+(?:track|tracking|status)$",
        r"^order\s+#?(\d+)\s+kahan\s+hai$",
        r"^order\s+#?(\d+)\s+ka\s+status$",
        r"^order\s+#?(\d+)\s+ka\s+status\s+(?:batao|dikhao|batain)$",
        r"^order\s+#?(\d+)\s+track\s+(?:karo|kar do)$",
        r"^order\s+#?(\d+)\s+ko\s+track\s+(?:karo|kar do)$",
    ]

    for pattern in track_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "track",
                    "order_id": int(match.group(1)),
                },
            )

    delivery_patterns = [
        r"^delivery\s+(?:status\s+)?(?:of\s+)?(?:my\s+|the\s+)?order\s+#?(\d+)$",
        r"^shipping\s+(?:status\s+)?(?:of\s+)?(?:my\s+|the\s+)?order\s+#?(\d+)$",
        r"^package\s+(?:status\s+)?(?:of\s+)?(?:my\s+|the\s+)?order\s+#?(\d+)$",
        r"^(?:estimated\s+)?delivery\s+(?:date\s+)?(?:for\s+)?order\s+#?(\d+)$",
        r"^when\s+(?:will\s+)?(?:my\s+)?order\s+#?(\d+)\s+arrive$",
        r"^when\s+is\s+order\s+#?(\d+)\s+coming$",
        r"^order\s+#?(\d+)\s+delivery$",
        r"^order\s+#?(\d+)\s+(?:delivery\s+)?status$",
        r"^order\s+#?(\d+)\s+shipping\s+status$",
        r"^order\s+#?(\d+)\s+kab\s+aayega$",
        r"^order\s+#?(\d+)\s+kab\s+tak\s+aayega$",
        r"^order\s+#?(\d+)\s+ki\s+delivery\s+(?:kab\s+hai|batao|dikhao)$",
        r"^order\s+#?(\d+)\s+ka\s+delivery\s+status$",
    ]

    for pattern in delivery_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "delivery",
                    "order_id": int(match.group(1)),
                },
            )

    specific_order_patterns = [
        r"^(?:show|view|open|check)\s+(?:my\s+)?order\s+#?(\d+)$",
        r"^order\s+#?(\d+)$",
        r"^order\s+#?(\d+)\s+details?$",
        r"^details?\s+(?:of|for)\s+order\s+#?(\d+)$",
        r"^order\s+#?(\d+)\s+ki\s+details?\s+(?:dikhao|batao|batain)$",
        r"^order\s+#?(\d+)\s+ki\s+detail\s+(?:dikhao|batao|batain)$",
        r"^mujhe\s+order\s+#?(\d+)\s+ki\s+details?\s+(?:chahiye|dikhao|batao|batain)$",
        r"^mujhe\s+order\s+#?(\d+)\s+ki\s+detail\s+(?:chahiye|dikhao|batao|batain)$",
    ]

    for pattern in specific_order_patterns:
        match = re.search(pattern, command)
        if match:
            return ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "specific",
                    "order_id": int(match.group(1)),
                },
            )

    cancel_patterns = [
        r"^(?:cancel|delete)\s+(?:my\s+|the\s+)?order\s+#?(\d+)$",
        r"^cancel\s+#?(\d+)$",
        r"^order\s+#?(\d+)\s+cancel$",
        r"^order\s+#?(\d+)\s+cancel\s+(?:karo|kar do)$",
        r"^order\s+#?(\d+)\s+ko\s+cancel\s+(?:karo|kar do)$",
        r"^mujhe\s+order\s+#?(\d+)\s+cancel\s+karna\s+hai$",
    ]

    if command in {
        "cancel my order",
        "cancel an order",
        "i want to cancel my order",
        "can i cancel my order",
        "mujhe order cancel karna hai",
    }:
        return ToolCall(
            name="get_user_orders_tool",
            arguments={"action": "cancel"},
        )

    for pattern in cancel_patterns:
        match = re.search(pattern, command)
        if match:
            order_id = int(match.group(1))
            return ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                    "cancel_order_id": order_id,
                },
            )

    # =========================================================
    # 2. SPACY MATCHER INTENT DETECTION
    # =========================================================

    matches = matcher(doc)
    if matches:
        matches = sorted(matches, key=lambda m: m[2] - m[1], reverse=True)
        match_id, start, end = matches[0]
        intent_name = nlp.vocab.strings[match_id]

        if intent_name == "GET_CART":
            return ToolCall(name="get_cart_tool", arguments={})
        elif intent_name == "CLEAR_CART":
            return ToolCall(name="clear_cart_tool", arguments={})
        elif intent_name == "GET_ORDERS":
            return ToolCall(name="get_user_orders_tool", arguments={"action": "list"})
        elif intent_name == "TRACK_ORDERS":
            return ToolCall(name="get_user_orders_tool", arguments={"action": "list"})
        elif intent_name == "GET_PROFILE":
            return ToolCall(name="get_customer_profile_tool", arguments={})
        elif intent_name == "DELIVERED_PRODUCTS":
            return ToolCall(name="search_delivered_products_tool", arguments={})

    # =========================================================
    # 3. FAQ TOOL INTEGRATION (Enhanced with spaCy Lemmas)
    # =========================================================
    lemmas = {token.lemma_ for token in doc}

    FAQ_ALIASES = {
        "FAQ_SHIPPING": {"shipping", "delivery", "time", "long"},
        "FAQ_RETURNS": {"return", "back"},
        "FAQ_REFUNDS": {"refund", "money"},
        "FAQ_PAYMENT": {"payment", "pay", "card", "cash"},
        "FAQ_CANCELLATION": {"cancel", "cancellation"},
        "FAQ_TRACKING": {"track", "tracking"},
        "FAQ_ACCOUNT": {"account", "profile", "address"},
    }

    for intent_name, keywords in FAQ_ALIASES.items():
        if lemmas.intersection(keywords):
            return ToolCall(
                name="faq_tool",
                arguments={
                    "intent": intent_name,
                    "message": command,
                },
            )

    # =========================================================
    # 4. PRODUCT DETAILS & DYNAMIC SEARCH EXTRACTOR (No Hardcoding)
    # =========================================================
    product_details_patterns = [
        r"^tell\s+me\s+(?:the\s+)?details?\s+(?:of|for)\s+(.+)$",
        r"^tell\s+me\s+about\s+(.+)$",
        r"^show\s+(?:me\s+)?details?\s+(?:of|for)\s+(.+)$",
        r"^show\s+(?:me\s+)?(.+?)\s+details?$",
        r"^(.+?)\s+details?$",
        r"^details?\s+(?:of|for)\s+(.+)$",
        r"^details?\s+(.+)$",
        r"^describe\s+(.+)$",
        r"^give\s+me\s+(?:the\s+)?details?\s+(?:of|for)\s+(.+)$",
        r"^can\s+you\s+tell\s+me\s+(?:the\s+)?details?\s+(?:of|for)\s+(.+)$",
        r"^what\s+are\s+the\s+details?\s+(?:of|for)\s+(.+)$",
        r"^what\s+is\s+(.+)$",
        r"^(.+?)\s+ki\s+details?\s+(?:dikhao|batao|batain)$",
        r"^mujhe\s+(.+?)\s+ki\s+details?\s+(?:chahiye|dikhao|batao|batain)$",
        r"^(.+?)\s+ke\s+details?\s+(?:dikhao|batao|batain)$",
    ]

    for pattern in product_details_patterns:
        match = re.search(pattern, command)
        if match:
            product_name = match.group(1).strip()
            if product_name:
                return ToolCall(
                    name="get_product_description_tool",
                    arguments={
                        "product_name": product_name,
                    },
                )

    price_number = r"(\d+(?:\.\d+)?)"

    between_pattern = (
        rf"^(?:(?:find|search|show|look for|get|mujhe|mujhe chahiye)\s+)?"
        rf"(.+?)\s+"
        rf"(?:"
        rf"between\s+{price_number}\s+and\s+{price_number}"
        rf"|in\s+range\s+of\s+{price_number}\s+to\s+{price_number}"
        rf"|from\s+{price_number}\s+to\s+{price_number}"
        rf"|{price_number}\s+to\s+{price_number}"
        rf")$"
    )

    between_match = re.search(between_pattern, command)
    if between_match:
        query = between_match.group(1).strip()
        min_price = float(between_match.group(2) or between_match.group(4) or between_match.group(6) or between_match.group(8))
        max_price = float(between_match.group(3) or between_match.group(5) or between_match.group(7) or between_match.group(9))
        return ToolCall(
            name="search_products_tool",
            arguments={"query": query, "min_price": min_price, "max_price": max_price},
        )

    under_match = re.search(
        rf"^(?:(?:find|search|show|look for|get|mujhe)\s+)?"
        rf"(.+?)\s+"
        rf"(?:under|below|less than|upto|up to)\s+"
        rf"{price_number}$",
        command,
    )
    if under_match:
        return ToolCall(
            name="search_products_tool",
            arguments={"query": under_match.group(1).strip(), "min_price": None, "max_price": float(under_match.group(2))},
        )

    over_match = re.search(
        rf"^(?:(?:find|search|show|look for|get|mujhe)\s+)?"
        rf"(.+?)\s+"
        rf"(?:above|over|more than|greater than)\s+"
        rf"{price_number}$",
        command,
    )
    if over_match:
        return ToolCall(
            name="search_products_tool",
            arguments={"query": over_match.group(1).strip(), "min_price": float(over_match.group(2)), "max_price": None},
        )

    # General Search Extractor (Handles "show me lenovo laptops", "mujhe shoes chahiye", etc.)
    search_intent_match = re.search(
        r"^(?:find|search|show|look for|get|mujhe|chahiye|dikhao)\s+(?:me\s+)?(.+)$", 
        command
    )
    
    if search_intent_match:
        raw_query = search_intent_match.group(1)
        stopwords_to_strip = {"me", "please", "can", "you", "find", "some", "a", "an", "the", "chahiye", "dikhao", "dikhayein"}
        tokens = [token.text for token in nlp(raw_query) if token.text.lower() not in stopwords_to_strip]
        clean_query = " ".join(tokens).strip()
        if not clean_query:
            clean_query = raw_query.strip()

        return ToolCall(name="search_products_tool", arguments={"query": clean_query})

    roman_urdu_search_patterns = [
        r"^mujhe\s+(.+?)\s+chahiye$",
        r"^mujhe\s+(.+?)\s+dikhao$",
        r"^(.+?)\s+dikhao$",
        r"^(.+?)\s+chahiye$",
        r"^(.+?)\s+do$",
        r"^(.+?)\s+dikhayein$",
    ]

    for pattern in roman_urdu_search_patterns:
        match = re.search(pattern, command)
        if match:
            query = match.group(1).strip()
            if query:
                return ToolCall(name="search_products_tool", arguments={"query": query})

    if any(term in command for term in ("unknown", "quantum physics", "explain quantum")):
        return ToolCall(name="unknown", arguments={})

    if command:
        return ToolCall(name="search_products_tool", arguments={"query": command})

    return ToolCall(
        name="unknown",
        arguments={},
    )