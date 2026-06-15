# database.py
# Database Configuration and Connection Handler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import settings
from backend.db.models import Base

# sqlite URL config
SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.DB_PATH}"

# create engine with check_same_thread disabled for SQLite multi-thread requests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates all metadata tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency injector for database session handle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
