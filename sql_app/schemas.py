from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
    image: Union[str, None] = None

#dans creation pas utilisation de id et associe pas a ownner
class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = [] 
#pour lire les donner par .id blabiha ["id"]car dict  whkda t9d aider aussi pour relationship 
    class Config:
        orm_mode = True
#pour heritage ne prend pas les donnre directement mais hta dir .uitems had kibchi tbl yjibhom

