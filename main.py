from typing import Union
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"world"}

@app.get("/items/{item_id}")
def read(item_id: int ,q:Union[str,None]=None):
    return {"item_id":item_id,"q":q}
##connect_args={"check_same_thread": False}. pour plusieur thread


