"""
Simple Configuration for LPDP Scholarship RAG Website
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'lpdp-scholarship-ai-assistant-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Application settings
    APP_NAME = "LPDP Scholarship AI Assistant"
    DESCRIPTION = "Simple AI assistant for LPDP Scholarship information"
    
    # Vector database settings
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './data/chroma_db')
    CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'lpdp_docs')
    
    # LLM settings
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
    
    # LangSmith settings for monitoring and observability
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
    LANGCHAIN_ENDPOINT = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
    LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT', 'lpdp-rag-assistant')
    LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'false').lower() == 'true'
    
    # Document processing settings
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './data/documents')
    
    # Translation settings
    USER_AGENT = os.getenv('USER_AGENT', 'LPDP-RAG-Bot/1.0')
    
    # Simple RAG settings
    MAX_INPUT_TOKENS = int(os.getenv('MAX_INPUT_TOKENS', 1000))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 800))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    
    # Web settings
    STATIC_FOLDER = "static"
    TEMPLATE_FOLDER = "templates"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True