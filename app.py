import streamlit as st
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from loguru import logger


URL = "https://www.producthunt.com/products/final-round-ai/reviews"
XPATH = "//*[@id=\"root-container\"]/div/div[3]/main/div/button"

# //*[@id="root-container"]/div/div[3]/main/div/button
# <button type="button" class="styles_reset__0clCw styles_button__BmLM4 styles_full__j4aVK mb-8" data-sentry-element="Element" data-sentry-component="Button" data-sentry-source-file="index.tsx">Show 72 more</button>
# <button type="button" class="styles_reset__0clCw styles_button__BmLM4 styles_full__j4aVK mb-8" data-sentry-element="Element" data-sentry-component="Button" data-sentry-source-file="index.tsx">Show 72 more</button>
# #root-container > div > div.styles_layout__cOQYA.pt-6.sm\:pt-10.styles_container__eS_WB > main > div > button
# document.querySelector("#root-container > div > div.styles_layout__cOQYA.pt-6.sm\\:pt-10.styles_container__eS_WB > main > div > button")
# //*[@id="root-container"]/div/div[3]/main/div/button
TIMEOUT = 20

st.title("Reviews")

firefoxOptions = Options()
firefoxOptions.add_argument("--headless")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(
    options=firefoxOptions,
    service=service,
)
driver.get(URL)

try:
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, XPATH,))
    )
    logger.debug('Successfully discovered elements')
except TimeoutException:
    st.warning("Timed out waiting for page to load")
    driver.quit()

# time.sleep(10)
# elements = driver.find_elements(By.XPATH, XPATH)
# st.write([el.text for el in elements])
# driver.quit()
