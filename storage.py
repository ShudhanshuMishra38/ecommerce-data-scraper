import csv
import sqlite3
import os
from typing import List

from parser import Book
from config import OUTPUT_CSV, OUTPUT_DB
from utils.logger import get_logger

logger = get_logger(__name__)


# ─────────────────────────────────────────────
# CSV Storage
# ─────────────────────────────────────────────

def save_to_csv(books: List[Book], filepath: str = OUTPUT_CSV) -> None:
    """
    Appends book records to a CSV file.
    Creates the file with a header row if it doesn't exist yet.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Product_Name", "Price", "Availability"])
            logger.debug("Created new CSV file: %s", filepath)

        for book in books:
            writer.writerow([book.name, book.price, book.availability])

    logger.info("Saved %d records to CSV: %s", len(books), filepath)


# ─────────────────────────────────────────────
# SQLite Storage
# ─────────────────────────────────────────────

def _get_connection(db_path: str = OUTPUT_DB) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def init_db(db_path: str = OUTPUT_DB) -> None:
    """Creates the books table if it doesn't already exist."""
    with _get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                price        TEXT,
                availability TEXT,
                scraped_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    logger.debug("Database initialised: %s", db_path)


def save_to_db(books: List[Book], db_path: str = OUTPUT_DB) -> None:
    """
    Inserts book records into the SQLite database.
    Uses executemany for efficiency.
    """
    init_db(db_path)
    rows = [(b.name, b.price, b.availability) for b in books]

    with _get_connection(db_path) as conn:
        conn.executemany(
            "INSERT INTO books (name, price, availability) VALUES (?, ?, ?)", rows
        )
        conn.commit()

    logger.info("Saved %d records to DB: %s", len(books), db_path)
