import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Gemini AI Detector",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Custom CSS
def load_css():
    with open("core/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    st.error("core/styles.css not found. Please ensure project structure is correct.")

from core import utils

# Main Layout
def main():
    # Session State Initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.markdown('<div class="main-header"><h1>AI Content Detector <span style="font-size:0.5em; opacity:0.6;">// RAG Edition</span></h1></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Ref. Knowledge Base")
        st.info("Upload texts (PDF/TXT) to compare against.")
        
        uploaded_files = st.file_uploader("Upload Documents", type=['txt', 'md', 'pdf'], accept_multiple_files=True)
        
        if uploaded_files:
            if "rag_files" not in st.session_state:
                st.session_state.rag_files = []
            
            from core.api import gemini
            import tempfile
            
            # Button to trigger processing
            if st.button("Process & Embed Documents"):
                progress_bar = st.progress(0)
                for idx, uploaded_file in enumerate(uploaded_files):
                    # Save to temp
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Upload to Gemini
                    file_ref = gemini.upload_file(tmp_path, display_name=uploaded_file.name)
                    if file_ref:
                        st.session_state.rag_files.append(file_ref)
                        st.toast(f"Uploaded: {uploaded_file.name}", icon="✅")
                    
                    # Cleanup
                    os.remove(tmp_path)
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                st.success(f"{len(st.session_state.rag_files)} documents ready for RAG analysis.")

    # Chat Interface Container
    chat_container = st.container()
    
    # Render History
    with chat_container:
        for msg in st.session_state.messages:
            role_class = "user-message" if msg["role"] == "user" else "ai-message"
            with st.chat_message(msg["role"]):
                st.markdown(f"{msg['content']}")

    # Input Area
    user_input = st.text_area("Input text to analyze...", height=150, placeholder="Paste article or essay here...", key="user_input_area")
    
    if st.button("Analyze Content", type="primary"):
        if user_input:
            # Add User Message to State
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            # AI Response Container
            with st.chat_message("assistant"):
                placeholder = st.empty()
                
                # Show Skeleton Loader
                placeholder.markdown(utils.generate_skeleton_loader(), unsafe_allow_html=True)
                
                # Call Gemini API
                from core.api import gemini
                response_text = gemini.generate_response(user_input, chat_history=st.session_state.messages[:-1])
                
                # simulated typewriter stream (since Gemini SDK stream=True is optional, we simulate for the visual effect requested)
                # Note: valid gemini.generate_response returns full text, so we stream the string locally for the effect.
                full_response = ""
                for chunk in utils.stream_text(response_text):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
            
            # Add AI Message to State
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
