import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_listing_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in product_list:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        product_name = product_name.get_text(strip=True) if product_name else "N/A"
        product_price = product.find('span', {'class': 'a-offscreen'})
        product_price = product_price.get_text(strip=True) if product_price else "N/A"
        rating = product.find('span', {'class': 'a-icon-alt'})
        rating = rating.get_text(strip=True) if rating else "N/A"
        review_count = product.find('span', {'class': 'a-size-base'})
        review_count = review_count.get_text(strip=True) if review_count else "N/A"

        data.append([product_url, product_name, product_price, rating, review_count])

    return data

def scrape_multiple_pages(base_url, num_pages):
    all_data = []
    for page in range(1, num_pages+1):
        url = f"{base_url}&page={page}"
        print(f"Processing Page {page}: {url}")
        data = scrape_listing_page(url)
        all_data.extend(data)
        time.sleep(1)  # Add a delay of 1 second between each request

    return all_data

def export_to_csv(data, filename):
    headers = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
num_pages = 20

print("Scraping Amazon product listings...")
scraped_data = scrape_multiple_pages(base_url, num_pages)
print("Scraping completed!")

export_to_csv(scraped_data, 'product_listings.csv')
