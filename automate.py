#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Import Service class
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

import time

dubizzle_base_url = 'https://uae.dubizzle.com/motors/used-cars'

# Start a new browser session (make sure to have the appropriate driver installed, e.g., chromedriver)
driver = webdriver.Firefox()

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

dubizzle_url = dubizzle_base_url

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



driver.get(dubizzle_url)  # Fix the variable name here
time.sleep(60)

