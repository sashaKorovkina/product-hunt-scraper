from flask import Flask, request, jsonify
from database import supabase_connect, click_btn_next_page, scrape_content
from selenium import webdriver

app = Flask(__name__)


@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        product_url = data.get("url")
        if not product_url:
            return jsonify({"error": "Missing 'url' in request body"}), 400

        cursor, connection = supabase_connect()
        driver = webdriver.Chrome()
        click_btn_next_page(driver, product_url)
        scrape_content(driver, cursor, connection, product_url)

        return jsonify({"message": "Product added to database!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
