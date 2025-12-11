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
import io

# Main Layout
def main():
    st.markdown('<div class="main-header"><h1>AI Content Detector <span style="font-size:0.5em; opacity:0.6;">// Dashboard</span></h1></div>', unsafe_allow_html=True)
    
    # Sidebar removed as per user request to delete left pane.
    # Upload functionality is now integrated into the main input card.

    # Dashboard Layout (Single Column)
    
    # Input Section
    st.markdown("### Enter text here or upload file to check for AI Content.")
    
    # Action Buttons
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        if st.button("📋 Paste Text", use_container_width=True):
            st.session_state.input_mode = "text"
            st.session_state.dashboard_input = "" 
    
    with b_col2:
        if st.button("📝 Sample Text", use_container_width=True):
            st.session_state.input_mode = "text"
            st.session_state.dashboard_input = "Artificial Intelligence has revolutionized the way we interact with technology. From predictive text to autonomous vehicles, AI systems are becoming increasingly sophisticated. However, this rapid advancement raises ethical questions about privacy and employment that society must address."
    
    with b_col3:
        if st.button("📤 Upload File", use_container_width=True):
            st.session_state.input_mode = "file"
    
    # Initialize state
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "text"
    
    # Input Area based on mode
    source_text = ""
    if st.session_state.input_mode == "text":
        user_input = st.text_area(
            "Content", 
            height=200, 
            placeholder="Paste your text here...", 
            key="dashboard_input", 
            label_visibility="collapsed"
        )
        source_text = user_input
        
    elif st.session_state.input_mode == "file":
        uploaded_source = st.file_uploader("Choose a file to analyze (TXT/PDF/MD)", type=['txt', 'pdf', 'md'], key="source_uploader")
        if uploaded_source:
            # Read file content immediately for analysis
            try:
                import PyPDF2
                if uploaded_source.type == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(uploaded_source)
                    source_text = ""
                    for page in pdf_reader.pages:
                        source_text += page.extract_text()
                else:
                    # For TXT and Markdown
                    stringio = io.StringIO(uploaded_source.getvalue().decode("utf-8"))
                    source_text = stringio.read()
                
                st.info(f"File loaded: {len(source_text)} characters.")
            except Exception as e:
                st.error(f"Error reading file: {e}")
        else:
            st.info("Upload a file to begin analysis.")
    
    # Analyze Button
    st.markdown('<div class="check-btn-container">', unsafe_allow_html=True)
    analyze_btn = st.button("Check for AI Content", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Result Section
    st.markdown("---")
    st.markdown("### 🔍 Analysis Result / 分析結果")
    result_container = st.container()
    
    with result_container:
        if analyze_btn:
            if source_text:
                placeholder = st.empty()
                # Call Gemini API
                from core.api import gemini
                response_text = gemini.generate_response(
                    source_text, 
                    chat_history=[], 
                    file_uris=st.session_state.get("rag_files", [])
                )
                
                # Try to parse a score
                import re
                match = re.search(r"<<SCORE:(\d+)>>", response_text)
                score = int(match.group(1)) if match else 0
                
                # Remove the score tag
                display_text = re.sub(r"<<SCORE:\d+>>", "", response_text).strip()
                
                # Display Gauge
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="text-align: center; width: 100%;">
                        <h2 style="margin:0; color: {'#ff4b4b' if score > 50 else '#00cc99'};">{score}%</h2>
                        <span style="font-size: 0.8em; opacity: 0.7;">AI Probability / AI 可能性</span>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 20px;">
                    <div style="background: {'#ff4b4b' if score > 50 else '#00cc99'}; width: {score}%; height: 100%;"></div>
                </div>
                """, unsafe_allow_html=True)

                # Stream Analysis Text
                full_response = ""
                for chunk in utils.stream_text(display_text):
                    full_response += chunk
                    placeholder.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        {full_response}▌
                    </div>
                    """, unsafe_allow_html=True)
                
                # Final clean render
                placeholder.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                    {full_response}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please input text or upload a file.")
        else:
            st.info("Awaiting input for analysis... / 等待輸入進行分析...")

if __name__ == "__main__":
    main()

