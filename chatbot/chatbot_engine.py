import os
from huggingface_hub import InferenceClient

# Create inference client with your HF token
client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ.get("HF_TOKEN"),
)

# Map detected emotions to chatbot responses
EMOTION_RESPONSES = {
    "joy": "That's wonderful! I'm so glad to hear that. 😊",
    "sadness": "I'm sorry you're feeling down. Do you want to talk about it?",
    "anger": "I understand you're upset. Want me to help calm things down?",
    "fear": "That sounds scary. You're not alone in this.",
    "surprise": "Wow, that sounds unexpected!",
    "love": "That's so heartwarming ❤️",
    "neutral": "I see. Tell me more about it."
}


def get_emotion(user_input):
    """Classify user input into an emotion using GoEmotions model."""
    try:
        result = client.text_classification(
            user_input,
            model="google/bert-base-uncased-goemotions"
        )
        if result and isinstance(result, list):
            top_emotion = max(result, key=lambda x: x['score'])['label']
            return top_emotion.lower()
    except Exception as e:
        print("Error with HF API:", e)
    return "neutral"


def get_chatbot_response(user_input):
    """Generate an empathetic response based on detected emotion."""
    emotion = get_emotion(user_input)
    return EMOTION_RESPONSES.get(emotion, "I'm here to listen. Tell me more.")
