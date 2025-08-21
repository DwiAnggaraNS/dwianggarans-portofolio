"""
Simple script to populate knowledge base with improved document handling and translation
"""
import os
import sys
import logging
from pathlib import Path

print("Script started...")

# Add project root to path (go up one level from scripts/)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"Project root: {project_root}")
print(f"Core directory exists: {(project_root / 'core').exists()}")

try:
    from services.vector_store import VectorStoreService
    print("VectorStoreService imported successfully")
except ImportError as e:
    print(f"Failed to import VectorStoreService: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to populate knowledge base with selective translation"""
    print("Main function called...")
    try:
        print("Starting LPDP RAG Knowledge Base Population...")
        print("=" * 60)
        
        # Initialize vector store service
        print("Initializing Vector Store Service...")
        vector_service = VectorStoreService()
        print("Vector service initialized")
        
        # Check current document count
        print("Getting collection count...")
        current_count = vector_service.get_collection_count()
        print(f" Current documents in vector store: {current_count}")
        
        if current_count > 0:
            response = input(" Vector store already contains documents. Continue adding? (y/n): ")
            if response.lower() != 'y':
                print("Population cancelled.")
                return 1
        
        # Populate from web sources and local files with selective translation
        print("\n Loading documents from web sources and local files...")
        print(" This process includes:")
        print("   • Loading web content from LPDP official website (will be translated to Indonesian)")
        print("   • Loading local PDF files (already in Indonesian, no translation needed)")
        print("   • Parsing JSON files for organizational structure and additional info")
        print("   • Embedding and storing in vector database")
        
        # Use the improved populate method
        print("Calling populate_from_web_and_files...")
        documents_dir = project_root / "data" / "documents"
        success = vector_service.populate_from_web_and_files(str(documents_dir))
        
        if success:
            # Check final document count
            final_count = vector_service.get_collection_count()
            added_count = final_count - current_count
            
            print("\n" + "=" * 60)
            print("[SUCCESS] Population completed successfully!")
            print(f" Total documents in vector store: {final_count}")
            print(f"+ Documents added in this session: {added_count}")
            print("=" * 60)
            
            print("\n Processed documents include:")
            print("   ✓ Web content from LPDP official website (translated)")
            print("   ✓ PDF scholarship guidebooks (Indonesian)")
            print("   ✓ Organizational structure (properly parsed)")
            print("   ✓ Additional contact and schedule information")
            
            print("\n Next steps:")
            print("1. Run the Flask application: python app.py")
            print("2. Open your browser and go to http://localhost:5000")
            print("3. Start asking questions about LPDP scholarships!")
            
        else:
            print("\n[FAILED] Population failed. Please check the logs for details.")
            return 1
            
    except Exception as e:
        logger.error(f"Error during population: {str(e)}")
        print(f"\n Error during population: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    print("Running main...")
    exit_code = main()
    print(f"Script completed with exit code: {exit_code}")