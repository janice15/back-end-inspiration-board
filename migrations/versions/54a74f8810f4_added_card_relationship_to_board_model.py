"""added card relationship to board model 


Revision ID: 54a74f8810f4
Revises: e520cf29e1a3
Create Date: 2023-06-27 11:48:09.786329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54a74f8810f4'
down_revision = 'e520cf29e1a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('owner', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('card_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(length=80), nullable=True),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('board')
    # ### end Alembic commands ###
