from database import supabase_connect
from openai import OpenAI
from database import click_btn_next_page, scrape_content
from loguru import logger
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st

def write_features(data):
    """
    This function returns the slide description
    in a JSON format. It includes the layout,
    header, images, charts, text.
    """

    if not os.getenv("OPEN_AI_API_KEY"):
        raise ValueError("Missing OPENAI_API_KEY environment variable. Please set your OpenAI API key.")

    client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
                    Based on the list of reviews provided, make 2 lists - one of positive features 
                    and one of negative features. Group them by theme, with a title sentence and the supporting
                    reviews under it as bullet points. Disregard generic reviews which do not reference specific
                    features. The reviews are here: {data}.
                """
            },
            {
                "role": "user",
                "content": f"""
                    Based on the list of reviews provided, make 2 lists - one of positive features 
                    and one of negative features. Group them by theme, with a title sentence and the supporting
                    reviews under it as bullet points. Disregard generic reviews which do not reference specific
                    features. The reviews are here: {data}.
                """
            }
        ]
    )

    # Extract response text and format as JSON
    response = completion.choices[0].message.content
    return response


def analyze(link):
    cursor, connection = supabase_connect()
    cursor.execute(
        "SELECT link FROM public.products WHERE link = %s",
        (link,)
    )
    result = cursor.fetchone()
    if result:
        logger.info("Link already exists.")
    else:
        @st.experimental_singleton
        def installff():
            os.system('sbase install geckodriver')
            os.system(
                'ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

        _ = installff()
        from selenium import webdriver
        from selenium.webdriver import FirefoxOptions
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)

        click_btn_next_page(driver, link)
        scrape_content(driver, cursor, connection, link)

    cursor.execute(
        "SELECT review "
        "FROM public.products "
        "WHERE link = %s",
        (link,)
    )

    results = cursor.fetchall()
    response = write_features(results)
    return response


if __name__ == "__main__":
    product_link = 'https://www.producthunt.com/products/final-round-ai/reviews'
    analyze(product_link)