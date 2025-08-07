from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    journal_entries = relationship("JournalEntry", back_populates="user")


class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    emotion = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="journal_entries")


engine = create_engine('sqlite:///journal.db')
SessionLocal = sessionmaker(bind=engine)
