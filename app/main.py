import streamlit as st
import os
from dotenv import load_dotenv
from utils import process_code_input, create_vector_store, get_retriever, get_conversational_chain
import re
from langchain.memory import ConversationBufferMemory

def main():
    load_dotenv()
    st.set_page_config(page_title="Python Code Copilot", page_icon="🐍", layout="wide")
    
    
    api_key_status = "Not Found"
    if os.getenv("GROQ_API_KEY"):
        api_key_status = "Loaded Successfully"
    
    st.sidebar.subheader("API Key Status")
    st.sidebar.info(api_key_status)

    st.title("🐍 Python Code Copilot")

    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vector_store_path" not in st.session_state:
        st.session_state.vector_store_path = None
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    
    with st.sidebar:
        st.subheader("Upload Your Code")
        uploaded_file = st.file_uploader("Upload a Python file or a ZIP archive", type=["py", "zip"])
        if st.button("Process"):
            with st.spinner("Analyzing your code..."):
                if uploaded_file is not None:
                    code_chunks = process_code_input(uploaded_file)
                    if code_chunks:
                        st.session_state.vector_store_path = create_vector_store(code_chunks)
                        
                        st.session_state.chat_history = []
                        st.session_state.memory.clear()
                        st.success("Analysis complete. You can now ask questions about your code.")
                    else:
                        st.error("Could not extract any Python code from the uploaded file.")
                else:
                    st.error("Please upload a file first.")

    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    if prompt := st.chat_input("Ask a question about your code..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.vector_store_path:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    retriever = get_retriever(st.session_state.vector_store_path)
                    conversation_chain = get_conversational_chain(retriever, st.session_state.memory)
                    
                    if conversation_chain:
                        response = conversation_chain({'question': prompt})
                        full_response = response.get('answer', 'Sorry, I could not find an answer.')

                        
                        
                        
                        if "### FULL_ANALYSIS_START ###" in full_response:
                            intro_match = re.search(r"### FULL_ANALYSIS_START ###(.*?)### ANALYSIS_SECTION ###", full_response, re.DOTALL)
                            analysis_match = re.search(r"### ANALYSIS_SECTION ###(.*?)### FULL_CORRECTED_CODE_SECTION ###", full_response, re.DOTALL)
                            corrected_code_section_match = re.search(r"### FULL_CORRECTED_CODE_SECTION ###(.*)### FULL_ANALYSIS_END ###", full_response, re.DOTALL)
                            
                            if intro_match and analysis_match and corrected_code_section_match:
                                intro = intro_match.group(1).strip()
                                analysis = analysis_match.group(1).strip()
                                corrected_code_section = corrected_code_section_match.group(1).strip()
                                
                                st.markdown(intro)
                                st.markdown("---")
                                st.markdown(analysis)
                                st.markdown("---")
                                st.markdown(corrected_code_section)
                            else:
                                st.markdown(full_response) 

                        
                        elif "### MODIFICATION_START ###" in full_response:
                            content_match = re.search(r"### MODIFICATION_START ###(.*)### MODIFICATION_END ###", full_response, re.DOTALL)
                            if content_match:
                                st.markdown(content_match.group(1).strip())
                            else:
                                st.markdown(full_response)

                        
                        elif "### COMPARISON_START ###" in full_response:
                            intro_match = re.search(r"### COMPARISON_START ###(.*?)### BUGGY_CODE ###", full_response, re.DOTALL)
                            buggy_code_match = re.search(r"### BUGGY_CODE ###(.*?)### CORRECTED_CODE ###", full_response, re.DOTALL)
                            corrected_code_match = re.search(r"### CORRECTED_CODE ###(.*)### COMPARISON_END ###", full_response, re.DOTALL)
                            
                            if intro_match and buggy_code_match and corrected_code_match:
                                intro = intro_match.group(1).strip()
                                buggy_code = buggy_code_match.group(1).strip().strip('`python').strip()
                                corrected_code = corrected_code_match.group(1).strip().strip('`python').strip()
                                
                                st.markdown(intro)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.subheader("Original Code")
                                    st.code(buggy_code, language='python')
                                with col2:
                                    st.subheader("Corrected Code")
                                    st.code(corrected_code, language='python')
                            else:
                                st.markdown(full_response)

                        
                        elif "### CONVERSATIONAL_START ###" in full_response:
                            content_match = re.search(r"### CONVERSATIONAL_START ###(.*)### CONVERSATIONAL_END ###", full_response, re.DOTALL)
                            if content_match:
                                st.markdown(content_match.group(1).strip())
                            else:
                                st.markdown(full_response)
                        
                        
                        else:
                            st.markdown(full_response)

                        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Could not create the conversational chain.")
        else:
            st.warning("Please upload and process a code file first.")

if __name__ == "__main__":
    main()
