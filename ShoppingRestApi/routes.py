from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi import APIRouter
from data.filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket,
    load_json    
)

from data.filehandler import *

routers = APIRouter()
'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User) -> User:
    try:
        # Convert Pydantic model to dictionary for filehandler
        user_dict = user.model_dump()
        add_user(user_dict)
        
        # Return the user as confirmation
        return user
        
    except ValueError as e:
        # Handle validation errors from our file operations
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    try:
        user = get_user_by_id(userid)
        import random
        basket_id = random.randint(1000, 9999)
        new_basket = {
            "id": basket_id,
            "user_id": userid,
            "items": []
        }
        add_basket(new_basket)
        return "Sikeres kosár hozzárendelés."
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        item_dict = item.model_dump()
        add_item_to_basket(userid, item_dict)
        
        # Get the actual basket data, not just items
        data = load_json()
        for basket in data.get("Baskets", []):
            if basket.get("user_id") == userid:
                return Basket(
                    id=basket["id"],
                    user_id=userid,
                    items=[Item(**item_data) for item_data in basket["items"]]
                )
        
        raise HTTPException(status_code=404, detail="Basket not found")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.put('/updateitem')
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    try:
        update_data = updateItem.model_dump()
        update_item_in_basket(userid, itemid, update_data)
        
        # Return the updated basket
        data = load_json()
        for basket in data.get("Baskets", []):
            if basket.get("user_id") == userid:
                return Basket(
                    id=basket["id"],
                    user_id=userid,
                    items=[Item(**item_data) for item_data in basket["items"]]
                )
        
        raise HTTPException(status_code=404, detail="Basket not found")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.delete('/deleteitem')
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        delete_item_from_basket(userid, itemid)
        
        # Return the updated basket
        data = load_json()
        for basket in data.get("Baskets", []):
            if basket.get("user_id") == userid:
                return Basket(
                    id=basket["id"],
                    user_id=userid,
                    items=[Item(**item_data) for item_data in basket["items"]]
                )
        
        raise HTTPException(status_code=404, detail="Basket not found")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.get('/user')
def user(userid: int) -> User:
    try:
        user_data = get_user_by_id(userid)
        return User(**user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.get('/users')
def users() -> list[User]:
    try:
        users_data = get_all_users()
        return [User(**user_data) for user_data in users_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.get('/shoppingbag')
def shoppingbag(userid: int) -> list[Item]:
    try:
        items_data = get_basket_by_user_id(userid)
        return [Item(**item_data) for item_data in items_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    try:
        return get_total_price_of_basket(userid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



