# Development Process & Project Architecture (Prompt History)

## 1. Project Architecture

### Structure
```text
.
├── app.py                  # Main Streamlit application entry point
├── .env                    # Environment variables (GEMINI_API_KEY)
├── debug.md                # Debugging log
├── prompt.md               # Development log (this file)
├── openspec.md             # Project specification and status
├── core/
│   ├── api.py              # Gemini API interaction & RAG logic
│   ├── styles.css          # CSS for Glassmorphism & Animations
│   └── utils.py            # Utility functions (streaming, skeletons)
└── assets/                 # Static assets
```

### Tech Stack
- **Frontend**: Streamlit, Vanilla CSS (Glassmorphism design)
- **Backend / LLM**: Python, Google Gemini 2.5 Flash API
- **RAG**: Google File Search Store (Vector Store)
- **Tools**: `python-dotenv`, `PyPDF2`

---

## 2. Detailed Development Process Information (Prompts)

The following represents the chronological sequence of user prompts and architectural decisions that built this project.

### Phase 1: Initiation & Design
**User Prompt**:
> "Initialize a new Streamlit project called 'AI-Human Content Detector'. I want a high-end, futuristic 'Glassmorphism' UI. Do not use standard Streamlit widgets if they look plain. Use custom CSS in `core/styles.css`."

**Action**:
- Created `app.py` and `core/styles.css`.
- Implemented background gradients and semi-transparent container classes (`.glass-panel`).

### Phase 2: Core Logic (Gemini API)
**User Prompt**:
> "Implement the backend logic in `core/api.py`. It needs to connect to Google Gemini API using an API Key from `.env`. Create a function `generate_response(text)` that asks the model to detect if the text is AI-generated."

**Action**:
- Setup `init_gemini()` in `api.py`.
- Created basic prompt engineering for AI detection.

### Phase 3: RAG Integration
**User Prompt**:
> "I want to upload reference documents (PDF/TXT) to help the AI decide. Use the Google Gemini File API for this. If I upload a file, it should be added to a Vector Store and used as context."

**Action**:
- Added `upload_file_to_store` in `api.py`.
- Integrated `tools='file_search'` in the Gemini chat session.
- Added file uploader to `app.py`.

### Phase 4: UI Refinement & Polish
**User Prompt**:
> "Refine the UI. The left sidebar is distracting; remove it. Move the upload functionality to the main dashboard. Add a 'Typewriter' effect for the output text so it looks like it's being generated in real-time. Also, verify PDF parsing works."

**Action**:
- Removed `st.sidebar`.
- Created a 3-column action area (Paste Text, Sample Text, Upload File).
- Implemented `utils.stream_text` for the visual effect.
- Integrated `PyPDF2` for PDF text extraction.

### Phase 5: Finalization
**User Prompt**:
> "Update tasks in `openspec.md` to be complete. Archive the current stable version to a new folder `Archive/03-UI_Refinement_and_Debug`."

**Action**:
- Updated checkmarks in `openspec.md`.
- Created archive backup.
