"""new_column_title_for_streams

Revision ID: 8d79017f4a3e
Revises: 300803741dca
Create Date: 2025-03-07 22:35:17.663459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d79017f4a3e'
down_revision: Union[str, None] = '300803741dca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new Column
    op.add_column('Streams', sa.Column('title', sa.String(), nullable=True))

    # Delete Column start_time
    op.drop_column('Streams', 'start_time')

    # Add again with right type
    op.add_column('Streams', sa.Column('start_time', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Delete new Column start_time
    op.drop_column('Streams', 'start_time')

    # Add with old type INTEGER
    op.add_column('Streams', sa.Column('start_time', sa.INTEGER(), nullable=True))

    # Delete Column title
    op.drop_column('Streams', 'title')
