from fastapi import FastAPI, HTTPException, Request
from .scraper import Scraper
from .models import ScrapeSettings
from .storage import Storage
from .config import Config
import logging

# Initialize the FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/scrape/")
async def scrape_products(settings: ScrapeSettings, request: Request):
    """
    Endpoint to scrape products from the specified number of pages.
    Requires an Authorization token in the request headers.

    Args:
        settings (ScrapeSettings): Scrape configuration including pages and optional proxy.
        request (Request): Incoming request object to extract headers.

    Returns:
        dict: A message indicating the number of products scraped and pages processed.
    """
    # Extract and validate the Authorization token
    token = request.headers.get('Authorization')
    if token != f"Bearer {Config.API_TOKEN}":
        logger.warning("Unauthorized access attempt with token: %s", token)
        raise HTTPException(status_code=403, detail="Unauthorized")

    logger.info("Starting the scraping process with settings: %s", settings)

    # Initialize the scraper with the base URL and proxy settings
    scraper = Scraper(base_url=Config.BASE_URL, proxy=settings.proxy)
    try:
        # Perform scraping for the specified number of pages
        products = scraper.scrape(pages=settings.pages)
        logger.info("Scraping completed. Total products scraped: %d", len(products))
    except Exception as e:
        logger.error("Error during scraping: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error during scraping")

    # Save scraped data to the storage (e.g., a JSON file)
    storage = Storage(file_path="scraped_data.json")
    try:
        storage.save_products(products)
        logger.info("Scraped data saved successfully to %s", storage.file_path)
    except Exception as e:
        logger.error("Error saving data to storage: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error saving data")

    # Return a response with scraping results
    message = f"Scraped {len(products)} products from {settings.pages} pages."
    logger.info(message)
    return {"message": message}
