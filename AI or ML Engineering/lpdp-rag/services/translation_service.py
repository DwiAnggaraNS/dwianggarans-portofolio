"""
Translation Service using deep-translator (more stable alternative to googletrans)
"""
import logging
from typing import List, Optional
from langchain_core.documents import Document

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

logger = logging.getLogger(__name__)

class TranslationService:
    """Translation service using deep-translator"""
    
    def __init__(self):
        """Initialize translation service"""
        self.translator = None
        
        if TRANSLATOR_AVAILABLE:
            try:
                self.translator = GoogleTranslator(source='en', target='id')
                logger.info("Translation service initialized with deep-translator")
            except Exception as e:
                logger.error(f"Failed to initialize translator: {e}")
                self.translator = None
        else:
            logger.warning("deep-translator not available")
    
    def translate_text(self, text: str, source_lang: str = 'en', target_lang: str = 'id') -> str:
        """Translate text from source to target language"""
        if not self.translator:
            return text
        
        try:
            # Update translator languages if different
            if source_lang != 'en' or target_lang != 'id':
                self.translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            # Split long text into chunks (deep-translator has limits)
            max_length = 5000
            if len(text) <= max_length:
                return self.translator.translate(text)
            
            # Handle long text by splitting
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            translated_chunks = []
            
            for chunk in chunks:
                translated_chunk = self.translator.translate(chunk)
                translated_chunks.append(translated_chunk)
            
            return ' '.join(translated_chunks)
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def translate_documents(self, documents: List[Document]) -> List[Document]:
        """Translate a list of documents"""
        if not self.translator:
            return documents
        
        translated_docs = []
        for doc in documents:
            try:
                translated_content = self.translate_text(doc.page_content)
                
                # Create new document with translated content
                translated_doc = Document(
                    page_content=translated_content,
                    metadata={
                        **doc.metadata,
                        'original_language': 'en',
                        'translated_to': 'id',
                        'translated': True
                    }
                )
                translated_docs.append(translated_doc)
                
            except Exception as e:
                logger.error(f"Error translating document: {e}")
                # Keep original if translation fails
                translated_docs.append(doc)
        
        return translated_docs
    
    def is_available(self) -> bool:
        """Check if translation service is available"""
        return self.translator is not None