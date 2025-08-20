import csv
import random
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
INPUT_CSV_FILE = "artisan_bots/products.csv"
OUTPUT_COLLAGE_FILE = "artisan_bots/promo_collage.jpg"
GENERATED_CAPTIONS_FILE = "artisan_bots/generated_captions.txt"

def load_products_from_csv(filename):
    """Loads product data from the specified CSV file."""
    products = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                products.append(row)
        print(f"Successfully loaded {len(products)} products from {filename}.")
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return products

def generate_caption(product):
    """Generates a sample Instagram caption for a given product."""

    # Templates for creating varied captions
    caption_templates = [
        "✨ Fresh find! ✨ Check out this gorgeous {product_name} from the amazing @{artisan_name}! Perfect for your collection. 😍 #ArtisanGifts #HandmadeWithLove #{tag}",
        "Obsessed with this {product_name}! 💖 Crafted by the talented @{artisan_name}. Want one? Find it in our shop! #SupportArtisans #ShopSmall #{tag}",
        "Bring a touch of artistry to your home with the {product_name} by @{artisan_name}. Truly one-of-a-kind! ✨ #HandmadeDecor #ArtisanMade #{tag}"
    ]

    # Simple logic to create a relevant hashtag from the product name
    tag = "".join(product['product_name'].split()[:2]).lower()
    artisan_ig = product['artisan_name'].replace(' ', '') # A mock instagram handle

    caption = random.choice(caption_templates).format(
        product_name=product['product_name'],
        artisan_name=artisan_ig,
        tag=tag
    )
    return caption

def create_promo_collage(products, output_path):
    """
    Creates a simple promotional collage from product data.

    NOTE: In a real-world script, you would download the images from
    'image_url'. For this demonstration, we will generate placeholder
    colored squares to simulate the images.
    """
    if not products:
        print("No products to create a collage from.")
        return

    print("Creating a promotional collage...")

    # Let's use the first 4 products for a 2x2 collage
    products_for_collage = products[:4]

    img_width, img_height = 200, 200
    collage_width = img_width * 2
    collage_height = img_height * 2

    collage = Image.new('RGB', (collage_width, collage_height), 'white')
    draw = ImageDraw.Draw(collage)

    for i, product in enumerate(products_for_collage):
        # Create a placeholder image with a random color
        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 255))
        placeholder_img = Image.new('RGB', (img_width, img_height), color)
        placeholder_draw = ImageDraw.Draw(placeholder_img)

        # Add product name to the placeholder image
        text = product['product_name'].split()[0] # First word
        try:
            # Use a default font if a specific .ttf is not available
            font = ImageFont.load_default()
            placeholder_draw.text((10, 10), text, fill='white', font=font)
        except IOError:
            print("Default font not found. Skipping text on placeholder.")
            placeholder_draw.text((10, 10), text, fill='white')


        # Position the image in the 2x2 grid
        x_pos = (i % 2) * img_width
        y_pos = (i // 2) * img_height
        collage.paste(placeholder_img, (x_pos, y_pos))

    try:
        collage.save(output_path)
        print(f"Promotional collage saved to {output_path}")
    except IOError as e:
        print(f"Error saving collage image: {e}")


def main():
    """Main function to run the content creation bot."""
    print("\n--- Starting Instagram Content Creation Bot ---")
    products = load_products_from_csv(INPUT_CSV_FILE)

    if products:
        # Generate captions for all products and save them to a file
        all_captions = []
        for product in products:
            caption = generate_caption(product)
            all_captions.append(caption)
            all_captions.append("-" * 20) # Separator

        try:
            with open(GENERATED_CAPTIONS_FILE, 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_captions))
            print(f"Generated captions saved to {GENERATED_CAPTIONS_FILE}")
        except IOError as e:
            print(f"Error writing captions file: {e}")

        # Create a sample collage
        create_promo_collage(products, OUTPUT_COLLAGE_FILE)

    print("--- Content Creation Bot Finished ---\n")

if __name__ == '__main__':
    main()
