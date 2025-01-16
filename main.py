"""
Website: https://www.producthunt.com/products/final-round-ai/reviews
//*[@id="root-container"]/div/div[3]/main/div/div[5]
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from bs4 import BeautifulSoup

# Set up the webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
