![image](https://github.com/user-attachments/assets/61ce2267-50e5-4890-8d25-9e82a0519c81)
# Hopper-AI - Personal Web Assistant 💬🧠

Hopper AI is a personal assistant web application that leverages **Google Gemini API** to interact using both **text** and **voice input**. This assistant is capable of answering questions, processing files, and providing intelligent responses in real-time through a modern and responsive UI.

## 🔥 Features

- 🎤 **Voice and Text Input Support**
- 📎 **File Uploading Support** (Text, PDF, Images)
- 🧠 **AI-Powered Responses** (via Gemini API)
- 🌗 **Light/Dark Mode Toggle**
- 🧾 **File Parsing** (Text summary generation using AI)
- 📱 **Responsive and Mobile-Friendly UI**
- ⚡ **Dynamic Buttons with Gradient Effects**
- ✨ Clean and Modern Gradient UI inspired by futuristic design

## 🛠️ Built With

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Flask (Python)
- **AI Engine**: Google Gemini API (Generative Language)
- **Speech-to-Text**: Web Speech API
- **Text-to-Speech**: Web Speech Synthesis API

## 📷 Screenshots

| Chat UI (Dark Mode) | Voice & Upload Features |
|---------------------|--------------------------|
| ![Dark Mode UI](./screenshots/dark-mode.png) | ![File Upload](./screenshots/file-upload.png) |

## ⚙️ How to Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/Hopper-ai.git
cd Hopper-ai

# Install Python dependencies (optional if Flask used)
pip install -r requirements.txt

# Add your Gemini API Key
Create a .env file and add:
GEMINI_API_KEY=your_key_here

# Run
python app.p

