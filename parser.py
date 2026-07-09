from bs4 import BeautifulSoup
from typing import Optional
from dataclasses import dataclass

from utils.logger import get_logger

logger = get_logger(__name__)

# More readable than dictionary and also supports error handling
@dataclass
class Book:
    """Represents a single scraped book product."""
    name: str
    price: str
    availability: str


def parse_books(html: str) -> list[Book]:
    """
    Parses all book products from a page's HTML.
    Skips malformed entries individually — one bad product
    won't crash the entire scrape.
    """
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    logger.info("Found %d products on page.", len(products))

    books = []
    for i, product in enumerate(products):
        book = _parse_single_product(product, index=i)
        if book:
            books.append(book)

    logger.info("Successfully parsed %d / %d products.", len(books), len(products))
    return books


def _parse_single_product(product, index: int) -> Optional[Book]:
    """
    Extracts name, price, and availability from a single product card.
    Returns None and logs a warning if any field is missing.
    """
    try:
        name = product.h3.a["title"]
        price = product.find("p", class_="price_color").text.strip()
        stock_tag = product.find("p", class_="instock availability")
        availability = stock_tag.text.strip() if stock_tag else "Unknown"

        return Book(name=name, price=price, availability=availability)

    except (AttributeError, TypeError, KeyError) as e:
        logger.warning("Skipping product at index %d due to error: %s", index, e)
        return None


def get_next_page_url(html: str, base_url: str) -> Optional[str]:
    """
    Finds the 'next' pagination button and returns the full URL.
    Returns None if we're on the last page.
    """
    soup = BeautifulSoup(html, "html.parser")
    next_btn = soup.find("li", class_="next")

    if not next_btn:
        logger.info("No next page found — reached the last page.")
        return None

    next_href = next_btn.a["href"]
    # The href is relative to the current category path
    next_url = base_url.rsplit("/", 1)[0] + "/" + next_href
    logger.debug("Next page URL: %s", next_url)
    return next_url
