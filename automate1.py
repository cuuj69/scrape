#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()
driver.get('https://uae.dubizzle.com/motors/used-cars/')

def wait_for_element_present(selector, timeout=11):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))


def change_filter_option(filter_name, new_value):
    try:
        # Click on the button to open the filter dropdown
        filter_button_xpath = '//*[@id="lpv-list"]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/button/div/div[2]/span[2]'
        filter_button = wait_for_element_present(filter_button_xpath)
        filter_button.click()

        # Wait for the input element to be present within the dropdown
        input_xpath = f'//div[contains(@data-testid, "{filter_name.lower()}-filter")]//input[@data-testid="{filter_name.lower()}_input"]'
        filter_input = wait_for_element_present(input_xpath)
        filter_input.clear()
        filter_input.send_keys(new_value)
        filter_input.send_keys(Keys.ENTER)

    except Exception as e:
        print(f"Error changing filter option for {filter_name}: {e}")


def extract_info_from_result(result_div):
    make = result_div.find_element(By.CSS_SELECTOR, 'div[data-testid="heading-text0"]').text
    model = result_div.find_element(By.CSS_SELECTOR, 'div[data-testid="heading-text-1"]').text
    price = result_div.find_element(By.CSS_SELECTOR, 'div[data-testid="listing-price"]').text

    print(f"Make: {make}, Model: {model}, Price: {price}")

def scrape_results():
    page_number = 2

    while True:
        try:
            # Wait for results to load
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div[type="primary"]'))
            WebDriverWait(driver, 11).until(element_present)
        except Exception as e:
            print(f"Timed out waiting for page {page_number} to load because of this {e}")

        # Extract information from each result div
        result_divs = driver.find_elements(By.CSS_SELECTOR, 'div[type="primary"]')
        for result_div in result_divs:
            extract_info_from_result(result_div)

        # Check if there is a next page
        next_page_button = driver.find_element(By.CSS_SELECTOR, 'button[type="next"]')
        if next_page_button.is_enabled():
            # Click the next page button
            next_page_button.click()
            page_number += 2
        else:
            # No more pages, break the loop
            break

# Change filter options before scraping results
change_filter_option('City', 'All Cities')
change_filter_option('Make', 'Mercedes-Benz')
change_filter_option('Model','S-Class')


# Click the "Filter" button to apply the changes
#filter_button = wait_for_element_present('div.filterbar button')
#filter_button.click()

# Scrape results from all pages
scrape_results()

# Close the browser
driver.quit()
