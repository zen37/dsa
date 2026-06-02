from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings, sqlalchemy_database_url

settings = get_settings()

engine = create_engine(sqlalchemy_database_url(settings.database_url), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
