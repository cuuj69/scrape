from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

dubizzle_base_url = 'https://uae.dubizzle.com'
chrome_url = 'C:\Development\chromedriver.exe'

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

print(dubizzle_url)

# Start a new browser session (make sure to have the appropriate driver installed, e.g., chromedriver)
# driver = webdriver.Firefox()
driver = webdriver.Chrome(service=Service(executable_path=chrome_url))

# Navigate to the URL
driver.get(dubizzle_url)
time.sleep(5)  # Allow time for the page to load, you might need to adjust this

# Get the page source
page_source = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all divs that contain relevant information based on their unique div class name
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

    # Extract text content from the found elements
    price = price_element.get_text() if price_element else 'N/A'
    year = year_element.get_text() if year_element else 'N/A'
    kilometers = kilometers_element.get_text() if kilometers_element else 'N/A'
    features = features_element.get_text() if features_element else 'N/A'
    location = location_element.get_text() if location_element else 'N/A'
    product_make = make_element.get_text() if make_element else 'N/A'
    product_model = model_element.get_text() if model_element else 'N/A'

    #due to how url is presented, dubizzle_base_url had to be changed in order to reuse it.
    url = url_element.get('href') if url_element else 'N/A'

    # Print the extracted information

    print(f'{year} {product_make} {product_model}')
    print(f'Price: {price}')
    # print(f'Year: {year}')
    print(f'Mileage: {kilometers}')
    print(f'Features: {features}')
    print(f'Location: {location}')

    # new dubizzle_base_url is used here
    print(f'Check it Out: {dubizzle_base_url}{url}')
    print('-' * 50)

# Close the browser
driver.quit()

