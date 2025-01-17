import requests

# API URL
url = "http://127.0.0.1:5000/add_product"

# Data payload
data = {
    "url": "https://www.producthunt.com/products/fireflies-ai/reviews"
}

# Sending the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.json())
