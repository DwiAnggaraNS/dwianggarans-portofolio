"""
Main Flask application for LPDP Scholarship RAG Website with Simple RAG Chain
"""
import os
import uuid
import tempfile
from flask import Flask, render_template, request, jsonify, session, send_from_directory, url_for
from config import Config
from services.simple_rag_service import SimpleRAGService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize services with error handling
    try:
        rag_service = SimpleRAGService()
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
        rag_service = None 
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        """About LPDP Scholarship page"""
        return render_template('about.html')
    
    @app.route('/chat', methods=['GET', 'POST'])
    def chat():
        """Enhanced chat interface with better error handling"""
        if request.method == 'GET':
            # Initialize session if needed
            if 'session_id' not in session:
                session['session_id'] = str(uuid.uuid4())
            return render_template('chat.html')
        
        try:
            if not rag_service:
                return jsonify({'error': 'Service tidak tersedia saat ini'}), 503
            
            data = request.get_json()
            question = data.get('question', '').strip()
            
            if not question:
                return jsonify({'error': 'Pertanyaan tidak boleh kosong'}), 400
            
            # Rate limiting: max 1 request per 2 seconds per session
            import time
            session_key = f"last_request_{session.get('session_id', 'default')}"
            last_request = session.get(session_key, 0)
            current_time = time.time()
            
            if current_time - last_request < 2:
                return jsonify({'error': 'Silakan tunggu sebentar sebelum mengirim pertanyaan lagi'}), 429
            
            session[session_key] = current_time
            
            # Get or create session ID
            session_id = session.get('session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                session['session_id'] = session_id
            
            # Get answer from RAG service
            response = rag_service.get_answer(question, session_id)
            
            return jsonify({
                'answer': response['answer'],
                'sources': response['sources'],
                'confidence': response['confidence'],
                'needs_continuation': response.get('needs_continuation', False),
                'session_id': session_id,
                'metadata': response.get('metadata', {})
            })
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return jsonify({'error': 'Terjadi kesalahan dalam memproses pertanyaan'}), 500
    
    @app.route('/chat/history', methods=['GET'])
    def get_chat_history():
        """Get chat history with error handling"""
        try:
            if not rag_service:
                return jsonify({'history': []})
            
            session_id = session.get('session_id')
            if not session_id:
                return jsonify({'history': []})
            
            history = rag_service.get_session_history(session_id)
            return jsonify({'history': history})
            
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            return jsonify({'error': 'Gagal mengambil riwayat percakapan'}), 500
    
    @app.route('/chat/clear', methods=['POST'])
    def clear_chat():
        """Clear chat history for current session"""
        try:
            session_id = session.get('session_id')
            if not session_id:
                return jsonify({'success': True})
            
            success = rag_service.clear_session(session_id)
            return jsonify({'success': success})
            
        except Exception as e:
            logger.error(f"Error clearing chat: {str(e)}")
            return jsonify({'error': 'Gagal membersihkan percakapan'}), 500
    
    @app.route('/admin')
    def admin():
        """Admin dashboard"""
        return render_template('admin/dashboard.html')
    
    @app.route('/admin/stats')
    def admin_stats():
        """Get admin statistics"""
        try:
            stats = rag_service.get_collection_stats()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error getting admin stats: {str(e)}")
            return jsonify({'error': 'Gagal mengambil statistik'}), 500
    
    @app.route('/admin/upload', methods=['POST'])
    def upload_documents():
        """Upload and process documents for RAG"""
        try:
            files = request.files.getlist('documents')
            if not files:
                return jsonify({'error': 'Tidak ada file yang diupload'}), 400
            
            processed_count = 0
            for file in files:
                if file.filename and file.filename.endswith(('.pdf', '.txt', '.docx')):
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file.filename.split(".")[-1]}') as temp_file:
                        file.save(temp_file.name)
                        
                        # Process document
                        if rag_service.add_documents([temp_file.name]):
                            processed_count += 1
                        
                        # Clean up
                        os.unlink(temp_file.name)
            
            return jsonify({
                'message': f'{processed_count} dokumen berhasil diproses',
                'count': processed_count
            })
            
        except Exception as e:
            logger.error(f"Error uploading documents: {str(e)}")
            return jsonify({'error': 'Gagal memproses dokumen'}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        try:
            return render_template('errors/404.html'), 404
        except:
            return f"<h1>404 - Halaman Tidak Ditemukan</h1><p><a href='{url_for('index')}'>Kembali ke Beranda</a></p>", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        try:
            return render_template('errors/500.html'), 500
        except:
            return "<h1>500 - Server Error</h1><p>Terjadi kesalahan pada server.</p>", 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """503 error handler"""
        return jsonify({'error': 'Service tidak tersedia saat ini'}), 503
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
