import pytest
from main import calculate_points, Receipt, Item

def test_calculate_points():
    # Test case 1
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="13:01",
        items=[
            Item(shortDescription="Mountain Dew 12PK", price="6.49"),
            Item(shortDescription="Emils Cheese Pizza", price="12.25"),
            Item(shortDescription="Knorr Creamy Chicken", price="1.26"),
            Item(shortDescription="Doritos Nacho Cheese", price="3.35"),
            Item(shortDescription="Klarbrunn 12-PK 12 FL OZ", price="12.00")
        ],
        total="35.35"
    )
    assert calculate_points(receipt) == 28

    # Test case 2
    receipt = Receipt(
        retailer="M&M Corner Market",
        purchaseDate="2022-03-20",
        purchaseTime="14:33",
        items=[
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25")
        ],
        total="9.00"
    )
    assert calculate_points(receipt) == 109

"""
Missing more test cases for null check of input data or null check of output. 
This is because I have not added try catch for those exceptions in the base code. 
Will update test cases here as I add such exception handling.
"""

if __name__ == "__main__":
    pytest.main()
