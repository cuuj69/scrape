import math
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def get_browser():
    # Start a new browser session (make sure to have the appropriate driver installed, e.g., chromedriver)
    return webdriver.Chrome(service=Service(executable_path=chrome_url))

def get_page_source(driver, url, sleep_time=5):
    # Navigate to the URL
    driver.get(url)
    time.sleep(sleep_time)  # Allow time for the page to load, you might need to adjust this
    return driver.page_source

def parse_html(source):
    # Parse the HTML using BeautifulSoup
    return BeautifulSoup(source, 'html.parser')

def get_total_listings(soup):
    # Calculate the number of pages
    total_listings_element = soup.find('span', {'class': 'sc-eTqNBC OMyRU'})
    total_listings_string = total_listings_element.get_text() if total_listings_element else 'N/A'
    return int(''.join(char for char in total_listings_string if char.isdigit()))

def calculate_pages(total_listings):
    # Calculate the number of pages based on 25 items per page
    return math.ceil(total_listings / 25)

def write_to_csv(file_path, csv_headers, information):
    # Write information to CSV file
    with open(file_path, 'a+', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(information)

def process_car_div(car_div, dubizzle_base_url):
    # Extract specific information from each car_div
    price_element = car_div.find('div', {'data-testid': 'listing-price'})
    year_element = car_div.find('div', {'data-testid': 'listing-year'})
    kilometers_element = car_div.find('div', {'data-testid': 'listing-kms'})
    make_element = car_div.find('div', {'data-testid': 'heading-text-1'})
    model_element = car_div.find('div', {'data-testid': 'heading-text-2'})
    features_element = car_div.find('h2', {'data-testid': 'subheading-text'})
    url_element = car_div.find('a', {'class': 'sc-tagGq sc-esYiGF wjsGY cocqIi'})
    location_element = car_div.find('div', {'class': 'sc-dZoequ lcDjpD'})
    image_divs = car_div.find_all('img')
    image_number_element = car_div.find('span', {'class': 'css-v1rqhp'})
    image_number = int(image_number_element.text.strip())
    images = [img['src'] for img in image_divs][:image_number]

    price = price_element.get_text() if price_element else 'N/A'
    year = year_element.get_text() if year_element else 'N/A'
    kilometers = kilometers_element.get_text() if kilometers_element else 'N/A'
    features = features_element.get_text() if features_element else 'N/A'
    location = location_element.get_text() if location_element else 'N/A'
    product_make = make_element.get_text() if make_element else 'N/A'
    product_model = model_element.get_text() if model_element else 'N/A'
    product_url = url_element.get('href') if url_element else 'N/A'

    return [
        f'{year} {product_make} {product_model}',
        f'{price}',
        f'{kilometers}',
        f'{features}',
        f'{location}',
        f'{dubizzle_base_url}{product_url}'
    ] + images

def process_page(driver, usable_url, dubizzle_base_url):
    # Get the page source
    page_source = get_page_source(driver, usable_url)
    # Parse the HTML using BeautifulSoup
    soup = parse_html(page_source)

    # Process the first car separately
    first_car_div = soup.find('div', {'class': 'sc-kdBSHD kZEvWp dbz-ads-listing'})
    process_first_car(first_car_div, dubizzle_base_url)

    # Process other cars
    car_listing_divs = soup.find_all('div', {'class': 'lpv-card-appear-done lpv-card-enter-done'})
    for car_div in car_listing_divs:
        information = process_car_div(car_div, dubizzle_base_url)
        write_to_csv('results.csv', csv_headers, information)

def process_first_car(first_car_div, dubizzle_base_url):
    # Extract specific information from the first car_div
    price_element = first_car_div.find('div', {'data-testid': 'listing-price'})
    year_element = first_car_div.find('div', {'data-testid': 'listing-year'})
    kilometers_element = first_car_div.find('div', {'data-testid': 'listing-kms'})
    make_element = first_car_div.find('div', {'data-testid': 'heading-text-1'})
    model_element = first_car_div.find('div', {'data-testid': 'heading-text-2'})
    features_element = first_car_div.find('h2', {'data-testid': 'subheading-text'})
    url_element = first_car_div.find('a', {'class': 'sc-tagGq sc-esYiGF wjsGY cocqIi'})
    location_element = first_car_div.find('div', {'class': 'sc-dZoequ lcDjpD'})
    image_divs = first_car_div.find_all('div', {'class': 'sc-kzqdkY knYQNn'})

    # Number of images
    # Only 4 images live on the actual page. the rest of the images are available through the product url.
    image_tags = [div.find('img') for div in image_divs]
    images = [img['src'] for img in image_tags]

    price = price_element.get_text() if price_element else 'N/A'
    year = year_element.get_text() if year_element else 'N/A'
    kilometers = kilometers_element.get_text() if kilometers_element else 'N/A'
    features = features_element.get_text() if features_element else 'N/A'
    location = location_element.get_text() if location_element else 'N/A'
    product_make = make_element.get_text() if make_element else 'N/A'
    product_model = model_element.get_text() if model_element else 'N/A'

    # due to how url is presented, dubizzle_base_url had to be changed in order to reuse it.
    product_url = url_element.get('href') if url_element else 'N/A'

    information = [
        f'{year} {product_make} {product_model}',
        f'{price}',
        f'{kilometers}',
        f'{features}',
        f'{location}',
        f'{dubizzle_base_url}{product_url}'
    ] + images

    write_to_csv('results.csv', csv_headers, information)

if __name__ == "__main__":
    # Your existing code to set up the URLs, filters, etc.

    # Initialize browser
    driver = get_browser()

    # Process the initial page
    process_page(driver, usable_url, dubizzle_base_url)

    # Calculate the number of pages
    total_listings = get_total_listings(parse_html(get_page_source(driver, usable_url)))
    pages = calculate_pages(total_listings)

    # Process remaining pages
    for page in range(2, pages + 1):
        new_dubizzle_url = usable_url + f'&page={page}'
        process_page(driver, new_dubizzle_url, dubizzle_base_url)

    # Close the browser
    driver.quit()
