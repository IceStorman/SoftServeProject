"""hai_bog_vrytue_this_migration

Revision ID: df7bd7ffe913
Revises: 6fd617981728
Create Date: 2025-03-08 14:30:15.472463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df7bd7ffe913'
down_revision: Union[str, None] = '6fd617981728'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('GamesStatuses',
    sa.Column('game_status_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('game_status_id')
    )
    op.create_table('Games',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('league_id', sa.Integer(), nullable=True),
    sa.Column('sport_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('team_away_id', sa.Integer(), nullable=True),
    sa.Column('team_home_id', sa.Integer(), nullable=True),
    sa.Column('score_away_team', sa.Integer(), nullable=True),
    sa.Column('score_home_team', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('api_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['Country.country_id'], ),
    sa.ForeignKeyConstraint(['league_id'], ['League.league_id'], ),
    sa.ForeignKeyConstraint(['sport_id'], ['Sports.sport_id'], ),
    sa.ForeignKeyConstraint(['team_away_id'], ['TeamIndex.team_index_id'], ),
    sa.ForeignKeyConstraint(['team_home_id'], ['TeamIndex.team_index_id'], ),
    sa.ForeignKeyConstraint(['type'], ['GamesStatuses.game_status_id'], ),
    sa.PrimaryKeyConstraint('game_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Games')
    op.drop_table('GamesStatuses')
    # ### end Alembic commands ###
