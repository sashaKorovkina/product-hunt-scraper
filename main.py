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
from supabase import create_client, Client

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


def scrape_content(driver):
    # Set up the webdriver
    element = driver.find_element(By.XPATH, '//*[@id="root-container"]/div/div[3]/main/div/div[5]')
    sub_elements = element.find_elements(By.XPATH, './*')  # Direct children

    # Print each sub-element
    for sub in sub_elements:
        soup = BeautifulSoup(sub.get_attribute('outerHTML'), 'html.parser')
        elements = soup.find_all('div',
                                 class_="styles_htmlText__eYPgj text-18 font-normal text-light-gray italic styles_format__8NeQe styles_overallExperience__x7Gqf")
        for element in elements:
            logger.debug(element.text.strip())

    # Close the driver
    driver.quit()


def click_btn_next_page(driver):
    driver.get("https://www.producthunt.com/products/final-round-ai/reviews")
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


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    click_btn_next_page(driver)
    scrape_content(driver)
