"""empty message

Revision ID: be94fa8f9e1d
Revises: 6bb5ecea04e2
Create Date: 2017-04-18 17:42:15.987921

"""

# revision identifiers, used by Alembic.
revision = 'be94fa8f9e1d'
down_revision = '6bb5ecea04e2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comparison', sa.Column('article2', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comparison', 'article2')
    # ### end Alembic commands ###
