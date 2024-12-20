from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#потім -> azure
DATABASE_URL = "postgresql://postgres:Vladik@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

