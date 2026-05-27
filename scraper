import time
import random
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    RetryError,
)
import logging

from config import (
    REQUEST_DELAY_MIN,
    REQUEST_DELAY_MAX,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    USER_AGENTS,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def _get_headers() -> dict:
    """Rotate User-Agent on every request to reduce bot detection."""
    return {"User-Agent": random.choice(USER_AGENTS)}


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.exceptions.RequestException,)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def fetch_page(url: str) -> requests.Response:
    """
    Fetches a single URL with:
      - Rotating User-Agent headers
      - Automatic retry with exponential backoff (up to MAX_RETRIES attempts)
      - Timeout enforcement
      - HTTP error raising (4xx / 5xx become exceptions)
    """
    logger.debug("Fetching: %s", url)
    response = requests.get(url, headers=_get_headers(), timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response


def polite_delay():
    """Sleep a random amount between requests to avoid hammering the server."""
    delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
    logger.debug("Sleeping %.2f seconds...", delay)
    time.sleep(delay)
