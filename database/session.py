from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mssql+pyodbc://softprog:Vladik228@softprog.database.windows.net:1433/SportsLib?driver=ODBC+Driver+17+for+SQL+Server"
#DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres-local"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

