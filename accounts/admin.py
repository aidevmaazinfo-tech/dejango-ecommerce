from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'full_name',
        'email',
        'phone_number',
        'role_badge',
        'status_badge',
        'staff_badge',
        'orders_count',
        'total_spent',
        'date_joined',
    ]

    list_filter = [
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    ]

    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'shipping_address',
    ]

    readonly_fields = [
        'last_login',
        'date_joined',
    ]

    list_per_page = 25

    date_hierarchy = 'date_joined'

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )

    actions = [
        'activate_users',
        'deactivate_users',
        'make_staff',
        'remove_staff',
        'make_customer',
        'make_admin',
    ]

    # =============================================
    # CUSTOM LIST DISPLAY METHODS
    # =============================================

    def full_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else '—'

    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'

    def role_badge(self, obj):
        if obj.role == 'ADMIN':
            bg, color = '#fdf4ff', '#9333ea'
        else:
            bg, color = '#eff6ff', '#2563eb'

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, obj.get_role_display()
        )

    role_badge.short_description = 'Role'
    role_badge.admin_order_field = 'role'

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

    def staff_badge(self, obj):
        if obj.is_superuser:
            bg, color, label = '#fdf4ff', '#9333ea', 'Superuser'
        elif obj.is_staff:
            bg, color, label = '#fffbeb', '#d97706', 'Staff'
        else:
            bg, color, label = '#f3f4f6', '#6b7280', 'Customer'

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg, color, label
        )

    staff_badge.short_description = 'Type'
    staff_badge.admin_order_field = 'is_staff'

    def orders_count(self, obj):
        count = obj.orders.count()
        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            count
        )

    orders_count.short_description = 'Orders'

    def total_spent(self, obj):
        total = obj.orders.aggregate(total=Sum('total_price'))['total'] or 0
        return format_html(
            '<strong style="color: #111827;">${}</strong>',
            total
        )

    total_spent.short_description = 'Total Spent'

    # =============================================
    # CUSTOM ACTIONS
    # =============================================

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated.")

    activate_users.short_description = "Activate Users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated.")

    deactivate_users.short_description = "Deactivate Users"

    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} user(s) marked as Staff.")

    make_staff.short_description = "Make Staff"

    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f"{updated} user(s) removed from Staff.")

    remove_staff.short_description = "Remove Staff"

    def make_customer(self, request, queryset):
        updated = queryset.update(role=User.Roles.CUSTOMER)
        self.message_user(request, f"{updated} user(s) marked as Customer.")

    make_customer.short_description = "Make Customer"

    def make_admin(self, request, queryset):
        updated = queryset.update(role=User.Roles.ADMIN, is_staff=True)
        self.message_user(request, f"{updated} user(s) marked as Admin.")

    make_admin.short_description = "Make Admin"