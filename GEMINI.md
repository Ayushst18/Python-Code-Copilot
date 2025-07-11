# Python Code Copilot

This project is a Python Code Copilot that uses LangChain and Groq to help users understand, debug, and improve their Python code.

## Project Structure

- `app/main.py`: The main Streamlit application file.
- `app/utils.py`: Helper functions for code processing, embedding generation, and vector store management.
- `app/vector_store/`: Directory to store the FAISS vector store.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables, including the Groq API key.

## How it works

1.  **Code Ingestion:** The user uploads a Python file or a ZIP archive of Python files.
2.  **Code Chunking:** The code is split into meaningful chunks (functions, classes) using Python's `ast` module.
3.  **Embedding Generation:** The code chunks are embedded using the `microsoft/codebert-base` model.
4.  **Vector Store:** The embeddings are stored in a FAISS vector store for efficient retrieval.
5.  **Retrieval and Correction:** When the user asks a question, the most relevant code chunks are retrieved from the vector store.
6.  **Code Generation:** The retrieved code and the user's question are passed to the Groq LLM to generate suggestions and corrected code.
7.  **Frontend:** The Streamlit frontend displays the original code, the corrected code, and allows the user to interact with the copilot.
