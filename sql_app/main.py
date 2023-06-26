from typing import List
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException,Header,UploadFile,File
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from . import crud, models, schemas
from .database import SessionLocal, engine
import shutil
import os
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Tags(Enum):
    items = "items"
    users = "users"
# Dependency cad une fois appeler de fct apres sa fin va executer close(),yield  is try catch de chaque appel de la funciton  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User,tags=[Tags.users])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User],tags=[Tags.users])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User ,tags=[Tags.users])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", tags=[Tags.items])
def create_item_for_user(
    title:str,description:str, user_id: int, file: UploadFile=File(...) ,db: Session = Depends(get_db)
):
    
    unique_filename = str(uuid.uuid4()) + ".png"
    save_path = os.path.join("./repertoire/", unique_filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return crud.create_user_item(db=db, title=title,description=description,save_path=save_path, user_id=user_id)

@app.post("/use50")
async def root(post_id: int, file: UploadFile = File(...),db: Session = Depends(get_db)):
    unique_filename = str(uuid.uuid4()) + ".png"
    save_path = os.path.join("./repertoire/", unique_filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file":save_path}







@app.patch("/users/update/{user_id}", response_model=schemas.User ,tags=[Tags.users])
def update_user(user_id: int, user_update: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = crud.update_user_data(db, db_user, user_update)
    return updated_user



# @app.patch("/items/{item_id}", response_model=schemas.Item)
# async def update_item(item_id: str, item: schemas.Item, db: Session = Depends(get_db)):
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     #pour exclure les valeur par edefault ghi lidefinaw fitem
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item


#on peut ajoutermidlwre qui ayant un code qui faut execute chaque requete
#midllware on peut enregistre requete avant du traitemeny et apres traitemeny dans midllware

#Cors pour specifier exactemnt url frontend autoriser et les  ,header cookies ,requete allowd
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/users/", response_model=List[schemas.User],tags=[Tags.users])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/items1/",response_model=List[schemas.User])
async def create_item( x_token: Annotated[str, Header()]):
    if x_token != "hello":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    
    return {"item":"item"}