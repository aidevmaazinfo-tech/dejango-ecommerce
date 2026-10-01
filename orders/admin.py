from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    fields = ['product', 'price', 'quantity', 'subtotal']
    readonly_fields = ['subtotal']

    def subtotal(self, obj):
        if obj.pk:
            return format_html(
                '<strong>${}</strong>',
                obj.price * obj.quantity
            )
        return "—"
    subtotal.short_description = 'Subtotal'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Existing order - readonly
            return ['product', 'price', 'quantity', 'subtotal']
        return ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_name',
        'email',
        'city',
        'total_price_display',
        'payment_status_badge',
        'order_status_badge',
        'items_count',
        'created_at',
    ]

    list_filter = [
        'payment_status',
        'order_status',
        'city',
        'created_at',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'email',
        'city',
        'address',
        'postal_code',
        'transaction_id',
        'payment_status',
        'order_status',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    list_per_page = 25

    date_hierarchy = 'created_at'

    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Order Information', {
            'fields': ('transaction_id', 'total_price', 'payment_status', 'order_status', 'estimated_delivery_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = [
        'mark_as_processing',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_cancelled',
        'mark_payment_completed',
        'mark_payment_failed',
    ]

    # =============================================
    # CUSTOM LIST DISPLAY METHODS
    # =============================================

    def customer_name(self, obj):
        return format_html(
            '<strong style="color: #111827;">{} {}</strong>',
            obj.first_name,
            obj.last_name
        )
    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'first_name'

    def total_price_display(self, obj):
        return format_html(
            '<strong style="color: #111827; font-size: 14px;">${}</strong>',
            obj.total_price
        )
    total_price_display.short_description = 'Total'
    total_price_display.admin_order_field = 'total_price'

    def payment_status_badge(self, obj):
        colors = {
            'PENDING': ('#fffbeb', '#d97706', '⏳'),
            'COMPLETED': ('#f0fdf4', '#16a34a', '✓'),
            'FAILED': ('#fef2f2', '#dc2626', '✗'),
        }
        bg, color, icon = colors.get(obj.payment_status, ('#f3f4f6', '#6b7280', ''))
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} {}</span>',
            bg, color, icon, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'
    payment_status_badge.admin_order_field = 'payment_status'

    def order_status_badge(self, obj):
        colors = {
            'PROCESSING': ('#eff6ff', '#2563eb', '⟳'),
            'SHIPPED': ('#fffbeb', '#d97706', '🚚'),
            'DELIVERED': ('#f0fdf4', '#16a34a', '✓'),
            'CANCELLED': ('#fef2f2', '#dc2626', '✗'),
        }
        bg, color, icon = colors.get(obj.order_status, ('#f3f4f6', '#6b7280', ''))
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} {}</span>',
            bg, color, icon, obj.get_order_status_display()
        )
    order_status_badge.short_description = 'Status'
    order_status_badge.admin_order_field = 'order_status'

    def items_count(self, obj):
        count = obj.items.count()
        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} item{}</span>',
            count,
            's' if count != 1 else ''
        )
    items_count.short_description = 'Items'

    # =============================================
    # CUSTOM ACTIONS
    # =============================================

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.PROCESSING)
        self.message_user(request, f"✅ {updated} order(s) marked as Processing.")
    mark_as_processing.short_description = "⟳ Mark as Processing"

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.SHIPPED)
        self.message_user(request, f"🚚 {updated} order(s) marked as Shipped.")
    mark_as_shipped.short_description = "🚚 Mark as Shipped"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.DELIVERED)
        self.message_user(request, f"✅ {updated} order(s) marked as Delivered.")
    mark_as_delivered.short_description = "✓ Mark as Delivered"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.CANCELLED)
        self.message_user(request, f"❌ {updated} order(s) marked as Cancelled.")
    mark_as_cancelled.short_description = "✗ Mark as Cancelled"

    def mark_payment_completed(self, request, queryset):
        updated = queryset.update(payment_status=Order.PaymentStatus.COMPLETED)
        self.message_user(request, f"💳 {updated} order(s) payment marked as Completed.")
    mark_payment_completed.short_description = "💳 Mark Payment Completed"

    def mark_payment_failed(self, request, queryset):
        updated = queryset.update(payment_status=Order.PaymentStatus.FAILED)
        self.message_user(request, f"⚠️ {updated} order(s) payment marked as Failed.")
    mark_payment_failed.short_description = "⚠️ Mark Payment Failed"

    # =============================================
    # PERMISSIONS
    # =============================================

    def has_delete_permission(self, request, obj=None):
        # Orders delete nahi honge, sirf cancel honge
        return False