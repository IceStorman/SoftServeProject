from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#потім -> azure
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres-local"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

