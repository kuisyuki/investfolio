import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Get DATABASE_URL from environment
raw_database_url = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://portfolio_user:portfolio_pass@portfolio_mysql:3306/portfolio?charset=utf8mb4",
)

# Ensure we're using pymysql driver for MySQL
if raw_database_url.startswith("mysql://"):
    DATABASE_URL = raw_database_url.replace("mysql://", "mysql+pymysql://", 1)
    # Add charset if not present
    if "charset=" not in DATABASE_URL:
        DATABASE_URL += "?charset=utf8mb4" if "?" not in DATABASE_URL else "&charset=utf8mb4"
else:
    DATABASE_URL = raw_database_url

# Create Base first
Base = declarative_base()

# Lazy initialization of engine and SessionLocal
_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _SessionLocal


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
