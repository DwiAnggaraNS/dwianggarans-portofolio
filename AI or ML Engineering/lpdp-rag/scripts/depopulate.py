"""
Script to clear the vector database and LangGraph checkpoints
"""
import chromadb
import os
import sqlite3
import shutil
import time
import gc
import psutil
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("depopulate.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def force_close_chroma_processes():
    """Force close any ChromaDB related processes"""
    try:
        current_pid = os.getpid()
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Skip current process
                if proc.info['pid'] == current_pid:
                    continue
                    
                # Check if process is related to ChromaDB or our application
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(keyword in cmdline.lower() for keyword in ['chroma', 'lpdp-rag', 'populate_knowledge_base']):
                    logger.info(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    proc.wait(timeout=5)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        logger.warning(f"Error closing processes: {str(e)}")

def clear_chroma_db():
    """Clear ChromaDB collection and database files with force cleanup"""
    try:
        # Get ChromaDB path from environment variables
        db_path = os.getenv('CHROMA_DB_PATH', './data/chroma_db')
        collection_name = os.getenv('CHROMA_COLLECTION_NAME', 'lpdp_docs')

        logger.info(f"Clearing ChromaDB at: {db_path}")

        # Try to delete the collection first (graceful approach)
        try:
            client = chromadb.PersistentClient(path=db_path)
            try:
                client.delete_collection(collection_name)
                logger.info(f"[OK] ChromaDB collection '{collection_name}' successfully deleted.")
            except Exception as e:
                logger.warning(f"Collection might not exist or already deleted: {str(e)}")
            
            # Properly close the client
            del client
            gc.collect()
            time.sleep(1)  # Give it time to release resources
            
        except Exception as e:
            logger.warning(f"Could not connect to ChromaDB gracefully: {str(e)}")

        # Force close any related processes
        logger.info("Forcing close of any ChromaDB related processes...")
        force_close_chroma_processes()
        time.sleep(2)

        # Force garbage collection
        gc.collect()
        time.sleep(1)

        # Try to remove the directory multiple times
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                if os.path.exists(db_path):
                    # Try to unlock files first
                    for root, dirs, files in os.walk(db_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                # Remove read-only attribute if present
                                os.chmod(file_path, 0o777)
                            except:
                                pass
                    
                    shutil.rmtree(db_path)
                    logger.info(f"[OK] Removed ChromaDB directory: {db_path}")
                    break
                else:
                    logger.info(f"[OK] ChromaDB directory already removed: {db_path}")
                    break
                    
            except Exception as e:
                if attempt < max_attempts - 1:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    logger.info(f"Waiting 3 seconds before retry...")
                    time.sleep(3)
                else:
                    logger.error(f"[FAIL] Failed to remove ChromaDB directory after {max_attempts} attempts: {str(e)}")
                    logger.info("Manual cleanup required:")
                    logger.info(f"1. Close all Python processes")
                    logger.info(f"2. Manually delete folder: {db_path}")
                    logger.info(f"3. Run this script again")
                    return False

        # Recreate the directory
        os.makedirs(db_path, exist_ok=True)
        logger.info(f"[OK] Recreated ChromaDB directory: {db_path}")

        # Initialize fresh ChromaDB
        try:
            client = chromadb.PersistentClient(path=db_path)
            client.create_collection(collection_name)
            logger.info(f"[OK] Created fresh ChromaDB collection '{collection_name}'")
            del client
            gc.collect()
        except Exception as e:
            logger.error(f"[FAIL] Failed to create fresh collection: {str(e)}")
            return False

        return True
        
    except Exception as e:
        logger.error(f"[FAIL] Error managing ChromaDB collection: {str(e)}")
        return False

def clear_langgraph_checkpoints():
    """Clear LangGraph SQLite checkpoints"""
    try:
        db_path = os.getenv('SQLITE_DB_PATH', './data/langgraph_checkpoints.db')
        
        if not os.path.exists(db_path):
            logger.info(f"LangGraph checkpoint database does not exist: {db_path}")
            return True
        
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Clear checkpoints table
        try:
            cursor.execute("DELETE FROM checkpoints")
            deleted_checkpoints = cursor.rowcount
        except sqlite3.OperationalError:
            deleted_checkpoints = 0
            logger.warning("Checkpoints table might not exist")
        
        # Clear writes table
        try:
            cursor.execute("DELETE FROM writes")
            deleted_writes = cursor.rowcount
        except sqlite3.OperationalError:
            deleted_writes = 0
            logger.warning("Writes table might not exist")
        
        conn.commit()
        conn.close()
        
        logger.info(f"[OK] Cleared {deleted_checkpoints} checkpoints and {deleted_writes} writes from LangGraph database")
        return True
        
    except Exception as e:
        logger.error(f"[FAIL] Error clearing LangGraph checkpoints: {str(e)}")
        return False

def clear_all():
    """Clear all data - ChromaDB and LangGraph checkpoints"""
    logger.info("Starting complete data cleanup...")
    logger.info("This will remove all ChromaDB files to fix schema compatibility issues")
    
    success = True
    
    # Clear ChromaDB
    if not clear_chroma_db():
        success = False
    
    # Clear LangGraph checkpoints
    if not clear_langgraph_checkpoints():
        success = False
    
    if success:
        logger.info("[SUCCESS] All data successfully cleared!")
        logger.info("ChromaDB schema has been reset to fix compatibility issues")
        logger.info("You can now repopulate with: python scripts/populate_knowledge_base.py")
    else:
        logger.error("[FAIL] Some operations failed. Check the logs above.")
        logger.info("\nTroubleshooting steps:")
        logger.info("1. Close all Python processes and IDEs")
        logger.info("2. Close any terminal windows running LPDP scripts")
        logger.info("3. Wait 30 seconds")
        logger.info("4. Run this script again")
    
    return success

if __name__ == "__main__":
    import sys
    
    # Check if psutil is available
    try:
        import psutil
    except ImportError:
        logger.error("psutil library required for process management")
        logger.info("Install with: pip install psutil")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--chroma-only":
            clear_chroma_db()
        elif sys.argv[1] == "--langgraph-only":
            clear_langgraph_checkpoints()
        elif sys.argv[1] == "--all":
            clear_all()
        else:
            print("Usage: python scripts/depopulate.py [--chroma-only|--langgraph-only|--all]")
    else:
        # Default: clear all
        clear_all()