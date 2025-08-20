# journal/journal_manager.py

from emotion_classifier import predict_emotion
from models.database import SessionLocal, JournalEntry

# create session
session = SessionLocal()

def save_entry(content, user_id, emotion=None):
    if not emotion:
        emotion, confidence = predict_emotion(content)

    entry = JournalEntry(content=content, emotion=emotion, user_id=user_id)
    session.add(entry)
    session.commit()
    return entry

def get_all_entries(user_id):
    return session.query(JournalEntry).filter_by(user_id=user_id).order_by(JournalEntry.timestamp.desc()).all()

def get_entry_by_id(entry_id, user_id):
    return session.query(JournalEntry).filter_by(id=entry_id, user_id=user_id).first()

def delete_entry(entry_id, user_id):
    entry = session.query(JournalEntry).filter_by(id=entry_id, user_id=user_id).first()
    if entry:
        session.delete(entry)
        session.commit()
        return True
    return False
