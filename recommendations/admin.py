from django.contrib import admin
from django.utils.html import format_html
from .models import UserInteraction, UserPreferenceProfile, CachedRecommendation


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor",
        "product",
        "action_type_badge",
        "weight_badge",
        "created_at",
    )

    list_filter = (
        "action_type",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "product__name",
        "product__sku",
        "session_key",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    # =============================================
    # CUSTOM METHODS
    # =============================================

    def actor(self, obj):
        if obj.user:
            return obj.user.username
        if obj.session_key:
            return f"Guest ({obj.session_key[:8]}...)"
        return "Guest"

    actor.short_description = "Actor"
    actor.admin_order_field = "user"

    def action_type_badge(self, obj):
        colors = {
            "VIEW": ("#eff6ff", "#2563eb"),
            "WISHLIST": ("#fdf4ff", "#9333ea"),
            "CART": ("#fffbeb", "#d97706"),
            "PURCHASE": ("#f0fdf4", "#16a34a"),
        }
        bg, color = colors.get(obj.action_type, ("#f3f4f6", "#6b7280"))
        label = obj.get_action_type_display()
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, label
        )

    action_type_badge.short_description = "Action"
    action_type_badge.admin_order_field = "action_type"

    def weight_badge(self, obj):
        if obj.weight >= 5:
            bg, color = "#f0fdf4", "#16a34a"
        elif obj.weight >= 3:
            bg, color = "#fffbeb", "#d97706"
        elif obj.weight >= 2:
            bg, color = "#fdf4ff", "#9333ea"
        else:
            bg, color = "#eff6ff", "#2563eb"

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, obj.weight
        )

    weight_badge.short_description = "Weight"
    weight_badge.admin_order_field = "weight"


@admin.register(UserPreferenceProfile)
class UserPreferenceProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor",
        "favorite_category",
        "price_range",
        "updated_at",
    )

    list_filter = (
        "favorite_category",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "session_key",
    )

    readonly_fields = (
        "updated_at",
    )

    list_per_page = 25

    def actor(self, obj):
        if obj.user:
            return obj.user.username
        if obj.session_key:
            return f"Guest ({obj.session_key[:8]}...)"
        return "Guest"

    actor.short_description = "Actor"
    actor.admin_order_field = "user"

    def price_range(self, obj):
        return format_html(
            '<strong>${}</strong> — <strong>${}</strong>',
            obj.target_price_min,
            obj.target_price_max
        )

    price_range.short_description = "Price Range"


@admin.register(CachedRecommendation)
class CachedRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor",
        "products_count",
        "last_updated",
    )

    list_filter = (
        "last_updated",
    )

    search_fields = (
        "user__username",
        "user__email",
        "session_key",
    )

    readonly_fields = (
        "last_updated",
    )

    filter_horizontal = (
        "recommended_products",
    )

    list_per_page = 25

    def actor(self, obj):
        if obj.user:
            return obj.user.username
        if obj.session_key:
            return f"Guest ({obj.session_key[:8]}...)"
        return "Guest"

    actor.short_description = "Actor"
    actor.admin_order_field = "user"

    def products_count(self, obj):
        count = obj.recommended_products.count()
        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} products</span>',
            count
        )

    products_count.short_description = "Products"