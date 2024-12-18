# fastapi-website-scrapper
A robust web scrapper built with FastAPI that extracts product information (titles, prices, and image URLs) from e-commerce websites and saves the data in a JSON file. This scraper is designed to handle multiple pages, logging, and error handling seamlessly.

# Features
- Scalable Web Scrapper: Scrape product data from multiple pages of an e-commerce site.
- Robust Error Handling: Detects and skips incomplete or missing product details with clear logging.
- Proxy Support: Optional proxy configuration for secure and controlled web scraping.
- Data Storage: Saves scraped data in a structured JSON format for easy usage and analysis.
- Retry Logic: Automatically retries failed requests to ensure consistent scraping.

# Requirements/ Prerequisites
- Python 3.7+
- FastAPI
- BeautifulSoup (bs4)
- Requests

# Installation
- Clone the repository:
  git clone https://github.com/your-username/fastapi-website-scrapper.git
  cd fastapi-website-scrapper

- Create a virtual environment and activate it:
  python -m venv myenv
  On Windows: myenv\Scripts\activate

- Install the dependencies:
  pip install -r requirements.txt
  (Optional) Set up a .env file with sensitive data

# Running the Application
- Start the FastAPI server:
  uvicorn app.main:app --reload

- The API will be available at:
  http://127.0.0.1:8000

- API Endpoints:
  /scrape/ (POST)
  Description: Initiates the scraping process for a given number of pages.
  Headers:
    Authorization: Bearer token to secure the endpoint.
    Request Body:
     {
       "pages": 5,
       "proxy": "http://your-proxy-url:port"
     }
      pages: Number of pages to scrape.
      proxy: (Optional) Proxy URL for web requests.
    Response:
     {
       "message": "Scraped 50 products from 5 pages."
     }
    
# Logging
- Logs are generated during the scraping process to help debug issues.
- Default logging levels are INFO and WARNING. Update logging.basicConfig() in the code to customize levels.
- Logs can optionally be saved to a file by modifying the logger configuration.

# Troubleshooting
- 403 Unauthorized:
  Ensure the Authorization header matches Config.API_TOKEN.
  Check for typos in the token.

- AttributeError:
  Verify that the target website's structure matches the selectors in scraper.py.

- Proxy Issues:
  Confirm your proxy is active and correctly configured.