##Install requests and Beautifulsoup for scraping to fetch and parse HTML
## requests allows you to make an HTTP request
## beautifulsoup extracts the data from the HTML
## returns the data in a parse tree that you can then parse through by what you are searching for


##pip install requests
##If scraping a site that uses javascript or any scripts, you will need to use selenium
#pip install selenium


import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'

def get_data(url):
    # Set up the Service and Options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Path to chromedriver on GitHub Actions (adjust for local if testing)
    chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'

    try:
        # Initialize the WebDriver with the path
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

        # Navigate to the page
        driver.get(url)

        # Wait for the product grid to load, Wait for the elements to be present (you might need to update the class name)
        product_grid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-grid__items"))
        )
        return product_grid.text  # Print the product grid items text

    except Exception as e:
        print(f"Error: {e}")
        return None  # Return None on error
    finally:
        # Ensure WebDriver is closed
        driver.quit()


def check_change(url, old_data_file='old_data.txt'):
    new_data = get_data(url)
    if not new_data:
        return false;
    try:
        #opens old data file and reads
        with open(old_data_file, 'r') as f:
            #sets old_data to what is found inside old data text file
            old_data =f.read()
            print("read in old data")
            #checks if the new found data is the same as the old read in data
        if new_data == old_data:
            #if not then it will overwrite the old file data with the new data
            with open(old_data_file, 'w') as f:
                f.write(new_data)
                print("read in new data")
            return True
    #if no file is found then it will create a file for itself to use
    except FileNotFoundError:
        with open(old_data_file, 'w') as f:
            f.write(new_data)
    return False

def send_noti(message):
    bot_token= '7629797667:AAHKli_4cr7SKNKw6L4Iq00N4sKcZrlbovE'
    chat_id= "7232594881"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload={
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error sending noti")


while True:
    if check_change(link):
        send_noti("Change detected"+ " "+link)
    time.sleep(3600)




