from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL database connection URL
DATABASE_URL = "postgresql://postgres:postgres@db:5432/vectordb"

# Create a SQLAlchemy engine for database connections
engine = create_engine(DATABASE_URL)

# Create a session factory for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
