"""trigger for comment delete

Revision ID: 53e757c5a752
Revises: 4b6df95d954f
Create Date: 2025-03-28 17:10:27.986859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53e757c5a752'
down_revision: Union[str, None] = '4b6df95d954f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
    CREATE OR REPLACE FUNCTION delete_comment_and_replies()
    RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM "Comments" WHERE parent_comment_id = OLD.comment_id;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER trigger_delete_comment
    BEFORE DELETE ON "Comments"
    FOR EACH ROW
    EXECUTE FUNCTION delete_comment_and_replies();
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TRIGGER IF EXISTS trigger_delete_comment ON \"Comments\";")

    op.execute("DROP FUNCTION IF EXISTS delete_comment_and_replies;")
    # ### end Alembic commands ###
