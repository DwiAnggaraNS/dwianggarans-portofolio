"""
Simple LLM Service for LPDP RAG System
"""
import os
import logging
from typing import Optional, Dict, Any

try:
    from langchain_groq import ChatGroq
except ImportError:
    try:
        from langchain_community.llms import Groq as ChatGroq
    except ImportError:
        ChatGroq = None

logger = logging.getLogger(__name__)

class LLMService:
    """Simple LLM service using Groq"""
    
    def __init__(self, langsmith_monitoring=None):
        """Initialize the LLM service"""
        self.llm = None
        self.langsmith = langsmith_monitoring
        
        if ChatGroq and os.getenv('GROQ_API_KEY'):
            try:                
                # Get LangSmith callbacks if available
                callbacks = []
                if self.langsmith:
                    langsmith_callbacks = self.langsmith.get_callbacks()
                    if langsmith_callbacks:
                        callbacks.extend(langsmith_callbacks)

                self.llm = ChatGroq(
                    groq_api_key=os.getenv('GROQ_API_KEY'),
                    model_name=os.getenv('GROQ_MODEL', 'llama3-8b-8192'),
                    temperature=0.1,
                    max_retries=1,
                    request_timeout=15.0,
                    max_tokens=512,
                    callbacks=callbacks if callbacks else None
                )
                logger.info("LLM Service initialized with Groq")
            except Exception as e:
                logger.error(f"Failed to initialize Groq LLM: {e}")
                self.llm = None
        else:
            logger.warning("Groq LLM not available")
    
    def bind_tools(self, tools):
        """Bind tools to LLM"""
        if self.llm:
            return self.llm.bind_tools(tools)
        return None
    
    def invoke(self, messages):
        """Invoke LLM with messages"""
        if self.llm:
            return self.llm.invoke(messages)
        return None
    
    def generate_answer(self, context: str, question: str) -> str:
        """Generate answer from context and question"""
        if not self.llm:
            return self._fallback_answer(context, question)
        
        try:
            prompt = f"""Berdasarkan konteks dokumen LPDP berikut, jawab pertanyaan dengan singkat dan akurat:

                    KONTEKS:
                    {context}

                    PERTANYAAN: {question}

                    JAWABAN (gunakan format markdown, maksimal 300 kata):"""
            
            response = self.llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return self._fallback_answer(context, question)
    
    def _fallback_answer(self, context: str, question: str) -> str:
        """Fallback answer when LLM is not available"""
        return f"Berdasarkan dokumen yang tersedia, berikut informasi terkait '{question}':\n\n{context[:500]}..."
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.llm is not None