from django.db import models


class ProductCSVImport(models.Model):
    file = models.FileField(
        upload_to="product_imports/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    processed = models.BooleanField(
        default=False
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    result = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.file.name