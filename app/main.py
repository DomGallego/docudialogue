"""
Main application entry point for the Document Q&A System.

This module orchestrates the initialization and setup of the application components
including environment configuration, UI elements, and chat functionality.
"""

import streamlit as st
from config import initialize_environment, initialize_session_state, initialize_chromadb, log_time
from ui import set_ui_css
from sidebar import set_sidebar_title, set_sidebar_file_uploader, set_sidebar_model_selection, set_sidebar_llm_params
from file_upload import handle_file_upload_and_processing
from chat import handle_chat


def main():
    """
    Initialize and run the main application workflow.
    
    Executes the following sequence:
    1. Environment and session setup
    2. UI component initialization
    3. File upload handling
    4. Chat interface setup
    5. Model configuration
    """
    initialize_environment()
    initialize_session_state()
    initialize_chromadb()
    
    set_ui_css()
    set_sidebar_title()
    
    uploaded_files = set_sidebar_file_uploader()
    handle_file_upload_and_processing(uploaded_files)
    handle_chat(uploaded_files)
    
    # Configure model settings
    set_sidebar_model_selection()
    set_sidebar_llm_params()


if __name__ == "__main__":
    main()
