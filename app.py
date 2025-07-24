from flask import Flask, render_template, request, redirect, url_for
from chatbot.chatbot_engine import get_bot_response
from journal.journal_manager import save_entry, get_all_entries, get_entry_by_id, delete_entry
from utils.helpers import get_current_timestamp, sanitize_input

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Journal Entries
@app.route('/journal')
def journal():
    entries = get_all_entries()
    return render_template('journal.html', entries=entries)

# Add New Entry
@app.route('/journal/new', methods=['GET', 'POST'])
def new_journal():
    if request.method == 'POST':
        title = sanitize_input(request.form['title'])
        content = sanitize_input(request.form['content'])
        mood = request.form.get('mood')
        save_entry(title, content, mood)
        return redirect(url_for('journal'))
    return render_template('new_journal.html')

# View Entry
@app.route('/journal/<int:entry_id>')
def view_entry(entry_id):
    entry = get_entry_by_id(entry_id)
    return render_template('view_entry.html', entry=entry)

# Delete Entry
@app.route('/journal/delete/<int:entry_id>')
def delete_entry_route(entry_id):
    delete_entry(entry_id)
    return redirect(url_for('journal'))

# Chatbot Page
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    user_input = ''
    bot_response = ''
    if request.method == 'POST':
        user_input = sanitize_input(request.form['user_input'])
        bot_response = get_bot_response(user_input)
    return render_template('chatbot.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
