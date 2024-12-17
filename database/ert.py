import pyodbc

server = 'softprog.database.windows.net'
database = 'SportsLib'
username = 'softprog'
password = 'Vladik228'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}")
cursor = conn.cursor()
print("Connected!")

#from sqlalchemy import create_engine
#DATABASE_URL = "mssql+pyodbc://softprog:Vladik228@softprog.database.windows.net:1433/SportsLib?driver=ODBC+Driver+17+for+SQL+Server"
#engine = create_engine(DATABASE_URL)
