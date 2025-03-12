"""add trigger to update interactions

Revision ID: b8d66f9b009f
Revises: 0d93e8ea82b6
Create Date: 2025-03-07 19:16:49.393740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8d66f9b009f'
down_revision: Union[str, None] = '0d93e8ea82b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION update_news_interactions_func()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.type_of_interaction = 1 THEN
            UPDATE public."News"
            SET likes = likes + 1 WHERE news_id = NEW.news_id;
        ELSIF NEW.type_of_interaction = 2 THEN
            UPDATE public."News"
            SET likes = likes - 1 WHERE news_id = NEW.news_id;
        ELSIF NEW.type_of_interaction = 3 THEN
            UPDATE public."News"
            SET views = views + 1 WHERE news_id = NEW.news_id;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER update_news_interactions
    AFTER INSERT OR UPDATE ON public."InteractionsWithNews"
    FOR EACH ROW
    EXECUTE FUNCTION update_news_interactions_func();
    """)


def downgrade() -> None:
    op.execute("""
    DROP TRIGGER IF EXISTS update_news_interactions ON public."InteractionsWithNews";
    DROP FUNCTION IF EXISTS update_news_interactions_func();
    """)
