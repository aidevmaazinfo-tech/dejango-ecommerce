from django.utils import timezone

from product_agent.models import ProductCSVImport
from product_agent.services.csv_importer import ProductCSVImporter


def import_product_csv(csv_import_id):
    """
    Tool: Import one uploaded product CSV.
    """

    # --------------------------------------------------
    # Get the uploaded CSV
    # --------------------------------------------------

    csv_import = ProductCSVImport.objects.get(
        id=csv_import_id
    )

    # --------------------------------------------------
    # Prevent processing the same CSV twice
    # --------------------------------------------------

    if csv_import.processed:
        return {
            "success": False,
            "message": "CSV has already been processed.",
            "csv_id": csv_import.id,
        }

    # --------------------------------------------------
    # Call the existing CSV importer
    # --------------------------------------------------

    importer = ProductCSVImporter(
        csv_import.file.file
    )

    result = importer.import_products()

    # --------------------------------------------------
    # Mark CSV as processed
    # --------------------------------------------------

    csv_import.processed = True
    csv_import.processed_at = timezone.now()
    csv_import.result = result

    csv_import.save(
        update_fields=[
            "processed",
            "processed_at",
            "result",
        ]
    )

    # --------------------------------------------------
    # Return tool result
    # --------------------------------------------------

    return {
        "success": True,
        "message": "CSV imported successfully.",
        "csv_id": csv_import.id,
        "result": result,
    }