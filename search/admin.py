from django.contrib import admin

from .models import SearchLog


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = (
        "query",
        "matched_intent",
        "matched_product",
        "created_at",
    )

    list_filter = (
        "matched_intent",
        "matched_product",
        "created_at",
    )

    search_fields = (
        "query",
        "matched_product__name",
        "matched_intent__name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    # =============================================
    # NEW: Additional Admin Settings
    # =============================================

    list_per_page = 50  # Ek page pe 50 entries

    date_hierarchy = "created_at"  # Date ke hisaab se navigate karo

    list_display_links = ("query",)  # Query pe click karke open karo

    # Search results ko highlight karo
    save_on_top = True  # Save button upar bhi dikhega

    # Admin ko manual SearchLog add karne se roko
    # (SearchLog automatically banta hai jab user search karta hai)
    def has_add_permission(self, request):
        return False

    # Admin search log delete nahi kar sakta
    def has_delete_permission(self, request, obj=None):
        return False