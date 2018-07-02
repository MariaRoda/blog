"""empty message

Revision ID: 94573a8c5cfa
Revises: c9c98c9dfd2c
Create Date: 2018-06-25 14:10:47.591769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94573a8c5cfa'
down_revision = 'c9c98c9dfd2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('portada', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'portada')
    # ### end Alembic commands ###
