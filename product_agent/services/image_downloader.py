from pathlib import Path
from urllib.parse import urlparse
import requests


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ORIGINAL_IMAGES_DIR = BASE_DIR / "product_images" / "original"

ORIGINAL_IMAGES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def download_image(image_url, filename):
    """
    Download an image from a URL and save it
    inside product_images/original/
    """

    if not image_url:
        return None

    image_url = image_url.strip()

    if not image_url:
        return None

    # Make sure filename has a safe extension
    parsed_url = urlparse(image_url)

    extension = Path(
        parsed_url.path
    ).suffix.lower()

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".jfif",
    }

    if extension not in allowed_extensions:
        extension = ".jpg"

    filename = Path(filename).stem + extension

    output_path = (
        ORIGINAL_IMAGES_DIR / filename
    )

    print(
        f"Downloading image:\n"
        f"{image_url}\n"
        f"-> {output_path}"
    )

    try:

        response = requests.get(
            image_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if not content_type.startswith("image/"):

            raise ValueError(
                f"URL did not return an image. "
                f"Content-Type: {content_type}"
            )

        with open(
            output_path,
            "wb"
        ) as image_file:

            image_file.write(
                response.content
            )

        print(
            f"Image downloaded successfully: "
            f"{output_path}"
        )

        return output_path

    except Exception as exc:

        print(
            f"Image download failed: "
            f"{image_url}"
        )

        print(
            f"Error: {exc}"
        )

        return None