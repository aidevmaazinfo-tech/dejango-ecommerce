import csv
import os
from decimal import Decimal

from django.core.files import File
from django.db import transaction
from django.utils.text import slugify

from products.models import Product, Category

from .image_downloader import download_image
from .image_processor import remove_background


class ProductCSVImporter:

    REQUIRED_COLUMNS = {
        "sku",
        "name",
        "description",
        "price",
        "stock_count",
        "category",
    }

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def import_products(self):

        self.csv_file.seek(0)

        decoded_file = (
            self.csv_file
            .read()
            .decode("utf-8-sig")
            .splitlines()
        )

        reader = csv.DictReader(decoded_file)

        # --------------------------------------------------
        # Validate columns
        # --------------------------------------------------

        if not reader.fieldnames:
            raise ValueError(
                "The CSV file has no header row."
            )

        columns = {
            column.strip()
            for column in reader.fieldnames
            if column
        }

        missing_columns = (
            self.REQUIRED_COLUMNS - columns
        )

        if missing_columns:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(
                    sorted(missing_columns)
                )
            )

        created = 0
        updated = 0
        skipped = 0

        images_downloaded = 0
        images_processed = 0
        images_failed = 0

        errors = []

        # --------------------------------------------------
        # Process rows
        # --------------------------------------------------

        for row_number, row in enumerate(
            reader,
            start=2,
        ):

            try:

                result = self.process_row(row)

                if result["product"] == "created":
                    created += 1

                elif result["product"] == "updated":
                    updated += 1

                if result["image_downloaded"]:
                    images_downloaded += 1

                if result["image_processed"]:
                    images_processed += 1

                if result["image_failed"]:
                    images_failed += 1

            except Exception as exc:

                skipped += 1

                errors.append(
                    f"Row {row_number}: {str(exc)}"
                )

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        result = (
            f"Created: {created}\n"
            f"Updated: {updated}\n"
            f"Skipped: {skipped}\n"
            f"Images downloaded: {images_downloaded}\n"
            f"Images processed: {images_processed}\n"
            f"Images failed: {images_failed}"
        )

        if errors:

            result += (
                "\n\nErrors:\n"
                + "\n".join(errors)
            )

        return result

    # ======================================================
    # DB TRANSACTION HELPER
    # ======================================================

    @transaction.atomic
    def _save_product(
        self,
        sku,
        name,
        description,
        price,
        stock_count,
        category,
    ):
        product = (
            Product.objects
            .filter(sku=sku)
            .first()
        )

        if product is None:

            product = Product.objects.create(
                sku=sku,
                name=name,
                slug=slugify(name),
                description=description,
                price=price,
                stock_count=stock_count,
                category=category,
                is_active=True,
            )

            return product, "created"

        product.name = name
        product.description = description
        product.price = price
        product.stock_count = stock_count
        product.category = category
        product.is_active = True

        if not product.slug:
            product.slug = slugify(name)

        product.save()

        return product, "updated"

    # ======================================================
    # PROCESS ROW
    # ======================================================

    def process_row(self, row):

        sku = (
            row.get("sku") or ""
        ).strip()

        name = (
            row.get("name") or ""
        ).strip()

        description = (
            row.get("description") or ""
        ).strip()

        price = (
            row.get("price") or ""
        ).strip()

        stock_count = (
            row.get("stock_count") or ""
        ).strip()

        category_name = (
            row.get("category") or ""
        ).strip()

        image_url = (
            row.get("image_url") or ""
        ).strip()

        # --------------------------------------------------
        # Validate
        # --------------------------------------------------

        if not sku:
            raise ValueError(
                "SKU is empty."
            )

        if not name:
            raise ValueError(
                "Product name is empty."
            )

        if not price:
            raise ValueError(
                "Price is empty."
            )

        if not stock_count:
            raise ValueError(
                "Stock count is empty."
            )

        if not category_name:
            raise ValueError(
                "Category is empty."
            )

        # --------------------------------------------------
        # Convert stock
        # --------------------------------------------------

        try:

            stock_count = int(
                stock_count
            )

        except ValueError:

            raise ValueError(
                f"Invalid stock_count: "
                f"{stock_count}"
            )

        if stock_count < 0:

            raise ValueError(
                "Stock count cannot be negative."
            )

        # --------------------------------------------------
        # Convert price
        # --------------------------------------------------

        try:

            price = Decimal(price)

        except Exception:

            raise ValueError(
                f"Invalid price: {price}"
            )

        if price < 0:

            raise ValueError(
                "Price cannot be negative."
            )

        # --------------------------------------------------
        # Category
        # --------------------------------------------------

        category_slug = slugify(
            category_name
        )

        category, _ = (
            Category.objects.get_or_create(
                slug=category_slug,
                defaults={
                    "name": category_name,
                },
            )
        )

        # --------------------------------------------------
        # Create / Update product
        # --------------------------------------------------

        product, product_status = self._save_product(
            sku=sku,
            name=name,
            description=description,
            price=price,
            stock_count=stock_count,
            category=category,
        )

        # ==================================================
        # IMAGE PIPELINE
        # ==================================================

        image_downloaded = False
        image_processed = False
        image_failed = False

        if image_url:

            try:

                # ------------------------------------------
                # 1. Download original
                # ------------------------------------------

                original_path = download_image(
                    image_url,
                    sku,
                )

                if original_path:

                    image_downloaded = True

                    # --------------------------------------
                    # 2. Remove background
                    # --------------------------------------

                    processed_path = remove_background(
                        original_path,
                        sku,
                    )

                    if processed_path:

                        image_processed = True

                        # ----------------------------------
                        # 3. Save processed image to Product
                        # ----------------------------------

                        filename = os.path.basename(
                            str(processed_path)
                        )

                        with open(
                            processed_path,
                            "rb",
                        ) as image_file:

                            product.image.save(
                                filename,
                                File(image_file),
                                save=True,
                            )

                        print(
                            f"Product image updated: "
                            f"{product.name}"
                        )

                    else:

                        image_failed = True

                else:

                    image_failed = True

            except Exception as exc:

                image_failed = True

                print(
                    f"Image processing failed "
                    f"for {sku}: {exc}"
                )

        # --------------------------------------------------
        # Return
        # --------------------------------------------------

        return {
            "product": product_status,
            "image_downloaded": image_downloaded,
            "image_processed": image_processed,
            "image_failed": image_failed,
        }