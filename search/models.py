from django.db import models

from intents.models import Intent
from products.models import Product


class SearchLog(models.Model):
    """
    Stores chatbot queries and their results.
    """

    query = models.TextField()

    matched_intent = models.ForeignKey(
        Intent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="search_logs",
    )

    matched_product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="search_logs",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

    def __str__(self):
        return self.query[:50]