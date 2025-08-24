from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load GoEmotions model locally
MODEL_NAME = "nateraw/bert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Map model labels to chatbot responses
EMOTION_RESPONSES = {
    "joy": "That's wonderful! I'm so glad to hear that. 😊",
    "sadness": "I'm sorry you're feeling down. Do you want to talk about it?",
    "anger": "I understand you're upset. Want me to help calm things down?",
    "fear": "That sounds scary. You're not alone in this.",
    "surprise": "Wow, that sounds unexpected!",
    "love": "That's so heartwarming ❤️",
    "neutral": "I'm here to listen. Tell me more."
}

# Model's label mapping
MODEL_LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval",
    "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
    "joy", "love", "nervousness", "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]

# Map some fine-grained labels to simpler emotions for chatbot responses
SIMPLIFIED_LABELS = {
    "admiration": "joy",
    "amusement": "joy",
    "anger": "anger",
    "annoyance": "anger",
    "approval": "joy",
    "caring": "love",
    "confusion": "neutral",
    "curiosity": "neutral",
    "desire": "neutral",
    "disappointment": "sadness",
    "disapproval": "anger",
    "disgust": "anger",
    "embarrassment": "sadness",
    "excitement": "joy",
    "fear": "fear",
    "gratitude": "love",
    "grief": "sadness",
    "joy": "joy",
    "love": "love",
    "nervousness": "fear",
    "optimism": "joy",
    "pride": "joy",
    "realization": "neutral",
    "relief": "joy",
    "remorse": "sadness",
    "sadness": "sadness",
    "surprise": "surprise",
    "neutral": "neutral"
}

def get_emotion(user_input: str) -> str:
    """Detect the emotion of the user input locally using Transformers."""
    try:
        inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        top_idx = torch.argmax(probs).item()
        fine_label = MODEL_LABELS[top_idx].lower()
        # Map fine-grained label to simplified label
        return SIMPLIFIED_LABELS.get(fine_label, "neutral")
    except Exception as e:
        print("Error detecting emotion:", e)
        return "neutral"

def get_chatbot_response(user_input: str) -> str:
    """Generate an empathetic response based on detected emotion."""
    emotion = get_emotion(user_input)
    return EMOTION_RESPONSES.get(emotion, "I'm here to listen. Tell me more.")
