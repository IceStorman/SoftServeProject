"""renamed fucking column

Revision ID: 6b6f8550bd03
Revises: 27eb623b7b34
Create Date: 2025-02-12 20:36:30.124252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b6f8550bd03'
down_revision: Union[str, None] = '27eb623b7b34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('League', sa.Column('country_id', sa.Integer(), nullable=True))
    op.drop_constraint('League_country_fkey', 'League', type_='foreignkey')
    op.create_foreign_key(None, 'League', 'Country', ['country_id'], ['country_id'])
    op.drop_column('League', 'country')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('League', sa.Column('country', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'League', type_='foreignkey')
    op.create_foreign_key('League_country_fkey', 'League', 'Country', ['country'], ['country_id'])
    op.drop_column('League', 'country_id')
    # ### end Alembic commands ###
