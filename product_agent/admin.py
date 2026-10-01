from django.contrib import admin

from .models import ProductCSVImport


@admin.register(ProductCSVImport)
class ProductCSVImportAdmin(admin.ModelAdmin):

    list_display = [
        "file",
        "uploaded_at",
        "processed",
        "processed_at",
    ]

    list_filter = [
        "processed",
        "uploaded_at",
    ]

    readonly_fields = [
        "uploaded_at",
        "processed_at",
        "result",
    ]