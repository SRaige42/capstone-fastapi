"""Create initial tables

Revision ID: 168e3bb0c34c
Revises: 
Create Date: 2024-11-27 14:24:21.637891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '168e3bb0c34c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create acad_program table
    op.create_table(
        'acad_program',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('acad_name', sa.String, index=True)
    )

    # Create student table
    op.create_table(
        'student',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('student_id', sa.String, index=True),
        sa.Column('acad_program_id', sa.Integer, sa.ForeignKey('acad_program.id'))
    )

    # Create course table
    op.create_table(
        'course',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('code', sa.String, index=True),
        sa.Column('title', sa.String, index=True)
    )

    # Create lesson table
    op.create_table(
        'lesson',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String, index=True)
    )

    # Create instructor table
    op.create_table(
        'instructor',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, index=True)
    )

    # Create test table
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('date', sa.Date)
    )

    # Create test_item table
    op.create_table(
        'test_item',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('question', sa.String, index=True),
        sa.Column('answer', sa.String, index=True)
    )

    # Create study table
    op.create_table(
        'study',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True),
        sa.Column('acad_program_id', sa.Integer, sa.ForeignKey('acad_program.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create enroll table
    op.create_table(
        'enroll',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create offer table
    op.create_table(
        'offer',
        sa.Column('acad_program_id', sa.Integer, sa.ForeignKey('acad_program.id'), primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True),
        sa.Column('curriculum_yr', sa.String, primary_key=True),
        sa.Column('term', sa.String)
    )

    # Create teach table
    op.create_table(
        'teach',
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructor.id'), primary_key=True),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create create table
    op.create_table(
        'create',
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructor.id'), primary_key=True),
        sa.Column('test_id', sa.Integer, sa.ForeignKey('test.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create construct table
    op.create_table(
        'construct',
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructor.id'), primary_key=True),
        sa.Column('test_item_id', sa.Integer, sa.ForeignKey('test_item.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create take table
    op.create_table(
        'take',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True),
        sa.Column('test_id', sa.Integer, sa.ForeignKey('test.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create answer table
    op.create_table(
        'answer',
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id'), primary_key=True),
        sa.Column('test_item_id', sa.Integer, sa.ForeignKey('test_item.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create have table
    op.create_table(
        'have',
        sa.Column('course_id', sa.Integer, sa.ForeignKey('course.id'), primary_key=True),
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create from table
    op.create_table(
        'from',
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id'), primary_key=True),
        sa.Column('test_id', sa.Integer, sa.ForeignKey('test.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

    # Create make table
    op.create_table(
        'make',
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey('lesson.id'), primary_key=True),
        sa.Column('test_item_id', sa.Integer, sa.ForeignKey('test_item.id'), primary_key=True),
        sa.Column('term', sa.String),
        sa.Column('sy', sa.String)
    )

def downgrade() -> None:
    # Drop all tables in reverse order of creation to handle dependencies
    op.drop_table('make')
    op.drop_table('from')
    op.drop_table('have')
    op.drop_table('answer')
    op.drop_table('take')
    op.drop_table('construct')
    op.drop_table('create')
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
