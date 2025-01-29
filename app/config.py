"""
Configuration module for the GenAI PDF Chat application.

This module handles initialization of environment variables, session state,
and vector database (ChromaDB) setup. It includes logging utilities for
performance monitoring.
"""


import time
import tempfile
import streamlit as st
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import create_langchain_embedding
from langchain_huggingface import HuggingFaceEmbeddings

# Global log storage for performance tracking
log_summary = []


def log_time(message: str) -> None:
    """
    Log execution time between checkpoints.

    Args:
        message (str): Checkpoint description to log

    Returns:
        None
    """
    current_time = time.time()
    if log_summary:
        elapsed_time = (current_time - log_summary[-1][1]) * 1000  # Convert to milliseconds
    else:
        elapsed_time = 0
    log_summary.append((message, current_time, elapsed_time))
    print(f"{message}: {elapsed_time:.2f} ms")

def initialize_environment() -> None:
    """
    Initialize environment variables from .env file and set up logging.
    """
    load_dotenv()
    print(f"\n\n\n{'='*100}\n")
    log_time("Script started")

def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    
    Sets up persistent storage for:
    - Chat messages
    - Uploaded files
    - API keys
    - Temporary directory
    - UI state flags
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = None
    if "toast_shown" not in st.session_state:
        st.session_state.toast_shown = False
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
    if "google_api_key" not in st.session_state:
        st.session_state.google_api_key = ""
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = tempfile.mkdtemp()

    log_time("Session state initialized")

def initialize_chromadb() -> None:
    """
    Initialize ChromaDB vector database with HuggingFace embeddings.
    
    Creates a persistent ChromaDB client and collection for storing
    document embeddings using the all-MiniLM-L6-v2 model.
    """
    if "chroma_client" not in st.session_state:
        st.session_state.temp_dir = tempfile.mkdtemp()
        st.session_state.chroma_client = chromadb.PersistentClient(
            path=st.session_state.temp_dir
        )
        
        try:
            st.session_state.collection = st.session_state.chroma_client.get_or_create_collection(
                name="pdf_collection", 
                embedding_function=create_langchain_embedding(HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
            )
        except Exception as e:
            st.error(f"Error initializing ChromaDB: {str(e)}")

    log_time("ChromaDB initialized")
