from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import google.generativeai as genai
import os
import PyPDF2
import docx

app = Flask(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyBMw5zLKW3m8zxff1ue81ReCF4LhnhLMkQ"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Temporary chat memory (cleared on tab/browser close)
chat_history = []

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    text = ""
    if ext == "txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif ext == "pdf":
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif ext == "docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global chat_history
    user_input = request.json.get("prompt", "")
    if not user_input:
        return jsonify({"response": "No input received."})

    chat_history.append({"role": "user", "parts": [user_input]})

    try:
        response = model.generate_content(chat_history)
        answer = response.text.strip()
        chat_history.append({"role": "model", "parts": [answer]})
        return jsonify({"response": answer})
    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"response": "Sorry, I encountered an error."})

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"response": "No file uploaded."})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"response": "No selected file."})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        extracted_text = extract_text(path)
        if not extracted_text.strip():
            return jsonify({"response": "Could not extract text from the file."})

        chat_history.append({"role": "user", "parts": [f"Analyze this file content:\n{extracted_text[:3000]}"]})
        try:
            response = model.generate_content(chat_history)
            answer = response.text.strip()
            chat_history.append({"role": "model", "parts": [answer]})
            return jsonify({"response": answer})
        except Exception as e:
            print("Gemini Error (File):", e)
            return jsonify({"response": "Gemini failed to analyze the file."})

    return jsonify({"response": "Unsupported file type."})

@app.route("/reset", methods=["POST"])
def reset():
    global chat_history
    chat_history = []
    return jsonify({"message": "Memory cleared."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
