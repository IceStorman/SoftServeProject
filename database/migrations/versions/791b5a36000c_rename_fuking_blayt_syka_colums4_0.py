"""rename FUKING BLAYT SYKA colums4.0

Revision ID: 791b5a36000c
Revises: 410e5fdf3a6e
Create Date: 2025-02-19 22:00:03.540755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '791b5a36000c'
down_revision: Union[str, None] = '410e5fdf3a6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('League', sa.Column('country_id', sa.Integer(), nullable=True))
    op.drop_constraint('League_country_fkey', 'League', type_='foreignkey')
    op.create_foreign_key('League_country_id_fkey', 'League', 'Country', ['country_id'], ['country_id'])
    op.drop_column('League', 'country')
    op.add_column('TeamIndex', sa.Column('league_id', sa.Integer(), nullable=True))
    op.drop_constraint('TeamIndex_league_fkey', 'TeamIndex', type_='foreignkey')
    op.create_foreign_key('TeamIndex_league_id_fkey', 'TeamIndex', 'League', ['league_id'], ['league_id'])
    op.drop_column('TeamIndex', 'league')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TeamIndex', sa.Column('league', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint('TeamIndex_league_id_fkey', 'TeamIndex', type_='foreignkey')
    op.create_foreign_key('TeamIndex_league_fkey', 'TeamIndex', 'League', ['league'], ['league_id'])
    op.drop_column('TeamIndex', 'league_id')
    op.add_column('League', sa.Column('country', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint('League_country_id_fkey', 'League', type_='foreignkey')
    op.create_foreign_key('League_country_fkey', 'League', 'Country', ['country'], ['country_id'])
    op.drop_column('League', 'country_id')
    # ### end Alembic commands ###