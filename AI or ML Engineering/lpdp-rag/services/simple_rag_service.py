"""
Simple RAG Service for LPDP RAG System
This service integrates all components while maintaining Single Responsibility Principle
"""
import os
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple

from .vector_store import VectorStoreService
from services.llm_service import LLMService
from core.rag_chain import SimpleRAGChain

logger = logging.getLogger(__name__)

class SimpleRAGService:
    """
    Simple RAG service that coordinates all components
    Follows Single Responsibility Principle by delegating to specialized services
    """
    
    def __init__(self):
        """Initialize the simple RAG service"""
        self.max_input_tokens = int(os.getenv('MAX_INPUT_TOKENS', 1000))
        
        # Initialize components
        try:
            # Vector store service for document storage and retrieval
            self.vector_service = VectorStoreService()
            
            # LLM service for answer generation
            self.llm_service = LLMService()
            
            # RAG chain for orchestrating the retrieval-augmented generation
            # Note: Chat history is handled by the stateful chain (MessagesState + checkpointer)
            self.rag_chain = SimpleRAGChain(self.vector_service)
            
            logger.info("Simple RAG Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
            raise
    
    def get_answer(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Get answer for a question using the RAG pipeline
        This is the main interface method that coordinates all components
        """
        try:
            # Validate input
            is_valid, error_msg = self._validate_input(question)
            if not is_valid:
                return self._create_error_response(error_msg)
            
            # Use RAG chain to get answer
            result = self.rag_chain.invoke(question, session_id)
            
            # Note: Chat history is automatically managed by the stateful chain
            # No need to manually add to separate chat history manager
            
            return result
            
        except Exception as e:
            logger.error(f"Error in RAG service: {str(e)}")
            return self._create_error_response(
                "Maaf, terjadi kesalahan dalam memproses pertanyaan Anda. Silakan coba lagi nanti."
            )
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get chat history for a session"""
        try:
            # Get from RAG chain (stateful chain manages history automatically)
            return self.rag_chain.get_session_history(session_id)
            
        except Exception as e:
            logger.error(f"Error getting session history: {str(e)}")
            return []
    
    def clear_session(self, session_id: str) -> bool:
        """Clear session history"""
        try:
            # Clear from RAG chain (stateful chain manages history)
            return self.rag_chain.clear_session(session_id)
            
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
            return False
    
    def add_documents(self, file_paths: List[str]) -> bool:
        """Add documents to the vector store"""
        try:
            return self.vector_service.add_documents_from_files(file_paths)
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            doc_count = self.vector_service.get_collection_count()
            
            return {
                'document_count': doc_count,
                'vector_store_type': 'Chroma',
                'embedding_model': 'paraphrase-multilingual-MiniLM-L12-v2',
                'llm_available': self.llm_service.is_available(),
                'rag_approach': 'stateful_chain',
                'chat_history_managed_by': 'langgraph_checkpointer'
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {}
    
    def _validate_input(self, question: str) -> Tuple[bool, str]:
        """Validate input question for token limits and content"""
        # Check length (approximate token count)
        estimated_tokens = len(question.split()) * 1.3
        
        if estimated_tokens > self.max_input_tokens:
            return False, f"Pertanyaan terlalu panjang. Maksimal sekitar {int(self.max_input_tokens/1.3)} kata."
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'\b(cerpen|novel|cerita|story)\b',
            r'\b(copy|paste|artikel|blog)\b',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, question.lower()):
                return False, "Pertanyaan harus terkait dengan informasi beasiswa LPDP."
        
        return True, ""
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            'answer': error_message,
            'sources': [],
            'confidence': 0.0,
            'needs_continuation': False,
            'metadata': {
                'error': True,
                'timestamp': datetime.now().isoformat()
            }
        }
