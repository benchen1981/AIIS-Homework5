# Debugging Process Log

This document records the major issues encountered during development and the prompts/solutions used to resolve them.

## 1. IndentationError in Application Logic
**Issue**: The application failed to start with `IndentationError: unexpected indent` at line 107 of `app.py`.
**Context**: This occurred after moving the logic from a notebook-style script to the Streamlit app structure, specifically within the `if analyze_btn:` block.
**Debugging Prompt**:
> "Refine UI and Debug. Resolve the IndentationError in app.py at line 107."
**Resolution**:
- Analyzed the code block under `with result_container:`.
- Re-aligned the `if source_text:` check and the subsequent API call logic to match the parent indentation level.

## 2. Gemini API Instability (503/429)
**Issue**: Frequent `503 Service Unavailable` and `429 Resource Exhausted` errors when calling the Gemini API.
**Debugging Prompt**:
> "Debugging Gemini API Stability. Ensure the upgraded Streamlit application functions correctly by fixing API key authentication errors and implementing robust retry mechanisms."
**Resolution**:
- Implemented a retry loop with exponential backoff in `core/api.py`.
- Added fallback logic: if the primary model fails or is exhausted, wait and retry, or suggest checking quota limits.

## 3. Streamlit UI & Layout Issues
**Issue**: The user requested a "Glassmorphism" look, but standard Streamlit widgets (like the Sidebar) were breaking the immersion. Also, the input/output pane was missing in earlier iterations.
**Debugging Prompt**:
> "Streamlit UI Refinement. Address the missing input/output pane and ensure the Glassmorphism design is correctly applied."
**Resolution**:
- **CSS**: heavily modified `core/styles.css` to override `st.text_area` and `st.button` styles.
- **Layout**: Removed `st.sidebar` entirely. Moved the "Upload" and "Sample Text" buttons to the main column using `st.columns(3)`.

## 4. PDF Parsing Errors
**Issue**: Uploading PDF files resulted in errors or empty text.
**Debugging Prompt**:
> "Ensure the input functionality correctly handles ... file uploads for TXT, PDF, and MD formats, with PyPDF2 installed."
**Resolution**:
- Added `import PyPDF2` inside the file upload handler.
- Implemented a page-by-page text extraction loop: `for page in pdf_reader.pages: source_text += page.extract_text()`.

## 5. Notebook Execution Errors (Historical)
**Issue**: Earlier in the project (during notebook generation), there were issues with t-SNE performance (`KeyboardInterrupt`) and incorrect plotting labels.
**Debugging Prompt**:
> "Debugging t-SNE Performance... debug any errors encountered... verify that the script runs to completion."
**Resolution**:
- Optimized data sampling for t-SNE to reduce computational load.
- Fixed plot label encoding to ensuring English labels were used to avoid font issues.
