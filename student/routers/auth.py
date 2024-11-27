from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2, utils

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = oauth2.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(username=user.username, password=hashed_password, student_id=user.student_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(database.get_db)):
    user = oauth2.get_current_user(db, token)
    return user
