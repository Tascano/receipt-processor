from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List
import sqlite3
import logging
import json
import math

app = FastAPI()

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLite databases and create tables if they don't exist
receipts_conn = sqlite3.connect("receipts.db")
receipts_cursor = receipts_conn.cursor()
receipts_cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id TEXT PRIMARY KEY,
        retailer TEXT,
        purchaseDate TEXT,
        purchaseTime TEXT,
        total TEXT
    )
""")
receipts_conn.commit()

items_conn = sqlite3.connect("items.db")
items_cursor = items_conn.cursor()
items_cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY,
        receiptId TEXT,
        shortDescription TEXT,
        price TEXT,
        FOREIGN KEY (receiptId) REFERENCES receipts (id)
    )
""")
items_conn.commit()

@app.post("/receipts/process", response_model=dict)
async def process_receipt(receipt: Receipt):
    points = calculate_points(receipt)
    receipt_id = str(uuid4())

    # Store the receipt in the receipts database
    receipts_cursor.execute("""
        INSERT INTO receipts (id, retailer, purchaseDate, purchaseTime, total)
        VALUES (?, ?, ?, ?, ?)
    """, (receipt_id, receipt.retailer, receipt.purchaseDate, receipt.purchaseTime, receipt.total))
    receipts_conn.commit()

    # Store the items in the items database
    for item in receipt.items:
        item_id = str(uuid4())
        items_cursor.execute("""
            INSERT INTO items (id, receiptId, shortDescription, price)
            VALUES (?, ?, ?, ?)
        """, (item_id, receipt_id, item.shortDescription, item.price))
    items_conn.commit()

    logger.info(f"Receipt processed. ID: {receipt_id}")
    return {"id": receipt_id}

@app.get("/receipts/{id}/points", response_model=dict)
async def get_points(id: UUID):
    # Retrieve the receipt from the receipts database
    receipts_cursor.execute("SELECT * FROM receipts WHERE id=?", (str(id),))
    row = receipts_cursor.fetchone()

    if row is None:
        return {"error": "Receipt not found"}

    receipt = Receipt(
        retailer=row[1],
        purchaseDate=row[2],
        purchaseTime=row[3],
        items=[],
        total=row[4]
    )

    # Retrieve the items from the items database
    items_cursor.execute("SELECT * FROM items WHERE receiptId=?", (str(id),))
    rows = items_cursor.fetchall()

    for item_row in rows:
        item = Item(
            shortDescription=item_row[2],
            price=item_row[3]
        )
        receipt.items.append(item)

    points = calculate_points(receipt)

    logger.info(f"Points retrieved for ID {id}: {points}")
    return {"points": points}

def calculate_points(receipt: Receipt) -> int:
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name (excluding whitespace and special characters)
    points += sum(char.isalnum() for char in receipt.retailer if char.isalpha())
    logger.info(f"Points after Rule 1: {points}")


    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if float(receipt.total) == int(float(receipt.total)):
        points += 50
    logger.info(f"Points after Rule 2: {points}")

    # Rule 3: 25 points if the total is a multiple of 0.25
    if float(receipt.total) % 0.25 == 0:
        points += 25
    logger.info(f"Points after Rule 3: {points}")

    # Rule 4: 5 points for every two items on the receipt
    points += 5 * (len(receipt.items) // 2)
    logger.info(f"Points after Rule 4: {points}")

    # Rule 5: Multiply the price by 0.2 and round up to the nearest integer for items with trimmed length as a multiple of 3
    for item in receipt.items:
        trimmed_length = len(item.shortDescription.strip())
        if trimmed_length % 3 == 0:
            item_points = math.ceil(float(item.price) * 0.2)
            points += item_points
            logger.info(f"Points after processing item '{item.shortDescription}': {points} (Item points: {item_points})")

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_day = int(receipt.purchaseDate.split("-")[-1])
    if purchase_day % 2 != 0:
        points += 6
    logger.info(f"Points after Rule 6: {points}")

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt.purchaseTime.split(":")
    if 14 <= int(purchase_time[0]) < 16:
        points += 10
    logger.info(f"Points after Rule 7: {points}")

    return points


# Close the database connections when the application shuts down
@app.on_event("shutdown")
def close_connections():
    receipts_cursor.close()
    receipts_conn.close()
    items_cursor.close()
    items_conn.close()
