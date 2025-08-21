@echo off
echo Force Cleanup for LPDP RAG ChromaDB
echo ===================================
echo.

echo Step 1: Killing Python processes...
taskkill /f /im python.exe /t 2>nul
taskkill /f /im pythonw.exe /t 2>nul

echo Step 2: Waiting for processes to close...
timeout /t 5 /nobreak >nul

echo Step 3: Removing ChromaDB directory...
if exist "data\chroma_db" (
    rmdir /s /q "data\chroma_db"
    echo ChromaDB directory removed
) else (
    echo ChromaDB directory does not exist
)

echo Step 4: Recreating directory...
mkdir "data\chroma_db" 2>nul

echo Step 5: Removing LangGraph checkpoints...
if exist "data\langgraph_checkpoints.db" (
    del "data\langgraph_checkpoints.db"
    echo LangGraph checkpoints removed
)

echo.
echo Cleanup completed!
echo You can now run: python scripts\populate_knowledge_base.py
pause
