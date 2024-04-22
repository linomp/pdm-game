import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATA_DIR = "mvp/data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

engine = create_engine(
    f"sqlite:///{DATA_DIR}/pdm_game.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
