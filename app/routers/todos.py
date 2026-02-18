from fastapi import APIRouter, Query, HTTPException, status, Depends
from sqlmodel import select
from typing import Annotated

from app.oauth2 import get_current_user
from .. import models, database

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model= list[models.GetTodos])
def get_item(db: database.SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10, current_user: int = Depends(get_current_user)):
    items = db.exec(select(models.Todos).offset(offset).limit(limit)).all()
    return items

@router.get("/{id}")
def get_aitem(id: int, db: database.SessionDep, current_user: int = Depends(get_current_user)):
    item = db.get(models.Todos, id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return item

@router.post("/add", response_model= models.GetTodos)
def create_item(item: models.CreateTodos, db: database.SessionDep, current_user: int = Depends(get_current_user)):
    post = models.Todos(user_id = current_user.id, **item.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.put("/{id}", response_model= models.GetTodos)
def update_item(id: int, item: models.CreateTodos, db: database.SessionDep, current_user: int = Depends(get_current_user)):
    find_item = db.get(models.Todos, id)
    if not find_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    items = item.model_dump(exclude_unset=True)
    find_item.sqlmodel_update(items)
    find_item.user_id = current_user.id
    db.add(find_item)
    db.commit()
    db.refresh(find_item)
    return find_item

@router.delete("/{id}")
def delete_item(id: int, db: database.SessionDep, current_user: int = Depends(get_current_user)):
    find_item = db.get(models.Todos, id)
    if not find_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if find_item.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "User not authorized")
    
    db.delete(find_item)
    db.commit()
    return {"Response": "Task Deleted Successfully"}