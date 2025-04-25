from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# สร้าง connection string
connection_string = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="P@ssw0rd",
    host="localhost",
    database="FASTAPI",
    query={"driver": "ODBC Driver 17 for SQL Server"}
)

# สร้าง engine
engine = create_engine(connection_string)

# สร้าง session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# สร้าง Base สำหรับ ORM model mapping
Base = declarative_base()
