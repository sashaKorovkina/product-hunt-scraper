"""
Code to scrape ProductHunt reviews for a
specific product.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import psycopg2


def supabase_connect():
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        logger.info("The database connection was successful!")

        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        print(f"Failed to connect: {e}")


def click_btn_next_page(driver, url):
    driver.get(url)
    time.sleep(3)
    button_xpath = '/html/body/div[1]/div/div[3]/main/div/button'
    while True:
        try:
            button = driver.find_element(By.XPATH, button_xpath)
            ActionChains(driver).move_to_element(button).click(button).perform()
            logger.info("Button clicked!")
            time.sleep(3)
        except Exception as e:
            logger.info('No more buttons to click')
            break


def scrape_content(driver, cursor, url):
    # Set up the webdriver
    element = driver.find_element(By.XPATH, '//*[@id="root-container"]/div/div[3]/main/div/div[5]')
    sub_elements = element.find_elements(By.XPATH, './*')  # Direct children

    for sub in sub_elements:
        soup = BeautifulSoup(sub.get_attribute('outerHTML'), 'html.parser')
        elements = soup.find_all(
            'div',
            class_="styles_htmlText__eYPgj text-18 font-normal text-light-gray italic styles_format__8NeQe styles_overallExperience__x7Gqf"
        )

        for element in elements:
            review_text = element.text.strip()  # Extract the review text
            logger.debug(f"Extracted review: {review_text}")

            try:
                logger.info('Attempting to insert data into the database...')
                cursor.execute(
                    "INSERT INTO public.products (review) VALUES (%s)",
                    (review_text,)
                )
                cursor.execute(
                    "INSERT INTO public.products (link) VALUES (%s)",
                    (url,)
                )
                connection.commit()
                logger.info('Data successfully inserted and transaction committed.')
            except Exception as e:
                logger.error(f"Database insertion error: {e}")

    # Close the driver
    driver.quit()


if __name__ == "__main__":
    link = "https://www.producthunt.com/products/final-round-ai/reviews"
    cursor, connection = supabase_connect()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    click_btn_next_page(driver, link)
    scrape_content(driver, cursor, link)
