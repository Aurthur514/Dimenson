# Business & Technical Blueprint: AI-Curated Artisan Boxes

This document outlines a comprehensive business and technical blueprint for a fully automated e-commerce website, "AI-Curated Artisan Boxes," which operates as a middleman using only free resources.

## 1. Website & Platform (Free Resources Only)

### Platform Choice
The recommended free e-commerce platform is **WordPress with the WooCommerce plugin**.

*   **Rationale:** While other platforms like Shift4Shop or Square Online offer free tiers, a self-hosted WordPress site (using a free plan from a hosting provider that offers one, or by finding a free hosting solution) provides the most flexibility and control. WooCommerce is a powerful, open-source plugin that can handle all core e-commerce functionality. The vast library of free plugins for WordPress allows for future expansion of automation capabilities.

### Design
A premium and trustworthy brand identity will be created using the following free tools:

*   **Theme:** Use a popular, highly-rated free theme from the WordPress repository like **Astra** or **Neve**. These themes are lightweight, customizable, and compatible with page builders.
*   **AI-Powered Design:**
    *   **Logo & Brand Kit:** Use **Canva's** free tier to design a professional logo, and select a color palette and typography to create a consistent brand identity.
    *   **Website Mockups:** Use **Microsoft Designer** to create mockups and promotional graphics. Its AI features can help generate ideas for website layouts and social media posts.

### Payment Gateway
**Stripe** will be used as the primary payment processor.

*   **Setup & Integration:**
    1.  Create a free Stripe account.
    2.  Install the official **Stripe for WooCommerce** plugin on the WordPress site.
    3.  Follow the plugin's setup wizard to connect the Stripe account to the website. This process is straightforward and requires copying API keys from the Stripe dashboard into the plugin's settings.
    4.  Enable various payment methods within Stripe (credit/debit cards, Apple Pay, Google Pay) to maximize conversion rates.

## 2. Automated Product Sourcing & Curation

### The 'Scraper & Curator' Bot
A Python script will be developed to automate product sourcing. This script can be run on a recurring schedule using **GitHub Actions**, which offers a generous free tier.

*   **Logic:**
    *   **Browsing:** The script will use libraries like `requests` and `BeautifulSoup` (or a more advanced tool like `selenium` if JavaScript rendering is needed) to scrape product information from Instagram, Etsy, and Pinterest based on predefined hashtags (e.g., `#handmadeceramics`, `#soycandles`, `#linocutprint`).
    *   **Curation:** The script will analyze the scraped data to identify suitable products.
        *   **Image Recognition:** Use a free API or a pre-trained model to assess image quality.
        *   **Text Analysis:** Use natural language processing (NLP) techniques to analyze product descriptions and comments for positive sentiment and relevant keywords.
    *   **Database Population:** The curated product information (product links, artisan contact details, prices, image URLs) will be automatically added to a **Google Sheet** using the `gspread` Python library.

### Automated Outreach
An automation service like **IFTTT** or a custom script will be used to send personalized outreach messages to artisans.

*   **Workflow:**
    1.  When a new row is added to the Google Sheet, an IFTTT applet (or a webhook from the Python script) will be triggered.
    2.  This trigger will send a pre-written, personalized email to the artisan using a free email service like Gmail.
    3.  The message will introduce the business, explain the commission-based model, and invite the artisan to be featured on the website.

## 3. Automated Order & Fulfillment Process

### The 'Order Forwarding' System
When a customer places an order, the following automated process will be triggered:

*   **Payment:** The customer's payment is processed by Stripe.
*   **Webhook:** WooCommerce will trigger a webhook upon successful payment.
*   **Order Forwarding:** A free-tier **Zapier** "Zap" or a similar IFTTT applet will catch the webhook.
    *   The Zap will parse the order data (customer name, shipping address, product ordered).
    *   It will calculate the artisan's payment (total price minus commission).
    *   It will then automatically send an email to the artisan with the order details and instructions for shipping. The payment can be forwarded manually at first, or an automated payout can be configured with Stripe Connect.
*   **Customer Confirmation:** Simultaneously, another automated email will be sent to the customer, confirming their order and letting them know that the artisan is preparing their unique item.

## 4. Automated Customer Acquisition (Instagram Funnel)

### Content Creation Bot
A Python script, also running on a **GitHub Actions** schedule, will manage the Instagram account.

*   **Content Sourcing:** The script will pull product images and artisan Instagram handles from the Google Sheet.
*   **AI-Powered Content Creation:**
    *   **Image Generation:** Use a library like `Pillow` to create simple collages or carousels of the product images.
    *   **Caption Generation:** Use a free AI text generation API to write compelling captions for the posts, including relevant hashtags and tagging the artisan's account.
*   **Scheduling:** The script will use an API or a library that interacts with the **Meta Business Suite** to schedule the posts to be published 1-2 times per day.

### Engagement Loop
**IFTTT** will be used to create an automated engagement loop.

*   **Workflow:**
    1.  Create an IFTTT applet that monitors Instagram for new posts with specific, relevant hashtags.
    2.  When a new post is detected, the applet will automatically "like" the post from the business's Instagram account.
    3.  This consistent engagement will drive traffic back to the business's profile, where the website link in the bio will serve as the primary call-to-action.
