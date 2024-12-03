from fastapi import Body, FastAPI, Form, File, UploadFile
from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl 

app = FastAPI()

print('Start server-->')
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

from enum import Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# http://127.0.0.1:8000/models/alexnet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# http://127.0.0.1:8000/users
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

# http://127.0.0.1:8000/items/?skip=1&limit=2
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# http://127.0.0.1:8000/items/23?q1=6&short=true1
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        return {"item_id": item_id, "q": q}
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.post("/body")
async def create_item(item: Item):
    return item

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/body/{item_id}")
async def update_item(
    item_id: int, item: Annotated[Item, Body(embed=True)], user: User, importance: Annotated[int, Body(gt=0)], q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance+1}
    if q:
        results.update({"q": q})
    return results

class Image(BaseModel):
    url: HttpUrl
    name: str

class ImageItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

@app.put("/image/{item_id}")
async def update_item(item_id: int, item: ImageItem):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.get("/")
def root():
    return {"message": "Hello World"}

