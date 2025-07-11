import os
import zipfile
import ast
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

def process_code_input(uploaded_file):
    """
    Processes the uploaded file (either a single python file or a zip archive)
    and returns a list of code chunks.
    """
    all_code_chunks = []
    if uploaded_file.name.endswith(".zip"):
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith(".py"):
                    with zip_ref.open(file_name) as python_file:
                        code = python_file.read().decode("utf-8")
                        all_code_chunks.extend(get_code_chunks(code))
    elif uploaded_file.name.endswith(".py"):
        code = uploaded_file.read().decode("utf-8")
        all_code_chunks.extend(get_code_chunks(code))
    return all_code_chunks


def get_code_chunks(code):
    """
    Splits a python code string into chunks using the AST module.
    If no functions or classes are found, the entire code is returned as a single chunk.
    """
    chunks = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                chunks.append(ast.get_source_segment(code, node))
        if not chunks:
            chunks.append(code)
    except SyntaxError:
        chunks.append(code)
    return chunks

def create_vector_store(code_chunks):
    """
    Creates a FAISS vector store from the given code chunks.
    """
    if not code_chunks:
        return None
    try:
        embeddings = HuggingFaceEmbeddings(model_name="microsoft/codebert-base")
        vector_store = FAISS.from_texts(texts=code_chunks, embedding=embeddings)
        if not os.path.exists("app/vector_store"):
            os.makedirs("app/vector_store")
        vector_store.save_local("app/vector_store/faiss_index")
        return "app/vector_store/faiss_index"
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

def get_retriever(vector_store_path="app/vector_store/faiss_index"):
    """
    Initializes and returns a retriever for the vector store.
    """
    try:
        embeddings = HuggingFaceEmbeddings(model_name="microsoft/codebert-base")
        vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
        return vector_store.as_retriever()
    except Exception as e:
        print(f"Error getting retriever: {e}")
        return None

from langchain.memory import ConversationBufferMemory

def get_conversational_chain(retriever, memory):
    """
    Creates a conversational chain with a sophisticated, multi-format prompt.
    """
    custom_prompt_template = """
    You are a world-class Python coding assistant. Your goal is to provide precise, efficient, and helpful responses by first understanding the user's intent based on their latest question and the chat history.

    **CHAT HISTORY:**
    {chat_history}

    **RETRIEVED CODE CONTEXT:**
    {context}

    **USER'S LATEST QUESTION:**
    {question}

    ---

    **STEP 1: Analyze the user's intent.**
    - Is it a broad, initial request for a full code review?
    - Is it a specific request to modify, add to, or explain a piece of the existing code?
    - Is it a request to compare a buggy snippet with a corrected one?
    - Is it a simple conversational question or comment?

    **STEP 2: Based on the intent, formulate your response in ONE of the following formats.**

    **FORMAT 1: Full Analysis**
    Use this for initial, broad requests.
    ### FULL_ANALYSIS_START ###
    (A friendly, conversational intro)
    ### ANALYSIS_SECTION ###
    - **Error/Improvement 1:** (Description)
      - **Explanation:** (Detailed explanation)
      - **Problematic Code:**
        ```python
        (The specific lines of problematic code)
        ```
    - **Error/Improvement 2:** (Description)
      - (Repeat the structure)
    ### FULL_CORRECTED_CODE_SECTION ###
    (A brief closing statement)
    ```python
    (The complete, corrected, runnable code)
    ```
    ### FULL_ANALYSIS_END ###

    **FORMAT 2: Targeted Modification/Explanation**
    Use this for specific follow-up questions about adding, changing, or explaining something.
    ### MODIFICATION_START ###
    (A direct, conversational answer to the user's question)
    ```python
    (Show ONLY the new or modified code snippet, NOT the whole file)
    ```
    ### MODIFICATION_END ###

    **FORMAT 3: Comparison**
    Use this when asked to compare code.
    ### COMPARISON_START ###
    (A conversational intro)
    ### BUGGY_CODE ###
    ```python
    (The original, buggy code snippet)
    ```
    ### CORRECTED_CODE ###
    ```python
    (The corrected code snippet)
    ```
    ### COMPARISON_END ###

    **FORMAT 4: Conversational**
    Use this for greetings, thanks, or questions that don't involve code.
    ### CONVERSATIONAL_START ###
    (A friendly, natural, conversational response. Do not mention the code.)
    ### CONVERSATIONAL_END ###

    **IMPORTANT RULES:**
    - Choose ONLY ONE format for your response.
    - Do not generate code unless it is specifically required by the format.
    - Be concise and directly address the user's latest question.

    Assistant's Response:
    """
    
    prompt = PromptTemplate(
        template=custom_prompt_template, input_variables=["chat_history", "context", "question"]
    )

    llm = ChatGroq(model_name="meta-llama/llama-4-maverick-17b-128e-instruct")
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    return chain
