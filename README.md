# 🐍 Python Code Copilot

A powerful AI-powered code analysis and assistance tool that helps developers understand, review, and improve their Python code using advanced language models and vector embeddings.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![LangChain](https://img.shields.io/badge/langchain-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

- **📁 Multi-format Support**: Upload single Python files or entire ZIP archives
- **🤖 AI-Powered Analysis**: Leverages Groq's Meta-Llama model for intelligent code review
- **🔍 Vector Search**: Uses FAISS and CodeBERT embeddings for semantic code understanding
- **💬 Conversational Interface**: Interactive chat-based code assistance
- **📊 Comprehensive Analysis**: Identifies errors, suggests improvements, and provides explanations
- **🔄 Multiple Response Formats**: Full analysis, targeted modifications, comparisons, and conversational responses
- **💾 Persistent Memory**: Maintains conversation context for better assistance

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key (get it from [Groq Console](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ayushst18/Python-Code-Copilot.git
   cd Python-Code-Copilot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501` to start using the application.

## 🔧 How It Works

### 1. Code Processing
- **File Upload**: Support for `.py` files and `.zip` archives
- **AST Parsing**: Intelligently chunks code into functions and classes
- **Vector Embedding**: Creates semantic embeddings using Microsoft's CodeBERT

### 2. AI Analysis
- **Retrieval System**: Uses FAISS vector store for relevant code retrieval
- **LLM Integration**: Powered by Meta-Llama model via Groq API
- **Context-Aware**: Maintains conversation history for coherent interactions

### 3. Response Formats
- **Full Analysis**: Comprehensive code review with detailed explanations
- **Targeted Modifications**: Specific code improvements and additions
- **Code Comparisons**: Side-by-side buggy vs. corrected code
- **Conversational**: Natural language responses for general queries

## 📖 Usage Examples

### Basic Code Review
1. Upload your Python file or ZIP archive
2. Click "Process" to analyze the code
3. Ask questions like:
   - "Can you review this code for errors?"
   - "How can I improve the performance?"
   - "Explain what this function does"

### Specific Improvements
- "Add error handling to the database connection function"
- "Optimize this loop for better performance"
- "Make this code more readable"

### Code Comparisons
- "Compare the original code with your suggested improvements"
- "Show me the before and after versions"

## 🏗️ Project Structure

```
Python-Code-Copilot/
├── app/
│   ├── main.py              # Streamlit application entry point
│   ├── utils.py             # Core utility functions
│   └── vector_store/        # Generated vector embeddings (auto-created)
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── .env                    # Environment variables (create this)
└── README.md               # Project documentation
```

## 🔑 Key Components

### `app/main.py`
- Streamlit web interface
- File upload and processing
- Chat interface and session management
- API key validation

### `app/utils.py`
- Code parsing and chunking (AST-based)
- Vector store creation and management
- Conversational chain setup
- Custom prompt templates

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Language Model**: Meta-Llama (via Groq API)
- **Embeddings**: Microsoft CodeBERT
- **Vector Store**: FAISS
- **Framework**: LangChain
- **Language**: Python 3.8+

## 📋 Requirements

```txt
streamlit
langchain
langchain-groq
sentence-transformers
faiss-cpu
python-dotenv
langchain-community
```

## 🔒 Environment Variables

Create a `.env` file with the following:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing fast LLM inference
- [Microsoft](https://microsoft.com/) for CodeBERT embeddings
- [LangChain](https://langchain.com/) for the powerful framework
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Meta](https://meta.com/) for the Llama model


## 🚧 Roadmap

- [ ] Support for more programming languages
- [ ] Integration with more LLM providers
- [ ] Advanced code metrics and analysis
- [ ] Collaborative features
- [ ] API endpoint for programmatic access
- [ ] Plugin system for extensibility

---

**Made with ❤️ by [Ayushst18](https://github.com/Ayushst18)**

⭐ Star this repository if you find it helpful!
