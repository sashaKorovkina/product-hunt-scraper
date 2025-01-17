"""
Code to scrape ProductHunt reviews and
add them to Supabase database.
"""

from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from bs4 import BeautifulSoup
import os
import psycopg2
from selenium.webdriver.common.action_chains import ActionChains
import streamlit as st
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
    TIMEOUT = 20
    button_xpath = '/html/body/div[1]/div/div[3]/main/div/button'

    try:
        driver.get(url)
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, button_xpath))
        )
        st.write("Page loaded successfully!")
    except TimeoutException:
        st.warning("Timed out waiting for page to load")
        driver.quit()

    time.sleep(3)

    while True:
        try:
            button = driver.find_element(By.XPATH, button_xpath)
            ActionChains(driver).move_to_element(button).click(button).perform()
            logger.info("Button clicked!")
            time.sleep(3)
        except Exception as e:
            logger.info('No more buttons to click')
            break


def scrape_content(driver, cursor, connection, url):
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
            if review_text is None:
                logger.debug('Picked up empty review...')
                continue
            logger.debug(f"Extracted review: {review_text}")
            if review_text == "":
                continue

            try:
                cursor.execute(
                    "INSERT INTO public.products (review, link) VALUES (%s, %s)",
                    (review_text, url)
                )
                connection.commit()
                logger.info('Data successfully inserted and transaction committed.')
            except Exception as e:
                logger.error(f"Database insertion error: {e}")

    driver.quit()


if __name__ == "__main__":
    link = "https://www.producthunt.com/products/meetgeek/reviews"
    cursor, connection = supabase_connect()
    driver = webdriver.Chrome()
    click_btn_next_page(driver, link)
    scrape_content(driver, cursor, connection, link)
