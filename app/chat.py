"""
Document Chat Interface Module

This module provides a Streamlit-based chat interface for interacting with documents
using various LLM providers (OpenAI GPT-4 and Google Gemini). It handles document context
retrieval and streaming responses while maintaining chat history.
"""

import streamlit as st
import os
from openai import OpenAI
import google.generativeai as genai
from config import log_time

def handle_chat(uploaded_files):
    """
    Manages the document chat interface and conversation flow.
    
    Args:
        uploaded_files: List of uploaded document files to chat about
        
    The function handles:
    - Document context management
    - API provider selection (OpenAI/Gemini)
    - Chat history tracking
    - Response streaming
    - User input validation
    """

    # Validate initial state
    if not uploaded_files:
        st.info("👈 Please upload document(s) in the sidebar first! And supply the API key as well!")
    else:

        # === UI Layout ===
        col1, col2 = st.columns([5,1])
        with col1:
            st.header("Chat with your Documents")
        with col2:
            if st.button("🧹 Clear Chat"):
                st.session_state.messages = []
                st.rerun()

        # === API Configuration ===
        api_key_valid = (
            (st.session_state.selected_model in ["gpt-4o", "gpt-4o-mini"] and st.session_state.openai_api_key) or
            (st.session_state.selected_model == "Gemini 2.0 Flash" and st.session_state.google_api_key)
        )

        if not api_key_valid:
            st.warning("Please enter an API key in the sidebar to start chatting.")
        else:
            if st.session_state.selected_model in ["gpt-4o", "gpt-4o-mini"]:
                client = OpenAI(api_key=st.session_state.openai_api_key)
            elif st.session_state.selected_model == "Gemini 2.0 Flash":
                genai.configure(api_key=st.session_state.google_api_key)

        # === Chat Display ===
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # === Chat Input Handler ===
        chat_placeholder = "Please enter API key first" if not api_key_valid else "Ask anything about your document(s)"
        if prompt := st.chat_input(
            chat_placeholder,
            disabled=not api_key_valid,
            key="chat_input"
        ):        
            
            # Retrieve relevant document context
            search_results = st.session_state.collection.query(
                query_texts=[prompt],
                n_results=5
            )
            
            context = ""
            if search_results and search_results['documents']:
                context = "\n\n".join([
                    f"Document {meta['source']} (Page {meta['page']}): {doc}"
                    for doc, meta in zip(search_results['documents'][0], search_results['metadatas'][0])
                ])
            
            system_message = f"""You are a versatile and contextually aware assistant, designed to process a broad range of documents—including PDFs, text snippets, spreadsheets, and other reference materials—and generate insightful, accurate, and clearly presented responses. Your purpose extends across multiple domains, from finance to research analysis, to general question-answering and summarization tasks. Strive to remain both flexible and domain-agnostic, adapting to any topic or medium while maintaining exactness, clarity, and a commitment to helping users achieve their goals.

                When responding to financial questions—such as inquiries about revenues, expenditures, or market trends—draw on provided references to supply grounded, verifiable figures. Ensure that all financial metrics are accurate, and contextualize them to highlight their relevance to the broader scenario. Present these findings in a manner that is both accessible and precise, noting key insights and pointing out patterns or anomalies where relevant.

                Summarize key facts and insights from any given source, be it a lengthy report, a single table, or a series of PDF extracts. Condense information thoughtfully, prioritizing the most valuable data points and analytical takeaways. Keep your summaries logically structured and balanced, spotlighting what is most essential while not omitting important details that might shape the reader’s understanding.

                In terms of formatting, continually refine your textual and tabular outputs for maximum clarity. If data lends itself to a tabular format, present it as a well-labeled, neatly aligned table that makes it easy to compare values. For textual explanations, consider using headings, bullet points, and concise statements that enhance readability and comprehension, always choosing the most effective format for the given content.

                Remain sensitive to user instructions and evolving inquiries, and handle follow-up questions in a way that integrates seamlessly with previously provided context. Refer back to earlier information and maintain continuity of discussion, ensuring that all responses are consistent and coherent. If new information is provided or corrections become necessary, adapt gracefully, updating your analysis without losing previously established insights.

                By upholding these standards—broad adaptability, financial precision, clear summarization, refined formatting, and dynamic engagement—you will provide users with a consistently high-value experience. Your overarching goal is to deliver thorough, thoughtful, and contextually relevant guidance that meets users’ present needs and anticipates their future questions.

                Use the following context to answer the question, and if the context doesn't contain the answer, say so:

                {context}"""
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # === Response Generation ===
            with st.chat_message("assistant"):
                if st.session_state.selected_model in ["gpt-4o", "gpt-4o-mini"]:
                    messages_for_api = [
                        {"role": "system", "content": system_message},
                        *[{"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages[:-1]],
                        {"role": "user", "content": prompt}
                    ]
                    
                    stream = client.chat.completions.create(
                        model=st.session_state.selected_model,
                        messages=messages_for_api,
                        stream=True,
                        temperature=st.session_state.temperature,
                        max_completion_tokens=st.session_state.max_length,
                        top_p=st.session_state.top_p
                    )
                    response = st.write_stream(stream)


                elif st.session_state.selected_model == "Gemini 2.0 Flash":
                    # Configure generation parameters
                    generation_config = {
                        "temperature": st.session_state.temperature,
                        "top_p": st.session_state.top_p,
                        "max_output_tokens": st.session_state.max_length,
                        "response_mime_type": "text/plain",
                    }

                    # Initialize model
                    model = genai.GenerativeModel(
                        model_name="gemini-2.0-flash-exp",
                        generation_config=generation_config,
                    )

                    # Convert message history to Gemini format
                    gemini_history = []
                    for msg in st.session_state.messages:
                        role = "model" if msg["role"] == "assistant" else msg["role"]
                        gemini_history.append({
                            "role": role,
                            "parts": [msg["content"]]
                        })

                    chat = model.start_chat(history=gemini_history)
        
                    # Construct prompt with context
                    contextualized_prompt = f"""Use the following context to answer the question, and if the context doesn't contain the answer, say so:

                        Context:
                        {context}

                        Question: {prompt}"""
                    
                    # Send message with context and stream response
                    response = chat.send_message(contextualized_prompt, stream=True)
                    
                    # Create placeholder once
                    placeholder = st.empty()

                    # Stream the response
                    response_text = ""
                    for chunk in response:
                        if chunk.text:
                            response_text += chunk.text
                            # Update placeholder with accumulated text
                            placeholder.markdown(response_text)

                    response = response_text

            st.session_state.messages.append({"role": "assistant", "content": response})

    log_time("Chat functionality initialized")
