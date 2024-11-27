from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from .. import models, schemas, oauth2, utils
from ..database import get_db

router = APIRouter(
    prefix="/instructors",
    tags=['Instructors']
)

# User Login
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = oauth2.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get Current User
@router.get("/me", response_model=schemas.UserOut)
def read_users_me(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    return user

# Edit User Credentials
@router.put("/me", response_model=schemas.UserOut)
def update_user(user_update: schemas.UserCreate, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user_update.username
    db_user.password = utils.get_password_hash(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user

# View Class
@router.get("/me/classes", response_model=List[schemas.Course])
def view_classes(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    classes = db.query(models.Course).join(models.Teach).filter(models.Teach.instructor_id == user.id).all()
    return classes

# Create Test
@router.post("/me/tests", response_model=schemas.Test)
def create_test(test: schemas.TestCreate, term: str, sy: str, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    new_test = models.Test(date=test.date)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    create = models.Create(instructor_id=user.id, test_id=new_test.id, term=term, sy=sy)
    db.add(create)
    db.commit()
    return new_test

# Edit Test
@router.put("/me/tests/{test_id}", response_model=schemas.Test)
def edit_test(test_id: int, test_update: schemas.TestCreate, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_test = db.query(models.Test).join(models.Create).filter(models.Create.instructor_id == user.id, models.Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    db_test.date = test_update.date
    db.commit()
    db.refresh(db_test)
    return db_test

# Delete Test
@router.delete("/me/tests/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test(test_id: int, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_test = db.query(models.Test).join(models.Create).filter(models.Create.instructor_id == user.id, models.Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    
    test_items = db.query(models.TestItem).join(models.Construct).filter(models.Construct.test_id == test_id).all()
    for item in test_items:
        if db.query(models.Construct).filter(models.Construct.test_item_id == item.id, models.Construct.test_id != test_id).count() > 0:
            raise HTTPException(status_code=400, detail="Cannot delete test as some test items are being used by other instructors")
    
    db.query(models.Construct).filter(models.Construct.test_id == test_id).delete()
    db.query(models.Create).filter(models.Create.test_id == test_id).delete()
    db.query(models.Test).filter(models.Test.id == test_id).delete()
    db.commit()
    return {"message": "Test deleted"}

# Add Test Item
@router.post("/me/tests/{test_id}/items", response_model=schemas.TestItem)
def add_test_item(test_id: int, test_item: schemas.TestItemCreate, term: str, sy: str, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    new_test_item = models.TestItem(question=test_item.question, answer=test_item.answer)
    db.add(new_test_item)
    db.commit()
    db.refresh(new_test_item)
    construct = models.Construct(instructor_id=user.id, test_item_id=new_test_item.id, test_id=test_id, term=term, sy=sy)
    db.add(construct)
    db.commit()
    return new_test_item

# Edit Test Item
@router.put("/me/tests/{test_id}/items/{test_item_id}", response_model=schemas.TestItem)
def edit_test_item(test_id: int, test_item_id: int, test_item_update: schemas.TestItemCreate, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_test_item = db.query(models.TestItem).join(models.Construct).filter(models.Construct.instructor_id == user.id, models.TestItem.id == test_item_id).first()
    if db_test_item is None:
        raise HTTPException(status_code=404, detail="Test item not found")
    db_test_item.question = test_item_update.question
    db_test_item.answer = test_item_update.answer
    db.commit()
    db.refresh(db_test_item)
    return db_test_item

# Delete Test Item
@router.delete("/me/tests/{test_id}/items/{test_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_item(test_id: int, test_item_id: int, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_test_item = db.query(models.TestItem).join(models.Construct).filter(models.Construct.instructor_id == user.id, models.TestItem.id == test_item_id).first()
    if db_test_item is None:
        raise HTTPException(status_code=404, detail="Test item not found")

    if db.query(models.Construct).filter(models.Construct.test_item_id == test_item_id, models.Construct.test_id != test_id).count() > 0:
        raise HTTPException(status_code=400, detail="Cannot delete test item as it is being used in other tests or by other instructors")

    db.query(models.Construct).filter(models.Construct.test_item_id == test_item_id).delete()
    db.query(models.TestItem).filter(models.TestItem.id == test_item_id).delete()
    db.commit()
    return {"message": "Test item deleted"}

# Publish Test Item
@router.post("/me/tests/{test_id}/items/{test_item_id}/publish")
def publish_test_item(test_id: int, test_item_id: int, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_test_item = db.query(models.TestItem).join(models.Construct).filter(models.Construct.instructor_id == user.id, models.TestItem.id == test_item_id).first()
    if db_test_item is None:
        raise HTTPException(status_code=404, detail="Test item not found")

    # Example logic for publishing the test item (could be making it visible to students)
    db_test_item.published = True
    db.commit()
    return {"message": "Test item published"}

# Generate Test Result
@router.get("/me/tests/{test_id}/results")
def generate_test_result(test_id: int, token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(get_db)):
    user = oauth2.get_current_user(db, token)
    db_test = db.query(models.Test).join(models.Create).filter(models.Create.instructor_id == user.id, models.Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")

    # Example logic for generating test results
    results = db.query(models.Take).filter(models.Take.test_id == test_id).all()
    return {"test_id": test_id, "results": results}
