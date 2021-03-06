"""'change_about_author'

Revision ID: 40e4e015d6db
Revises: 5425b1d612c4
Create Date: 2022-01-25 19:28:41.967332

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '40e4e015d6db'
down_revision = '5425b1d612c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'about_author')
    op.add_column('users', sa.Column('about_author', sa.Text(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'about_author')
    op.add_column('posts', sa.Column('about_author', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
