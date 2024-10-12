# app/services/logistics_service.py

from typing import Optional, List

# Placeholder data for warehouse locations and inventory
WAREHOUSES = [
    {"id": 1, "location": "New York", "inventory": {101: 10, 102: 5}},  # Inventory is a dictionary of product_id: stock
    {"id": 2, "location": "Los Angeles", "inventory": {101: 20, 103: 15}},
    {"id": 3, "location": "Chicago", "inventory": {102: 7, 104: 3}}
]

def find_nearest_warehouse(buyer_location: str, expand_search: bool = False) -> Optional[dict]:
    """
    Simulates finding the nearest warehouse based on buyer location.
    In production, this could use geolocation or external APIs for accuracy.
    
    :param buyer_location: The location of the buyer (e.g., city name).
    :param expand_search: If True, expands the search to all available warehouses.
    :return: The nearest warehouse dictionary or None if no suitable warehouse is found.
    """
    # Placeholder logic: Simply return the first warehouse for the example
    for warehouse in WAREHOUSES:
        if warehouse["location"].lower() == buyer_location.lower():
            return warehouse

    # If expand_search is True, return the first available warehouse as a fallback
    if expand_search:
        return WAREHOUSES[0] if WAREHOUSES else None
    
    return None


def check_warehouse_inventory(warehouse: dict, product_id: int) -> bool:
    """
    Checks if a given warehouse has a product in stock.
    :param warehouse: A dictionary representing the warehouse.
    :param product_id: The product ID to check inventory for.
    :return: True if the product is in stock, False otherwise.
    """
    return warehouse["inventory"].get(product_id, 0) > 0

