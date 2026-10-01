from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from django.urls import reverse


class GlobalAdminSearchMixin:
    """
    Is mixin ko kisi bhi ModelAdmin mein add karo taake global search mil jaye.
    """

    def get_search_results(self, request, queryset, search_term):
        """
        Override karke MySQL FULLTEXT + regular search dono use karo.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Additional search fields for better results
            search_fields = getattr(self, 'global_search_fields', [])
            if search_fields:
                query = Q()
                for field in search_fields:
                    query |= Q(**{f"{field}__icontains": search_term})
                queryset = queryset.filter(query).distinct()

        return queryset, use_distinct