from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    student_id: Optional[str] = None

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class AcadProgramBase(BaseModel):
    acad_name: str

class AcadProgramCreate(AcadProgramBase):
    pass

class AcadProgram(AcadProgramBase):
    id: int

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    student_id: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    code: str
    title: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int

    class Config:
        from_attributes = True

class InstructorBase(BaseModel):
    name: str

class InstructorCreate(InstructorBase):
    pass

class Instructor(InstructorBase):
    id: int

    class Config:
        from_attributes = True

class TestBase(BaseModel):
    date: date

class TestCreate(TestBase):
    pass

class Test(TestBase):
    id: int

    class Config:
        from_attributes = True

class TestItemBase(BaseModel):
    question: str
    answer: str

class TestItemCreate(TestItemBase):
    pass

class TestItem(TestItemBase):
    id: int

    class Config:
        from_attributes = True

class Assessment(BaseModel):
    test: Test
    items: List[TestItem]

    class Config:
        from_attributes = True

class StudyBase(BaseModel):
    student_id: int
    acad_program_id: int
    term: str
    sy: str

class Study(StudyBase):
    class Config:
        from_attributes = True

class EnrollBase(BaseModel):
    student_id: int
    course_id: int
    term: str
    sy: str

class Enroll(EnrollBase):
    class Config:
        from_attributes = True

class OfferBase(BaseModel):
    acad_program_id: int
    course_id: int
    curriculum_yr: str
    term: str

class Offer(OfferBase):
    class Config:
        from_attributes = True

class TeachBase(BaseModel):
    instructor_id: int
    course_id: int
    term: str
    sy: str

class Teach(TeachBase):
    class Config:
        from_attributes = True

class CreateBase(BaseModel):
    instructor_id: int
    test_id: int
    term: str
    sy: str

class Create(CreateBase):
    class Config:
        from_attributes = True

class ConstructBase(BaseModel):
    instructor_id: int
    test_item_id: int
    term: str
    sy: str

class Construct(ConstructBase):
    class Config:
        from_attributes = True

class TakeBase(BaseModel):
    student_id: int
    test_id: int
    term: str
    sy: str

class Take(TakeBase):
    class Config:
        from_attributes = True

class AnswerBase(BaseModel):
    student_id: int
    test_item_id: int
    term: str
    sy: str

class Answer(AnswerBase):
    class Config:
        from_attributes = True

class HaveBase(BaseModel):
    course_id: int
    lesson_id: int
    term: str
    sy: str

class Have(HaveBase):
    class Config:
        from_attributes = True

class FromBase(BaseModel):
    lesson_id: int
    test_id: int
    term: str
    sy: str

class From(FromBase):
    class Config:
        from_attributes = True

class MakeBase(BaseModel):
    lesson_id: int
    test_item_id: int
    term: str
    sy: str

class Make(MakeBase):
    class Config:
        from_attributes = True

class StudentEnrollment(BaseModel):
    student: Student
    enrollments: List[Course]
    acad_program: AcadProgram

    class Config:
        from_attributes = True
