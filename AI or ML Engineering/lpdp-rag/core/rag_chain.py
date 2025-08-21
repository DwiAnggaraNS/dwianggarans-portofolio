"""
Simple RAG Chain using LangGraph with Stateful Chain approach and LangSmith integration
"""
import os
import logging
from typing import Dict, List, Any, Optional, Annotated
from datetime import datetime

# LangGraph imports
try:
    from langgraph.graph import MessagesState, StateGraph, END
except ImportError:
    # Fallback for older versions
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from typing_extensions import TypedDict
    from langchain_core.messages import BaseMessage
    
    # Create MessagesState if not available
    class MessagesState(TypedDict):
        messages: Annotated[List[BaseMessage], add_messages]

from langgraph.prebuilt import ToolNode

# Try different memory imports based on version
try:
    from langgraph.checkpoint.memory import MemorySaver
except ImportError:
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        MemorySaver = None
    except ImportError:
        MemorySaver = None

# LangChain imports
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.documents import Document
from langchain_core.tools import tool

try:
    from langchain_groq import ChatGroq
except ImportError:
    try:
        from langchain_community.llms import Groq as ChatGroq
    except ImportError:
        ChatGroq = None

# Conditional import for tools condition
try:
    from langgraph.prebuilt import tools_condition
except ImportError:
    # Fallback implementation
    def tools_condition(state):
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return END

from services.vector_store import VectorStoreService
from services.llm_service import LLMService
from services.langsmith_monitoring import LangSmithMonitoring

# Import LangSmith monitoring
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from services.langsmith_monitoring import LangSmithMonitoring
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

logger = logging.getLogger(__name__)

class SimpleRAGChain:
    """Simple RAG Chain using LangGraph with stateful chain approach and LangSmith monitoring"""
    
    def __init__(self, vector_service: VectorStoreService):
        """Initialize the RAG chain"""
        self.vector_service = vector_service
        self.retriever = vector_service.get_retriever(k=5)
        
        # Initialize LangSmith monitoring
        if LANGSMITH_AVAILABLE:
            self.langsmith = LangSmithMonitoring()
        else:
            self.langsmith = None
        
        # Initialize LLM with LangSmith monitoring
        self.llm_service = LLMService(langsmith_monitoring=self.langsmith)
        self.llm = self.llm_service.llm

        # Create retrieve tool
        self.search_tool = self._create_retrieve_tool()
        
        # Initialize graph
        self.graph = self._build_stateful_graph()
        
        # Initialize memory with fallback
        self.memory = self._initialize_memory()
        
        # Compile graph with or without memory
        if self.memory:
            self.compiled_graph = self.graph.compile(checkpointer=self.memory)
        else:
            self.compiled_graph = self.graph.compile()
            # Fallback: use simple in-memory storage
            self.session_histories = {}
        
        logger.info("Simple RAG Chain initialized with stateful approach and LangSmith monitoring")
    
    def _initialize_memory(self):
        """Initialize memory with version compatibility"""
        try:
            if MemorySaver:
                return MemorySaver()
            else:
                logger.warning("MemorySaver not available, using fallback history management")
                return None
        except Exception as e:
            logger.error(f"Failed to initialize memory: {e}")
            return None
    
    def _create_retrieve_tool(self):
        """Create retrieve tool for document retrieval"""
        @tool("search")
        def search(query: str) -> List[Document]:
            """Search for relevant documents about LPDP scholarship information for a given query."""
            try:
                documents = self.retriever.invoke(query)
                logger.info(f"Retrieved {len(documents)} documents for query: {query}")
                return documents
            except Exception as e:
                logger.error(f"Error in retrieval: {str(e)}")
                return []
        
        return search
    
    def _build_stateful_graph(self):
        """Build the stateful RAG graph following the specified pattern"""
        # Initialize StateGraph with MessagesState
        graph_builder = StateGraph(MessagesState)
        
        # Step 1: Query or respond node
        def query_or_respond(state: MessagesState):
            """Generate tool call for retrieval or respond."""
            if not self.llm:
                # Fallback without LLM
                return {"messages": [AIMessage(content="LLM tidak tersedia saat ini.")]}
            
            try:
                # Add system message to guide tool usage
                system_msg = SystemMessage(content=(
                    "Anda adalah AI assistant untuk beasiswa LPDP. "
                    "Untuk setiap pertanyaan pengguna, WAJIB gunakan tool 'search' untuk mencari informasi yang relevan "
                    "dari database dokumen beasiswa LPDP sebelum memberikan jawaban. "
                    "Jangan pernah menjawab tanpa menggunakan tool search terlebih dahulu."
                ))
                
                # Prepare messages with system guidance
                messages_with_system = [system_msg] + state["messages"]
                
                llm_with_tools = self.llm.bind_tools([self.search_tool])
                response = llm_with_tools.invoke(messages_with_system)
                # MessagesState appends messages to state instead of overwriting
                return {"messages": [response]}
            except Exception as e:
                logger.error(f"Error in query_or_respond: {e}")
                return {"messages": [AIMessage(content="Terjadi kesalahan dalam memproses permintaan.")]}
        
        # Step 2: Tool execution
        tools = ToolNode([self.search_tool])
        
        # Step 3: Generate response using retrieved content
        def generate(state: MessagesState):
            """Generate answer."""
            if not self.llm:
                return {"messages": [AIMessage(content="LLM tidak tersedia untuk menghasilkan jawaban.")]}
            
            try:
                # Get generated ToolMessages
                recent_tool_messages = []
                for message in reversed(state["messages"]):
                    if hasattr(message, 'type') and message.type == "tool":
                        recent_tool_messages.append(message)
                    else:
                        break
                tool_messages = recent_tool_messages[::-1]

                # Format into prompt
                docs_content = "\n\n".join(str(doc.content) for doc in tool_messages)
                system_message_content = (
                    "Role\n"
                    "Anda adalah AI Assistant ahli untuk program Beasiswa LPDP (Lembaga Pengelola Dana Pendidikan) Indonesia. "
                    "Anda memiliki pengetahuan mendalam tentang semua aspek beasiswa LPDP termasuk persyaratan, prosedur pendaftaran, "
                    "jenis beasiswa, dan informasi terkait dari dokumen-dokumen yang ada pada vector db.\n\n"
                    
                    "# Input\n"
                    "Pengguna bertanya tentang program Beasiswa LPDP dan membutuhkan informasi yang akurat dan terpercaya. "
                    "Konteks dokumen berikut tersedia untuk menjawab pertanyaan:\n\n"
                    f"{docs_content}\n\n"

                    "# Steps\n"
                    "1. Analisis pertanyaan dengan cermat untuk memahami kebutuhan informasi pengguna\n"
                    "2. Gunakan konteks dokumen yang disediakan sebagai sumber utama informasi\n"
                    "3. Berikan jawaban yang akurat dan berdasarkan fakta dari dokumen\n"
                    "4. Format jawaban dalam markdown dengan struktur yang jelas\n"
                    "5. Gunakan numbered lists (1. 2. 3.) untuk langkah-langkah atau daftar berurutan\n"
                    "6. Gunakan bullet points (-) untuk daftar item tanpa urutan\n"
                    "7. Gunakan **bold** dan *italic* untuk penekanan penting\n"
                    "8. Jika informasi tidak tersedia atau kurang yakin, jujur sampaikan keterbatasan\n\n"
                    
                    "# Expectation\n"
                    "- Bahasa: Indonesia yang baik dan benar\n"
                    "- Format: Markdown dengan struktur jelas\n"
                    "- Panjang: 3-5 paragraf atau sesuai kompleksitas pertanyaan\n"
                    
                    "# Narrowing\n"
                    "Pastikan pertanyaan dan jawaban berada di domain LPDP. Jika user bertanya hal diluar domain maka jawab tidak bisa dan gunakan bahasa yang sopan\n"
                )
                
                conversation_messages = [
                    message
                    for message in state["messages"]
                    if hasattr(message, 'type') and message.type in ("human", "system")
                    or (hasattr(message, 'type') and message.type == "ai" and not hasattr(message, 'tool_calls'))
                ]
                prompt = [SystemMessage(content=system_message_content)] + conversation_messages

                # Run
                response = self.llm.invoke(prompt)
                return {"messages": [response]}
            except Exception as e:
                logger.error(f"Error in generate: {e}")
                return {"messages": [AIMessage(content="Terjadi kesalahan dalam menghasilkan jawaban.")]}
        
        # Add nodes to graph
        graph_builder.add_node("query_or_respond", query_or_respond)
        graph_builder.add_node("tools", tools)
        graph_builder.add_node("generate", generate)
        
        # Set entry point
        graph_builder.set_entry_point("query_or_respond")
        
        # Add conditional edges
        graph_builder.add_conditional_edges(
            "query_or_respond",
            tools_condition,
            {END: END, "tools": "tools"},
        )
        graph_builder.add_edge("tools", "generate")
        graph_builder.add_edge("generate", END)
        
        return graph_builder
    
    def invoke(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """Invoke the RAG chain with a question and LangSmith tracing"""
        try:
            start_time = datetime.now()
            
            # Create dynamic thread_id based on session and user
            config = {"configurable": {"thread_id": f"user_{session_id}"}}
            
            # Invoke the graph
            if self.memory:
                # Use memory-based approach
                result = self.compiled_graph.invoke(
                    {"messages": [HumanMessage(content=question)]},
                    config
                )
            else:
                # Use fallback approach with manual history management
                # Get existing history
                existing_messages = self.session_histories.get(session_id, [])
                current_messages = existing_messages + [HumanMessage(content=question)]
                
                result = self.compiled_graph.invoke({"messages": current_messages})
                
                # Save history manually
                self.session_histories[session_id] = result["messages"]
            
            # Extract the final answer
            final_message = result["messages"][-1]
            answer = final_message.content if hasattr(final_message, 'content') else str(final_message)
            
            # Extract sources
            sources = self._extract_sources_from_messages(result["messages"])
            
            # Format response
            rag_result = {
                "answer": answer,
                "sources": sources,
                "confidence": 0.8,  # Simple confidence score
                "needs_continuation": False,
                "metadata": {
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat(),
                    "approach": "stateful_chain",
                    "processing_time": (datetime.now() - start_time).total_seconds()
                }
            }
            
            # LangSmith tracing
            if self.langsmith:
                try:
                    self.langsmith.trace_rag_chain(question, rag_result, session_id)
                except Exception as e:
                    logger.warning(f"LangSmith tracing failed: {e}")
            
            return rag_result
            
        except Exception as e:
            logger.error(f"Error in RAG chain invocation: {str(e)}")
            return {
                "answer": "Maaf, terjadi kesalahan dalam memproses pertanyaan Anda.",
                "sources": [],
                "confidence": 0.0,
                "needs_continuation": False,
                "metadata": {"error": str(e)}
            }
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session history"""
        try:
            if self.memory:
                # Use memory-based approach
                config = {"configurable": {"thread_id": f"user_{session_id}"}}
                state = self.compiled_graph.get_state(config)
                
                if not state.values or "messages" not in state.values:
                    return []
                
                history = []
                for message in state.values["messages"]:
                    if hasattr(message, 'type') and message.type in ["human", "ai"]:
                        history.append({
                            "type": message.type,
                            "content": message.content,
                            "timestamp": getattr(message, 'timestamp', None)
                        })
                
                return history
            else:
                # Use fallback approach
                messages = self.session_histories.get(session_id, [])
                history = []
                for message in messages:
                    if hasattr(message, 'type') and message.type in ["human", "ai"]:
                        history.append({
                            "type": message.type,
                            "content": message.content,
                            "timestamp": getattr(message, 'timestamp', None)
                        })
                return history
            
        except Exception as e:
            logger.error(f"Error getting session history: {str(e)}")
            return []
    
    def clear_session(self, session_id: str) -> bool:
        """Clear session history"""
        try:
            if self.memory:
                # Use memory-based approach
                config = {"configurable": {"thread_id": f"user_{session_id}"}}
                # Clear by updating state with empty messages
                self.compiled_graph.update_state(config, {"messages": []})
            else:
                # Use fallback approach
                if session_id in self.session_histories:
                    del self.session_histories[session_id]
            
            return True
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
            return False
    
    def _extract_sources_from_messages(self, messages: List[BaseMessage]) -> List[Dict[str, Any]]:
        """Extract sources from tool messages"""
        sources = []
        for message in messages:
            if hasattr(message, 'type') and message.type == "tool":
                # Tool message contains retrieved documents
                try:
                    # This is simplified - in real implementation, you'd parse the tool content
                    sources.append({
                        "title": "Retrieved Document",
                        "source": "Vector Database"
                    })
                except:
                    pass
        return sources