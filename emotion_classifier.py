# emotion_classifier.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Emotion labels (GoEmotions taxonomy + "neutral")
LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion",
    "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment",
    "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism",
    "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
]

# Load tokenizer & model only once (at import time)
tokenizer = AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-go-emotion")
model = AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/bert-base-go-emotion")

# Use GPU if available, otherwise CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(DEVICE)
model.eval()  # Set model to evaluation mode

def predict_emotion(text: str):
    """
    Predicts the most likely emotion from input text using GoEmotions model.
    Returns: (label, confidence_score)
    """
    if not text.strip():
        return "neutral", 0.0

    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(DEVICE)

    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)

    # Get highest probability class
    top_prob, top_class = torch.max(probs, dim=1)
    return LABELS[top_class.item()], float(top_prob)
