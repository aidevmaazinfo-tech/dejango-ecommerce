from django.contrib import admin
from django.utils.html import format_html

from .models import Intent


@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    """
    Admin interface for deterministic intents.
    """

    list_display = (
        "id",
        "intent_name",
        "trigger_count",
        "status_badge",
        "response_preview",
        "updated_at",
    )

    search_fields = (
        "intent_name",
        "trigger_phrase",
        "response",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    fieldsets = (
        ("Intent Information", {
            "fields": ("intent_name", "is_active")
        }),
        ("Trigger Phrases", {
            "fields": ("trigger_phrase",),
            "description": "Comma separated trigger words or phrases. Example: 'hello, hi, hey, salam'"
        }),
        ("Response", {
            "fields": ("response",),
            "description": "The response the assistant will give when this intent is triggered."
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    actions = [
        'activate_intents',
        'deactivate_intents',
    ]

    # =============================================
    # CUSTOM METHODS
    # =============================================

    def trigger_count(self, obj):
        """
        Count how many trigger phrases this intent has.
        """
        if obj.trigger_phrase:
            phrases = [p.strip() for p in obj.trigger_phrase.split(',') if p.strip()]
            count = len(phrases)
        else:
            count = 0

        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} phrases</span>',
            count
        )

    trigger_count.short_description = "Triggers"

    def status_badge(self, obj):
        if obj.is_active:
            bg, color, label = '#f0fdf4', '#16a34a', 'Active'
        else:
            bg, color, label = '#fef2f2', '#dc2626', 'Inactive'

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, label
        )

    status_badge.short_description = "Status"
    status_badge.admin_order_field = "is_active"

    def response_preview(self, obj):
        if obj.response:
            preview = obj.response[:60] + '...' if len(obj.response) > 60 else obj.response
            return format_html(
                '<span style="color: #6b7280; font-size: 13px;">{}</span>',
                preview
            )
        return '—'

    response_preview.short_description = "Response Preview"

    # =============================================
    # CUSTOM ACTIONS
    # =============================================

    def activate_intents(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} intent(s) activated.")

    activate_intents.short_description = "Activate Intents"

    def deactivate_intents(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} intent(s) deactivated.")

    deactivate_intents.short_description = "Deactivate Intents"