from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from typing import Annotated
from sqlmodel import select
from app import models
from . import database, config
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = f"{config.settings.secret_key}"
ALGORITHM = f"{config.settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = f"{config.settings.access_token_expire_minutes}"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = models.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: database.SessionDep):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.exec(select(User).where(User.id == token.id)).first()

    return user