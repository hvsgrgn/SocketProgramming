# Socket Programming & REST API 

Python networking projects: two TCP socket tasks with binary protocols built on `struct`, and a REST API for a webshop's shopping baskets built with **FastAPI**.

## Projects

### `task1/`: TCP client

`task1_client.py` connects to a server and runs a short purchase conversation:

1. It sends a student code and an item name, packed into a fixed-size binary message (`struct` format `6s 20s`).
2. It receives the item's price as an integer.
3. It replies `purchase` if the price is 6000 or less, and `back_out` otherwise.
4. It prints the server's final reply.

The test server (`feladat1_server_obf.py`) was provided by the course in obfuscated form.

```
python task1/feladat1_server_obf.py <ip> <port>     # provided test server
python task1/task1_client.py <ip> <port>
```

### `task2/`: Multi-client TCP server

`task2_server.py` is a server that uses `select()` to handle **several clients at the same time**. It keeps a shared **3×3 integer matrix** and supports three binary commands (`struct` format `3s i i i`):

| Command | Effect | Reply |
|---|---|---|
| `SET r c v` | sets cell `(r, c)` to `v` | the new value |
| `GET r c` | reads cell `(r, c)` | the cell's value |
| `SUM` | adds up the whole matrix | the sum |

The test client (`feladat2_client_obf.py`) was provided by the course in obfuscated form.

```
python task2/task2_server.py <ip> <port> <id>
python task2/feladat2_client_obf.py <ip> <port>     # provided test client
```

The provided obfuscated files need the bundled `pyarmor_runtime`, which only works on **Windows** with **Python 3.13**.

### `ShoppingRestApi/`: FastAPI webshop backend

A REST API for managing a webshop's users and their shopping baskets. The data is stored in `data.json`, and every input is validated with **Pydantic**: IDs, prices and quantities can't be negative, and emails must look valid.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/adduser` | add a new user |
| `POST` | `/addshoppingbag?userid=` | create a basket for a user |
| `POST` | `/additem?userid=` | put an item in a user's basket |
| `PUT` | `/updateitem?userid=&itemid=` | update an item in the basket |
| `DELETE` | `/deleteitem?userid=&itemid=` | remove an item from the basket |
| `GET` | `/user?userid=` | get one user |
| `GET` | `/users` | list all users |
| `GET` | `/shoppingbag?userid=` | list the items in a user's basket |
| `GET` | `/getusertotal?userid=` | total price of a user's basket |

Errors return the matching HTTP status code: 400 for invalid data, 404 when something isn't found, and 500 for server errors.

```
pip install fastapi uvicorn
cd ShoppingRestApi
uvicorn main:app --reload --port 9000
```

Then open **http://127.0.0.1:9000/docs** to try the endpoints in the interactive Swagger UI.

## Tech stack

Python 3 · `socket` · `select` · `struct` · FastAPI · Pydantic · Uvicorn

## About

University assignments from ELTE (2025). Comments in the code and the task description (`Python beadandó feladat 1.pdf`) are in Hungarian.
