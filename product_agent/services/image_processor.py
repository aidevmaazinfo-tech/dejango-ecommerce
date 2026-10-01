from pathlib import Path
from PIL import Image
from rembg import remove, new_session

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ORIGINAL_IMAGES_DIR = BASE_DIR / "product_images" / "original"
PROCESSED_IMAGES_DIR = BASE_DIR / "product_images" / "processed"

PROCESSED_IMAGES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Initialize global session
SESSION = new_session("u2net")


def remove_background(image_path, filename):
    """
    Remove background from an image.
    Returns the processed image path.
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Ensure output filename has .png extension
    stem = Path(filename).stem
    output_path = PROCESSED_IMAGES_DIR / f"{stem}.png"

    print(f"Removing background from: {image_path}")

    try:
        # Load via Pillow to safely handle formats and release file locks immediately
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            output_img = remove(img, session=SESSION)
            output_img.save(output_path, format="PNG")

        print(f"Processed image saved: {output_path}")
        return output_path

    except Exception as exc:
        print(f"Failed to process background for {filename}: {exc}")
        raise exc