from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Category

User = get_user_model()


class UserInteraction(models.Model):
    ACTION_WEIGHTS = {
        "VIEW": 1.0,
        "WISHLIST": 2.0,
        "CART": 3.5,
        "PURCHASE": 5.0,
    }

    ACTION_CHOICES = [
        ("VIEW", "Product View"),
        ("WISHLIST", "Added to Wishlist"),
        ("CART", "Added to Cart"),
        ("PURCHASE", "Purchased"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    action_type = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        db_index=True,
    )
    weight = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "action_type"]),
            models.Index(fields=["session_key", "action_type"]),
        ]
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.weight == 1.0 and self.action_type in self.ACTION_WEIGHTS:
            self.weight = self.ACTION_WEIGHTS[self.action_type]
        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            actor = self.user.username
        else:
            actor = f"Guest ({self.session_key[:8]})" if self.session_key else "Guest"

        prod_title = getattr(self.product, 'sku', getattr(self.product, 'name', 'Product'))
        return f"{actor} - {self.action_type} - {prod_title}"

    @classmethod
    def log(cls, request, product, action_type):
        user = request.user if request.user.is_authenticated else None
        if not request.session.session_key:
            request.session.save()

        return cls.objects.create(
            user=user,
            session_key=request.session.session_key,
            product=product,
            action_type=action_type,
        )


class UserPreferenceProfile(models.Model):
    """
    Stores aggregated preferences calculated from UserInteraction logs.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="preference_profile",
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
    )
    favorite_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    target_price_min = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    target_price_max = models.DecimalField(
        max_digits=10, decimal_places=2, default=10000.00
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Profile for {self.user.username}"
        return f"Profile for Guest ({self.session_key[:8]})" if self.session_key else "Guest Profile"


class CachedRecommendation(models.Model):
    """
    Stores pre-computed recommendations generated asynchronously by the autonomous agent loop.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cached_recommendations",
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
    )
    recommended_products = models.ManyToManyField(
        Product,
        related_name="cached_recommendations",
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["session_key"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        if self.user:
            actor = self.user.username
        else:
            actor = f"Guest ({self.session_key[:8]})" if self.session_key else "Guest"
        return f"Agent Cache for {actor} - {self.last_updated.strftime('%Y-%m-%d %H:%M')}"