from database import supabase_connect
from openai import OpenAI
from database import click_btn_next_page, scrape_content
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
import os


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
                    Based on the list of reviews provided, extract specific features or aspects 
                    that users explicitly like or dislike about the product. For each feature, 
                    group positive and negative sentiments clearly and concisely. For example, 
                    if a user mentions the product's speed positively, it should appear under 
                    "Positive." If another user mentions poor customer service, it should appear 
                    under "Negative." Only include examples directly tied to product features or 
                    services. Reviews: {data}
                """
            },
            {
                "role": "user",
                "content": f"""
                    Based on the list of reviews provided, extract specific features or aspects 
                    that users explicitly like or dislike about the product. For each feature, 
                    group positive and negative sentiments clearly and concisely. Reviews: {data}
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
        logger.info("Link does not exist.")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        click_btn_next_page(driver, link)
        scrape_content(driver, cursor, link)

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