"""
Unit tests for parser.py

Run with:  pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from bs4 import BeautifulSoup
from parser import parse_books, get_next_page_url, _parse_single_product


# ─────────────────────────────────────────────
# Fixtures — reusable mock HTML fragments
# ─────────────────────────────────────────────

VALID_PRODUCT_HTML = """
<article class="product_pod">
    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html"
           title="A Light in the Attic">A Light in the Attic</a></h3>
    <p class="price_color">£51.77</p>
    <p class="instock availability">In stock</p>
</article>
"""

MISSING_PRICE_HTML = """
<article class="product_pod">
    <h3><a href="catalogue/some-book/index.html" title="Some Book">Some Book</a></h3>
    <p class="instock availability">In stock</p>
</article>
"""

MISSING_STOCK_HTML = """
<article class="product_pod">
    <h3><a href="catalogue/some-book/index.html" title="Some Book">Some Book</a></h3>
    <p class="price_color">£10.00</p>
</article>
"""

PAGE_WITH_NEXT = """
<ul class="pager">
    <li class="next"><a href="page-2.html">next</a></li>
</ul>
"""

PAGE_WITHOUT_NEXT = """
<ul class="pager">
    <li class="previous"><a href="page-1.html">previous</a></li>
</ul>
"""


# ─────────────────────────────────────────────
# Tests: _parse_single_product
# ─────────────────────────────────────────────

def get_product_tag(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("article", class_="product_pod")


def test_parse_valid_product():
    product = get_product_tag(VALID_PRODUCT_HTML)
    book = _parse_single_product(product, index=0)
    assert book is not None
    assert book.name == "A Light in the Attic"
    assert book.price == "£51.77"
    assert book.availability == "In stock"


def test_parse_missing_price_returns_none():
    product = get_product_tag(MISSING_PRICE_HTML)
    book = _parse_single_product(product, index=0)
    assert book is None


def test_parse_missing_stock_uses_unknown():
    product = get_product_tag(MISSING_STOCK_HTML)
    book = _parse_single_product(product, index=0)
    assert book is not None
    assert book.availability == "Unknown"


# ─────────────────────────────────────────────
# Tests: parse_books (full page)
# ─────────────────────────────────────────────

def test_parse_books_returns_list():
    full_page = f"<html><body>{VALID_PRODUCT_HTML}</body></html>"
    books = parse_books(full_page)
    assert isinstance(books, list)
    assert len(books) == 1


def test_parse_books_skips_malformed():
    full_page = f"<html><body>{VALID_PRODUCT_HTML}{MISSING_PRICE_HTML}</body></html>"
    books = parse_books(full_page)
    assert len(books) == 1  # only the valid one


def test_parse_books_empty_page():
    books = parse_books("<html><body></body></html>")
    assert books == []


# ─────────────────────────────────────────────
# Tests: get_next_page_url
# ─────────────────────────────────────────────

def test_next_page_found():
    base = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    url = get_next_page_url(PAGE_WITH_NEXT, base)
    assert url is not None
    assert "page-2.html" in url


def test_no_next_page_returns_none():
    base = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    url = get_next_page_url(PAGE_WITHOUT_NEXT, base)
    assert url is None
