from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=40,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=180
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)