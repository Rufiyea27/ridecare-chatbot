from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from chatbot.intents import INTENTS

# Build training dataset
sentences = []
labels = []

for intent_name, intent_data in INTENTS.items():
    for keyword in intent_data["keywords"]:
        sentences.append(keyword)
        labels.append(intent_name)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)


def detect_intent_nlp(user_input):
    user_vec = vectorizer.transform([user_input])

    similarity = cosine_similarity(user_vec, X)

    best_match = similarity.argmax()
    score = similarity[0][best_match]

    if score < 0.2:
        return "unknown"

    return labels[best_match]