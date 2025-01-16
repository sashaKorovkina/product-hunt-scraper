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


def scrape_content(driver):
    # Set up the webdriver
    driver.get("https://www.producthunt.com/products/final-round-ai/reviews")
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
            print("Button clicked")
            time.sleep(3)
        except Exception as e:
            logger.error(e)
            break


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    click_btn_next_page(driver)
    scrape_content(driver)
