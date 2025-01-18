import requests
import streamlit as st
from selenium import webdriver
from analyzer import analyze

# Streamlit app title
st.title("Simple Link Content Viewer")

# User input for the link
link = st.text_input("Enter a URL:", placeholder="https://example.com")

if st.button("Fetch Content"):
    if link:
        try:
            driver = webdriver.Chrome()
            text = analyze(link, driver)
            bold_text = text.replace('**', '✱✱')  # Highlight for processing bold later
            st.markdown(f"**Webpage Content:**\n{bold_text}", unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the URL: {e}")
    else:
        st.warning("Please enter a valid URL.")