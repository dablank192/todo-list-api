
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from pydantic import BaseModel


class TodosBase(SQLModel):
    title: str = Field(index= True)
    desc: str = Field(index= True)

class User(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    created_at: datetime = Field(default_factory= datetime.now)

    todos: List["Todos"] = Relationship(back_populates= "user")

class Todos(TodosBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory= datetime.now)
    user_id: int = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates= "todos") 

class GetTodos(TodosBase):#response model
    id: int
    created_at: datetime = Field(default_factory= datetime.now)

class CreateTodos(TodosBase):
    pass

class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

