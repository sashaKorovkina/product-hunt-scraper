import requests
import streamlit as st
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

st.title("ProductHunt Review Summaries")

# User input for the link
XPATH = "//*[@id=\"root-container\"]/div/div[3]/main/div/button"
TIMEOUT = 20
link = st.text_input("Enter a URL:", placeholder="https://example.com")

if st.button("Fetch Content"):
    if link:
        try:
            firefoxOptions = Options()
            firefoxOptions.add_argument("--headless")
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(
                options=firefoxOptions,
                service=service,
            )

            try:
                WebDriverWait(driver, TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, XPATH,))
                )
            except TimeoutException:
                st.warning("Timed out waiting for page to load")
                driver.quit()
            elements = driver.find_elements(By.XPATH, XPATH)
            st.write([el.text for el in elements])
            driver.quit()

            # text = analyze(link, driver)
            # bold_text = text.replace('**', '✱✱')
            # st.markdown(f"**Webpage Content:**\n{bold_text}", unsafe_allow_html=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the URL: {e}")
    else:
        st.warning("Please enter a valid URL.")
