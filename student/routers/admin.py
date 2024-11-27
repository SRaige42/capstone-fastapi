from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from .. import models, schemas, oauth2, utils
from ..database import get_db

router = APIRouter(
    prefix="/admins",
    tags=['Admins']
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

# View Assessment
@router.get("/assessments", response_model=List[schemas.Assessment])
def view_assessments(db: Session = Depends(get_db)):
    assessments = db.query(models.Test).all()
    return assessments

# Add Class
@router.post("/classes", response_model=schemas.Course)
def add_class(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Edit/Update Class
@router.put("/classes/{class_id}", response_model=schemas.Course)
def update_class(class_id: int, class_update: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_class = db.query(models.Course).filter(models.Course.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    db_class.update(class_update.dict())
    db.commit()
    return db_class

# Delete Class
@router.delete("/classes/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    db_class = db.query(models.Course).filter(models.Course.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(db_class)
    db.commit()
    return {"message": "Class deleted"}

# View Class
@router.get("/classes/{class_id}", response_model=schemas.Course)
def view_class(class_id: int, db: Session = Depends(get_db)):
    db_class = db.query(models.Course).filter(models.Course.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

# Add Instructor
@router.post("/instructors", response_model=schemas.Instructor)
def add_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    new_instructor = models.Instructor(**instructor.dict())
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)
    return new_instructor

# Edit/Update Instructor
@router.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(instructor_id: int, instructor_update: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db_instructor.update(instructor_update.dict())
    db.commit()
    return db_instructor

# Delete Instructor
@router.delete("/instructors/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db.delete(db_instructor)
    db.commit()
    return {"message": "Instructor deleted"}

# View Faculty
@router.get("/faculty", response_model=List[schemas.Instructor])
def view_faculty(db: Session = Depends(get_db)):
    faculty = db.query(models.Instructor).order_by(models.Instructor.name).all()
    return faculty

# Create Login Credentials for Instructor
@router.post("/instructors/credentials", response_model=schemas.UserOut)
def create_instructor_credentials(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    new_user.password = utils.get_password_hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Add Academic Program
@router.post("/acad_programs", response_model=schemas.AcadProgram)
def add_acad_program(acad_program: schemas.AcadProgramCreate, db: Session = Depends(get_db)):
    new_acad_program = models.AcadProgram(**acad_program.dict())
    db.add(new_acad_program)
    db.commit()
    db.refresh(new_acad_program)
    return new_acad_program

# Edit/Update Academic Program
@router.put("/acad_programs/{acad_program_id}", response_model=schemas.AcadProgram)
def update_acad_program(acad_program_id: int, acad_program_update: schemas.AcadProgramCreate, db: Session = Depends(get_db)):
    db_acad_program = db.query(models.AcadProgram).filter(models.AcadProgram.id == acad_program_id).first()
    if db_acad_program is None:
        raise HTTPException(status_code=404, detail="Academic program not found")
    db_acad_program.update(acad_program_update.dict())
    db.commit()
    return db_acad_program

# Delete Academic Program
@router.delete("/acad_programs/{acad_program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_acad_program(acad_program_id: int, db: Session = Depends(get_db)):
    db_acad_program = db.query(models.AcadProgram).filter(models.AcadProgram.id == acad_program_id).first()
    if db_acad_program is None:
        raise HTTPException(status_code=404, detail="Academic program not found")
    db.delete(db_acad_program)
    db.commit()
    return {"message": "Academic program deleted"}

# View Degree Programs
@router.get("/degree_programs", response_model=List[schemas.AcadProgram])
def view_degree_programs(db: Session = Depends(get_db)):
    degree_programs = db.query(models.AcadProgram).all()
    return degree_programs

# Add Course
@router.post("/courses", response_model=schemas.Course)
def add_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Edit/Update Course
@router.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(course_id: int, course_update: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.update(course_update.dict())
    db.commit()
    return db_course

# Delete Course
@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted"}

# View Course
@router.get("/courses/{course_id}", response_model=schemas.Course)
def view_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course
