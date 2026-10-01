from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):

    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'Cash on Delivery'
        STRIPE = 'STRIPE', 'Stripe'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    class OrderStatus(models.TextChoices):
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True
    )

    first_name = models.CharField(
        max_length=50
    )

    last_name = models.CharField(
        max_length=50
    )

    email = models.EmailField()

    address = models.CharField(
        max_length=250
    )

    postal_code = models.CharField(
        max_length=20
    )

    city = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================
    # DELIVERY
    # =========================================================

    estimated_delivery_date = models.DateField(
        null=True,
        blank=True
    )

    # =========================================================
    # ORDER TOTAL
    # =========================================================

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # =========================================================
    # PAYMENT
    # =========================================================

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.COD
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    # =========================================================
    # ORDER STATUS
    # =========================================================

    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"Item #{self.id} for Order #{self.order.id}"

    def get_cost(self):
        return self.price * self.quantity