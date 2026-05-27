"""
main.py — Entry point for the book scraper.

Pipeline:
  1. Fetch page HTML (with retry + backoff)
  2. Parse all book products from the page
  3. Save results to both CSV and SQLite DB
  4. Follow pagination to the next page and repeat
  5. Stop when no next page is found
"""

from scraper import fetch_page, polite_delay
from parser import parse_books, get_next_page_url
from storage import save_to_csv, save_to_db
from config import START_URL
from utils.logger import get_logger

logger = get_logger(__name__)


def run():
    logger.info("=" * 50)
    logger.info("Scraper started.")
    logger.info("=" * 50)

    url = START_URL
    total_books = 0
    page_num = 1

    while url:
        logger.info("── Scraping page %d: %s", page_num, url)

        try:
            response = fetch_page(url)
        except Exception as e:
            logger.error("Failed to fetch page %d after all retries: %s", page_num, e)
            break

        html = response.text

        # Parse products from current page
        books = parse_books(html)

        if books:
            save_to_csv(books)
            save_to_db(books)
            total_books += len(books)
        else:
            logger.warning("No books parsed on page %d.", page_num)

        # Find next page URL (returns None on last page)
        next_url = get_next_page_url(html, url)
        url = next_url
        page_num += 1

        # Be polite — don't hammer the server
        if url:
            polite_delay()

    logger.info("=" * 50)
    logger.info("Scrape complete. Total books saved: %d", total_books)
    logger.info("=" * 50)


if __name__ == "__main__":
    run()
