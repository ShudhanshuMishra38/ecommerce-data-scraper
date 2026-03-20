import requests
from bs4 import BeautifulSoup
import csv

def scrape_ecommerce_data():
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    headers = {"User-Agent": "Mozilla/5.0"} 
    print("Connecting to the server...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return
      
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all("article", class_="product_pod")
    print("Extracting data...")
    with open("scraped_products.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Product_Name", "Price", "Availability"]) 
        
        for product in products:
            name = product.h3.a["title"]
            price_container = product.find("p", class_="price_color")
            price = price_container.text.strip()
            stock_container = product.find("p", class_="instock availability")
            stock = stock_container.text.strip()
            writer.writerow([name, price, stock])
            
    print("\nSuccess! Data successfully saved to scraped_products.csv")

if __name__ == "__main__":
    scrape_ecommerce_data()
