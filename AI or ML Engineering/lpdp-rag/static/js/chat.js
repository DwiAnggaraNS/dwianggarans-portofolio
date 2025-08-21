/**
 * Enhanced Chat functionality with LangGraph integration and improved markdown rendering
 */

// Initialize markdown renderer with enhanced configuration
const md = window.markdownit({
    html: false,
    breaks: true,          // Convert '\n' to <br>
    linkify: true,
    typographer: true,
    quotes: '""',        // Fixed quotes configuration
}).enable(['table', 'strikethrough']);

// Global variables
let chatMessages = document.getElementById('chat-messages');
let messageInput = document.getElementById('message-input');
let chatForm = document.getElementById('chat-form');
let sendButton = document.getElementById('send-button');
let sendText = document.getElementById('send-text');
let loadingText = document.getElementById('loading-text');
let charCounter = document.getElementById('char-counter');
let sessionId = null;
let currentRating = 0;
let currentRunId = null;

// Initialize chat functionality
function initializeChat() {
    // Add custom CSS for better formatting
    addChatStyles();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load chat history and session info
    loadChatHistory();
    
    // Handle prefilled questions
    handlePrefilledQuestion();
    
    // Auto-focus on input
    messageInput.focus();
}

// Add custom CSS styles for better markdown rendering
function addChatStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .chat-message .prose {
            line-height: 1.6;
        }
        .chat-message .prose p {
            margin-bottom: 0.75rem;
        }
        .chat-message .prose ul, .chat-message .prose ol {
            margin: 0.75rem 0;
            padding-left: 1.5rem;
        }
        .chat-message .prose li {
            margin-bottom: 0.25rem;
        }
        .chat-message .prose strong {
            font-weight: 600;
            color: #1f2937;
        }
        .chat-message .prose em {
            font-style: italic;
            color: #374151;
        }
        .chat-message .prose h1, .chat-message .prose h2, .chat-message .prose h3 {
            font-weight: 600;
            margin: 1rem 0 0.5rem 0;
            color: #1f2937;
        }
        .chat-message .prose h1 { font-size: 1.25rem; }
        .chat-message .prose h2 { font-size: 1.125rem; }
        .chat-message .prose h3 { font-size: 1rem; }
        .chat-message .prose blockquote {
            border-left: 4px solid #d1d5db;
            padding-left: 1rem;
            margin: 1rem 0;
            font-style: italic;
            color: #6b7280;
        }
        .chat-message .prose code {
            background-color: #f3f4f6;
            padding: 0.125rem 0.25rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
        }
        .chat-message .prose pre {
            background-color: #f9fafb;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 1rem 0;
        }
        .chat-message .prose ol {
            list-style-type: decimal;
        }
        .chat-message .prose ul {
            list-style-type: disc;
        }
    `;
    document.head.appendChild(style);
}

// Setup event listeners
function setupEventListeners() {
    // Character counter
    messageInput.addEventListener('input', function() {
        const length = this.value.length;
        const maxLength = 1000;
        charCounter.textContent = `${length}/${maxLength}`;
        
        if (length > maxLength * 0.8) {
            charCounter.classList.add('text-red-500');
        } else {
            charCounter.classList.remove('text-red-500');
        }
    });

    // Form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
        }
    });

    // Enter key to send (with Shift+Enter for new line)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
}

// Handle prefilled questions from localStorage
function handlePrefilledQuestion() {
    const prefilledQuestion = localStorage.getItem('prefilledQuestion');
    if (prefilledQuestion) {
        messageInput.value = prefilledQuestion;
        localStorage.removeItem('prefilledQuestion');
        messageInput.focus();
    }
}

// Send message function with LangGraph integration
async function sendMessage(message) {
    if (message.length > 1000) {
        alert('Pertanyaan terlalu panjang. Maksimal 1000 karakter.');
        return;
    }

    messageInput.value = '';
    charCounter.textContent = '0/1000';
    setLoading(true);

    addMessage(message, 'user');
    document.getElementById('suggested-questions').style.display = 'none';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message })
        });

        const data = await response.json();

        if (response.ok) {
            sessionId = data.session_id;
            document.getElementById('session-id').textContent = sessionId.substring(0, 8);
            
            addMessage(data.answer, 'ai', data.sources, data.confidence, data.needs_continuation, data.metadata);
            
            // Store run ID for feedback
            currentRunId = data.metadata?.run_id;
        } else {
            addMessage(data.error || 'Terjadi kesalahan dalam memproses pertanyaan.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Terjadi kesalahan koneksi. Silakan coba lagi.', 'error');
    } finally {
        setLoading(false);
    }
}

// Enhanced message display with improved markdown rendering
function addMessage(content, type, sources = null, confidence = null, needsContinuation = false, metadata = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message';

    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="flex items-start justify-end">
                <div class="bg-primary-600 text-white rounded-lg p-3 shadow max-w-md ml-auto">
                    <p class="whitespace-pre-wrap">${escapeHtml(content)}</p>
                </div>
                <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center ml-3 flex-shrink-0">
                    <i class="fas fa-user text-white text-xs"></i>
                </div>
            </div>
        `;
    } else if (type === 'ai') {
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = `
                <div class="mt-3 pt-3 border-t border-gray-200">
                    <p class="text-xs text-gray-500 mb-2">
                        <i class="fas fa-book mr-1"></i>Sumber informasi:
                    </p>
                    <div class="space-y-1">
                        ${sources.map(source => `
                            <div class="text-xs text-gray-600 bg-gray-50 rounded p-1">
                                <i class="fas fa-file-alt mr-1"></i>
                                ${escapeHtml(source.title || source.source)}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        let confidenceHtml = '';
        if (confidence !== null) {
            const confidencePercent = Math.round(confidence * 100);
            let confidenceColor = 'gray';
            if (confidencePercent >= 80) confidenceColor = 'green';
            else if (confidencePercent >= 60) confidenceColor = 'yellow';
            else confidenceColor = 'red';
            
            confidenceHtml = `
                <div class="mt-2 flex items-center justify-between">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-${confidenceColor}-100 text-${confidenceColor}-800">
                        <i class="fas fa-shield-alt mr-1"></i>
                        Tingkat keyakinan: ${confidencePercent}%
                    </span>
                    <button onclick="openFeedbackModal()" class="text-xs text-gray-500 hover:text-gray-700 ml-2">
                        <i class="fas fa-thumbs-up mr-1"></i>Berikan Feedback
                    </button>
                </div>
            `;
        }

        let continuationHtml = '';
        if (needsContinuation) {
            continuationHtml = `
                <div class="mt-2">
                    <button onclick="sendSuggestedQuestion('lanjutkan')" 
                            class="bg-primary-100 text-secondary-700 px-3 py-1 rounded-full text-xs hover:bg-primary-200 transition-colors">
                        <i class="fas fa-arrow-right mr-1"></i>Lanjutkan
                    </button>
                </div>
            `;
        }

        let metadataHtml = '';
        if (metadata && Object.keys(metadata).length > 0) {
            metadataHtml = `
                <div class="mt-2 text-xs text-gray-400">
                    <details>
                        <summary class="cursor-pointer hover:text-gray-600">Debug Info</summary>
                        <pre class="mt-1 text-xs bg-gray-100 p-2 rounded overflow-x-auto">${JSON.stringify(metadata, null, 2)}</pre>
                    </details>
                </div>
            `;
        }

        messageDiv.innerHTML = `
            <div class="flex items-start">
                <div class="w-8 h-8 bg-secondary-500 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                    <i class="fas fa-robot text-white text-xs"></i>
                </div>
                <div class="bg-white rounded-lg p-3 shadow max-w-3xl">
                    <div class="prose prose-sm max-w-none">
                        ${renderMarkdown(content)}
                    </div>
                    ${confidenceHtml}
                    ${continuationHtml}
                    ${sourcesHtml}
                    ${metadataHtml}
                </div>
            </div>
        `;
    } else if (type === 'error') {
        messageDiv.innerHTML = `
            <div class="flex items-start">
                <div class="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                    <i class="fas fa-exclamation-triangle text-white text-xs"></i>
                </div>
                <div class="bg-red-50 border border-red-200 text-red-800 rounded-lg p-3 max-w-md">
                    <p class="whitespace-pre-wrap">${escapeHtml(content)}</p>
                </div>
            </div>
        `;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Enhanced markdown rendering with fallback
function renderMarkdown(text) {
    try {
        // Pre-process text for better numbered list detection
        let processedText = text
            // Normalize line endings
            .replace(/\r\n/g, '\n')
            .replace(/\r/g, '\n')
            // Fix numbered lists - ensure proper spacing and formatting
            .replace(/^(\d+)\.\s+(.+)$/gm, '$1. $2')
            // Fix bullet points
            .replace(/^[•\-\*]\s+(.+)$/gm, '- $1')
            // Ensure proper paragraph breaks
            .replace(/\n{3,}/g, '\n\n')
            // Fix spacing around lists
            .replace(/(\n)(\d+\.\s)/g, '\n\n$2')
            .replace(/(\n)([•\-\*]\s)/g, '\n\n$2');

        // Use markdown-it to render
        if (window.markdownit && md) {
            const renderedHtml = md.render(processedText);
            return window.DOMPurify ? DOMPurify.sanitize(renderedHtml) : renderedHtml;
        } else {
            // Fallback manual formatting if markdown-it fails
            return formatTextManually(processedText);
        }
    } catch (error) {
        console.error('Markdown rendering error:', error);
        return formatTextManually(text);
    }
}

// Improved manual text formatting fallback
function formatTextManually(text) {
    // Split into lines for better processing
    const lines = text.split('\n');
    let result = [];
    let inOrderedList = false;
    let inUnorderedList = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (!line) {
            // Close any open lists on empty line
            if (inOrderedList) {
                result.push('</ol>');
                inOrderedList = false;
            }
            if (inUnorderedList) {
                result.push('</ul>');
                inUnorderedList = false;
            }
            result.push('<br>');
            continue;
        }

        // Check for numbered list
        const numberedMatch = line.match(/^(\d+)\.\s+(.+)$/);
        if (numberedMatch) {
            if (!inOrderedList) {
                // Close unordered list if open
                if (inUnorderedList) {
                    result.push('</ul>');
                    inUnorderedList = false;
                }
                result.push('<ol>');
                inOrderedList = true;
            }
            result.push(`<li>${escapeHtml(numberedMatch[2])}</li>`);
            continue;
        }

        // Check for bullet points
        const bulletMatch = line.match(/^[•\-\*]\s+(.+)$/);
        if (bulletMatch) {
            if (!inUnorderedList) {
                // Close ordered list if open
                if (inOrderedList) {
                    result.push('</ol>');
                    inOrderedList = false;
                }
                result.push('<ul>');
                inUnorderedList = true;
            }
            result.push(`<li>${escapeHtml(bulletMatch[1])}</li>`);
            continue;
        }

        // Regular text - close any open lists
        if (inOrderedList) {
            result.push('</ol>');
            inOrderedList = false;
        }
        if (inUnorderedList) {
            result.push('</ul>');
            inUnorderedList = false;
        }

        // Format regular text
        let formattedLine = escapeHtml(line)
            // Bold text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Italic text
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Headers
            .replace(/^### (.+)$/, '<h3>$1</h3>')
            .replace(/^## (.+)$/, '<h2>$1</h2>')
            .replace(/^# (.+)$/, '<h1>$1</h1>');

        // Check if it's a header, if not wrap in paragraph
        if (!formattedLine.match(/^<h[1-6]>/)) {
            formattedLine = `<p>${formattedLine}</p>`;
        }

        result.push(formattedLine);
    }

    // Close any remaining open lists
    if (inOrderedList) {
        result.push('</ol>');
    }
    if (inUnorderedList) {
        result.push('</ul>');
    }

    return result.join('\n');
}

// Load chat history from LangGraph
async function loadChatHistory() {
    try {
        const response = await fetch('/chat/history');
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            // Clear current messages except welcome
            const welcomeMsg = chatMessages.querySelector('.chat-message');
            chatMessages.innerHTML = '';
            if (welcomeMsg) {
                chatMessages.appendChild(welcomeMsg);
            }
            
            // Add history messages
            data.history.forEach(msg => {
                if (msg.type === 'human') {
                    addMessage(msg.content, 'user');
                } else if (msg.type === 'ai') {
                    addMessage(msg.content, 'ai');
                }
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Clear chat with LangGraph session management
async function clearChat() {
    if (confirm('Apakah Anda yakin ingin menghapus semua percakapan?')) {
        try {
            const response = await fetch('/chat/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                // Reset chat interface
                chatMessages.innerHTML = `
                    <div class="chat-message">
                        <div class="flex items-start">
                            <div class="w-8 h-8 bg-secondary-500 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                                <i class="fas fa-robot text-white text-xs"></i>
                            </div>
                            <div class="bg-white rounded-lg p-3 shadow max-w-md">
                                <p class="text-gray-800">
                                    Halo! 👋 Saya adalah AI Assistant untuk program Beasiswa LPDP 2025. 
                                    Saya menggunakan teknologi LangGraph untuk memberikan pengalaman yang lebih baik!
                                </p>
                                <p class="text-sm text-gray-500 mt-2">
                                    <i class="fas fa-info-circle mr-1"></i> Dengan state management dan continuity support
                                </p>
                            </div>
                        </div>
                    </div>
                `;
                document.getElementById('suggested-questions').style.display = 'block';
            }
        } catch (error) {
            console.error('Error clearing chat:', error);
            alert('Gagal membersihkan percakapan');
        }
    }
}

// Send suggested question
function sendSuggestedQuestion(question) {
    messageInput.value = question;
    sendMessage(question);
}

// Set loading state
function setLoading(isLoading) {
    if (isLoading) {
        sendText.classList.add('hidden');
        loadingText.classList.remove('hidden');
        sendButton.disabled = true;
        messageInput.disabled = true;
    } else {
        sendText.classList.remove('hidden');
        loadingText.classList.add('hidden');
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

// Feedback functionality
function openFeedbackModal() {
    document.getElementById('feedback-modal').classList.remove('hidden');
}

function closeFeedbackModal() {
    document.getElementById('feedback-modal').classList.add('hidden');
    currentRating = 0;
    document.getElementById('feedback-comment').value = '';
    // Reset rating buttons
    document.querySelectorAll('.rating-btn').forEach(btn => {
        btn.classList.remove('bg-secondary-500', 'text-white');
    });
}

function setRating(rating) {
    currentRating = rating;
    document.querySelectorAll('.rating-btn').forEach(btn => {
        btn.classList.remove('bg-secondary-500', 'text-white');
    });
    document.querySelector(`[data-rating="${rating}"]`).classList.add('bg-secondary-500', 'text-white');
}

async function submitFeedback() {
    if (currentRating === 0) {
        alert('Silakan pilih rating terlebih dahulu');
        return;
    }

    try {
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                run_id: currentRunId,
                rating: currentRating,
                comment: document.getElementById('feedback-comment').value
            })
        });

        if (response.ok) {
            alert('Terima kasih atas feedback Anda!');
            closeFeedbackModal();
        } else {
            alert('Gagal mengirim feedback');
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('Terjadi kesalahan saat mengirim feedback');
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeChat);

// Also initialize on window load as fallback
window.addEventListener('load', initializeChat);