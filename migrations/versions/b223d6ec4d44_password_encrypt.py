"""'Password_encrypt'

Revision ID: b223d6ec4d44
Revises: 9e71cfc2cd91
Create Date: 2022-01-23 13:45:08.278933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b223d6ec4d44'
down_revision = '9e71cfc2cd91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
