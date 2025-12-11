# OpenSpec Project Specification

## 1. Project Overview
**Project Name:** AI-Human Content Detector (Gemini RAG Edition)
**Description:** A futuristic, high-performance web application designed to detect and analyze AI-generated content versus human writing. It leverages Google's Gemini 2.5 Flash model with RAG (Retrieval-Augmented Generation) capabilities, inspired by an n8n workflow architecture. The interface features a premium "Glassmorphism" aesthetic with advanced animations like token-by-token typewriter effects and micro-skeleton loading states.

## 2. Objectives
- **Core Functionality:** Accurate detection/analysis of text sources (Human vs. AI) using Gemini.
- **RAG Integration:** Allow uploading of reference documents (Human/AI samples) to enhance detection accuracy via Google File Search Store.
- **User Experience:** deliver a "Wow" factor with a translucent, futuristic UI, fluid animations, and a responsive chat-like interface.

## 3. Architecture
### 3.1. System Context
- **User:** Interacts via Web Browser (Streamlit App).
- **Web Server:** Streamlit (Python) hosting the UI and orchestrating calls.
- **LLM Provider:** Google Gemini API (handling Generation & Embeddings).
- **Vector Store:** Google File Search Store (managed via API) for RAG context.

### 3.2. Detailed Components
- **Frontend Layer (Streamlit + CSS):**
    - `core/styles.css`: Custom CSS for Glassmorphism, animations (`@keyframes`), and reshaping Streamlit's default widgets.
    - `app.py`: Main entry point. Manages session state (chat history, file upload status).
- **Logic Layer (Python):**
    - `core/api.py`: 
        - `ChatManager`: Handles the chat session and prompt injection.
        - `StoreManager`: Wrapper for `google.generativeai` to create stores, upload files, and delete stores.
    - `core/utils.py`: Text processing, "Micro-skeleton" generator helpers.
- **Data Layer:**
    - Local: In-memory Session State for transient data.
    - Remote: Google File Search Store for persistent document embeddings.

## 4. Features
### Phase 1: MVP (The "Wow" Experience)
- **Visuals:** Full Glassmorphism system (frosted glass, gradients, minimal translucent cards).
- **Input/Output:** Text input area with "Typewriter" streaming output.
- **Loading State:** "Micro-skeleton" animation (fast initial segment -> progressive load).
- **Core Logic:** "AI Detector" prompt pipeline using Gemini.

### Phase 2: RAG Integration
- **File Upload:** Upload reference text files to Google File Store via Sidebar.
- **Contextual Detection:** The "Detector" Agent includes `tools=['file_search']` to cross-reference uploaded documents.

## 5. Tech Stack
- **Language:** Python 3.10+
- **Framework:** Streamlit
- **Libraries:** `google-generativeai`, `streamlit-extras` (for some UI components if needed), `python-dotenv`.
- **Styling:** Vanilla CSS (injected via `st.markdown`).

## 6. Project Structure
```text
.
├── app.py                  # Main Streamlit application
├── .env                    # Environment variables (GEMINI_API_KEY)
├── core/
│   ├── api.py              # Gemini API interaction logic
│   ├── styles.css          # Glassmorphism & Animation styles
│   └── utils.py            # Utility functions (skeleton generation)
├── assets/                 # Static assets (images, icons)
├── Archive/                # Project snapshots
└── openspec.md             # Living specification
```

## 7. Implementation Roadmap
### Task 1: Project Initialization
1.  [x] Setup Python environment and install `streamlit`, `google-generativeai`, `python-dotenv`.
2.  [x] Create project directory structure.
3.  [x] Configure `.env` for API keys.

### Task 2: Visual System (The "Glass" UI)
4.  [x] Create `core/styles.css` with:
    -   Root variables for colors (Futuristic Cyan/Purple).
    -   `.stApp` background gradient.
    -   `.glass-panel` classes.
    -   Custom animation keyframes (`fade-in`, `typewriter`).
5.  [x] Implement `app.py` scaffolding to inject CSS and test the visual look.

### Task 3: Backend Core (Gemini & RAG)
6.  [x] Implement `core/api.py`:
    -   `init_gemini()` connection.
    -   `upload_file_to_store()` function.
    -   `get_chat_response()` with RAG tool enabled.

### Task 4: Interaction & Animation
7.  [x] Implement "Typewriter" streaming logic in Streamlit.
8.  [x] Create the "Micro-skeleton" loader (dummy placeholder text that shimmers before real content arrives).

### Task 5: Integration & Polish
9.  [x] Connect Chat UI to Backend.
10. [x] Add Sidebar for File Uploads.
11. [x] Final design review and tweak.
