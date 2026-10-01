from django.db.models import Q, Sum
from django.contrib.auth import get_user_model
from orders.models import Order
from products.models import Product

from .llm_query_parser import get_llm_filters

User = get_user_model()


class GlobalSearchService:
    """
    Admin ke liye powerful global smart search system.
    Teen models (Users, Orders, Products) ek saath search hote hain.

    UPDATE: pehle status/boolean/price wali cheezein hardcoded
    'if "pending" in query_lower' jaisi lines se detect hoti thi, is liye
    admin ko exact keyword yaad rakhna parta tha. Ab wo hissa local Ollama
    LLM (llm_query_parser.py) nikalta hai, jo kisi bhi natural tareeqe se
    likhi gayi baat ko samajh kar structured filters bana deta hai
    (e.g. "who hasn't logged in properly" type cheezon ko chorr kar,
    "pending orders from Lahore last week" jaisi cheezein).

    Plain text (names, emails, city, product name) hamesha icontains se
    search hota rehta hai jaisa pehle hota tha - wo already flexible tha,
    usay LLM ki zaroorat nahi thi. Agar Ollama band ho ya kuch samajh na
    aaye, sirf icontains wala hissa chalta rehta hai - result kabhi bhi
    sirf LLM ki wajah se khaali nahi hota.
    """

    @staticmethod
    def search_all(query, limit=50):
        """
        Single search box se sab kuch search karo.
        Returns: {
            'users': QuerySet,
            'orders': QuerySet,
            'products': QuerySet,
            'total_count': int
        }
        """
        if not query or len(query.strip()) < 2:
            return {
                'users': User.objects.none(),
                'orders': Order.objects.none(),
                'products': Product.objects.none(),
                'total_count': 0
            }

        query = query.strip()

        # Local LLM se structured filters (status/boolean/date/number) nikalo.
        # Best-effort hai - Ollama down ho to khaali dict aata hai, kuch nahi tootega.
        llm_filters = get_llm_filters(query)

        # =============================================
        # 1. USERS SEARCH
        # =============================================
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(shipping_address__icontains=query) |
            Q(role__icontains=query)
        )
        if llm_filters['users']:
            users = users | User.objects.filter(**llm_filters['users'])
        users = users.distinct()[:limit]

        # =============================================
        # 2. ORDERS SEARCH
        # =============================================
        orders = Order.objects.filter(
            Q(transaction_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(city__icontains=query) |
            Q(address__icontains=query) |
            Q(order_status__icontains=query) |
            Q(payment_status__icontains=query)
        )
        if llm_filters['orders']:
            orders = orders | Order.objects.filter(**llm_filters['orders'])
        orders = orders.distinct()[:limit]

        # =============================================
        # 3. PRODUCTS SEARCH
        # =============================================
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )
        if llm_filters['products']:
            products = products | Product.objects.filter(**llm_filters['products'])
        products = products.distinct()[:limit]

        # =============================================
        # TOTAL COUNT
        # =============================================
        total_count = users.count() + orders.count() + products.count()

        return {
            'users': users,
            'orders': orders,
            'products': products,
            'total_count': total_count
        }

    @staticmethod
    def search_by_model(model_type, query, filters=None, limit=50):
        """
        Specific model ke liye advanced search. (Unchanged)
        model_type: 'users', 'orders', 'products'
        """
        if model_type == 'users':
            queryset = User.objects.all()
        elif model_type == 'orders':
            queryset = Order.objects.all()
        elif model_type == 'products':
            queryset = Product.objects.all()
        else:
            return None

        if query and len(query.strip()) >= 2:
            query = query.strip()

            if model_type == 'users':
                queryset = queryset.filter(
                    Q(username__icontains=query) |
                    Q(email__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(phone_number__icontains=query) |
                    Q(role__icontains=query)
                )
            elif model_type == 'orders':
                queryset = queryset.filter(
                    Q(transaction_id__icontains=query) |
                    Q(email__icontains=query) |
                    Q(city__icontains=query) |
                    Q(order_status__icontains=query) |
                    Q(payment_status__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query)
                )
            elif model_type == 'products':
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(sku__icontains=query) |
                    Q(brand__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__name__icontains=query)
                )

        if filters:
            queryset = queryset.filter(**filters)

        return queryset.distinct()[:limit]

    @staticmethod
    def get_stats():
        """
        Dashboard ke liye quick stats. (Unchanged)
        """
        return {
            'total_users': User.objects.count(),
            'total_orders': Order.objects.count(),
            'total_products': Product.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'pending_orders': Order.objects.filter(order_status__icontains='PENDING').count(),
            'delivered_orders': Order.objects.filter(order_status__icontains='DELIVERED').count(),
            'total_revenue': Order.objects.aggregate(total=Sum('total_price'))['total'] or 0,
            'out_of_stock_products': Product.objects.filter(stock_count=0).count(),
        }