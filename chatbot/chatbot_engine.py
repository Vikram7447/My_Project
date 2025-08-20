from emotion_classifier import predict_emotion

def get_bot_response(user_input):
    emotion, confidence = predict_emotion(user_input)

    if emotion in ["sadness", "grief", "remorse"]:
        return f"I sense you may be feeling {emotion}. That sounds heavy 💙. You're not alone — would you like to talk more about it?"

    elif emotion in ["joy", "excitement", "love", "pride"]:
        return f"That's wonderful! I'm glad you're feeling {emotion} 🌸."

    elif emotion in ["fear", "nervousness"]:
        return f"It seems like you're experiencing {emotion}. Try deep breathing, journaling, or reaching out to someone you trust."

    elif emotion in ["anger", "annoyance", "disapproval"]:
        return f"It looks like you're feeling {emotion}. It’s okay to feel this way — maybe writing it out in your journal could help."

    else:
        return f"I hear you. It seems like you might be experiencing {emotion}. I'm here to listen — tell me more."
