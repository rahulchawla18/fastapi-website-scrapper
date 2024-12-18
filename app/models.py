from pydantic import BaseModel
from typing import Optional
from .config import Config

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeSettings(BaseModel):
    pages: Optional[int] = Config.DEFAULT_PAGES
    proxy: Optional[str] = None
