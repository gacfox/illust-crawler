from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

DATABASE_URL = 'sqlite:///crawler.db'
engine = create_engine(DATABASE_URL, echo=True, future=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
