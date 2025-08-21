"""
Agent-based RAG Chain using LangGraph (Experimental - Commented)
"""

# """
# Experimental Agent-based RAG implementation
# This code is commented out to avoid conflicts with the main stateful chain approach
# Uncomment to experiment with agent-based approach

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# LangGraph imports
# from langgraph.prebuilt import create_react_agent
# from langgraph.checkpoint.memory import MemorySaver

# LangChain imports
# from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_core.documents import Document
# from langchain_core.tools import tool

# try:
#     from langchain_groq import ChatGroq
# except ImportError:
#     try:
#         from langchain_community.llms import Groq as ChatGroq
#     except ImportError:
#         ChatGroq = None

# from services.vector_store import VectorStoreService

# logger = logging.getLogger(__name__)

# class AgentRAGChain:
#     \"\"\"Agent-based RAG Chain using LangGraph create_react_agent\"\"\"
    
#     def __init__(self, vector_service: VectorStoreService):
#         \"\"\"Initialize the agent RAG chain\"\"\"
#         self.vector_service = vector_service
#         self.retriever = vector_service.get_retriever(k=5)
        
#         # Initialize LLM
#         self.llm = self._initialize_llm()
        
#         # Create retrieve tool
#         self.retrieve_tool = self._create_retrieve_tool()
        
#         # Memory for conversation state
#         self.memory = MemorySaver()
        
#         # 1. Create Agent Executor
#         # Agent is created in one line, including LLM, tools list, 
#         # and checkpointer for memory.
#         if self.llm:
#             self.agent_executor = create_react_agent(
#                 self.llm, 
#                 [self.retrieve_tool], 
#                 checkpointer=self.memory
#             )
#         else:
#             self.agent_executor = None
        
#         logger.info("Agent RAG Chain initialized (experimental)")
    
#     def _initialize_llm(self):
#         \"\"\"Initialize LLM\"\"\"
#         if ChatGroq and os.getenv('GROQ_API_KEY'):
#             try:
#                 return ChatGroq(
#                     groq_api_key=os.getenv('GROQ_API_KEY'),
#                     model_name=os.getenv('GROQ_MODEL', 'llama3-8b-8192'),
#                     temperature=0.1,
#                     max_retries=1,
#                     request_timeout=15.0,
#                     max_tokens=512
#                 )
#             except Exception as e:
#                 logger.error(f"Failed to initialize LLM: {e}")
#                 return None
#         return None
    
#     def _create_retrieve_tool(self):
#         \"\"\"Create retrieve tool for document retrieval\"\"\"
#         @tool
#         def retrieve(query: str) -> List[Document]:
#             \"\"\"Retrieve relevant documents for a given query.\"\"\"
#             try:
#                 documents = self.retriever.invoke(query)
#                 logger.info(f"Retrieved {len(documents)} documents for query: {query}")
#                 return documents
#             except Exception as e:
#                 logger.error(f"Error in retrieval: {str(e)}")
#                 return []
        
#         return retrieve
    
#     def invoke(self, question: str, session_id: str = "default") -> Dict[str, Any]:
#         \"\"\"Invoke the agent RAG chain with a question\"\"\"
#         try:
#             if not self.agent_executor:
#                 return {
#                     "answer": "Agent tidak tersedia saat ini.",
#                     "sources": [],
#                     "confidence": 0.0,
#                     "needs_continuation": False,
#                     "metadata": {"error": "Agent not available"}
#                 }
            
#             # 2. Configuration for conversation thread
#             # Create unique ID for each conversation session.
#             # Here we use session_id to differentiate from chain thread.
#             config = {"configurable": {"thread_id": f"agent_{session_id}"}}
            
#             # 3. Define user input
#             # This question is intentionally made complex to show agent capabilities
#             # in taking multiple steps.
#             input_message = {
#                 "messages": [{"role": "user", "content": question}]
#             }
            
#             # 4. Call (Invoke) Agent and collect results
#             # Use .stream() to see each step the agent takes in real-time.
#             result_messages = []
#             for event in self.agent_executor.stream(
#                 input_message,
#                 stream_mode="values",
#                 config=config,
#             ):
#                 # Collect the last message from each step
#                 result_messages.extend(event["messages"])
            
#             # Extract final answer from the last AI message
#             final_answer = "Tidak ada jawaban yang dihasilkan."
#             for message in reversed(result_messages):
#                 if hasattr(message, 'type') and message.type == 'ai':
#                     final_answer = message.content
#                     break
            
#             # Format response
#             return {
#                 "answer": final_answer,
#                 "sources": self._extract_sources_from_messages(result_messages),
#                 "confidence": 0.8,
#                 "needs_continuation": False,
#                 "metadata": {
#                     "session_id": session_id,
#                     "timestamp": datetime.now().isoformat(),
#                     "approach": "agent_based",
#                     "steps_taken": len(result_messages)
#                 }
#             }
            
#         except Exception as e:
#             logger.error(f"Error in agent RAG chain invocation: {str(e)}")
#             return {
#                 "answer": "Maaf, terjadi kesalahan dalam memproses pertanyaan Anda.",
#                 "sources": [],
#                 "confidence": 0.0,
#                 "needs_continuation": False,
#                 "metadata": {"error": str(e)}
#             }
    
#     def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
#         \"\"\"Get session history\"\"\"
#         try:
#             if not self.agent_executor:
#                 return []
                
#             config = {"configurable": {"thread_id": f"agent_{session_id}"}}
#             state = self.agent_executor.get_state(config)
            
#             if not state.values or "messages" not in state.values:
#                 return []
            
#             history = []
#             for message in state.values["messages"]:
#                 if hasattr(message, 'type') and message.type in ["human", "ai"]:
#                     history.append({
#                         "type": message.type,
#                         "content": message.content,
#                         "timestamp": getattr(message, 'timestamp', None)
#                     })
            
#             return history
            
#         except Exception as e:
#             logger.error(f"Error getting agent session history: {str(e)}")
#             return []
    
#     def clear_session(self, session_id: str) -> bool:
#         \"\"\"Clear session history\"\"\"
#         try:
#             if not self.agent_executor:
#                 return True
                
#             config = {"configurable": {"thread_id": f"agent_{session_id}"}}
#             self.agent_executor.update_state(config, {"messages": []})
#             return True
#         except Exception as e:
#             logger.error(f"Error clearing agent session: {str(e)}")
#             return False
    
#     def _extract_sources_from_messages(self, messages: List) -> List[Dict[str, Any]]:
#         \"\"\"Extract sources from tool messages\"\"\"
#         sources = []
#         for message in messages:
#             if hasattr(message, 'type') and message.type == "tool":
#                 sources.append({
#                     "title": "Retrieved Document",
#                     "source": "Agent Tool Call"
#                 })
#         return sources

# """
# 
# End of commented experimental agent-based implementation
# 
# To experiment with this approach:
# 1. Uncomment the code above
# 2. Install required dependencies
# 3. Update the main RAG service to use AgentRAGChain instead of SimpleRAGChain
# 4. Note that this approach may be more resource-intensive than the stateful chain
# """
