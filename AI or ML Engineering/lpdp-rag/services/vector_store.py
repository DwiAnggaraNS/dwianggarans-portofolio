"""
Simple Vector Store Service for LPDP RAG System
"""
import os
import json
import logging
from typing import List, Dict, Any

# Import langchain components with fallbacks
try:
    from langchain_core.documents import Document
except ImportError:
    try:
        from langchain.schema import Document
    except ImportError:
        from langchain_community.schema import Document

try:
    from langchain_chroma import Chroma
except ImportError:
    try:
        from langchain_community.vectorstores import Chroma
    except ImportError:
        from langchain.vectorstores import Chroma

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except ImportError:
        from langchain.embeddings import HuggingFaceEmbeddings

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
except ImportError:
    from langchain.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader

import bs4
from .translation_service import TranslationService

logger = logging.getLogger(__name__)

class VectorStoreService:
    """Simple vector store service using ChromaDB with translation support"""
    
    def __init__(self):
        """Initialize the vector store service"""
        self.db_path = os.getenv('CHROMA_DB_PATH', './data/chroma_db')
        self.collection_name = os.getenv('CHROMA_COLLECTION_NAME', 'lpdp_docs')
        
        # Ensure directory exists
        os.makedirs(self.db_path, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", "!", "?", ",", " ", ""]
        )
        
        # Initialize translation service
        self.translation_service = TranslationService()
        
        # LPDP web sources configuration for import
        self.lpdp_web_sources = [
            {
                "url": "https://lpdp.kemenkeu.go.id/en/tentang/selayang-pandang/",
                "bs_kwargs": {"parse_only": bs4.SoupStrainer(class_="container")},
                "metadata": {"source": "LPDP Selayang Pandang", "type": "web"}
            },
            {
                "url": "https://lpdp.kemenkeu.go.id/en/tentang/visi-misi/",
                "bs_kwargs": {"parse_only": bs4.SoupStrainer(class_="container")},
                "metadata": {"source": "LPDP Visi Misi", "type": "web"}
            },
            {
                "url": "https://lpdp.kemenkeu.go.id/en/beasiswa/kebijakan-umum/",
                "bs_kwargs": {"parse_only": bs4.SoupStrainer("div", class_="ant-col ant-col-24 ant-col-md-17 ant-col-md-order-1")},
                "metadata": {"source": "LPDP Kebijakan Umum", "type": "web"}
            },
        ]
        
        logger.info("Vector Store Service initialized")
    
    def add_documents_from_files(self, file_paths: List[str], translate_web_docs: bool = False) -> bool:
        """Add documents from files to the vector store 
        
        Args:
            file_paths: List of file paths to process
            translate_web_docs: Only translate web documents (not PDF/JSON files)
        """
        try:
            all_documents = []
            
            for file_path in file_paths:
                documents = self._load_document(file_path)
                if documents:
                    all_documents.extend(documents)
            
            if all_documents:
                # Only translate web documents if requested
                if translate_web_docs:
                    web_documents = [doc for doc in all_documents if doc.metadata.get('type') == 'web']
                    non_web_documents = [doc for doc in all_documents if doc.metadata.get('type') != 'web']
                    
                    if web_documents:
                        logger.info(f"Translating {len(web_documents)} web documents to Indonesian...")
                        translated_web_docs = self._translate_documents(web_documents)
                        all_documents = translated_web_docs + non_web_documents
                    
                # Split documents into chunks
                split_docs = self.text_splitter.split_documents(all_documents)
                
                # Add to vector store
                self.vectorstore.add_documents(split_docs)
                
                logger.info(f"Added {len(split_docs)} document chunks to vector store")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search"""
        try:
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []
    
    def get_retriever(self, k: int = 5):
        """Get retriever for the vector store"""
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        try:
            return self.vectorstore._collection.count()
        except:
            return 0
    
    def _load_document(self, file_path: str) -> List[Document]:
        """Load document from file with special handling for JSON files"""
        try:
            filename = os.path.basename(file_path)
            
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                
                # Add metadata
                for doc in documents:
                    doc.metadata.update({
                        'source': filename,
                        'title': filename,
                        'file_type': 'pdf',
                        'language': 'indonesian'
                    })
                return documents
                
            elif file_path.endswith('.txt'):
                # Check if it's a special JSON file
                if 'struktur_organisasi.json' in filename:
                    return self._parse_organizational_structure(file_path)
                elif 'additional_info.json' in filename:
                    return self._parse_additional_info(file_path)
                else:
                    # Regular text file
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents = loader.load()
                    
                    # Add metadata
                    for doc in documents:
                        doc.metadata.update({
                            'source': filename,
                            'title': filename,
                            'file_type': 'txt',
                            'language': 'indonesian'
                        })
                    return documents
                    
            elif file_path.endswith('.json'):
                # Handle JSON files specifically
                if 'struktur_organisasi.json' in filename:
                    return self._parse_organizational_structure(file_path)
                elif 'additional_info.json' in filename:
                    return self._parse_additional_info(file_path)
                else:
                    # Generic JSON handling
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Convert JSON to readable text
                        content = json.dumps(data, indent=2, ensure_ascii=False)
                        document = Document(
                            page_content=content,
                            metadata={
                                'source': filename,
                                'title': filename,
                                'file_type': 'json',
                                'language': 'indonesian'
                            }
                        )
                        return [document]
                    except Exception as e:
                        logger.error(f"Error parsing JSON file {filename}: {str(e)}")
                        return []
            else:
                logger.warning(f"Unsupported file type: {filename}")
                return []
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            return []
    
    def load_web_sources(self) -> List[Document]:
        """Load documents from LPDP web sources"""
        documents = []
        
        # Set user agent from environment variable
        user_agent = os.getenv('USER_AGENT', 'LPDP-RAG-Bot/1.0')
        
        for source_config in self.lpdp_web_sources:
            try:
                logger.info(f"Loading web source: {source_config['url']}")
                
                # Create WebBaseLoader with user agent and specific parsing rules
                loader = WebBaseLoader(
                    web_paths=(source_config["url"],),
                    bs_kwargs=source_config["bs_kwargs"],
                    header_template={'User-Agent': user_agent}
                )
                
                # Load documents
                web_docs = loader.load()
                
                # Add metadata to documents
                for doc in web_docs:
                    doc.metadata.update(source_config["metadata"])
                    doc.metadata["url"] = source_config["url"]
                
                documents.extend(web_docs)
                logger.info(f"Successfully loaded {len(web_docs)} documents from {source_config['url']}")
                
            except Exception as e:
                logger.error(f"Error loading web source {source_config['url']}: {str(e)}")
                continue
        
        return documents
    
    def populate_from_web_and_files(self, documents_dir: str = "./data/documents") -> bool:
        """Populate vector store from web sources and local files with selective translation"""
        try:
            all_documents = []
            
            # 1. Load web sources
            logger.info("Loading web sources...")
            web_docs = self.load_web_sources()
            if web_docs:
                # Translate web documents to Indonesian
                logger.info(f"Translating {len(web_docs)} web documents to Indonesian...")
                translated_web_docs = self._translate_web_documents(web_docs)  # Changed from _translate_documents
                all_documents.extend(translated_web_docs)
            
            # 2. Load local files (PDF, TXT, JSON)
            logger.info("Loading local files...")
            import glob
            import os
            
            # Get all PDF and JSON files from documents directory
            pdf_files = glob.glob(os.path.join(documents_dir, "*.pdf"))
            json_files = glob.glob(os.path.join(documents_dir, "*.json"))
            
            for file_path in pdf_files + json_files:
                file_docs = self._load_document(file_path)
                if file_docs:
                    # Local files (PDF, JSON) are NOT translated - they're already in Indonesian
                    all_documents.extend(file_docs)
            
            if all_documents:
                # Split documents into chunks
                split_docs = self.text_splitter.split_documents(all_documents)
                
                # Add to vector store
                self.vectorstore.add_documents(split_docs)
                
                logger.info(f"Successfully populated vector store with {len(split_docs)} chunks from {len(all_documents)} documents")
                return True
            else:
                logger.warning("No documents found to populate")
                return False
            
        except Exception as e:
            logger.error(f"Error populating from web and files: {str(e)}")
            return False
    
    def _translate_web_documents(self, documents: List[Document]) -> List[Document]:
        """Translate web documents from English to Indonesian"""
        if not self.translation_service.is_available():
            logger.warning("Translation service not available, keeping original documents")
            return documents
        
        logger.info(f"Translating {len(documents)} web documents to Indonesian...")
        translated_docs = []
        
        for i, doc in enumerate(documents, 1):
            try:
                # Use the correct method name: translate_text instead of translate_to_indonesian
                translated_content = self.translation_service.translate_text(
                    doc.page_content, 
                    source_lang='en', 
                    target_lang='id'
                )
                
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
                logger.info(f"Successfully translated document {i}/{len(documents)}")
                
            except Exception as e:
                logger.error(f"Error translating document {i}: {e}")
                # Keep original if translation fails
                translated_docs.append(doc)
        
        return translated_docs
        
    def _parse_organizational_structure(self, file_path: str) -> List[Document]:
        """Parse organizational structure JSON file into readable documents"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            
            # Parse President Director
            if "President Director" in data:
                doc_content = f"Direktur Utama LPDP: {data['President Director']}"
                documents.append(Document(
                    page_content=doc_content,
                    metadata={"source": "struktur_organisasi.json", "type": "organizational_structure", "role": "president_director"}
                ))
            
            # Parse Head of Internal Audit Unit
            if "Head of Internal Audit Unit" in data:
                doc_content = f"Kepala Unit Audit Internal LPDP: {data['Head of Internal Audit Unit']}"
                documents.append(Document(
                    page_content=doc_content,
                    metadata={"source": "struktur_organisasi.json", "type": "organizational_structure", "role": "audit_head"}
                ))
            
            # Parse Directorates with proper structure
            if "Directorates" in data:
                for directorate in data["Directorates"]:
                    director_name = directorate.get("Director", "")
                    position = directorate.get("Position", "")
                    
                    # Create director document with complete info
                    director_content = f"{director_name} adalah {position} di LPDP."
                    documents.append(Document(
                        page_content=director_content,
                        metadata={
                            "source": "struktur_organisasi.json", 
                            "type": "organizational_structure", 
                            "role": "director",
                            "director_name": director_name,
                            "position": position
                        }
                    ))
                    
                    # Parse divisions under this directorate
                    if "Divisions" in directorate:
                        for division in directorate["Divisions"]:
                            head_name = division.get("Head", "")
                            division_title = division.get("Division", "")
                            
                            if head_name and head_name.lower() != "null":
                                # Create division document with hierarchy info
                                division_content = f"{head_name} adalah {division_title} di bawah {position} ({director_name}) di LPDP."
                                documents.append(Document(
                                    page_content=division_content,
                                    metadata={
                                        "source": "struktur_organisasi.json", 
                                        "type": "organizational_structure", 
                                        "role": "division_head",
                                        "head_name": head_name,
                                        "division": division_title,
                                        "director": director_name,
                                        "directorate": position
                                    }
                                ))
                            else:
                                # Document vacant position
                                vacant_content = f"Posisi {division_title} di bawah {position} ({director_name}) saat ini kosong atau sedang dicari."
                                documents.append(Document(
                                    page_content=vacant_content,
                                    metadata={
                                        "source": "struktur_organisasi.json", 
                                        "type": "organizational_structure", 
                                        "role": "vacant_position",
                                        "division": division_title,
                                        "director": director_name,
                                        "directorate": position
                                    }
                                ))
                    
                    # Create summary document for the directorate
                    division_names = [div.get("Division", "") for div in directorate.get("Divisions", [])]
                    directorate_summary = f"Direktorat {position} dipimpin oleh {director_name} dan membawahi divisi-divisi: {', '.join(division_names)}."
                    documents.append(Document(
                        page_content=directorate_summary,
                        metadata={
                            "source": "struktur_organisasi.json", 
                            "type": "organizational_structure", 
                            "role": "directorate_summary",
                            "director": director_name,
                            "directorate": position,
                            "num_divisions": len(division_names)
                        }
                    ))
            
            logger.info(f"Parsed {len(documents)} documents from organizational structure")
            return documents
            
        except Exception as e:
            logger.error(f"Error parsing organizational structure: {str(e)}")
            return []
    
    def _parse_additional_info(self, file_path: str) -> List[Document]:
        """Parse additional info JSON file into readable documents"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            
            # Parse contact information
            if "contact_information" in data:
                contact_info = data["contact_information"]
                
                # Customer service info
                if "customer_service" in contact_info:
                    cs_info = contact_info["customer_service"]
                    cs_content = f"""Informasi Customer Service LPDP:
                        - Telepon: {cs_info.get('phone', '')}
                        - Email: {cs_info.get('email', '')}
                        - Website: {cs_info.get('website', '')}
                        - Jam Operasional: {cs_info.get('operating_hours', '')}"""
                    
                    documents.append(Document(
                        page_content=cs_content,
                        metadata={"source": "additional_info.json", "type": "contact_info", "category": "customer_service"}
                    ))
                
                # Address info
                if "address" in contact_info:
                    addr_info = contact_info["address"]
                    addr_content = f"""Alamat Kantor Pusat LPDP:
                    {addr_info.get('head_office', '')}
                    Kode Pos: {addr_info.get('postal_code', '')}
                    Provinsi: {addr_info.get('province', '')}"""
                    
                    documents.append(Document(
                        page_content=addr_content,
                        metadata={"source": "additional_info.json", "type": "contact_info", "category": "address"}
                    ))
            
            # Parse social media
            if "social_media" in data:
                social_media = data["social_media"]
                social_content = f"""Media Sosial LPDP:
                    - Facebook: {social_media.get('facebook', '')}
                    - Twitter: {social_media.get('twitter', '')}
                    - Instagram: {social_media.get('instagram', '')}
                    - YouTube: {social_media.get('youtube', '')}
                    - LinkedIn: {social_media.get('linkedin', '')}"""
                
                documents.append(Document(
                    page_content=social_content,
                    metadata={"source": "additional_info.json", "type": "social_media"}
                ))
            
            # Parse important dates
            if "important_dates_2025" in data:
                dates_info = data["important_dates_2025"]
                if "registration_periods" in dates_info:
                    for batch in dates_info["registration_periods"]:
                        batch_content = f"""Jadwal Pendaftaran {batch.get('batch', '')} 2025:
                        - Pendaftaran Dibuka: {batch.get('registration_start', '')}
                        - Pendaftaran Ditutup: {batch.get('registration_end', '')}
                        - Pengumuman: {batch.get('announcement', '')}"""
                        
                        documents.append(Document(
                            page_content=batch_content,
                            metadata={
                                "source": "additional_info.json", 
                                "type": "registration_schedule", 
                                "batch": batch.get('batch', ''),
                                "year": "2025"
                            }
                        ))
            
            # Parse scholarship statistics
            if "scholarship_statistics" in data:
                stats = data["scholarship_statistics"]
                stats_content = f"""Statistik Beasiswa LPDP:
                - Total Penerima Beasiswa sejak 2013: {stats.get('total_awardees_since_2013', '')}
                - Negara yang Dicakup: {stats.get('countries_covered', '')}
                - Universitas Mitra: {stats.get('universities_partnered', '')}
                - Bidang Studi: {stats.get('fields_of_study', '')}"""
                
                documents.append(Document(
                    page_content=stats_content,
                    metadata={"source": "additional_info.json", "type": "statistics"}
                ))
            
            logger.info(f"Parsed {len(documents)} documents from additional info")
            return documents
            
        except Exception as e:
            logger.error(f"Error parsing additional info: {str(e)}")
            return []
