"""(add_updated_on_posts)

Revision ID: 0b0311c924e0
Revises: 70f34b334c25
Create Date: 2022-05-25 12:58:49.948103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b0311c924e0'
down_revision = '70f34b334c25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('updated', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'updated')
    # ### end Alembic commands ###
