import json
import os
from typing import Dict, Any, List

'''
Útmutató a féjl használatához:

Felhasználó adatainak lekérdezése:

user_id = 1
user = get_user_by_id(user_id)
print(f"Felhasználó adatai: {user}")

Felhasználó kosarának tartalmának lekérdezése:

user_id = 1
basket = get_basket_by_user_id(user_id)
print(f"Felhasználó kosarának tartalma: {basket}")

Összes felhasználó lekérdezése:

users = get_all_users()
print(f"Összes felhasználó: {users}")

Felhasználó kosarában lévő termékek összárának lekérdezése:

user_id = 1
total_price = get_total_price_of_basket(user_id)
print(f"A felhasználó kosarának összára: {total_price}")

Hogyan futtasd?

Importáld a függvényeket a filehandler.py modulból:

from filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

#function to open, read and parse the json
def load_json() -> Dict[str, Any]:
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError("Data file not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in data file")

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    data = load_json()  #naming the output of the loading function
    
    # Search for the user with matching ID in the output's Users array of the data dictionary
    for user in data.get("Users", []):
        if user.get("id") == user_id:
            return user
    
    # If no user found, raise the required error
    raise ValueError(f"User with ID {user_id} not found")

def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    data = load_json()
    
    # Search for basket with matching user_id
    for basket in data.get("Baskets", []):
        if basket.get("user_id") == user_id:
            return basket.get("items", [])  # Return the items list from the basket
    
    # If no basket found, return empty list (user might have no basket yet)
    return []

def get_all_users() -> List[Dict[str, Any]]:
    data = load_json()
    return data.get("Users", [])

def get_total_price_of_basket(user_id: int) -> float:
    items = get_basket_by_user_id(user_id)
    total = 0.0
    
    for item in items:
        price = item.get("price", 0)
        quantity = item.get("quantity", 0)
        total += price * quantity
    
    return round(total, 2)  # Round to 2 decimal places for currency
