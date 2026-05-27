# 📚 Book Scraper

A production-grade web scraper for [books.toscrape.com](http://books.toscrape.com), built with professional software engineering practices.

## Features

- ✅ **Pagination** — follows all pages automatically
- ✅ **Retry logic** — exponential backoff on failed requests
- ✅ **Rotating User-Agents** — reduces bot detection
- ✅ **Rate limiting** — randomised delays between requests
- ✅ **Per-item error handling** — bad products are skipped, not crash-inducing
- ✅ **Dual storage** — saves to both CSV and SQLite database
- ✅ **Structured logging** — console + file logs with timestamps
- ✅ **Modular architecture** — clean separation of concerns
- ✅ **Unit tested** — pytest test suite for parsing logic

## Project Structure

```
scraper/
├── main.py            # Entry point — orchestrates the pipeline
├── scraper.py         # HTTP fetching with retry + rate limiting
├── parser.py          # HTML parsing logic
├── storage.py         # CSV and SQLite storage
├── config.py          # All settings in one place
├── utils/
│   └── logger.py      # Logging setup
├── tests/
│   └── test_parser.py # Unit tests (pytest)
├── requirements.txt
└── README.md
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the scraper
python main.py

# 4. Run tests
pytest tests/
```

## Output

| File | Description |
|---|---|
| `output/scraped_products.csv` | All scraped books in CSV format |
| `output/books.db` | SQLite database with timestamped records |
| `output/scraper.log` | Full debug log of the scraping session |

## Configuration

All settings live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `REQUEST_DELAY_MIN` | 1.5s | Minimum delay between requests |
| `REQUEST_DELAY_MAX` | 3.5s | Maximum delay between requests |
| `MAX_RETRIES` | 3 | Retry attempts on failure |
| `REQUEST_TIMEOUT` | 10s | Request timeout |
