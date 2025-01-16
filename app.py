import requests
from analyzer import analyze
import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Streamlit app title
st.title("ProductHunt Review Summaries")

# User input for the link
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
            text = analyze(link, driver)
            bold_text = text.replace('**', '✱✱')
            st.markdown(f"**Webpage Content:**\n{bold_text}", unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the URL: {e}")
    else:
        st.warning("Please enter a valid URL.")
