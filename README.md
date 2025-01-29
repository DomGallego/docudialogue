# 🤖 DocuDialogue

Transform your documents into interactive conversations.

## Overview

DocuDialogue is a Streamlit application that allows you to upload PDFs and interact with them using conversational AI models like OpenAI's GPT-4o and Google's Gemini 2.0 Flash.


## Demo


https://github.com/user-attachments/assets/292cd0c6-8787-450d-b729-ac38cbd078a4






## Prerequisites

- **Python 3.11.11**
- **conda** (Anaconda package manager)

## Installation

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd thinking-machines-mle-genai-exam
    ```

2. **Create a conda environment (recommended)**

    ```bash
    conda create --name myenv python=3.11.11
    ```

    **Activate the conda environment:**

    ```bash
    conda activate myenv
    ```

3. **Install the required packages**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**

    ```bash
    streamlit run app/main.py
    ```

2. **Access the application**

    Open your web browser and navigate to [http://localhost:8501](http://localhost:8501).

3. **Upload your documents**

    Use the sidebar to upload your PDF files.

4. **Configure the model**

    In the sidebar:
    - **Model Selection**: Choose the AI model you want to use.
    - **API Key**: Enter your API key when prompted.

5. **Interact with your documents**

    Start asking questions in the chat interface about your uploaded documents.

## Notes

- **No .env file is needed**: API keys are entered directly in the application's sidebar.
- **LLM Parameters**: Adjust parameters like Temperature, Max Output Tokens, and Top P in the sidebar under "LLM Parameters".

## License

This project is licensed under the MIT License. See the LICENSE file for details.
