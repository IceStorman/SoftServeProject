# воно виглядає так, ніби не має взагалі існувати
from sqlalchemy_utils import database_exists, create_database


from models.base import Base
from session import engine

#from session import SessionLocal

def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
#де це поки що має викликатись?
init_db()

#db = SessionLocal()
#new_user = create_user(db, "test", "test@gmail.com",
#                       "passwrd", 2, 3, "dark?")