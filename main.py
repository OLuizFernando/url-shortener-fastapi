from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import Union
from pydantic import BaseModel

app = FastAPI()


class Link(BaseModel):
    url: str
    slug: Union[str, None] = None


@app.get("/")
def read_root():
    return RedirectResponse("/docs")


@app.post("/")
def insert_link(link: Link):
    return link


@app.get("/items/{item_id}")
def read_item(item_id: int, q: int = 0):
    return {"item_id": item_id, "q": q}