import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import json
import time
import logging
from .utils import check_missing_elements, check_missing_elements_after_conversion, CleanData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Product:
    """
    Represents a product with title, price, and image URL.
    """
    def __init__(self, product_title: str, product_price: float, path_to_image: str):
        self.product_title = product_title
        self.product_price = product_price
        self.path_to_image = path_to_image

    def to_dict(self):
        """
        Converts the Product instance to a dictionary.
        """
        return {
            "product_title": self.product_title,
            "product_price": self.product_price,
            "path_to_image": self.path_to_image
        }

class Scraper:
    """
    Scrapes product data from a website.
    """
    def __init__(self, base_url: str, proxy: Optional[str] = None):
        self.base_url = base_url
        self.proxy = proxy
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def retry_request(self, url: str, retries: int = 3, delay: int = 5) -> Optional[requests.Response]:
        """
        Makes a GET request with retries in case of failure.

        Args:
            url (str): The URL to fetch.
            retries (int): Number of retry attempts.
            delay (int): Delay between retries.

        Returns:
            Optional[requests.Response]: The response object or None if failed.
        """
        for attempt in range(retries):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    proxies={'http': self.proxy, 'https': self.proxy} if self.proxy else None
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                time.sleep(delay)
        logger.error(f"Failed to fetch {url} after {retries} attempts.")
        return None

    def scrape_page(self, page_number: int) -> List[Product]:
        """
        Scrapes a single page for product data.

        Args:
            page_number (int): The page number to scrape.

        Returns:
            List[Product]: A list of Product objects scraped from the page.
        """
        url = f"{self.base_url}page/{page_number}/"
        response = self.retry_request(url)
        if response is None:
            logger.error(f"Failed to retrieve page {page_number}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        response_data = soup.select("li.product")
        products = []

        for product in response_data:
            productName = product.select_one(".woo-loop-product__title a")
            productPrice = product.select_one(".price .woocommerce-Price-amount bdi")
            imageURL = product.select_one(".mf-product-thumbnail img")

            if check_missing_elements(page=page_number, productName=productName, productPrice=productPrice, imageURL=imageURL):
                logger.warning(f"Missing elements on page {page_number}. Skipping product.")
                continue

            productPrice = CleanData().price(productPrice)
            productName = CleanData().name(productName)
            imageURL = CleanData().image_url(imageURL)

            if check_missing_elements_after_conversion(page=page_number, productName=productName, productPrice=productPrice, imageURL=imageURL):
                logger.warning(f"Cleaned data missing required elements on page {page_number}. Skipping product.")
                continue

            if productName and productPrice and imageURL:
                product = Product(product_title=productName, product_price=productPrice, path_to_image=imageURL)
                products.append(product)
            else:
                logger.warning(f"One or more required fields are missing. Skipping product on page {page_number}.")

        logger.info(f"Scraped {len(products)} products from page {page_number}.")
        return products

    def scrape(self, pages: int) -> List[Product]:
        """
        Scrapes multiple pages for product data.

        Args:
            pages (int): The number of pages to scrape.

        Returns:
            List[Product]: A list of all products scraped across pages.
        """
        all_products = []
        for page in range(1, pages + 1):
            logger.info(f"Scraping page {page}...")
            products = self.scrape_page(page)
            all_products.extend(products)
            logger.info(f"Total products scraped after page {page}: {len(all_products)}")
        return all_products

    def save_to_json(self, products: List[Product], filename: str = 'scraped_data.json'):
        """
        Saves the scraped products to a JSON file.

        Args:
            products (List[Product]): List of products to save.
            filename (str): The file name to save the data.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([product.to_dict() for product in products], f, ensure_ascii=False, indent=4)
            logger.info(f"Saved {len(products)} products to {filename}.")
        except Exception as e:
            logger.error(f"Failed to save products to {filename}: {e}", exc_info=True)
