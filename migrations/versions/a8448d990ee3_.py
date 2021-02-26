"""empty message

Revision ID: a8448d990ee3
Revises: 
Create Date: 2021-02-25 23:53:05.112858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8448d990ee3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sqlite_sequence')
    op.create_unique_constraint(None, 'actors', ['name'])
    op.create_unique_constraint(None, 'movies', ['title'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movies', type_='unique')
    op.drop_constraint(None, 'actors', type_='unique')
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
