from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from models.database import Base, engine, JournalEntry, User
from utils.helpers import sanitize_input
from chatbot.chatbot_engine import get_chatbot_response  # now uses local Transformers model

import os

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

# SQLAlchemy session
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
session = Session()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = sanitize_input(request.form['username'])
        password = request.form['password']

        if session.query(User).filter_by(username=username).first():
            flash('Username already exists. Try another.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = sanitize_input(request.form['username'])
        password = request.form['password']

        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user.username)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---------------- Journal Routes ----------------

@app.route('/journal')
@login_required
def journal():
    entries = session.query(JournalEntry).filter_by(user_id=current_user.id)\
        .order_by(JournalEntry.timestamp.desc()).all()
    return render_template('journal.html', entries=entries)

@app.route('/new_journal', methods=['GET', 'POST'])
@login_required
def new_journal():
    if request.method == 'POST':
        title = sanitize_input(request.form['title'])
        content = sanitize_input(request.form['content'])
        mood = sanitize_input(request.form.get('mood', 'Unknown'))

        entry = JournalEntry(title=title, content=content, mood=mood, user_id=current_user.id)
        session.add(entry)
        session.commit()
        flash("New journal entry added!", "success")
        return redirect(url_for('journal'))

    return render_template('new_journal.html')

@app.route('/view_entry/<int:entry_id>')
@login_required
def view_entry(entry_id):
    entry = session.query(JournalEntry).filter_by(id=entry_id, user_id=current_user.id).first()
    if not entry:
        flash("Entry not found or access denied.", "danger")
        return redirect(url_for('journal'))
    return render_template('view_entry.html', entry=entry)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = session.query(JournalEntry).filter_by(id=entry_id, user_id=current_user.id).first()
    if entry:
        session.delete(entry)
        session.commit()
        flash("Entry deleted.", "info")
    else:
        flash("Entry not found or access denied.", "danger")
    return redirect(url_for('journal'))

# ---------------- Chatbot Routes ----------------

@app.route('/chatbot_api', methods=['POST'])
@login_required
def chatbot_api():
    try:
        data = request.get_json(force=True)
        user_message = data.get('message') if data else None

        if not user_message:
            return jsonify({'error': 'No message received'}), 400

        bot_response = get_chatbot_response(user_message)  # now uses local model
        return jsonify({'response': bot_response})

    except Exception as e:
        print("Chatbot API Error:", e)
        return jsonify({'error': 'Server error'}), 500

@app.route('/chatbot', methods=['GET'])
@login_required
def chatbot_ui():
    return render_template('chatbot.html')

# ---------------- Mood Tracker ----------------
@app.route('/mood_tracker')
@login_required
def mood_tracker():
    return render_template('mood_tracker.html')

# ---------------- Cleanup ----------------
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# ---------------- MAIN ----------------
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
