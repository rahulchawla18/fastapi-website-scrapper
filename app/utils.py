import logging
import time
from typing import List, Optional
from bs4.element import Tag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CleanData:
    """
    Class to clean and extract data from HTML elements.
    """
    @staticmethod
    def price(price: Tag) -> float:
        """
        Extracts and converts the price from a Tag element.

        Args:
            price (Tag): HTML element containing the price.

        Returns:
            float: Cleaned and converted price.
        """
        try:
            cleaned_price = float(price.text.replace("₹", "").replace(" ", ""))
            logger.debug("Extracted price: %s", cleaned_price)
            return cleaned_price
        except (ValueError, AttributeError) as e:
            logger.error("Failed to extract price: %s", e, exc_info=True)
            return 0.0

    @staticmethod
    def name(name: Tag) -> str:
        """
        Extracts the product name from a Tag element.

        Args:
            name (Tag): HTML element containing the product name.

        Returns:
            str: Cleaned product name.
        """
        try:
            cleaned_name = name.text.strip()
            logger.debug("Extracted name: %s", cleaned_name)
            return cleaned_name
        except AttributeError as e:
            logger.error("Failed to extract name: %s", e, exc_info=True)
            return ""

    @staticmethod
    def image_url(image: Tag) -> Optional[str]:
        """
        Extracts the image URL from a Tag element.

        Args:
            image (Tag): HTML element containing the image.

        Returns:
            Optional[str]: Cleaned image URL.
        """
        try:
            image_url = str(image.get("data-lazy-src"))
            logger.debug("Extracted image URL: %s", image_url)
            return image_url
        except AttributeError as e:
            logger.error("Failed to extract image URL: %s", e, exc_info=True)
            return None


def check_missing_elements(page, productName, productPrice, imageURL) -> bool:
    """
    Checks if any of the required elements (name, price, image URL) are missing.

    Args:
        page (int): Page number being processed.
        productName (Tag): HTML element for the product name.
        productPrice (Tag): HTML element for the product price.
        imageURL (Tag): HTML element for the product image URL.

    Returns:
        bool: True if any required elements are missing, False otherwise.
    """
    missing_elements = []
    if not productName:
        missing_elements.append("Title")
    if not productPrice:
        missing_elements.append("Price")
    if not imageURL:
        missing_elements.append("Image")
    if missing_elements:
        if len(missing_elements) == 3:
            logger.warning(
                "Skipping product on page %d due to all elements missing: %s", 
                page, ", ".join(missing_elements)
            )
        else:
            logger.warning(
                "Skipping product on page %d due to missing elements: %s", 
                page, ", ".join(missing_elements)
            )
        return True
    return False


def check_missing_elements_after_conversion(page, productName, productPrice, imageURL) -> bool:
    """
    Checks if any required elements are missing after data extraction and conversion.

    Args:
        page (int): Page number being processed.
        productName (str): Extracted product name.
        productPrice (float): Extracted product price.
        imageURL (str): Extracted product image URL.

    Returns:
        bool: True if any required elements are missing after conversion, False otherwise.
    """
    missing_elements = []
    if not productName:
        missing_elements.append("Title")
    if not productPrice:
        missing_elements.append("Price")
    if not imageURL:
        missing_elements.append("Image")
    if missing_elements:
        if len(missing_elements) == 3:
            logger.warning(
                "Skipping product on page %d due to data extraction and type conversion issues: "
                "All expected elements missing: %s", 
                page, ", ".join(missing_elements)
            )
        else:
            logger.warning(
                "Skipping product on page %d due to data extraction and type conversion issues: "
                "Missing elements: %s", 
                page, ", ".join(missing_elements)
            )
        return True
    return False
