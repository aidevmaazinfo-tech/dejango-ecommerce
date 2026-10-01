import hashlib
import time

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Product


class Command(BaseCommand):
    help = "Fix and assign unique product images."

    # ============================================================
    # SETTINGS
    # ============================================================

    REQUEST_TIMEOUT = 45
    MAX_RETRIES = 2
    DELAY_BETWEEN_PRODUCTS = 0.20

    IMAGE_WIDTH = 1200
    IMAGE_HEIGHT = 800

    # ============================================================
    # EXISTING IMAGE URLS
    #
    # These are your existing Unsplash images.
    # Your seed data does NOT need to be changed.
    # ============================================================

    IMAGE_URLS = {

        "laptop": [
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1200",
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200",
            "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=1200",
        ],

        "phone": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200",
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=1200",
            "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=1200",
        ],

        "tablet": [
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=1200",
            "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=1200",
        ],

        "monitor": [
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=1200",
            "https://images.unsplash.com/photo-1551645120-d70bfe84c826?w=1200",
        ],

        "keyboard": [
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=1200",
            "https://images.unsplash.com/photo-1595225476474-87563907a212?w=1200",
        ],

        "mouse": [
            "https://images.unsplash.com/photo-1527814050087-3793815479db?w=1200",
            "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=1200",
        ],

        "headphones": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=1200",
        ],

        "earbuds": [
            "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=1200",
            "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=1200",
        ],

        "speaker": [
            "https://images.unsplash.com/photo-1589003077984-894e133dabab?w=1200",
            "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=1200",
        ],

        "camera": [
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200",
            "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=1200",
        ],

        "watch": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1200",
            "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=1200",
        ],

        "gaming": [
            "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=1200",
            "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=1200",
        ],

        "desk": [
            "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=1200",
            "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1200",
        ],

        "smart_home": [
            "https://images.unsplash.com/photo-1558008258-3256797b43f3?w=1200",
            "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=1200",
        ],

        "router": [
            "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=1200",
        ],

        "storage": [
            "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=1200",
        ],

        "printer": [
            "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=1200",
        ],

        "tv": [
            "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=1200",
            "https://images.unsplash.com/photo-1461151304267-38535e780c79?w=1200",
        ],

        "charger": [
            "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=1200",
        ],
    }

    # ============================================================
    # CATEGORY -> IMAGE TYPE
    # ============================================================

    CATEGORY_TYPES = {

        "Electronics & Laptops": "laptop",

        "Smartphones": "phone",

        "Tablets": "tablet",

        "Monitors": "monitor",

        "Keyboards & Mice": "keyboard",

        "Mice & Controllers": "mouse",

        "Audio & Headphones": "headphones",

        "Earbuds": "earbuds",

        "Speakers": "speaker",

        "Cameras": "camera",

        "Wearables & Fitness": "watch",

        "Gaming Gear": "gaming",

        "Smart Home": "smart_home",

        "Office & Workspace": "desk",

        "Storage": "storage",

        "Networking": "router",

        "Printers": "printer",

        "Televisions": "tv",

        "Chargers & Power": "charger",
    }

    # ============================================================
    # MAIN COMMAND
    # ============================================================

    def handle(self, *args, **kwargs):

        self.stdout.write("")

        self.stdout.write(
            self.style.WARNING(
                "=================================================="
            )
        )

        self.stdout.write(
            self.style.WARNING(
                "       PRODUCT IMAGE FIXER"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                "=================================================="
            )
        )

        # --------------------------------------------------------
        # IMPORTANT:
        #
        # Process ALL products.
        #
        # We want to replace the duplicate category images too.
        # --------------------------------------------------------

        products = (
            Product.objects
            .select_related("category")
            .order_by("id")
        )

        total = products.count()

        self.stdout.write(
            f"\nProducts found: {total}\n"
        )

        if total == 0:

            self.stdout.write(
                self.style.ERROR(
                    "No products found."
                )
            )

            return

        downloaded = 0
        failed = 0

        # --------------------------------------------------------
        # Process every product
        # --------------------------------------------------------

        for index, product in enumerate(
            products,
            start=1,
        ):

            self.stdout.write("")
            self.stdout.write(
                "=" * 65
            )

            self.stdout.write(
                f"[{index}/{total}] "
                f"{product.name}"
            )

            self.stdout.write(
                f"Category: {product.category.name}"
            )

            # ----------------------------------------------------
            # Determine image type
            # ----------------------------------------------------

            image_type = self.get_image_type(
                product
            )

            self.stdout.write(
                f"Image type: {image_type}"
            )

            # ----------------------------------------------------
            # Get ordered image URLs
            # ----------------------------------------------------

            urls = self.get_product_urls(
                product,
                image_type,
            )

            success = False

            # ----------------------------------------------------
            # Try category images
            # ----------------------------------------------------

            for url in urls:

                self.stdout.write(
                    f"Trying: {url}"
                )

                if self.download_image(
                    product,
                    url,
                ):

                    downloaded += 1
                    success = True

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Image saved for "
                            f"{product.name}"
                        )
                    )

                    break

            # ----------------------------------------------------
            # Fallback image
            # ----------------------------------------------------

            if not success:

                self.stdout.write(
                    self.style.WARNING(
                        "Category images failed."
                    )
                )

                fallback_url = (
                    self.get_fallback_url(
                        product,
                        image_type,
                    )
                )

                self.stdout.write(
                    f"Trying fallback: "
                    f"{fallback_url}"
                )

                if self.download_image(
                    product,
                    fallback_url,
                ):

                    downloaded += 1
                    success = True

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Fallback image saved "
                            f"for {product.name}"
                        )
                    )

                else:

                    failed += 1

                    self.stdout.write(
                        self.style.ERROR(
                            f"✗ Could not download "
                            f"image for {product.name}"
                        )
                    )

            # ----------------------------------------------------
            # Delay
            # ----------------------------------------------------

            time.sleep(
                self.DELAY_BETWEEN_PRODUCTS
            )

        # ========================================================
        # FINAL REPORT
        # ========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=================================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "             IMAGE FIX COMPLETE"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=================================================="
            )
        )

        self.stdout.write(
            f"Total products : {total}"
        )

        self.stdout.write(
            f"Images saved   : {downloaded}"
        )

        self.stdout.write(
            f"Images failed  : {failed}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=================================================="
            )
        )

    # ============================================================
    # DETERMINE IMAGE TYPE
    # ============================================================

    def get_image_type(
        self,
        product,
    ):

        category_name = (
            product.category.name
        )

        # Exact category match first.

        if category_name in self.CATEGORY_TYPES:

            return self.CATEGORY_TYPES[
                category_name
            ]

        # --------------------------------------------------------
        # Fallback matching
        # --------------------------------------------------------

        category_lower = (
            category_name.lower()
        )

        if "laptop" in category_lower:
            return "laptop"

        if "phone" in category_lower:
            return "phone"

        if "tablet" in category_lower:
            return "tablet"

        if "monitor" in category_lower:
            return "monitor"

        if "keyboard" in category_lower:
            return "keyboard"

        if "mouse" in category_lower:
            return "mouse"

        if "headphone" in category_lower:
            return "headphones"

        if "earbud" in category_lower:
            return "earbuds"

        if "speaker" in category_lower:
            return "speaker"

        if "camera" in category_lower:
            return "camera"

        if "wearable" in category_lower:
            return "watch"

        if "gaming" in category_lower:
            return "gaming"

        if "office" in category_lower:
            return "desk"

        if "storage" in category_lower:
            return "storage"

        if "network" in category_lower:
            return "router"

        if "printer" in category_lower:
            return "printer"

        if "television" in category_lower:
            return "tv"

        if "charger" in category_lower:
            return "charger"

        if "power" in category_lower:
            return "charger"

        if "smart home" in category_lower:
            return "smart_home"

        # Generic fallback.

        return "gaming"

    # ============================================================
    # GET PRODUCT-SPECIFIC URL ORDER
    # ============================================================

    def get_product_urls(
        self,
        product,
        image_type,
    ):

        urls = self.IMAGE_URLS.get(
            image_type,
            [],
        )

        if not urls:
            return []

        # --------------------------------------------------------
        # Create a deterministic starting position.
        #
        # Product 1 doesn't always start at URL 0.
        # Product 2 starts somewhere else.
        # Product 3 starts somewhere else.
        #
        # This spreads the existing category images around
        # instead of giving every product urls[0].
        # --------------------------------------------------------

        name_hash = hashlib.md5(
            product.name.encode(
                "utf-8"
            )
        ).hexdigest()

        number = int(
            name_hash[:8],
            16,
        )

        start = number % len(urls)

        ordered = []

        for offset in range(
            len(urls)
        ):

            index = (
                start + offset
            ) % len(urls)

            url = urls[index]

            if url not in ordered:

                ordered.append(url)

        return ordered

    # ============================================================
    # UNIQUE FALLBACK
    # ============================================================

    def get_fallback_url(
        self,
        product,
        image_type,
    ):

        """
        Picsum is only used if the category-specific Unsplash
        images cannot be downloaded.

        The seed contains the product ID and name.

        Therefore:

        Product A != Product B

        and the same product gets the same fallback image
        when the command is run again.
        """

        seed_string = (
            f"{product.id}-"
            f"{product.name}-"
            f"{image_type}"
        )

        seed = hashlib.sha256(
            seed_string.encode(
                "utf-8"
            )
        ).hexdigest()[:16]

        return (
            f"https://picsum.photos/seed/"
            f"{seed}/"
            f"{self.IMAGE_WIDTH}/"
            f"{self.IMAGE_HEIGHT}"
        )

    # ============================================================
    # DOWNLOAD IMAGE
    # ============================================================

    def download_image(
        self,
        product,
        url,
    ):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0.0.0 "
                "Safari/537.36"
            ),
            "Accept": (
                "image/avif,image/webp,"
                "image/apng,image/svg+xml,"
                "image/*,*/*;q=0.8"
            ),
        }

        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):

            try:

                self.stdout.write(
                    f"    Download attempt "
                    f"{attempt}/"
                    f"{self.MAX_RETRIES}"
                )

                response = requests.get(
                    url,
                    timeout=self.REQUEST_TIMEOUT,
                    headers=headers,
                    allow_redirects=True,
                )

                response.raise_for_status()

                # ------------------------------------------------
                # Check Content-Type
                # ------------------------------------------------

                content_type = (
                    response
                    .headers
                    .get(
                        "Content-Type",
                        "",
                    )
                    .lower()
                )

                if not content_type.startswith(
                    "image/"
                ):

                    raise ValueError(
                        "Server did not return an image. "
                        f"Content-Type: "
                        f"{content_type}"
                    )

                # ------------------------------------------------
                # Check actual data
                # ------------------------------------------------

                if not response.content:

                    raise ValueError(
                        "Downloaded file is empty."
                    )

                # ------------------------------------------------
                # Unique local filename
                # ------------------------------------------------

                filename = (
                    f"{slugify(product.name)}"
                    f"-{product.id}.jpg"
                )

                # ------------------------------------------------
                # Delete old main image
                # ------------------------------------------------

                if product.image:

                    old_image = (
                        product.image.name
                    )

                    try:

                        product.image.delete(
                            save=False
                        )

                        self.stdout.write(
                            f"    Replacing old image: "
                            f"{old_image}"
                        )

                    except Exception as error:

                        self.stdout.write(
                            self.style.WARNING(
                                f"    Could not delete "
                                f"old image: {error}"
                            )
                        )

                # ------------------------------------------------
                # Save new image
                # ------------------------------------------------

                product.image.save(
                    filename,
                    ContentFile(
                        response.content
                    ),
                    save=True,
                )

                return True

            except requests.RequestException as error:

                self.stdout.write(
                    self.style.ERROR(
                        f"    Request failed: "
                        f"{error}"
                    )
                )

            except Exception as error:

                self.stdout.write(
                    self.style.ERROR(
                        f"    Image failed: "
                        f"{error}"
                    )
                )

            # ----------------------------------------------------
            # Retry delay
            # ----------------------------------------------------

            if attempt < self.MAX_RETRIES:

                time.sleep(
                    2 * attempt
                )

        return False
