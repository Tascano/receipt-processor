import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = "http://localhost:8000/"

def post_request(url, payload):
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"POST request failed: {e}")

def get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"GET request failed: {e}")

def process_receipt(payload):
    url = base_url+"receipts/process"
    return post_request(url, payload)

def get_points(receipt_id):
    url = base_url+f"receipts/{receipt_id}/points"
    return get_request(url)

# Define the payload
payload = {
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {
            "shortDescription": "Pepsi - 12-oz",
            "price": "1.25"
        },
        {
            "shortDescription": "Dasani",
            "price": "1.40"
        }
    ]
}

# Send the POST request to process the receipt
data = process_receipt(payload)

if data:
    receipt_id = data.get("id")
    logger.info(f"Generated ID: {receipt_id}")

    if receipt_id:
        # Send the GET request to retrieve the points
        points_data = get_points(receipt_id)

        if points_data:
            points = points_data.get("points")
            logger.info(f"Points: {points}")
            assert points == 15, "Points mismatch. Expected: 15"
        else:
            logger.error("Failed to retrieve points.")
else:
    logger.error("Failed to process receipt.")
