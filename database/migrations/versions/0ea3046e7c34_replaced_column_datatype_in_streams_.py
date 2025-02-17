from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea3046e7c34'
down_revision = '410e5fdf3a6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Використовуємо to_timestamp() для коректного перетворення
    op.alter_column('Streams', 'start_time',
                    existing_type=sa.INTEGER(),
                    type_=sa.DateTime(),
                    existing_nullable=True,
                    postgresql_using="TO_TIMESTAMP(start_time)")


def downgrade() -> None:
    # Якщо потрібно повернути назад у UNIX-час (INTEGER)
    op.alter_column('Streams', 'start_time',
                    existing_type=sa.DateTime(),
                    type_=sa.INTEGER(),
                    existing_nullable=True,
                    postgresql_using="EXTRACT(EPOCH FROM start_time)::INTEGER")
