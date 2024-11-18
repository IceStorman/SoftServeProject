from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#потім -> azure
DATABASE_URL = "postgresql+psycopg2://mac:D100406m@localhost/postgres"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

