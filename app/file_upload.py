"""
PDF document processing module for streamlit application.

This module handles file upload operations, PDF processing, and vector storage integration.
It provides functionality to split PDFs into chunks and store them in a vector database.
"""


import os
import streamlit as st
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import log_time

def handle_file_upload_and_processing(uploaded_files):
    """
    Process uploaded PDF files and store their contents in a vector database.

    Args:
        uploaded_files: List of uploaded file objects from Streamlit

    The function performs the following operations:
    - Maintains state of processed files
    - Splits PDF documents into chunks
    - Stores document chunks in vector database
    - Manages temporary file cleanup
    """

    if "files_processed" not in st.session_state:
        st.session_state.files_processed = False
        
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    if uploaded_files:
        st.sidebar.metric("Files Uploaded", f"{len(uploaded_files)} PDFs")
        
        # Determine which files need processing
        current_files = {file.name for file in uploaded_files}
        new_files = current_files - st.session_state.processed_files
        
        if new_files:
            try:
                for uploaded_file in uploaded_files:
                    if uploaded_file.name not in st.session_state.processed_files:
                        # Create temporary file for PDF processing
                        temp_path = os.path.join(st.session_state.temp_dir, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Load and process PDF
                        loader = PyPDFLoader(temp_path)
                        pages = loader.load()
                        
                        # Configure text splitting parameters
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1500,
                            chunk_overlap=300
                        )
                        chunks = []
                        for page in tqdm(pages, desc="Splitting documents"):
                            chunks.extend(text_splitter.split_documents([page]))
                        
                        # Prepare data for vector store
                        texts = [chunk.page_content for chunk in chunks]
                        metadatas = [{"source": uploaded_file.name, "page": i} for i, _ in enumerate(chunks)]
                        ids = [f"{uploaded_file.name}-{i}" for i in range(len(chunks))]
                        
                        try:
                            # Store document chunks in vector database
                            st.session_state.collection.add(
                                documents=texts,
                                metadatas=metadatas,
                                ids=ids
                            )
                            # Add to processed files set after successful processing
                            st.session_state.processed_files.add(uploaded_file.name)
                        except Exception as e:
                            st.error(f"Error adding documents: {str(e)}")
                        
                        # Cleanup temporary file
                        os.remove(temp_path)

                st.toast('Documents processed successfully!', icon='✅')
                
            except Exception as e:
                st.error(f"Error processing files: {str(e)}")
        
        # Handle case when files are removed
        if len(current_files) < len(st.session_state.processed_files):
            st.session_state.processed_files = current_files
    else:
        # Reset processed files when no files are uploaded
        st.session_state.processed_files = set()

    log_time("File processing completed")
