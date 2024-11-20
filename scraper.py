##Install requests and Beautifulsoup for scraping to fetch and parse HTML
## requests allows you to make an HTTP request
## returns the data in a parse tree that you can then parse through by what you are searching for


##pip install requests
##If scraping a site that uses javascript or any scripts, you will need to use selenium
#pip install selenium
import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'

def get_data(url):
    # Define the ChromeDriver path
    chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'

    # Set up the Service and Options
    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    driver.get(url)

    try:
        # Wait for the elements to be present (adjust the element selectors to your needs)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-grid__items"))
        )

        # For example, let's extract product names and prices
        product_names = driver.find_elements(By.CLASS_NAME, "product-card__title")
        product_prices = driver.find_elements(By.CLASS_NAME, "product-price")
        product_links = driver.find_elements(By.CLASS_NAME, "product-card__img-link-overlay")

        # Create a dictionary to store product name and price
        product_data = {}
        for i, name in enumerate(product_names):
            # Get the href value from the <a> tag
            href = product_links[i].get_attribute('href')  # Grabbing the href attribute
            product_data[name.text] = {
                'price': product_prices[i].text,
                'href': href
            }

        return product_data  # Return the product data as a dictionary

    except Exception as e:
        print(f"Error: {e}")
        return {}

    finally:
        driver.quit()


def check_change(url, old_data_file='old_data.json'):
    new_data = get_data(url)
    if not new_data:  # If no data is fetched, skip the comparison
        return False

    try:
        # Open the old data file and read the previous data
        with open(old_data_file, 'r') as f:
            old_data = json.load(f)  # Use json.load to read the data

        # Compare the new data with the old data
        changes = []
        for product, data in new_data.items():
            if product not in old_data or old_data[product] != data:
                changes.append(f"{product} - {data['price']} - {data['href']}")

        if changes:
            # If there are any changes, update the file and return the changes
            with open(old_data_file, 'w') as f:
                json.dump(new_data, f)  # Use json.dump to safely write the data
            return changes  # Return the list of changes
        else:
            print("No changes detected.")
            return []

    except FileNotFoundError:
        # If the file doesn't exist, create it and write the current data
        with open(old_data_file, 'w') as f:
            json.dump(new_data, f)
        print("First time run, saving data.")
        return []


def send_noti(message):
    bot_token = '7629797667:AAHKli_4cr7SKNKw6L4Iq00N4sKcZrlbovE'
    chat_id = "7232594881"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error sending notification:", e)


while True:
    changes = check_change(link)
    if changes:
        change_details = "\n".join(changes)
        send_noti(f"Changes detected:\n{change_details}")
    time.sleep(1)  # Run every minute instead of every second
