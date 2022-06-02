"""'like'

Revision ID: 241b87a9076a
Revises: 2a3581abf356
Create Date: 2022-02-24 11:25:51.268191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '241b87a9076a'
down_revision = '2a3581abf356'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likepost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anjing', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likepost')
    # ### end Alembic commands ###