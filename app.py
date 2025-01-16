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
            # Set up Selenium WebDriver with headless Firefox
            firefoxOptions = Options()
            firefoxOptions.add_argument("--headless")
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(
                options=firefoxOptions,
                service=service,
            )

            # Navigate to the URL
            driver.get(link)

            # Wait for the button to be visible
            try:
                WebDriverWait(driver, TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, XPATH))
                )
                st.success("Page loaded successfully!")
            except TimeoutException:
                st.warning("Timed out waiting for the button to load")
                driver.quit()

            # Click the button
            try:
                button = driver.find_element(By.XPATH, XPATH)
                button.click()
                st.success("Button clicked successfully!")
            except Exception as e:
                st.error(f"Error clicking the button: {e}")
                driver.quit()
        finally:
            # Clean up the driver
            driver.quit()
    else:
        st.warning("Please enter a valid URL.")
