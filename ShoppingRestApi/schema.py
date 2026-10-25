from pydantic import BaseModel, field_validator
from typing import List
'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''
#checking for positive values for ints, is that an issue? - TO BE ANSWERED
#purpose of this file: A schema defines the structure and validation rules for our data, basically a blueprint that tells our API what data to expect and what's valid.

# just a constant
ShopName='Bolt'

#pydantic classes:
#Pydantic is a library that helps with data validation using Python type annotations. The BaseModel classes will automatically validate our data based on the types we define.
class Item(BaseModel):
    item_id: int
    name: str
    brand: str
    price: float
    quantity: int
    
    #the field validation happens here with this decorator and function
    @field_validator('item_id', 'price', 'quantity') #names of the fields to be checked one by one
    @classmethod #this is needed bc validation happens on raw data before the instance is cretated, therefore there is no self to be called on yet  
    def check_positive_numbers(cls, value): #class instead of self again
        if value < 0:
            raise ValueError('Value must be non-negative')
        return value


class User(BaseModel):
    id: int
    name : str
    email: str

    @field_validator('id')
    @classmethod
    def check_positive_id(cls, value):
        if value < 0:
            raise ValueError('ID must be non-negative')
        return value
    
    @field_validator('email')
    @classmethod
    def check_email_format(cls, value):
        if '@' not in value or '.' not in value.split('@')[-1]:
            raise ValueError('Invalid email format')
        return value

class Basket(BaseModel):
    id: int
    user_id : int
    items: List[Item]

    @field_validator('id', 'user_id')
    @classmethod
    def check_positive_numbers(cls, value):
        if value < 0:
            raise ValueError('Value must be non-negative')
        return value




