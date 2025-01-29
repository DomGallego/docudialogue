"""
UI styling module for Streamlit application.

This module contains functions to customize the Streamlit UI appearance through CSS.
"""

import streamlit as st

def set_ui_css():
    """
    Apply custom CSS styling to the Streamlit application.
    
    Modifies the following UI elements:
    - Main app container padding
    - Title container alignment and spacing
    - Heading font sizes and weights
    - Subtitle text appearance and margins
    """
    st.markdown("""
        <style>
        .stApp {
            padding-top: 0rem;
        }
        .title-container {
            text-align: center;
            padding: 0.5rem 0 1rem 0;
            margin-top: -1rem;
        }
        .big-font {
            font-size: 35px !important;
            font-weight: bold !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        .subtitle {
            font-size: 16px !important;
            color: #666666;
            margin: 0.2rem 0 0 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        </style>
    """, unsafe_allow_html=True)
