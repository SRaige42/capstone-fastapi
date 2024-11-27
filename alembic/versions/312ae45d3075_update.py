"""Update table constraints and rename conflicting tables

Revision ID: 312ae45d3075
Revises: 168e3bb0c34c
Create Date: 2024-11-27 14:45:21.637891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'n312ae45d3075'
down_revision: Union[str, None] = '168e3bb0c34c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop tables if they exist to avoid duplicates
    op.execute("DROP TABLE IF EXISTS acad_program CASCADE")
    op.execute("DROP TABLE IF EXISTS student CASCADE")
    op.execute("DROP TABLE IF EXISTS course CASCADE")
    op.execute("DROP TABLE IF EXISTS lesson CASCADE")
    op.execute("DROP TABLE IF EXISTS instructor CASCADE")
    op.execute("DROP TABLE IF EXISTS test CASCADE")
    op.execute("DROP TABLE IF EXISTS test_item CASCADE")
    op.execute("DROP TABLE IF EXISTS study CASCADE")
    op.execute("DROP TABLE IF EXISTS enroll CASCADE")
    op.execute("DROP TABLE IF EXISTS offer CASCADE")
    op.execute("DROP TABLE IF EXISTS teach CASCADE")
    op.execute("DROP TABLE IF EXISTS test_create CASCADE")
    op.execute("DROP TABLE IF EXISTS construct CASCADE")
    op.execute("DROP TABLE IF EXISTS test_take CASCADE")
    op.execute("DROP TABLE IF EXISTS test_answer CASCADE")
    op.execute("DROP TABLE IF EXISTS course_have CASCADE")
    op.execute("DROP TABLE IF EXISTS lesson_from CASCADE")
    op.execute("DROP TABLE IF EXISTS lesson_make CASCADE")

    # Create acad_program table
    op.create_table(
        'acad_program',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('acad_name', sa.String, nullable=False, index=True)
    )

    # Create student table
    op.create_table(
        'student',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('student_id', sa.String, nullable=False, index=True),
        sa.Column('acad_program_id', sa.Integer, sa.ForeignKey('acad_program.id'), nullable=False)
    )

    # Create course table
    op.create_table(
        'course',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('code', sa.String, nullable=False, index=True),
        sa.Column('title', sa.String, nullable=False, index=True)
    )

    # Create lesson table
    op.create_table(
        'lesson',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('title', sa.String, nullable=False, index=True)
    )

    # Create instructor table
    op.create_table(
        'instructor',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('name', sa.String, nullable=False, index=True)
    )

    # Create test table
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('date', sa.Date, nullable=False)
    )

    # Create test_item table
    op.create_table(
        'test_item',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True),
        sa.Column('question', sa.String, nullable=False, index=True),
        sa.Column('answer', sa.String, nullable=False, index=True)
    )

    # Create study table
    op.create_table(
        'study',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True, nullable=False),
        sa.Column('acad_program_id', sa.Integer, sa.ForeignKey('acad_program.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create enroll table
    op.create_table(
        'enroll',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True, nullable=False),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create offer table
    op.create_table(
        'offer',
        sa.Column('acad_program_id', sa.Integer, sa.ForeignKey('acad_program.id'), primary_key=True, nullable=False),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True, nullable=False),
        sa.Column('curriculum_yr', sa.String, primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False)
    )

    # Create teach table
    op.create_table(
        'teach',
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructor.id'), primary_key=True, nullable=False),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create test_creation table
    op.create_table(
        'test_creation',
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructor.id'), primary_key=True, nullable=False),
        sa.Column('test_id', sa.Integer, sa.ForeignKey('test.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create test_construction table
    op.create_table(
        'test_construction',
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructor.id'), primary_key=True, nullable=False),
        sa.Column('test_item_id', sa.Integer, sa.ForeignKey('test_item.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create test_participation table
    op.create_table(
        'test_participation',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True, nullable=False),
        sa.Column('test_id', sa.Integer, sa.ForeignKey('test.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create test_response table
    op.create_table(
        'test_response',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True, nullable=False),
        sa.Column('test_item_id', sa.Integer, sa.ForeignKey('test_item.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create course_content table
    op.create_table(
        'course_content',
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True, nullable=False),
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create lesson_test table
    op.create_table(
        'lesson_test',
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id'), primary_key=True, nullable=False),
        sa.Column('test_id', sa.Integer, sa.ForeignKey('test.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

    # Create lesson_item table
    op.create_table(
        'lesson_item',
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id'), primary_key=True, nullable=False),
        sa.Column('test_item_id', sa.Integer, sa.ForeignKey('test_item.id'), primary_key=True, nullable=False),
        sa.Column('term', sa.String, nullable=False),
        sa.Column('sy', sa.String, nullable=False)
    )

def downgrade() -> None:
    # Drop all tables in reverse order of creation to handle dependencies
    op.drop_table('lesson_item')
    op.drop_table('lesson_test')
    op.drop_table('course_content')
    op.drop_table('test_response')
    op.drop_table('test_participation')
    op.drop_table('test_construction')
    op.drop_table('test_creation')
    op.drop_table('teach')
    op.drop_table('offer')
    op.drop_table('enroll')
    op.drop_table('study')
    op.drop_table('test_item')
    op.drop_table('test')
    op.drop_table('instructor')
    op.drop_table('lesson')
    op.drop_table('course')
    op.drop_table('student')
    op.drop_table('acad_program')