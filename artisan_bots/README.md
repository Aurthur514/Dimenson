# AI-Curated Artisan Box - Automation Bots

This project contains the Python scripts for the "AI-Curated Artisan Boxes" business concept. These bots are designed to automate product sourcing and social media content creation.

## Project Structure

- `scraper.py`: A script to scrape product information from an e-commerce website.
- `content_creator.py`: A script to generate social media content based on scraped product data.
- `requirements.txt`: A list of Python dependencies required to run the scripts.
- `products.csv`: The output of the scraper bot; a database of curated products.
- `generated_captions.txt`: One of the outputs of the content creator bot.
- `promo_collage.jpg`: The other output of the content creator bot.
- `mock_etsy_page.html`: A mock HTML file used for demonstrating the scraper's functionality without accessing a live website.

## Setup

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    Make sure you are in the root directory of the repository.
    ```bash
    pip install -r artisan_bots/requirements.txt
    ```

## How to Run

### 1. Run the Scraper Bot

This script will read the `mock_etsy_page.html` file, parse it, and save the curated product data into `artisan_bots/products.csv`.

```bash
python artisan_bots/scraper.py
```

### 2. Run the Content Creation Bot

This script reads the `products.csv` file and generates:
- A text file with sample Instagram captions (`artisan_bots/generated_captions.txt`).
- A sample promotional image collage (`artisan_bots/promo_collage.jpg`).

```bash
python artisan_bots/content_creator.py
```

## Adapting for Live Use

These scripts are designed as a template. To use them in a live production environment, you would need to:

- **`scraper.py`**:
  - Modify the `TARGET_URL` to the actual website you want to scrape.
  - Update the BeautifulSoup selectors in the `parse_products` function to match the live website's HTML structure.
  - Implement more robust error handling and potentially use tools like Selenium if the target site relies heavily on JavaScript.
- **`content_creator.py`**:
  - In `create_promo_collage`, replace the placeholder image generation with code that downloads the actual product images from the URLs found in `products.csv`.
  - Integrate with a social media API (e.g., the Instagram/Meta Graph API) to post the generated content automatically.
- **Authentication**: For services like Google Sheets or the Instagram API, you would need to handle API keys and user authentication securely.
