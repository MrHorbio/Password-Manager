from fastapi import FastAPI,Cookie,Header,Form,UploadFile,File,HTTPException
from fastapi.encoders import jsonable_encoder
from model import Manufacturer,Product,User,Response,oo
from db import collections
from bson import ObjectId


app = FastAPI()

# @app.post("/add/")
# async def add_product(product: Product, seller: Seller):
#     return{"product": product, "seller": seller}


@app.post('/product')
def add_product(product: Product):
    return product


@app.post("/user")
def create_user(user:User):
    return user


#Read Cookies

@app.get("/read_cookie")
def read_cookie(session_id: str = Cookie(None)):
    return {"Session_id" :  session_id}

#Header
@app.get("/read_header/")
def read_header(user_agent:str = Header(None)):
    return {"user_agent":user_agent}

@app.get("/item/",response_model=Response)
def get_item():
    return{
        "User_name": "Hacker",
        "name":"Laptop",
        "price": 1000.0 ,
        "password":"secret@123"
        }

@app.post("/login",tags=["Login"],description="verify users creds",summary="Login")
def login(username: str = Form(), password: str = Form()):
    return{"username": username}

@app.post("/upload")
def upload(file:UploadFile = File()):
    return {"filename":file.filename}


@app.post("/submit")
def submit_form(file: UploadFile = File(), name: str = Form()):
    return {"filename": file.filename, "name":name}


@app.get("/item/{item_id}")
def read_item(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}


@app.get("/item/",tags=["Item"], summary="Get Item",description="This gets an items")
def get_item():
    return {"name":"Book"}





@app.post("/oo")
def oo(id:str,item: oo):
    json_compatible_item = jsonable_encoder(item)
    return json_compatible_item
