import csv
import requests
from bs4 import BeautifulSoup

# --- Configuration ---
# For a live website, you would use the actual URL.
# For this example, we are using a local mock HTML file.
TARGET_URL = "https://www.etsy.com/c/home-and-living/home-decor/candles"
LOCAL_FILE_PATH = "artisan_bots/mock_etsy_page.html"
OUTPUT_CSV_FILE = "artisan_bots/products.csv"

def fetch_live_html(url):
    """
    Fetches HTML content from a live URL.

    NOTE: Many websites have anti-scraping measures. For a real-world scenario,
    you would need to handle this with more advanced techniques, such as:
    - Rotating user agents and proxies.
    - Using a headless browser like Selenium or Playwright if content is loaded
      with JavaScript.
    - Respecting the website's robots.txt file.
    """
    print(f"Fetching live URL: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching live URL: {e}")
        return None

def fetch_local_html(filepath):
    """Fetches HTML content from a local file for testing purposes."""
    print(f"Fetching local file: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

def parse_products(html_content):
    """
    Parses the HTML content to extract product information.

    NOTE: The selectors used here (`.product-card`, `.product-title`, etc.)
    are based on our `mock_etsy_page.html`. These would need to be changed
    to match the HTML structure of the actual target website.
    """
    if not html_content:
        print("No HTML content to parse.")
        return []

    soup = BeautifulSoup(html_content, 'lxml')
    products = []

    product_cards = soup.find_all('div', class_='product-card')
    print(f"Found {len(product_cards)} product cards.")

    for card in product_cards:
        try:
            link_tag = card.find('a', class_='product-link')
            product_url = link_tag['href'] if link_tag else 'N/A'

            title_tag = card.find('h2', class_='product-title')
            product_name = title_tag.text.strip() if title_tag else 'N/A'

            artisan_tag = card.find('p', class_='artisan-name')
            artisan_name = artisan_tag.text.strip() if artisan_tag else 'N/A'

            price_tag = card.find('p', class_='price')
            price = price_tag.text.strip() if price_tag else 'N/A'

            img_tag = card.find('img')
            image_url = img_tag['src'] if img_tag else 'N/A'

            products.append({
                'product_name': product_name,
                'artisan_name': artisan_name,
                'price': price,
                'product_url': product_url,
                'image_url': image_url,
            })
        except Exception as e:
            print(f"Error parsing a product card: {e}")
            continue

    return products

def save_to_csv(products, filename):
    """Saves a list of product dictionaries to a CSV file."""
    if not products:
        print("No products to save.")
        return

    # Define the headers based on the keys of the first product dictionary
    headers = products[0].keys()

    print(f"Saving {len(products)} products to {filename}...")
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(products)
        print("Successfully saved to CSV.")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def main():
    """Main function to run the scraper bot."""
    print("--- Starting Scraper & Curator Bot ---")

    # We use the local file for this example.
    # To run on a live site, you would comment out the local fetch
    # and uncomment the live fetch.
    html_content = fetch_local_html(LOCAL_FILE_PATH)
    # html_content = fetch_live_html(TARGET_URL) # Uncomment for live scraping

    if html_content:
        products = parse_products(html_content)
        if products:
            save_to_csv(products, OUTPUT_CSV_FILE)

    print("--- Scraper & Curator Bot Finished ---")

if __name__ == '__main__':
    main()
