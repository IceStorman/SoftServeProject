"""initial tables

Revision ID: c07f730a359d
Revises: 
Create Date: 2024-11-12 22:14:33.576327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c07f730a359d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('News',
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('blob_id', sa.String(), nullable=True),
    sa.Column('interest_rate', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('news_id')
    )
    op.create_table('Sports',
    sa.Column('sport_id', sa.Integer(), nullable=False),
    sa.Column('sport_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('sport_id')
    )
    op.create_table('Users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('sport_pref_key', sa.Integer(), nullable=True),
    sa.Column('club_pref_key', sa.Integer(), nullable=True),
    sa.Column('theme', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('ClubPreferences',
    sa.Column('pref_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('preferences', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['users_id'], ['Users.user_id'], ),
    sa.PrimaryKeyConstraint('pref_id')
    )
    op.create_table('SportsIndex',
    sa.Column('index_id', sa.Integer(), nullable=False),
    sa.Column('sport_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sport_id'], ['Sports.sport_id'], ),
    sa.PrimaryKeyConstraint('index_id')
    )
    op.create_table('Streams',
    sa.Column('stream_id', sa.Integer(), nullable=False),
    sa.Column('stream_url', sa.String(), nullable=True),
    sa.Column('start_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('sport_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sport_id'], ['Sports.sport_id'], ),
    sa.PrimaryKeyConstraint('stream_id')
    )
    op.create_table('UserPreferences',
    sa.Column('user_pref_id', sa.Integer(), nullable=False),
    sa.Column('sports_id', sa.Integer(), nullable=True),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sports_id'], ['Sports.sport_id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['Users.user_id'], ),
    sa.PrimaryKeyConstraint('user_pref_id')
    )
    op.create_table('BlobIndex',
    sa.Column('blob_id', sa.Integer(), nullable=False),
    sa.Column('sports_index_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['sports_index_id'], ['SportsIndex.index_id'], ),
    sa.PrimaryKeyConstraint('blob_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('BlobIndex')
    op.drop_table('UserPreferences')
    op.drop_table('Streams')
    op.drop_table('SportsIndex')
    op.drop_table('ClubPreferences')
    op.drop_table('Users')
    op.drop_table('Sports')
    op.drop_table('News')
    # ### end Alembic commands ###
