"""empty message

Revision ID: 4b6108d98008
Revises: 
Create Date: 2017-05-11 23:29:07.514000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4b6108d98008'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'body',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('articles', 'title',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('comments', 'body',
               existing_type=mysql.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'body',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('articles', 'title',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('articles', 'body',
               existing_type=mysql.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
