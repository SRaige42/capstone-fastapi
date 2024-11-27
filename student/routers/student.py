from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from .. import models, schemas, oauth2, utils
from ..database import get_db

router = APIRouter(
    prefix="/students",
    tags=['Students']
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

# Take Assessment
@router.post("/{student_id}/assessments/{test_id}/take")
def take_assessment(student_id: int, test_id: int, term: str, sy: str, db: Session = Depends(get_db)):
    take = models.Take(student_id=student_id, test_id=test_id, term=term, sy=sy)
    db.add(take)
    db.commit()
    return {"message": "Assessment started"}

# Answer Test Item
@router.post("/{student_id}/test_items/{test_item_id}/answer")
def answer_test_item(student_id: int, test_item_id: int, term: str, sy: str, answer: str, db: Session = Depends(get_db)):
    answer_record = models.Answer(student_id=student_id, test_item_id=test_item_id, term=term, sy=sy, answer=answer)
    db.add(answer_record)
    db.commit()
    return {"message": "Answer recorded"}

# Display Enrolled Courses and Academic Program
@router.get("/{student_id}/enrollments", response_model=schemas.StudentEnrollment)
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    enrollments = db.query(models.Enroll).filter(models.Enroll.student_id == student_id).all()
    acad_program = db.query(models.AcadProgram).filter(models.AcadProgram.id == student.acad_program_id).first()
    return {"student": student, "enrollments": enrollments, "acad_program": acad_program}
