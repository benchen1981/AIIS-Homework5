# AI-Human Content Detector (Gemini RAG Edition)

A high-performance, futuristic web application designed to detect and analyze AI-generated content versus human writing. It leverages **Google's Gemini 2.5 Flash model** with **RAG (Retrieval-Augmented Generation)** capabilities, utilizing a premium "Glassmorphism" design aesthetic.

---

## 🚀 Features

-   **Dual-Engine Detection**: Uses Gemini's generative capabilities combined with RAG context from uploaded documents to analyze text patterns.
-   **Glassmorphism UI**: A premium, translucent interface with dynamic gradients and micro-animations (`core/styles.css`).
-   **RAG Integration**: Upload PDF/TXT/MD files to Google's File Search Store to act as a knowledge base for the detector.
-   **Smart Inputs**: Paste text, generate sample text, or upload files directly for analysis.
-   **Real-time Streaming**: "Typewriter" effect for analysis results, mimicking a live AI thought process.

---

## 🛠 System Architecture

### Technology Stack
-   **Frontend**: Streamlit, Vanilla CSS (Custom Glassmorphism System)
-   **LLM**: Google Gemini 2.5 Flash
-   **RAG**: Google File Search Store (Vector Database)
-   **Backend Logic**: Python

### Project Structure
```text
.
├── app.py                  # Main Application Entry Point
├── .env                    # Configuration (API Keys)
├── core/
│   ├── api.py              # Gemini API & RAG Logic
│   ├── styles.css          # Visual Design System
│   └── utils.py            # Helper Functions (Skeleton loaders, streaming)
├── debug.md                # Debugging Log
├── prompt.md               # Development Process (Prompts)
└── openspec.md             # Functional Specification
```

---

## ⚡️ Quick Start

### 1. Prerequisites
-   Python 3.10+
-   A Google Cloud Project with Gemini API enabled.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/benchen1981/AIIS-Homework5.git
cd AIIS-Homework5

# Install dependencies
pip install streamlit google-generativeai python-dotenv PyPDF2
```

### 3. Configuration
Create a `.env` file in the root directory and add your Google Gemini API key:
```ini
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```
The application will launch in your default browser at `http://localhost:8501`.

---

## 📝 Development Process (Prompts)

The development followed a rigorous "Agentic Coding" workflow. Detailed logs of the specific prompts used to generate the architecture and code are available in **[prompt.md](./prompt.md)**.

**Summary of Phases:**
1.  **Architecture Design**: Establishing the folder structure and File/Folder separation.
2.  **UI Implementation**: Crafting the `styles.css` for the specific "Glass" look.
3.  **Core Logic**: Connecting `api.py` to Google Gemini.
4.  **RAG Integration**: Implementing the file upload and vector store logic.
5.  **Refinement**: Debugging indentation errors and UI glitches.

---

## 🐞 Debugging & Troubleshooting

A comprehensive log of technical issues encountered (e.g., `IndentationError`, API `503` errors, PDF parsing issues) and their solutions is recorded in **[debug.md](./debug.md)**.

**Common Fixes:**
-   **Port Conflicts**: Use `--server.port=xxxx` if port 8501 is busy.
-   **API Limits**: The app includes retry logic, but if you hit Quota limits, wait 60s before retrying.

---

## 📜 License
This project is created for AIIS Homework 5.
