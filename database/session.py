from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#потім -> azure
DATABASE_URL = "mssql+pyodbc://softprog:Vladik228@softprog.database.windows.net:1433/SportsLib?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

