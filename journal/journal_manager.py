# journal/journal_manager.py

from models.database import session, JournalEntry

def save_entry(title, content, mood=None):
    entry = JournalEntry(title=title, content=content, mood=mood)
    session.add(entry)
    session.commit()
    return entry

def get_all_entries():
    return session.query(JournalEntry).order_by(JournalEntry.created_at.desc()).all()

def get_entry_by_id(entry_id):
    return session.query(JournalEntry).filter(JournalEntry.id == entry_id).first()

def delete_entry(entry_id):
    entry = session.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if entry:
        session.delete(entry)
        session.commit()
        return True
    return False
