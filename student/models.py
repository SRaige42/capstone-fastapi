from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class AcadProgram(Base):
    __tablename__ = "acad_program"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    acad_name = Column(String, index=True, nullable=False)
    students = relationship("Student", back_populates="acad_program")
    studies = relationship("Study", back_populates="acad_program")
    offers = relationship("Offer", back_populates="acad_program")

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, index=True, nullable=False)
    acad_program_id = Column(Integer, ForeignKey('acad_program.id'), nullable=False)
    acad_program = relationship("AcadProgram", back_populates="students")
    studies = relationship("Study", back_populates="student")
    enrollments = relationship("Enroll", back_populates="student")
    takes = relationship("Take", back_populates="student")
    answers = relationship("Answer", back_populates="student")

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    enrollments = relationship("Enroll", back_populates="course")
    offers = relationship("Offer", back_populates="course")
    has_lessons = relationship("Have", back_populates="course")
    teaches = relationship("Teach", back_populates="course")

class Lesson(Base):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    has_lessons = relationship("Have", back_populates="lesson")
    from_tests = relationship("From", back_populates="lesson")
    makes_test_items = relationship("Make", back_populates="lesson")

class Instructor(Base):
    __tablename__ = "instructor"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    teaches = relationship("Teach", back_populates="instructor")
    creates = relationship("Create", back_populates="instructor")
    constructs = relationship("Construct", back_populates="instructor")

class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    creates = relationship("Create", back_populates="test")
    takes = relationship("Take", back_populates="test")
    from_tests = relationship("From", back_populates="test")

class TestItem(Base):
    __tablename__ = "test_item"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String, index=True, nullable=False)
    answer = Column(String, index=True, nullable=False)
    constructs = relationship("Construct", back_populates="test_item")
    answers = relationship("Answer", back_populates="test_item")
    makes_test_items = relationship("Make", back_populates="test_item")

class Study(Base):
    __tablename__ = "study"
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    acad_program_id = Column(Integer, ForeignKey('acad_program.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    student = relationship("Student", back_populates="studies")
    acad_program = relationship("AcadProgram", back_populates="studies")

class Enroll(Base):
    __tablename__ = "enroll"
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Offer(Base):
    __tablename__ = "offer"
    acad_program_id = Column(Integer, ForeignKey('acad_program.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    curriculum_yr = Column(String, primary_key=True, nullable=False)
    term = Column(String, nullable=False)
    acad_program = relationship("AcadProgram", back_populates="offers")
    course = relationship("Course", back_populates="offers")

class Teach(Base):
    __tablename__ = "teach"
    instructor_id = Column(Integer, ForeignKey('instructor.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    instructor = relationship("Instructor", back_populates="teaches")
    course = relationship("Course", back_populates="teaches")

class TestCreate(Base):
    __tablename__ = "test_create"
    instructor_id = Column(Integer, ForeignKey('instructor.id'), primary_key=True)
    test_id = Column(Integer, ForeignKey('test.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    instructor = relationship("Instructor", back_populates="creates")
    test = relationship("Test", back_populates="creates")

class Construct(Base):
    __tablename__ = "construct"
    instructor_id = Column(Integer, ForeignKey('instructor.id'), primary_key=True)
    test_item_id = Column(Integer, ForeignKey('test_item.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    instructor = relationship("Instructor", back_populates="constructs")
    test_item = relationship("TestItem", back_populates="constructs")

class TestTake(Base):
    __tablename__ = "test_take"
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    test_id = Column(Integer, ForeignKey('test.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    student = relationship("Student", back_populates="takes")
    test = relationship("Test", back_populates="takes")

class TestAnswer(Base):
    __tablename__ = "test_answer"
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    test_item_id = Column(Integer, ForeignKey('test_item.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    student = relationship("Student", back_populates="answers")
    test_item = relationship("TestItem", back_populates="answers")

class CourseHave(Base):
    __tablename__ = "course_have"
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    course = relationship("Course", back_populates="has_lessons")
    lesson = relationship("Lesson", back_populates="has_lessons")

class LessonFrom(Base):
    __tablename__ = "lesson_from"
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True)
    test_id = Column(Integer, ForeignKey('test.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    lesson = relationship("Lesson", back_populates="from_tests")
    test = relationship("Test", back_populates="from_tests")

class LessonMake(Base):
    __tablename__ = "lesson_make"
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True)
    test_item_id = Column(Integer, ForeignKey('test_item.id'), primary_key=True)
    term = Column(String, nullable=False)
    sy = Column(String, nullable=False)
    lesson = relationship("Lesson", back_populates="makes_test_items")
    test_item = relationship("TestItem", back_populates="makes_test_items")
