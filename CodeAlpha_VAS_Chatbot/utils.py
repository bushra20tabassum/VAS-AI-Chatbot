import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ----------------------------
# Stopwords list
# ----------------------------
stop_words = set([
    'i','me','my','myself','we','our','ours','ourselves','you','your','yours',
    'yourself','yourselves','he','him','his','himself','she','her','hers','herself',
    'it','its','itself','they','them','their','theirs','themselves','what','which',
    'who','whom','this','that','these','those','am','is','are','was','were','be','been',
    'being','have','has','had','having','do','does','did','doing','a','an','the','and',
    'but','if','or','because','as','until','while','of','at','by','for','with','about',
    'against','between','into','through','during','before','after','above','below','to',
    'from','up','down','in','out','on','off','over','under','again','further','then',
    'once','here','there','when','where','why','how','all','any','both','each','few',
    'more','most','other','some','such','no','nor','not','only','own','same','so',
    'than','too','very','s','t','can','will','just','don','should','now'
])

# ----------------------------
# Preprocess text
# ----------------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Remove punctuation
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# ----------------------------
# Compute TF-IDF matrix
# ----------------------------
def vectorize(text_list):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(text_list)
    return vectorizer, X

# ----------------------------
# Find best matching answer
# ----------------------------
def get_best_match(user_input, vectorizer, X, faq_answers, threshold=0.05):
    if not user_input.strip():
        return None, 0.0
    input_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(input_vec, X)
    max_index = np.argmax(similarities)
    max_score = similarities[0][max_index]
    if max_score >= threshold:
        return faq_answers[max_index], max_score
    else:
        return None, max_score
