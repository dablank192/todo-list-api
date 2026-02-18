from fastapi import APIRouter, HTTPException, status, Depends
from .. import utils, oauth2
from app.database import SessionDep
from app.models import User, UserCreate, UserOut


router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model= UserOut)
def create_user(db: SessionDep, user: UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    # new_user = User(**user.dict())
    new_user = User(**user.model_dump(exclude_unset=True))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= UserOut)
def get_user(id: int , db: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User's id not found")
    
    return user