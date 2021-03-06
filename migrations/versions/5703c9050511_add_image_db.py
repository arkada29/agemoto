"""'add_image_db'

Revision ID: 5703c9050511
Revises: 5f0cf26b8a21
Create Date: 2022-02-09 11:28:39.842824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5703c9050511'
down_revision = '5f0cf26b8a21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=50), nullable=False),
    sa.Column('thumbnail', sa.String(length=50), nullable=False),
    sa.Column('file_size', sa.Integer(), nullable=False),
    sa.Column('file_width', sa.Integer(), nullable=False),
    sa.Column('file_height', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
