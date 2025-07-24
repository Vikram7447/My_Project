# chatbot/chatbot_engine.py

def get_bot_response(user_input):
    user_input = user_input.lower()

    if "sad" in user_input or "depressed" in user_input:
        return "I'm sorry you're feeling that way. Remember, you're not alone. Talking to a friend or journaling might help."

    elif "happy" in user_input or "good" in user_input:
        return "That's wonderful to hear! Keep spreading the positivity."

    elif "stress" in user_input or "anxious" in user_input:
        return "Stress is tough. Try taking deep breaths, journaling, or going for a walk."

    elif "help" in user_input:
        return "You can write about your thoughts in the journal or reach out to a mental health professional."

    else:
        return "I'm here to listen. Tell me more about how you're feeling."
