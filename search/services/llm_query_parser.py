"""
Local-only (Ollama) natural language -> structured filter parser.
No external API calls - talks to http://localhost:11434 only, nothing
ever leaves your server.

This is deliberately kept SEPARATE from the plain icontains text search in
global_search.py: the LLM only extracts status/boolean/numeric/date type
filters (things like "pending", "active users", "price above 500", "last
week"). Free text like names, emails, or product names is still matched by
the existing icontains search - that part never depended on exact wording
anyway, so there's no reason to route it through the LLM.

Every key the LLM returns is checked against ALLOWED_LOOKUPS before it is
ever used in a .filter(**kwargs) call, so a hallucinated or malformed field
name can never reach the ORM. If Ollama is unreachable or returns garbage,
get_llm_filters() returns empty dicts rather than raising - the caller's
normal text search keeps working regardless.
"""
import json
import logging

import requests
from django.utils import timezone

logger = logging.getLogger(__name__)

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:3b"   # small enough to run on CPU; upgrade later if you get a GPU/more RAM

# The ONLY lookup keys the LLM is allowed to produce, per model.
# Add to these lists if you want the LLM to understand more fields later -
# but never let user/model-supplied strings build a lookup key dynamically.
ALLOWED_LOOKUPS = {
    "users": {
        "role", "role__icontains", "is_active", "is_staff", "is_superuser",
        "date_joined__date", "date_joined__gte", "date_joined__lte",
    },
    "orders": {
        "order_status", "order_status__icontains",
        "payment_status", "payment_status__icontains",
        "city__icontains", "total_price", "total_price__gt", "total_price__lt",
        "total_price__gte", "total_price__lte",
        "created_at__date", "created_at__gte", "created_at__lte",
    },
    "products": {
        "is_active", "price", "price__gt", "price__lt", "price__gte", "price__lte",
        "stock_count", "stock_count__gt", "stock_count__lt", "stock_count__gte",
        "stock_count__lte", "brand__icontains",
    },
}

BOOLEAN_KEYS = {"is_active", "is_staff", "is_superuser"}
NUMERIC_KEYS_OR_SUFFIXES = ("__gt", "__lt", "__gte", "__lte", "total_price", "price", "stock_count")

SYSTEM_PROMPT_TEMPLATE = """You are a search filter extractor for a Django e-commerce admin.
Today's date is {today}.

Given the admin's search text, output STRICT JSON only (no markdown, no explanation) in this exact shape:
{{
  "users": {{}},
  "orders": {{}},
  "products": {{}}
}}

Only use these exact keys, never invent new ones:

users: role, role__icontains, is_active, is_staff, is_superuser, date_joined__date, date_joined__gte, date_joined__lte
orders: order_status, order_status__icontains, payment_status, payment_status__icontains, city__icontains, total_price, total_price__gt, total_price__lt, total_price__gte, total_price__lte, created_at__date, created_at__gte, created_at__lte
products: is_active, price, price__gt, price__lt, price__gte, price__lte, stock_count, stock_count__gt, stock_count__lt, stock_count__gte, stock_count__lte, brand__icontains

Rules:
- order_status values must be exactly one of: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED
- payment_status values must be exactly one of: PENDING, COMPLETED, FAILED, REFUNDED
- boolean values must be the string true or false
- convert relative dates ("last week", "today", "this month") into an actual YYYY-MM-DD value using today's date
- if a section has nothing relevant to the query, leave it as an empty object {{}}
- if you are not confident about a value, omit it rather than guessing
- do NOT put plain free-text terms here (names, emails, cities as loose text, product names) -
  that part is handled separately; this JSON is only for status/boolean/numeric/date filters
- CRITICAL: only include a key when the query explicitly talks about that specific aspect.
  Never add order_status just because the query is about orders in general - only add it if
  delivery/shipping/order-progress is mentioned. Never add payment_status unless payment/billing
  is mentioned. Adding an unrelated field is worse than leaving a section empty, because it makes
  the search too narrow and can hide correct results.

Roman Urdu / Hindi vocabulary you will commonly see - map these carefully and exactly:
- "atka hua", "ruka hua", "phansa hua", "nakaam", "reject" -> payment_status: FAILED
- "wasool ho gaya", "mil gaya", "complete", "ho gaya" (about payment) -> payment_status: COMPLETED
- "abhi tak nahi hua", "intezar mein", "pending" (about payment) -> payment_status: PENDING
- "wapis kar diya", "refund", "paise wapis" -> payment_status: REFUNDED
- "bheja ja chuka", "rasta mein", "shipped" -> order_status: SHIPPED
- "pahunch gaya", "deliver ho gaya", "mil gaya" (about the order/parcel) -> order_status: DELIVERED
- "cancel ho gaya", "radd", "cancelled" -> order_status: CANCELLED
- "process ho raha", "taiyari mein" -> order_status: PROCESSING
- If a phrase is genuinely ambiguous between payment and order progress, prefer leaving it out
  over guessing - an empty section is safer than a wrong one.

Examples (the query language may be English or Roman Urdu/Hindi):

Query: "orders jinka payment atka hua hai"
Output: {{"users": {{}}, "orders": {{"payment_status": "FAILED"}}, "products": {{}}}}

Query: "active users"
Output: {{"users": {{"is_active": true}}, "orders": {{}}, "products": {{}}}}

Query: "price 500 se zyada wale products"
Output: {{"users": {{}}, "orders": {{}}, "products": {{"price__gt": 500}}}}

Query: "orders jo deliver ho chuke hain"
Output: {{"users": {{}}, "orders": {{"order_status": "DELIVERED"}}, "products": {{}}}}

Query: "Dell laptop"
Output: {{"users": {{}}, "orders": {{}}, "products": {{}}}}
"""


def _coerce_value(key, value):
    if key in BOOLEAN_KEYS:
        return str(value).strip().lower() in ("true", "1", "yes")
    if key.endswith(NUMERIC_KEYS_OR_SUFFIXES) or key in ("total_price", "price", "stock_count"):
        try:
            return float(value) if "." in str(value) else int(value)
        except (TypeError, ValueError):
            return None
    return value


def _validate(model_key, raw_filters):
    clean = {}
    if not isinstance(raw_filters, dict):
        return clean
    allowed = ALLOWED_LOOKUPS.get(model_key, set())
    for key, value in raw_filters.items():
        if key not in allowed:
            logger.warning("Dropping unallowed lookup '%s' for model '%s'", key, model_key)
            continue
        coerced = _coerce_value(key, value)
        if coerced is None or coerced == "":
            continue
        clean[key] = coerced
    return clean


def get_llm_filters(query, model=OLLAMA_MODEL, host=OLLAMA_HOST, timeout=60):
    """
    Returns {'users': {...}, 'orders': {...}, 'products': {...}} of VALIDATED
    filter kwargs, ready to pass straight into .filter(**kwargs).
    Never raises - returns empty dicts if Ollama is down or output is unusable,
    so the normal icontains search in GlobalSearchService keeps working either way.
    """
    empty = {"users": {}, "orders": {}, "products": {}}
    prompt = SYSTEM_PROMPT_TEMPLATE.format(today=timezone.now().strftime("%Y-%m-%d"))
    full_prompt = f'{prompt}\nAdmin search text: "{query}"\n\nJSON:'

    try:
        resp = requests.post(
            f"{host}/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0},
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        raw_text = resp.json().get("response", "")
        parsed = json.loads(raw_text)
    except requests.RequestException as e:
        logger.warning("Ollama not reachable, falling back to plain text search only: %s", e)
        return empty
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning("Could not parse LLM output, falling back to plain text search only: %s", e)
        return empty

    return {
        "users": _validate("users", parsed.get("users")),
        "orders": _validate("orders", parsed.get("orders")),
        "products": _validate("products", parsed.get("products")),
    }