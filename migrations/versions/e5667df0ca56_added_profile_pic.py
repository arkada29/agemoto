"""'added_profile_pic'

Revision ID: e5667df0ca56
Revises: 40e4e015d6db
Create Date: 2022-01-25 20:03:03.752168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5667df0ca56'
down_revision = '40e4e015d6db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    # ### end Alembic commands ###