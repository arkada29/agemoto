"""'add_unique_upcomings'

Revision ID: 41b681be85b2
Revises: efff90552a5d
Create Date: 2022-02-02 21:38:25.367285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41b681be85b2'
down_revision = 'efff90552a5d'
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