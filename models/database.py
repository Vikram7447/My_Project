from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from flask_login import UserMixin
import datetime

Base = declarative_base()

class User(Base, UserMixin):  # Added UserMixin for Flask-Login
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    # Relationship to Journal Entries
    journal_entries = relationship("JournalEntry", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))  # Title field
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    emotion = Column(String(50))  # Emotion detected by GoEmotions model
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship back to User
    user = relationship("User", back_populates="journal_entries")

    def __repr__(self):
        return f"<JournalEntry(id={self.id}, title='{self.title}', emotion='{self.emotion}', user_id={self.user_id})>"


# SQLite Database
engine = create_engine('sqlite:///journal.db', echo=False)

# Session Factory
SessionLocal = sessionmaker(bind=engine)
