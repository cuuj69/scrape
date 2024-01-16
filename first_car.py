import math
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

dubizzle_base_url = 'https://uae.dubizzle.com'
chrome_url = r'C:\Development\chromedriver.exe'

# Get user's input and store them within variables
city = ''
make = 'Mercedes-Benz'
model = 'C-Class'
price1 = '1'
price2 = '500000'
year1 = '1920'
year2 = '2025'
kilos1 = '0'
kilos2 = '100000'

features = [make, model]

dubizzle_url = dubizzle_base_url + '/motors/used-cars'

for feature in features:
    if feature != '':
        dubizzle_url += f'/{feature.lower()}/?'

filters = [price1, price2, year1, year2, kilos1, kilos2]

if filters[0] and filters[1] != '':
    dubizzle_url += f'price__gte={filters[0]}&price__lte={filters[1]}'

if filters[2] != '':
    dubizzle_url += f'&year__gte={filters[2]}'

if filters[5] != '':
    dubizzle_url += f'&kilometers__lte={filters[5]}'

if filters[3] != '':
    dubizzle_url += f'&year__lte={filters[3]}'

if filters[4] != '':
    dubizzle_url += f'&kilometers__gte={filters[4]}'

# print(dubizzle_url)
usable_url = dubizzle_url
# Start a new browser session (make sure to have the appropriate driver installed, e.g., chromedriver)
# driver = webdriver.Firefox() # this is your line for firefox enable it and disable the next line
driver = webdriver.Chrome(service=Service(executable_path=chrome_url))

# Navigate to the URL
driver.get(dubizzle_url)
time.sleep(5)  # Allow time for the page to load, you might need to adjust this

# Get the page source
page_source = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Calculate number of pages
# Fetch the number of results obtained and divide it by 25 items per page
total_listings_element = soup.find('span', {'class': 'sc-eTqNBC OMyRU'})
total_listings_string = total_listings_element.get_text() if total_listings_element else 'N/A'
total_listings = int(''.join(char for char in total_listings_string if char.isdigit()))
print(total_listings)
pages = math.ceil(total_listings / 25)

# clear the results.txt before a new search.
csv_headers = ['Name', 'Price', 'Mileage', 'Features', 'Location', 'Link', 'Picture1', 'Picture2', 'Picture3',
               'Picture4', 'Picture5', 'Picture6', 'Picture7', 'Picture8', 'Picture9', 'Picture10', 'Picture11',
               'Picture12', 'Picture13', 'Picture14', 'Picture15', 'Picture16', 'Picture17', 'Picture18', 'Picture19',
               'Picture20', 'Picture21', 'Picture22', 'Picture23', 'Picture24', 'Picture25'
               ]

with open('results.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(csv_headers)

driver.quit()

for page in range(1, pages + 1):
    if page == 1:
        new_dubizzle_url = usable_url
    else:
        new_dubizzle_url = usable_url + f'&page={page}'
    # Start a new browser session (make sure to have the appropriate driver installed, e.g., chromedriver)
    # driver = webdriver.Firefox() # this is your line for firefox enable it and disable the next line
    driver = webdriver.Chrome(service=Service(executable_path=chrome_url))
    print(new_dubizzle_url)
    # Navigate to the URL
    driver.get(new_dubizzle_url)
    time.sleep(5)  # Allow time for the page to load, you might need to adjust this

    # Get the page source
    page_source = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    # soup = BeautifulSoup(page_source, 'lxml')
    # print(soup)
# ------------------------------ FIRST CAR ------------------------------------------------------------
    # Find all divs that contain relevant information based on their unique div class name
    first_car_div = soup.find('div', {'class': 'sc-kdBSHD kZEvWp dbz-ads-listing'})

    # Extract specific information from each car_div
    price_element = first_car_div.find('div', {'data-testid': 'listing-price'})
    year_element = first_car_div.find('div', {'data-testid': 'listing-year'})
    kilometers_element = first_car_div.find('div', {'data-testid': 'listing-kms'})

    make_element = first_car_div.find('div', {'data-testid': 'heading-text-1'})
    model_element = first_car_div.find('div', {'data-testid': 'heading-text-2'})

    features_element = first_car_div.find('h2', {'data-testid': 'subheading-text'})
    url_element = first_car_div.find('a', {'class': 'sc-tagGq sc-esYiGF wjsGY cocqIi'})
    # Find the location element using their unique class name
    location_element = first_car_div.find('div', {'class': 'sc-dZoequ lcDjpD'})
    # location_element = first_car_div.find(By.CLASS_NAME, '')
    # Find images url
    image_divs = first_car_div.find_all('div', {'class': 'sc-kzqdkY knYQNn'})

    # Number of images
    # Only 4 images live on the actual page. the rest of the images are available through the product url.
    image_tags = [div.find('img') for div in image_divs]
    images = [img['src'] for img in image_tags]

    # Extract text content from the found elements
    price = price_element.get_text() if price_element else 'N/A'
    year = year_element.get_text() if year_element else 'N/A'
    kilometers = kilometers_element.get_text() if kilometers_element else 'N/A'
    features = features_element.get_text() if features_element else 'N/A'
    location = location_element.get_text() if location_element else 'N/A'
    product_make = make_element.get_text() if make_element else 'N/A'
    product_model = model_element.get_text() if model_element else 'N/A'

    # due to how url is presented, dubizzle_base_url had to be changed in order to reuse it.
    product_url = url_element.get('href') if url_element else 'N/A'

    information = []
    if images:
        # Convert elements to strings and join them with commas
        image_urls = images
    else:
        image_urls = []

        information = [
                      f'{year} {product_make} {product_model}',
                      f'{price}',
                      f'{kilometers}',
                      f'{features}', f'{location}',
                      f'{dubizzle_base_url}{product_url}'
                  ] + image_urls

    with open('results.csv', 'a+', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(information)

    print('first car printed')

# -------------------------------------- OTHER CARS -------------------------------------------------

    car_listing_divs = soup.find_all('div', {'class': 'lpv-card-appear-done lpv-card-enter-done'})

    for car_div in car_listing_divs:
        # Extract specific information from each car_div
        price_element = car_div.find('div', {'data-testid': 'listing-price'})
        year_element = car_div.find('div', {'data-testid': 'listing-year'})
        kilometers_element = car_div.find('div', {'data-testid': 'listing-kms'})

        make_element = car_div.find('div', {'data-testid': 'heading-text-1'})
        model_element = car_div.find('div', {'data-testid': 'heading-text-2'})

        features_element = car_div.find('h2', {'data-testid': 'subheading-text'})
        url_element = car_div.find('a', {'class': 'sc-tagGq sc-esYiGF wjsGY cocqIi'})
        # Find the location element using their unique class name
        location_element = car_div.find('div', {'class': 'sc-dZoequ lcDjpD'})

        # Find images url
        image_divs = car_div.find_all('img')

        # Number of images
        # use this number to remove other images that are not car images.
        image_number_element = car_div.find('span', {'class': 'css-v1rqhp'})
        image_number = int(image_number_element.text.strip())

        images = [img['src'] for img in image_divs]
        # reduce the list of images to exclude unwanted images
        images = images[:image_number]

        # Extract text content from the found elements
        price = price_element.get_text() if price_element else 'N/A'
        year = year_element.get_text() if year_element else 'N/A'
        kilometers = kilometers_element.get_text() if kilometers_element else 'N/A'
        features = features_element.get_text() if features_element else 'N/A'
        location = location_element.get_text() if location_element else 'N/A'
        product_make = make_element.get_text() if make_element else 'N/A'
        product_model = model_element.get_text() if model_element else 'N/A'

        # due to how url is presented, dubizzle_base_url had to be changed in order to reuse it.
        product_url = url_element.get('href') if url_element else 'N/A'

        if images:
            # Convert elements to strings and join them with commas
            image_urls = images
        else:
            image_urls = []

        information = [
                          f'{year} {product_make} {product_model}',
                          f'{price}',
                          f'{kilometers}',
                          f'{features}', f'{location}',
                          f'{dubizzle_base_url}{product_url}'
                      ] + image_urls

        with open('results.csv', 'a+', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(information)

    print(f'page {page} written')

    # Close the browser
    driver.quit()
