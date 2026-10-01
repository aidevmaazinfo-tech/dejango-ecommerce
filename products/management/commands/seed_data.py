import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Category, Product


class Command(BaseCommand):

    help = "Deletes existing products/categories and creates 30 products with images."

    # ============================================================
    # PRODUCT DATA
    # ============================================================

    DATA = [

        {
            "category": "Electronics & Laptops",
            "description": "High-performance laptops, workstations, and computing hardware.",

            "products": [

                {
                    "name": "UltraBook Pro 15",
                    "price": 1299.99,
                    "stock": 15,
                    "desc": "Sleek aluminum laptop with 16GB RAM and M-series performance.",
                    "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1000",
                },

                {
                    "name": "OLED Curved Monitor 34",
                    "price": 799.50,
                    "stock": 8,
                    "desc": "Immersive 175Hz curved display for extreme productivity.",
                    "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=1000",
                },

                {
                    "name": "Portable NVMe SSD 2TB",
                    "price": 189.99,
                    "stock": 45,
                    "desc": "Ultra-fast external storage with up to 2000MB/s read speed.",
                    "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=1000",
                },

                {
                    "name": "USB-C Dual Monitor Dock",
                    "price": 129.00,
                    "stock": 20,
                    "desc": "11-in-1 hub supporting 4K dual displays and 100W passthrough.",
                    "image": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=1000",
                },

                {
                    "name": "Mechanical Wireless Keyboard",
                    "price": 110.00,
                    "stock": 30,
                    "desc": "Tactile hot-swappable mechanical switches with RGB lighting.",
                    "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=1000",
                },
            ],
        },

        {
            "category": "Audio & Headphones",
            "description": "Studio-grade sound equipment, wireless earbuds, and speakers.",

            "products": [

                {
                    "name": "Wireless ANC Headphones",
                    "price": 249.99,
                    "stock": 25,
                    "desc": "Active Noise Cancellation with 40-hour battery life.",
                    "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1000",
                },

                {
                    "name": "True Wireless Studio Earbuds",
                    "price": 129.99,
                    "stock": 50,
                    "desc": "Water-resistant fit with deep bass and clear microphone.",
                    "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=1000",
                },

                {
                    "name": "Hi-Fi Desktop Speakers",
                    "price": 199.00,
                    "stock": 12,
                    "desc": "Wooden enclosure bookshelf speakers with Bluetooth 5.0.",
                    "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=1000",
                },

                {
                    "name": "USB Condenser Microphone",
                    "price": 89.95,
                    "stock": 18,
                    "desc": "Cardioid pickup pattern for streaming, podcasts, and calls.",
                    "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=1000",
                },

                {
                    "name": "Waterproof Outdoor Speaker",
                    "price": 69.99,
                    "stock": 40,
                    "desc": "IPX7 rated rugged portable speaker with 12-hour playtime.",
                    "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=1000",
                },
            ],
        },

        {
            "category": "Wearables & Fitness",
            "description": "Smartwatches, health trackers, and wearable sensors.",

            "products": [

                {
                    "name": "SmartWatch Ultra GPS",
                    "price": 349.99,
                    "stock": 10,
                    "desc": "Titanium case with heart rate sensor and multi-sport tracking.",
                    "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1000",
                },

                {
                    "name": "Fitness Tracker Smart Band",
                    "price": 49.99,
                    "stock": 60,
                    "desc": "Lightweight OLED band tracking sleep, steps, and SpO2.",
                    "image": "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?w=1000",
                },

                {
                    "name": "Smart Health & Sleep Ring",
                    "price": 299.00,
                    "stock": 14,
                    "desc": "Discreet ceramic ring providing round-the-clock biometrics.",
                    "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=1000",
                },

                {
                    "name": "Heart Rate Chest Strap",
                    "price": 59.99,
                    "stock": 22,
                    "desc": "ANT+ and Bluetooth dual-band precision workout sensor.",
                    "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1000",
                },

                {
                    "name": "GPS Running Companion",
                    "price": 179.50,
                    "stock": 19,
                    "desc": "Dedicated fitness watch with offline map routing.",
                    "image": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=1000",
                },
            ],
        },

        {
            "category": "Gaming Gear",
            "description": "Precision controllers, headsets, and gaming peripherals.",

            "products": [

                {
                    "name": "Pro RGB Gaming Mouse",
                    "price": 79.99,
                    "stock": 35,
                    "desc": "26k DPI optical sensor with sub-60g ultra-light design.",
                    "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=1000",
                },

                {
                    "name": "7.1 Surround Gaming Headset",
                    "price": 99.99,
                    "stock": 28,
                    "desc": "Detachable noise-canceling mic with memory foam pads.",
                    "image": "https://images.unsplash.com/photo-1599669454699-248893623440?w=1000",
                },

                {
                    "name": "Ergonomic Gaming Chair",
                    "price": 289.00,
                    "stock": 6,
                    "desc": "High-density foam with 4D armrests and lumbar support.",
                    "image": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=1000",
                },

                {
                    "name": "Wireless Gamepad Controller",
                    "price": 64.99,
                    "stock": 40,
                    "desc": "Low latency wireless controller compatible with PC and Mobile.",
                    "image": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=1000",
                },

                {
                    "name": "Speed Cloth XL Desk Mat",
                    "price": 29.99,
                    "stock": 100,
                    "desc": "Stitching-reinforced oversized mousepad surface.",
                    "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=1000",
                },
            ],
        },

        {
            "category": "Smart Home",
            "description": "Automation tools, security cameras, and ambient lighting.",

            "products": [

                {
                    "name": "Smart Outdoor Security Camera",
                    "price": 119.99,
                    "stock": 16,
                    "desc": "2K color night vision camera with motion spotlight.",
                    "image": "https://images.unsplash.com/photo-1558008258-3256797b43f3?w=1000",
                },

                {
                    "name": "Voice Assistant Smart Speaker",
                    "price": 49.99,
                    "stock": 45,
                    "desc": "Compact smart speaker with integrated home hub capabilities.",
                    "image": "https://images.unsplash.com/photo-1589003077984-894e133dabab?w=1000",
                },

                {
                    "name": "Smart LED Light Strip 5M",
                    "price": 34.99,
                    "stock": 50,
                    "desc": "Wi-Fi app controlled addressable RGB color modes.",
                    "image": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2?w=1000",
                },

                {
                    "name": "Wi-Fi Smart Plug 4-Pack",
                    "price": 29.99,
                    "stock": 70,
                    "desc": "Schedule energy usage and turn off appliances remotely.",
                    "image": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=1000",
                },

                {
                    "name": "Smart Video Doorbell",
                    "price": 139.00,
                    "stock": 11,
                    "desc": "Two-way audio chime with instant phone alerts.",
                    "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=1000",
                },
            ],
        },

        {
            "category": "Office & Workspace",
            "description": "Ergonomic accessories and modern desk setup gear.",

            "products": [

                {
                    "name": "Aluminum Laptop Stand",
                    "price": 39.99,
                    "stock": 30,
                    "desc": "Vented heat-dissipating riser for improved posture.",
                    "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1000",
                },

                {
                    "name": "Vertical Ergonomic Mouse",
                    "price": 45.00,
                    "stock": 22,
                    "desc": "Reduces wrist strain with natural handshake posture.",
                    "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=1000",
                },

                {
                    "name": "HD 1080p Web Camera",
                    "price": 59.99,
                    "stock": 27,
                    "desc": "Auto-focus lens with dual privacy shutter microphones.",
                    "image": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=1000",
                },

                {
                    "name": "Vegan Leather Desk Pad",
                    "price": 24.99,
                    "stock": 80,
                    "desc": "Waterproof desk mat providing smooth cursor movement.",
                    "image": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=1000",
                },

                {
                    "name": "Dimmable Monitor Light Bar",
                    "price": 49.90,
                    "stock": 18,
                    "desc": "Space-saving screen glare reduction desk lamp.",
                    "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=1000",
                },
            ],
        },
    ]

    # ============================================================
    # DOWNLOAD IMAGE
    # ============================================================

    def download_image(self, product, image_url):
        """
        Download image from the internet and save it using
        Django's ImageField.

        Django will automatically put the file inside:

        MEDIA_ROOT/products/YYYY/MM/DD/
        """

        try:

            self.stdout.write(
                f"    Downloading image for {product.name}..."
            )

            response = requests.get(
                image_url,
                timeout=30,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

            filename = (
                f"{slugify(product.name)}.jpg"
            )

            product.image.save(
                filename,
                ContentFile(response.content),
                save=True,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"    Image saved: {product.image.name}"
                )
            )

            return True

        except Exception as error:

            self.stdout.write(
                self.style.ERROR(
                    f"    Image failed for {product.name}: {error}"
                )
            )

            return False

    # ============================================================
    # MAIN
    # ============================================================

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING(
                "\nWARNING: This will DELETE all existing "
                "Products and Categories.\n"
            )
        )

        # --------------------------------------------------------
        # DELETE OLD DATA
        # --------------------------------------------------------

        self.stdout.write(
            "Deleting existing products..."
        )

        Product.objects.all().delete()

        self.stdout.write(
            "Deleting existing categories..."
        )

        Category.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Old product data deleted.\n"
            )
        )

        # --------------------------------------------------------
        # CREATE PRODUCTS
        # --------------------------------------------------------

        total_products = 0
        successful_images = 0
        failed_images = 0

        for category_data in self.DATA:

            category_name = category_data["category"]

            category = Category.objects.create(
                name=category_name,
                slug=slugify(category_name),
                description=category_data["description"],
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nCATEGORY: {category.name}"
                )
            )

            for product_data in category_data["products"]:

                product = Product.objects.create(

                    category=category,

                    name=product_data["name"],

                    slug=slugify(
                        product_data["name"]
                    ),

                    description=product_data["desc"],

                    price=product_data["price"],

                    stock_count=product_data["stock"],

                    is_active=True,
                )

                total_products += 1

                self.stdout.write(
                    f"  Product: {product.name}"
                )

                # ------------------------------------------------
                # DOWNLOAD PRODUCT IMAGE
                # ------------------------------------------------

                image_success = self.download_image(
                    product,
                    product_data["image"],
                )

                if image_success:

                    successful_images += 1

                else:

                    failed_images += 1

        # --------------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------------

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "DATABASE SEED COMPLETE"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            f"Categories created : {Category.objects.count()}"
        )

        self.stdout.write(
            f"Products created   : {total_products}"
        )

        self.stdout.write(
            f"Images downloaded  : {successful_images}"
        )

        self.stdout.write(
            f"Images failed      : {failed_images}"
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Images are now managed by Django's ImageField."
            )
        )