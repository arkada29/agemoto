"""'add_unique_upcomings'

Revision ID: efff90552a5d
Revises: d4d1a8b9c2b7
Create Date: 2022-02-02 21:32:14.404134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efff90552a5d'
down_revision = 'd4d1a8b9c2b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'upcomings', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'upcomings', type_='unique')
    # ### end Alembic commands ###
