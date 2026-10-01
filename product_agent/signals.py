from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProductCSVImport
from .tools.product_csv_tool import import_product_csv


@receiver(post_save, sender=ProductCSVImport)
def product_csv_uploaded(
    sender,
    instance,
    created,
    **kwargs,
):
    if created:

        print(
            f"\n[SIGNAL] New CSV uploaded: "
            f"{instance.file.name}"
        )

        print(
            f"[SIGNAL] Calling tool for CSV ID: "
            f"{instance.id}"
        )

        result = import_product_csv(instance.id)

        print(
            f"[SIGNAL] Tool finished: "
            f"{result}"
        )