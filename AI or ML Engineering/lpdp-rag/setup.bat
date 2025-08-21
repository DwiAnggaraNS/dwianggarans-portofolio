@echo off
color 0A
echo ============================================
echo    LPDP Scholarship RAG Assistant Setup
echo    AI Engineering Project-Based Learning
echo    By: Dwi Anggara N.S
echo ============================================
echo.
echo This setup will configure a complete RAG system using:
echo - LangChain for document processing and retrieval
echo - LangGraph for state management and workflows  
echo - LangSmith for monitoring and observability
echo - ChromaDB for vector storage
echo - Groq LLM for answer generation
echo.

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.10+ first
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo ✓ Python found
)

echo Step 2: Creating Python virtual environment...
if exist venv (
    echo ✓ Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    ) else (
        echo ✓ Virtual environment created
    )
)

echo Step 3: Activating virtual environment...
call venv\Scripts\activate

echo Step 4: Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✓ Pip upgraded

echo Step 5: Installing Python dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
) else (
    echo ✓ All dependencies installed successfully
)

echo Step 6: Setting up configuration...
if not exist .env (
    copy .env.example .env >nul 2>&1
    echo ✓ Created .env file from template
    echo.
    echo IMPORTANT: Please edit .env file with your API keys:
    echo   - GROQ_API_KEY (required - get free at console.groq.com)
    echo   - LANGCHAIN_API_KEY (optional - for monitoring at smith.langchain.com)
) else (
    echo ✓ .env file already exists
)

echo Step 7: Creating data directories...
if not exist "data" mkdir "data"
if not exist "data\documents" mkdir "data\documents"
if not exist "data\chroma_db" mkdir "data\chroma_db"
if not exist "data\uploads" mkdir "data\uploads"
echo ✓ Data directories created

echo Step 8: Verifying LangChain installation...
python -c "import langchain; import langchain_community; import langchain_groq; import chromadb; print('✓ All core packages imported successfully')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Some packages may have import issues
    echo Try running: pip install --upgrade langchain chromadb
)

echo.
echo ================================================
echo           Setup completed successfully!
echo ================================================
echo.
echo Your LPDP RAG Assistant is now configured with:
echo.
echo 🔧 CORE COMPONENTS:
echo   • LangChain - Document processing and RAG pipeline
echo   • LangGraph - State management for conversations
echo   • ChromaDB - Vector database for semantic search
echo   • Groq API - Fast LLM inference
echo.
echo 🎯 LEARNING OBJECTIVES:
echo   • RAG Architecture implementation
echo   • Vector database operations
echo   • State-based conversation management
echo   • Production-ready Flask application
echo.
echo 📋 NEXT STEPS:
echo.
echo 1. Configure API Keys:
echo    Edit .env file and add your keys:
echo    • GROQ_API_KEY=your_groq_api_key_here
echo    • LANGCHAIN_API_KEY=your_langsmith_key (optional)
echo.
echo 2. Add LPDP Documents (optional):
echo    Place PDF files in data\documents\ folder:
echo    • Panduan Pendaftaran LPDP 2025.pdf
echo    • Persyaratan Beasiswa LPDP 2025.pdf
echo    • Other LPDP documentation
echo.
echo 3. Populate Knowledge Base:
echo    python scripts\simple_populate.py
echo.
echo 4. Start the Application:
echo    python app.py
echo    Then open: http://localhost:5000
echo.
echo 📚 LEARNING RESOURCES:
echo   • LangChain Tutorial: https://python.langchain.com/docs/tutorials/rag/
echo   • LangGraph Docs: https://langchain-ai.github.io/langgraph/
echo   • LangSmith Platform: https://smith.langchain.com/
echo.
echo Happy learning! 🚀
echo Project by: Dwi Anggara N.S
echo.
pause