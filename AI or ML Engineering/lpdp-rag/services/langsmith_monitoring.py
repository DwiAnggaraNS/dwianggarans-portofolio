"""
LangSmith Monitoring Service for LPDP Scholarship AI Assistant
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

# LangSmith imports
try:
    from langsmith import Client
    from langsmith.run_helpers import traceable
    from langchain.callbacks.tracers import LangChainTracer
    from langchain.callbacks.manager import CallbackManager
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

logger = logging.getLogger(__name__)

class LangSmithMonitoring:
    """
    LangSmith monitoring and observability service for LPDP RAG system
    """
    
    def __init__(self):
        self.client = None
        self.tracer = None
        self.enabled = False
        self.project_name = os.getenv('LANGCHAIN_PROJECT', 'lpdp-rag-assistant')
        
        # Initialize LangSmith if available and configured
        if LANGSMITH_AVAILABLE and os.getenv('LANGCHAIN_API_KEY'):
            try:
                self.client = Client(
                    api_url=os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com'),
                    api_key=os.getenv('LANGCHAIN_API_KEY')
                )
                
                self.tracer = LangChainTracer(
                    project_name=self.project_name,
                    client=self.client
                )
                
                self.enabled = True
                logger.info(f"LangSmith monitoring initialized successfully for project: {self.project_name}")
                
            except Exception as e:
                logger.warning(f"Failed to initialize LangSmith: {e}")
                self.enabled = False
        else:
            if not LANGSMITH_AVAILABLE:
                logger.info("LangSmith not available. Install langsmith package to enable monitoring.")
            else:
                logger.info("LangSmith API key not found. Set LANGCHAIN_API_KEY environment variable to enable monitoring.")
            self.enabled = False
    
    def get_callback_manager(self) -> Optional[CallbackManager]:
        """Get callback manager with LangSmith tracer"""
        if self.enabled and self.tracer:
            return CallbackManager([self.tracer])
        return None
    
    def get_callbacks(self) -> List:
        """Get callbacks list for langchain operations"""
        if self.enabled and self.tracer:
            return [self.tracer]
        return []
    
    @traceable(name="document_retrieval")
    def trace_retrieval(self, query: str, documents: list, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Trace document retrieval operations"""
        if not self.enabled:
            return {}
            
        return {
            "query": query,
            "num_documents": len(documents),
            "document_sources": [doc.metadata.get('source', 'unknown') for doc in documents] if documents else [],
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @traceable(name="answer_generation")
    def trace_generation(self, query: str, context: str, answer: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Trace answer generation"""
        if not self.enabled:
            return {}
            
        return {
            "query": query,
            "context_length": len(context),
            "answer_length": len(answer),
            "answer": answer,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @traceable(name="rag_chain_execution")
    def trace_rag_chain(self, query: str, result: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Trace complete RAG chain execution"""
        if not self.enabled:
            return {}
            
        return {
            "query": query,
            "session_id": session_id,
            "answer": result.get("answer", ""),
            "confidence": result.get("confidence", 0.0),
            "num_sources": len(result.get("sources", [])),
            "needs_continuation": result.get("needs_continuation", False),
            "metadata": result.get("metadata", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def log_user_feedback(self, run_id: str, feedback: Dict[str, Any]) -> bool:
        """Log user feedback to LangSmith"""
        if not self.enabled or not self.client:
            return False
            
        try:
            self.client.create_feedback(
                run_id=run_id,
                key="user_rating",
                score=feedback.get("rating", 0),
                comment=feedback.get("comment", ""),
                metadata=feedback.get("metadata", {})
            )
            return True
        except Exception as e:
            logger.error(f"Error logging feedback: {e}")
            return False
    
    def get_run_stats(self, limit: int = 100) -> Dict[str, Any]:
        """Get run statistics from LangSmith"""
        if not self.client:
            return {}
            
        try:
            runs = self.client.list_runs(
                project_name=self.project_name,
                limit=limit
            )
            
            stats = {
                "total_runs": len(runs),
                "avg_latency": 0,
                "error_rate": 0,
                "run_types": {}
            }
            
            if runs:
                total_latency = 0
                errors = 0
                
                for run in runs:
                    # Calculate latency
                    if run.end_time and run.start_time:
                        latency = (run.end_time - run.start_time).total_seconds()
                        total_latency += latency
                    
                    # Count errors
                    if run.error:
                        errors += 1
                    
                    # Count run types
                    run_type = run.run_type or "unknown"
                    stats["run_types"][run_type] = stats["run_types"].get(run_type, 0) + 1
                
                stats["avg_latency"] = total_latency / len(runs)
                stats["error_rate"] = errors / len(runs)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting run stats: {e}")
            return {}
    
    def create_dataset(self, name: str, examples: list) -> bool:
        """Create a dataset in LangSmith"""
        if not self.client:
            return False
            
        try:
            dataset = self.client.create_dataset(
                dataset_name=name,
                description=f"LPDP RAG Dataset - {datetime.now().isoformat()}"
            )
            
            for example in examples:
                self.client.create_example(
                    dataset_id=dataset.id,
                    inputs=example.get("inputs", {}),
                    outputs=example.get("outputs", {})
                )
            
            logger.info(f"Created dataset '{name}' with {len(examples)} examples")
            return True
            
        except Exception as e:
            logger.error(f"Error creating dataset: {e}")
            return False

# Global monitoring instance
monitoring = LangSmithMonitoring()
