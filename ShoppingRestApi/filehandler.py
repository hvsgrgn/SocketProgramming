import json
import os
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # If file doesn't exist, return empty structure - NOT SURE this is the expected behaviour?
        return {"Users": [], "Baskets": []}
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in data file")

def save_json(data: Dict[str, Any]) -> None:
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def add_user(user: Dict[str, Any]) -> None:
    data = load_json()
    
    # Check if user ID already exists
    for existing_user in data["Users"]:
        if existing_user["id"] == user["id"]:
            raise ValueError(f"User with ID {user['id']} already exists")
    
    # Add the new user
    data["Users"].append(user)
    
    # Save back to file
    save_json(data)

def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()
    
    # Check if user exists first
    user_exists = any(user["id"] == basket["user_id"] for user in data["Users"])
    if not user_exists:
        raise ValueError(f"User with ID {basket['user_id']} does not exist")
    
    # Now check everything in one loop
    for existing_basket in data["Baskets"]:
        if existing_basket["id"] == basket["id"]:
            raise ValueError(f"Basket with ID {basket['id']} already exists")
        if existing_basket["user_id"] == basket["user_id"]:
            raise ValueError(f"User with ID {basket['user_id']} already has a basket")
    
    data["Baskets"].append(basket)
    save_json(data)

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    data = load_json()
    
    basket_found = False
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket_found = True
            
            for existing_item in basket["items"]:
                if existing_item["item_id"] == item["item_id"]:
                    raise ValueError(f"Item with ID {item['item_id']} already exists in basket")
            
            basket["items"].append(item)
            break
    
    if not basket_found:
        raise ValueError(f"No basket found for user ID {user_id}")
    
    save_json(data)

def update_item_in_basket(user_id: int, item_id: int, updated_item: Dict[str, Any]) -> None:
    data = load_json()
    
    basket_found = False
    item_found = False
    
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket_found = True
            
            # Find the item to update
            for item in basket["items"]:
                if item["item_id"] == item_id:
                    item_found = True
                    
                    # Prevent changing the item_id (simpler approach)
                    if updated_item["item_id"] != item_id:
                        raise ValueError("Cannot change item_id during update")
                    
                    # Update the item with new values (except item_id)
                    item.update(updated_item)
                    break
            
            if item_found:
                break
    
    if not basket_found:
        raise ValueError(f"No basket found for user ID {user_id}")
    if not item_found:
        raise ValueError(f"No item with ID {item_id} found in basket")
    
    save_json(data)

def delete_item_from_basket(user_id: int, item_id: int) -> None:
    data = load_json()
    
    basket_found = False
    item_found = False
    
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket_found = True
            
            # Find and remove the item
            for i, item in enumerate(basket["items"]):
                if item["item_id"] == item_id:
                    item_found = True
                    # Remove the item from the list
                    del basket["items"][i]
                    break
            
            if item_found:
                break
    
    if not basket_found:
        raise ValueError(f"No basket found for user ID {user_id}")
    if not item_found:
        raise ValueError(f"No item with ID {item_id} found in basket")
    
    save_json(data)

__all__ = [
    'add_user',
    'add_basket', 
    'add_item_to_basket',
    'update_item_in_basket',  # Add this
    'delete_item_from_basket'  # Add this
]