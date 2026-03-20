# E-Commerce Data Scraper

A Python automation script designed to extract unstructured product data from an e-commerce storefront and transform it into a clean, structured CSV dataset for data analysis.

## Core Technologies Used
* **Python 3**
* **Requests Library:** Handled HTTP GET requests and User-Agent header spoofing to successfully connect to the target server.
* **BeautifulSoup 4 (bs4):** Parsed the DOM and extracted specific HTML nodes (titles, prices, and stock status) using class identifiers.
* **CSV Library:** Managed file I/O operations to dynamically generate and populate the output dataset.

## How It Works
1. The script connects to the target storefront url.
2. It downloads the raw HTML content of the page.
3. `BeautifulSoup` isolates the individual product containers.
4. The script iterates through the DOM structure, extracting the product name, listed price, and inventory availability.
5. The extracted data is immediately written to a locally generated `scraped_products.csv` file. 

## Future Enhancements
* Implementing pagination to scrape multiple pages of products automatically.
* Adding Pandas to clean the currency symbols from the price column before saving.
