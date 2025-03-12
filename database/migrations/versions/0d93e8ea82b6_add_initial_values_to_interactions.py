"""add initial values to interactions

Revision ID: 0d93e8ea82b6
Revises: 47f635e8f66a
Create Date: 2025-03-07 18:17:00.515199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d93e8ea82b6'
down_revision: Union[str, None] = 'a808a1ce833e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO "InteractionTypes" (interaction_type_id, name) VALUES
        (1, 'like'),
        (2, 'dislike'),
        (3, 'read'),
        (4, 'open'),
        (5, 'comment');
    """)
    op.execute("""
    CREATE OR REPLACE FUNCTION update_news_interactions_func()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.interaction_type = 1 THEN
            UPDATE public."News"
            SET likes = likes + 1 WHERE news_id = NEW.news_id;
        ELSIF NEW.interaction_type = 2 THEN
            UPDATE public."News"
            SET likes = likes - 1 WHERE news_id = NEW.news_id;
        ELSIF NEW.interaction_type = 3 THEN
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
    op.execute("""
        DELETE FROM "InteractionsWithNews" 
        WHERE interaction_type IN (1, 2, 3, 4, 5);
    """)
    op.execute("""
        DELETE FROM "InteractionTypes" WHERE interaction_type_id IN (1, 2, 3, 4, 5);
    """)


