# models/database.py

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Setup database
engine = create_engine('sqlite:///journal.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Journal Entry Model
class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    mood = Column(String(50))  # Optional: sad, happy, anxious
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)
