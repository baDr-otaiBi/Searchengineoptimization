import math
import random
import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Download necessary NLTK data for TextBlob
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

def mock_questions(keyword, limit=20):
    """Generates mock questions for demo purposes."""
    base_questions = [
        f"What is the best way to learn {keyword}?",
        f"How to start with {keyword} for beginners?",
        f"Why is {keyword} so popular?",
        f"Is {keyword} worth it in 2024?",
        f"Where can I find {keyword} resources?",
        f"What are the risks of {keyword}?",
        f"How does {keyword} compare to competitors?",
        f"Best tools for {keyword} automation",
        f"Can {keyword} make you rich?",
        f"The future of {keyword} explained",
        f"Common mistakes in {keyword}",
        f"Advanced {keyword} strategies",
        f"Who invented {keyword}?",
        f"When will {keyword} be regulated?",
        f"How much does {keyword} cost?",
    ]

    # Generate variations to meet the limit
    questions = []
    # Ensure we have enough unique seeds or just repeat with variations
    for i in range(limit):
        base = random.choice(base_questions)
        questions.append(f"{base} (Var {i+1})")

    return list(questions)[:limit]

def analyze_sentiment(question):
    """Returns the sentiment polarity of the question (-1 to 1)."""
    return TextBlob(question).sentiment.polarity

def get_question_type_score(question):
    """
    Returns a score based on the question type.
    How/Why imply deeper intent -> Higher score.
    """
    q_lower = question.lower()
    if any(x in q_lower for x in ['how', 'why', 'best']):
        return 3.0
    elif any(x in q_lower for x in ['what', 'where', 'when']):
        return 2.0
    else:
        return 1.0

def calculate_value_score(question):
    """
    Calculates a 'Value Score' using a complex mathematical equation.
    Formula: Score = (10 * log(Word Count + 1)) + (5 * Type Score) + (5 * (1 - |Sentiment|))
    """
    words = question.split()
    word_count = len(words)

    # Logarithmic length score to avoid over-rewarding just being verbose
    length_score = 10 * math.log(word_count + 1)

    type_score = 5 * get_question_type_score(question)

    sentiment = analyze_sentiment(question)
    # Prioritizes Neutral questions (informational)
    sentiment_score = 5 * (1 - abs(sentiment))

    return round(length_score + type_score + sentiment_score, 2)

def cluster_questions(questions, n_clusters=5):
    """
    Clusters questions using TF-IDF and KMeans.
    Returns a list of cluster labels.
    """
    if not questions:
        return []

    if len(questions) < n_clusters:
        n_clusters = max(1, len(questions))

    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        X = vectorizer.fit_transform(questions)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X)

        return kmeans.labels_
    except ValueError:
        # Fallback if vocabulary is empty or other issues
        return [0] * len(questions)
