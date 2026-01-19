# 🌿 PlantDocBot – AI Plant Disease Diagnosis

A professional AI-powered plant disease diagnosis system using **Image Recognition**, **Voice Input**, and **Text Symptoms**. Built with Streamlit, PyTorch, and Groq LLM.

---

## ✨ Features

| Mode | Description |
|------|-------------|
| 📷 **Image Upload** | Upload leaf photos for CNN-based disease detection (ResNet50) |
| 🎤 **Voice Input** | Describe symptoms via audio – transcribed using Whisper |
| 💬 **Text Symptoms** | Type symptoms for semantic classification via Groq LLM |

- **Single-mode diagnosis** – Only one input type active at a time for clarity
- **Confidence-aware results** – Shows prediction confidence for image-based diagnosis
- **Treatment recommendations** – Provides causes, symptoms, treatment & prevention info
- **Clean white UI** – Professional light theme with centered layout

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Image Model | ResNet50 (PyTorch) |
| Voice Transcription | OpenAI Whisper (local) |
| Text Classification | Groq LLM API |
| Knowledge Base | JSON (diseases.json) |

---

## 📁 Project Structure

```
PlantChatBot-Project/
├── app.py                      # Main Streamlit application
├── .env                        # API keys (not in git)
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
├── backend/
│   ├── __init__.py             # Module exports
│   ├── app.py                  # Voice processing coordinator
│   ├── chatbot.py              # Greeting & help responses
│   ├── groq_fallback.py        # Groq LLM API integration
│   ├── symptom_matcher.py      # Text → Disease classification
│   └── voice_handler.py        # Audio → Text transcription
├── knowledge/
│   ├── __init__.py             # Module exports
│   ├── diseases.json           # Disease database
│   └── treatments.py           # JSON loader & formatters
└── models/
    └── resnet50_*.pth          # Trained image model
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- FFmpeg (for voice features)
- Groq API key (for text/voice diagnosis)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/springboardmentor88888-mahaprasad/Intern-PlantChatBot-Project.git
   cd Intern-PlantChatBot-Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo GROQ_API_KEY=your_groq_api_key_here > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM classification | Yes (for voice/text) |

Get your API key from: https://console.groq.com

---

## 📋 Requirements

```
streamlit
torch
torchvision
openai-whisper
pillow
numpy
python-dotenv
groq
```

---

## 🎨 Theme Configuration

The app uses a light theme defined in `.streamlit/config.toml`:

```toml
[theme]
base="light"
primaryColor="#2e7d32"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#000000"
font="sans serif"
```

---

## 🌱 Supported Diseases

- Tomato Late Blight
- Tomato Early Blight
- Tomato Leaf Mold
- Tomato Septoria Leaf Spot
- Tomato Bacterial Spot
- Tomato Yellow Leaf Curl Virus
- Tomato Mosaic Virus
- Tomato Target Spot
- Tomato Spider Mites
- Tomato Healthy

---

## 👥 Team

**Mentor:** Mahaprasad Jena

### Intern Guidelines
- Each intern must create their own branch
- All work must be committed under personal branches
- No code should be pushed directly to main
- Use GitHub for documentation & file sharing

---

## 📄 License

This project is for educational purposes as part of the internship program.

---

<p align="center">
  <b>PlantDocBot</b> | AI-Powered Plant Disease Diagnosis
</p>
