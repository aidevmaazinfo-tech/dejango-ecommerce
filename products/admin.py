from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ['image_preview', 'image']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 6px;" />',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = 'Preview'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'product_count',
        'description_preview',
    ]

    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25

    def product_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{} products</span>',
            count
        )

    product_count.short_description = 'Products'

    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '—'

    description_preview.short_description = 'Description'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview',
        'name',
        'sku',
        'brand',
        'category',
        'price_display',
        'stock_badge',
        'status_badge',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'category',
        'brand',
        'created_at',
    ]

    search_fields = [
        'name',
        'sku',
        'brand',
        'description',
        'category__name',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'image_preview_large',
    ]

    list_per_page = 25

    date_hierarchy = 'created_at'

    prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductImageInline]

    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('SKU & Brand', {
            'fields': ('sku', 'brand')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_count')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = [
        'mark_active',
        'mark_inactive',
        'restock_10',
        'restock_50',
        'clear_stock',
    ]

    # =============================================
    # CUSTOM LIST DISPLAY METHODS
    # =============================================

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 6px;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background: #f3f4f6; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #9ca3af; font-size: 16px;">—</div>'
        )

    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: cover; border-radius: 10px;" />',
                obj.image.url
            )
        return "No image uploaded"

    image_preview_large.short_description = 'Image Preview'

    def price_display(self, obj):
        return format_html(
            '<strong style="color: #111827;">${}</strong>',
            obj.price
        )

    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def stock_badge(self, obj):
        if obj.stock_count == 0:
            bg, color = '#fef2f2', '#dc2626'
            label = 'Out of Stock'
        elif obj.stock_count <= 5:
            bg, color = '#fffbeb', '#d97706'
            label = f'Low: {obj.stock_count}'
        else:
            bg, color = '#f0fdf4', '#16a34a'
            label = f'In Stock: {obj.stock_count}'

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, label
        )

    stock_badge.short_description = 'Stock'
    stock_badge.admin_order_field = 'stock_count'

    def status_badge(self, obj):
        if obj.is_active:
            bg, color, label = '#f0fdf4', '#16a34a', 'Active'
        else:
            bg, color, label = '#fef2f2', '#dc2626', 'Inactive'

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, label
        )

    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'is_active'

    # =============================================
    # CUSTOM ACTIONS
    # =============================================

    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} product(s) marked as Active.")

    mark_active.short_description = "Mark as Active"

    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} product(s) marked as Inactive.")

    mark_inactive.short_description = "Mark as Inactive"

    def restock_10(self, request, queryset):
        for product in queryset:
            product.stock_count += 10
            product.save()
        self.message_user(request, f"{queryset.count()} product(s) restocked with 10 units.")

    restock_10.short_description = "Restock +10"

    def restock_50(self, request, queryset):
        for product in queryset:
            product.stock_count += 50
            product.save()
        self.message_user(request, f"{queryset.count()} product(s) restocked with 50 units.")

    restock_50.short_description = "Restock +50"

    def clear_stock(self, request, queryset):
        updated = queryset.update(stock_count=0)
        self.message_user(request, f"{updated} product(s) stock cleared.")

    clear_stock.short_description = "Clear Stock"