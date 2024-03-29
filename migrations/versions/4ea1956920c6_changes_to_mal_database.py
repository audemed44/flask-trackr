"""changes to mal_database

Revision ID: 4ea1956920c6
Revises: 7fd462e440e5
Create Date: 2019-09-25 22:49:56.372036

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4ea1956920c6'
down_revision = '7fd462e440e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_MAL__database_image_url', table_name='mal__database')
    op.drop_index('ix_MAL__database_mal_id', table_name='mal__database')
    op.drop_table('mal__database')
    op.create_table('MAL__database',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('mal_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('anime_type', sa.String(length=20), nullable=True),
    sa.Column('start_date', sa.String(length=50), nullable=True),
    sa.Column('end_date', sa.String(length=50), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('mal_url', sa.String(length=256), nullable=True),
    sa.Column('episodes', sa.Integer(), nullable=True),
    sa.Column('mal_score', sa.String(length=4), nullable=True),
    sa.Column('members', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MAL__database_image_url'), 'MAL__database', ['image_url'], unique=False)
    op.create_index(op.f('ix_MAL__database_mal_id'), 'MAL__database', ['mal_id'], unique=True)
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mal__database',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('rank', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mal_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('title', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('anime_type', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('start_date', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('end_date', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('image_url', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('mal_url', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('episodes', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mal_score', mysql.VARCHAR(length=4), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_MAL__database_mal_id', 'mal__database', ['mal_id'], unique=True)
    op.create_index('ix_MAL__database_image_url', 'mal__database', ['image_url'], unique=False)
    op.drop_index(op.f('ix_MAL__database_mal_id'), table_name='MAL__database')
    op.drop_index(op.f('ix_MAL__database_image_url'), table_name='MAL__database')
    op.drop_table('MAL__database')
    # ### end Alembic commands ###
