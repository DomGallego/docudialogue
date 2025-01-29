"""
Sidebar component for the DocuDialogue application.

This module handles the sidebar UI components including file upload,
model selection, and parameter configuration for the LLM models.
"""

import streamlit as st
from config import log_time

def set_sidebar_title():
    """Set up the main sidebar title and subtitle for the application."""

    st.sidebar.markdown("""
        <div class="title-container">
            <p class="big-font">🤖 DocuDialogue</p>
            <p class="subtitle">Transform your documents into interactive conversations</p>
        </div>
    """, unsafe_allow_html=True)

def set_sidebar_file_uploader():
    """Initialize and render the PDF file upload component.

    Returns:
        list: List of uploaded file objects from Streamlit's file_uploader
    """

    uploaded_files = st.sidebar.file_uploader(
        "Drop your PDF files here",
        type=["pdf"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    log_time("File uploader initialized")
    return uploaded_files

def set_sidebar_model_selection():
    """Configure and render the model selection interface.
    
    Handles model selection radio buttons and API key input fields
    for both OpenAI and Google models.
    """

    with st.sidebar.expander("🤖 Model Selection"):
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "gpt-4o-mini"
        
        MODEL_OPTIONS = {
            "gpt-4o-mini": "OpenAI GPT4o-mini (default)",
            "gpt-4o": "OpenAI GPT4o",
            "Gemini 2.0 Flash": "Google Gemini 2.0 Flash",
        }

        st.session_state.selected_model = st.radio(
            "Choose Model",
            options=list(MODEL_OPTIONS.keys()),
            format_func=lambda x: MODEL_OPTIONS[x],
            help="Select the AI model to use for generating responses."
        )

        st.markdown("### API Key")
        
        if st.session_state.selected_model in ["gpt-4o", "gpt-4o-mini"]:
            new_openai_key = st.text_input(
                "OpenAI API Key",
                value=st.session_state.openai_api_key,
                type="password",
                help="Enter your OpenAI API key"
            )
            if new_openai_key != st.session_state.openai_api_key:
                st.session_state.openai_api_key = new_openai_key
                st.rerun()
        
        elif st.session_state.selected_model == "Gemini 2.0 Flash":
            new_google_key = st.text_input(
                "Google API Key",
                value=st.session_state.google_api_key,
                type="password",
                help="Enter your Google API key"
            )
            if new_google_key != st.session_state.google_api_key:
                st.session_state.google_api_key = new_google_key
                st.rerun()

    log_time("Model selection initialized")

def set_sidebar_llm_params():
    """Configure and render the LLM parameter controls.
    
    Provides sliders for adjusting temperature, max output tokens,
    and top_p sampling parameters for the selected model.
    """

    
    with st.sidebar.expander("🛠️ LLM Parameters"):
        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.7
        if "max_length" not in st.session_state:
            st.session_state.max_length = 1024
        if "top_p" not in st.session_state:
            st.session_state.top_p = 0.9

        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            help="Controls randomness in output"
        )

        st.session_state.max_length = st.slider(
            "Max Output Tokens",
            min_value=64,
            max_value=2048,
            value=st.session_state.max_length,
            help="Maximum response length"
        )

        st.session_state.top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.top_p,
            help="Controls diversity via nucleus sampling"
        )

    log_time("LLM parameters initialized")
    print(f"\n\n\n{'='*100}\n")
