from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "products:product_list_by_category",
            args=[self.slug]
        )

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE
    )

    # =====================================================
    # SKU & BRAND (Recommended for Search Agents)
    # =====================================================

    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True  # Indexing speeds up brand-specific queries (e.g. "HP", "Dell")
    )

    # =====================================================
    # PRODUCT INFORMATION
    # =====================================================

    name = models.CharField(
        max_length=200,
        db_index=True  # Indexing speeds up name searches
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True  # Indexing speeds up range filters (min_price / max_price)
    )

    # =====================================================
    # INVENTORY
    # =====================================================

    stock_count = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # IMAGES
    # =====================================================

    image = models.ImageField(
        upload_to="products/%Y/%m/%d/",
        blank=True,
        null=True
    )

    # =====================================================
    # STATUS
    # =====================================================

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    # =====================================================
    # DATES
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['is_active', 'price']),  # Optimizes price range filtering on active items
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "products:product_detail",
            args=[self.id, self.slug]
        )

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        related_name="additional_images",
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="products/gallery/%Y/%m/%d/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Image for {self.product.name}"