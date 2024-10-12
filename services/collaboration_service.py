# app/services/collaboration_service.py

from typing import List, Optional

# Placeholder data for seller collaborators
SELLER_COLLABORATORS = {
    1: [2, 3],  # Seller with ID 1 collaborates with sellers 2 and 3
    2: [1],     # Seller with ID 2 collaborates with seller 1
    3: [1, 2],  # Seller with ID 3 collaborates with sellers 1 and 2
}

SELLER_INVENTORY = {
    1: {101: 5, 102: 0},   # Seller 1's inventory: product_id -> stock quantity
    2: {101: 3, 103: 10},  # Seller 2's inventory
    3: {102: 7, 104: 3}    # Seller 3's inventory
}

def find_seller_collaborators(seller_id: int, expand_search: bool = False) -> List[int]:
    """
    Finds a list of seller collaborators for the given seller_id.
    
    :param seller_id: The ID of the seller looking for collaborators.
    :param expand_search: If True, expands the search for all sellers.
    :return: A list of collaborator seller IDs.
    """
    if expand_search:
        # Return all seller IDs except the current seller
        return [s_id for s_id in SELLER_INVENTORY.keys() if s_id != seller_id]
    
    return SELLER_COLLABORATORS.get(seller_id, [])


def check_seller_inventory(seller_id: int, product_id: int) -> bool:
    """
    Checks if a given seller has the product in stock.
    :param seller_id: The ID of the seller.
    :param product_id: The product ID to check inventory for.
    :return: True if the seller has the product in stock, False otherwise.
    """
    return SELLER_INVENTORY.get(seller_id, {}).get(product_id, 0) > 0

