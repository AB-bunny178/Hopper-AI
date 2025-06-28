from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini
GEMINI_API_KEY = "AIzaSyBFjbD6YhYFl8WeK42Hzr4Xa_2EKdybuBA"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Temporary chat memory (cleared on tab/browser close)
chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global chat_history
    user_input = request.json.get("prompt", "")
    if not user_input:
        return jsonify({"response": "No input received."})

    # Add user input to memory
    chat_history.append({"role": "user", "parts": [user_input]})

    try:
        # Get Gemini response with context
        response = model.generate_content(chat_history)
        answer = response.text.strip()

        # Add Gemini reply to memory
        chat_history.append({"role": "model", "parts": [answer]})

        return jsonify({"response": answer})
    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"response": "Sorry, I encountered an error."})

@app.route("/reset", methods=["POST"])
def reset():
    global chat_history
    chat_history = []
    return jsonify({"message": "Memory cleared."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
