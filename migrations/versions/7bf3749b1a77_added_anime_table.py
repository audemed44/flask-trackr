"""added anime table

Revision ID: 7bf3749b1a77
Revises: a3323f3d6fe2
Create Date: 2019-09-20 20:08:52.809344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bf3749b1a77'
down_revision = 'a3323f3d6fe2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('mal_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('episodes', sa.Integer(), nullable=True),
    sa.Column('mal_score', sa.String(), nullable=True),
    sa.Column('my_score', sa.String(), nullable=True),
    sa.Column('synopsis', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_anime_mal_id'), 'anime', ['mal_id'], unique=True)
    op.create_index(op.f('ix_top_anime_mal_id'), 'top_anime', ['mal_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_top_anime_mal_id'), table_name='top_anime')
    op.drop_index(op.f('ix_anime_mal_id'), table_name='anime')
    op.drop_table('anime')
    # ### end Alembic commands ###
