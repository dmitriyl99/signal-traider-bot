from sqlalchemy import create_engine

from app.config import config

engine = create_engine(config.DATABASE_URL)
