import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find('div', {'id': 'productDescription'})
    description = description.get_text(strip=True).replace('\n', '') if description else "N/A"

    asin = soup.find('th', string='ASIN')
    asin = asin.find_next('td').get_text(strip=True) if asin else "N/A"

    product_description = soup.find('div', {'id': 'productDescription'})
    product_description = product_description.get_text(strip=True).replace('\n', '') if product_description else "N/A"

    manufacturer = soup.find('th', string='Manufacturer')
    manufacturer = manufacturer.find_next('td').get_text(strip=True) if manufacturer else "N/A"

    return description, asin, product_description, manufacturer

def scrape_product_pages(product_data):
    all_data = []
    for product in product_data:
        product_url = product[0]
        print(f"Processing Product: {product_url}")
        description, asin, product_description, manufacturer = scrape_product_page(product_url)
        all_data.append([product_url, description, asin, product_description, manufacturer])
        time.sleep(1)  # Add a delay of 1 second between each request

    return all_data

def export_to_csv(data, filename):
    headers = ['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer']

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

product_listings_file = 'product_listings.csv'
product_details_file = 'product_details.csv'

# Read the product listings from Part 1
product_data = []
with open(product_listings_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    product_data = list(reader)

print("Scraping product details...")
scraped_data = scrape_product_pages(product_data)
print("Scraping completed!")

export_to_csv(scraped_data, product_details_file)
