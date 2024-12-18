import json
import os
import logging
from typing import List
from .models import Product

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Storage:
    """
    Handles saving and loading of product data to and from a file.

    Attributes:
        file_path (str): Path to the file where product data will be saved.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_products(self, products: List[Product]):
        """
        Saves a list of products to a JSON file.

        Args:
            products (List[Product]): List of Product objects to save.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([product.to_dict() for product in products], f, ensure_ascii=False, indent=4)
            logger.info("Successfully saved %d products to %s", len(products), self.file_path)
        except Exception as e:
            logger.error("Failed to save products to %s: %s", self.file_path, e, exc_info=True)
            raise

    def load_products(self) -> List[Product]:
        """
        Loads products from the JSON file.

        Returns:
            List[Product]: A list of Product objects loaded from the file.
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    products = [Product(**prod) for prod in json.load(f)]
                    logger.info("Successfully loaded %d products from %s", len(products), self.file_path)
                    return products
            except json.JSONDecodeError as e:
                logger.error("Error decoding JSON from %s: %s", self.file_path, e, exc_info=True)
                raise
            except Exception as e:
                logger.error("Error loading products from %s: %s", self.file_path, e, exc_info=True)
                raise
        else:
            logger.warning("File %s does not exist. Returning an empty list.", self.file_path)
        return []
