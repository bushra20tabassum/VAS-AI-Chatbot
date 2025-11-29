from flask import Flask, render_template, request, jsonify
from utils import preprocess, vectorize, get_best_match

app = Flask(__name__)

# ----------------------------
# Load FAQs
# ----------------------------
faq_questions = []
faq_answers = []

try:
    with open("faqs.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 2:
                question = parts[0].strip()
                answer = "|".join(parts[1:]).strip()  # Join if answer has extra '|'
                faq_questions.append(preprocess(question))
                faq_answers.append(answer)
except FileNotFoundError:
    print("Error: faqs.txt file not found!")
except Exception as e:
    print(f"Error reading FAQs: {e}")

# Ensure we have FAQs before vectorizing
if faq_questions:
    vectorizer, X = vectorize(faq_questions)
    print(f"Loaded {len(faq_questions)} FAQs.")  # Debug
else:
    vectorizer, X = None, None
    print("Warning: No FAQs loaded.")

# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------
# Chatbot API
# ----------------------------
@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json(force=True)
        user_input = data.get("message", "")
    except:
        return jsonify({"response": "Invalid request format", "confidence": "0.00"})

    if not user_input.strip():
        return jsonify({"response": "Please type a message.", "confidence": "0.00"})

    processed_input = preprocess(user_input)

    if vectorizer is None or X is None:
        return jsonify({"response": "Chatbot is not ready. No FAQs loaded.", "confidence": "0.00"})

    # Use lower threshold for better matching
    response, score = get_best_match(processed_input, vectorizer, X, faq_answers, threshold=0.05)
    print(f"User: {user_input} | Score: {score}")  # Debug

    if response:
        return jsonify({"response": response, "confidence": f"{score:.2f}"})
    else:
        return jsonify({"response": "Sorry, I don't understand your question. Please try another one.", "confidence": "0.00"})

if __name__ == "__main__":
    app.run(debug=True)
