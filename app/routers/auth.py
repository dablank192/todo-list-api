from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, oauth2
from typing import Annotated
from datetime import timedelta
from sqlmodel import select

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model= models.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: database.SessionDep
) -> models.Token:
    user = db.exec(select(models.User).where(models.User.username == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(
        data={"user_id": str(user.id)}, expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")