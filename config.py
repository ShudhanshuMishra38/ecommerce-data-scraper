#Single source of truth principle
import os
from dotenv import load_dotenv

load_dotenv()

# --- Target ---
BASE_URL = "http://books.toscrape.com"
START_URL = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"

# --- Request Settings ---
REQUEST_DELAY_MIN = 1.5   
REQUEST_DELAY_MAX = 3.5    
REQUEST_TIMEOUT   = 10    
MAX_RETRIES       = 3     # how many times to retry a failed request

# --- Output ---
OUTPUT_CSV = "output/scraped_products.csv"
OUTPUT_DB  = "output/books.db"
LOG_FILE   = "output/scraper.log"

# --- User-Agent Rotation ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]
