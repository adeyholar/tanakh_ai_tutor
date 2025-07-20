// src/web/static/js/hebrew-helpers.js
// CORRECTED VERSION - Complete File
// Changes made: Fixed display functions to properly show Hebrew analysis results
// Original issue: JavaScript wasn't properly enumerating and displaying analysis data

/**
 * Hebrew AI Platform - Client-side Helper Functions
 * Enhanced with proper result display and enumeration
 */

// Global configuration
const CONFIG = {
    API_BASE_URL: '/api',
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,
    DEFAULT_TIMEOUT: 30000
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Hebrew AI Platform - Client initialized');
    initializeHebrewHelpers();
});

function initializeHebrewHelpers() {
    // Initialize all event listeners
    setupEventListeners();
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    console.log('✅ Hebrew helpers initialized');
}

function setupEventListeners() {
    // Word analysis form
    const wordForm = document.getElementById('wordAnalysisForm');
    if (wordForm) {
        wordForm.addEventListener('submit', handleWordAnalysis);
    }
    
    // Verse study form
    const verseForm = document.getElementById('verseStudyForm');
    if (verseForm) {
        verseForm.addEventListener('submit', handleVerseStudy);
    }
    
    // Quick action buttons
    document.querySelectorAll('.quick-verse').forEach(button => {
        button.addEventListener('click', handleQuickVerse);
    });
    
    document.querySelectorAll('.quick-word').forEach(button => {
        button.addEventListener('click', handleQuickWord);
    });
}

// =============================================================================
// WORD ANALYSIS FUNCTIONS
// =============================================================================

async function handleWordAnalysis(event) {
    event.preventDefault();
    
    const wordInput = document.getElementById('hebrewWordInput');
    if (!wordInput) return;
    
    const word = wordInput.value.trim();
    if (!word) {
        showError('Please enter a Hebrew word');
        return;
    }
    
    await analyzeWord(word);
}

async function handleQuickWord(event) {
    const word = event.target.dataset.word;
    if (word) {
        document.getElementById('hebrewWordInput').value = word;
        await analyzeWord(word);
    }
}

async function analyzeWord(word) {
    try {
        showWordLoading();
        hideWordResults();
        hideWordError();
        
        console.log(`🔍 Analyzing Hebrew word: ${word}`);
        
        const response = await fetchWithRetry(`${CONFIG.API_BASE_URL}/analyze-word`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ word: word })
        });
        
        const data = await response.json();
        console.log('📊 Word analysis response:', data);
        
        hideWordLoading();
        
        if (data.success !== false) {
            displayWordResults(data);
        } else {
            showWordError(data.error || 'Failed to analyze word');
        }
        
    } catch (error) {
        console.error('❌ Word analysis error:', error);
        hideWordLoading();
        showWordError('Network error: ' + error.message);
    }
}

function displayWordResults(data) {
    console.log('📊 Displaying word results:', data);
    
    const resultsDiv = document.getElementById('wordResults');
    if (!resultsDiv) return;
    
    // Show results container
    resultsDiv.style.display = 'block';
    
    // Create results HTML
    const resultsHTML = `
        <div class="alert alert-success">
            <h5>📝 Word Analysis Complete!</h5>
            
            <div class="word-analysis-card">
                <div class="row">
                    <div class="col-md-4 text-center">
                        <div class="hebrew-word-display">
                            <h2 class="hebrew-text">${data.word}</h2>
                            <span class="badge bg-${getConfidenceColor(data.confidence)} fs-6">
                                ${(data.confidence * 100).toFixed(1)}% Confidence
                            </span>
                        </div>
                    </div>
                    
                    <div class="col-md-8">
                        <h6>📚 Translation & Meaning:</h6>
                        <p class="mb-3"><strong>${data.translation}</strong></p>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <h6>🔤 Grammar Details:</h6>
                                <ul class="list-unstyled">
                                    ${data.grammar_info.hebrew_root ? 
                                      `<li><strong>Root:</strong> ${data.grammar_info.hebrew_root}</li>` : ''}
                                    ${data.grammar_info.morphological_analysis ? 
                                      `<li><strong>Structure:</strong> ${data.grammar_info.morphological_analysis}</li>` : ''}
                                    ${data.grammar_info.word_type ? 
                                      `<li><strong>Type:</strong> ${data.grammar_info.word_type}</li>` : ''}
                                    ${data.grammar_info.biblical_context ? 
                                      `<li><strong>Context:</strong> ${data.grammar_info.biblical_context}</li>` : ''}
                                </ul>
                            </div>
                            
                            <div class="col-md-6">
                                <h6>🤖 AI Analysis:</h6>
                                <ul class="list-unstyled">
                                    <li><strong>Model:</strong> ${data.model_used}</li>
                                    <li><strong>Device:</strong> ${data.grammar_info.device_used || 'CPU'}</li>
                                    <li><strong>Processing:</strong> ${data.grammar_info.processing_time || 'N/A'}</li>
                                </ul>
                                
                                <small class="text-muted">
                                    Analyzed: ${new Date(data.timestamp).toLocaleString()}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = resultsHTML;
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// =============================================================================
// VERSE STUDY FUNCTIONS
// =============================================================================

async function handleVerseStudy(event) {
    event.preventDefault();
    
    const book = document.getElementById('bookSelect')?.value;
    const chapter = parseInt(document.getElementById('chapterInput')?.value);
    const verse = parseInt(document.getElementById('verseInput')?.value);
    
    if (!book || !chapter || !verse) {
        showError('Please fill in all fields');
        return;
    }
    
    await studyVerse(book, chapter, verse);
}

async function handleQuickVerse(event) {
    const book = event.target.dataset.book;
    const chapter = parseInt(event.target.dataset.chapter);
    const verse = parseInt(event.target.dataset.verse);
    
    // Fill form fields if they exist
    const bookSelect = document.getElementById('bookSelect');
    const chapterInput = document.getElementById('chapterInput');
    const verseInput = document.getElementById('verseInput');
    
    if (bookSelect) bookSelect.value = book;
    if (chapterInput) chapterInput.value = chapter;
    if (verseInput) verseInput.value = verse;
    
    await studyVerse(book, chapter, verse);
}

async function studyVerse(book, chapter, verse) {
    try {
        showVerseLoading();
        hideVerseResults();
        hideVerseError();
        
        console.log(`🔍 Studying ${book} ${chapter}:${verse}`);
        
        const response = await fetchWithRetry(`${CONFIG.API_BASE_URL}/study/${book}/${chapter}/${verse}`);
        const data = await response.json();
        
        console.log('📊 Verse study response:', data);
        
        hideVerseLoading();
        
        if (data.success) {
            displayVerseResults(data);
        } else {
            showVerseError(data.error || 'Failed to analyze verse');
        }
        
    } catch (error) {
        console.error('❌ Verse study error:', error);
        hideVerseLoading();
        showVerseError('Network error: ' + error.message);
    }
}

function displayVerseResults(data) {
    console.log('📊 Displaying verse results:', data);
    
    if (!data.success) {
        showVerseError('Failed to analyze verse: ' + (data.error || 'Unknown error'));
        return;
    }
    
    const resultsDiv = document.getElementById('verseResults');
    if (!resultsDiv) return;
    
    // Show the results container
    resultsDiv.style.display = 'block';
    
    // Display Hebrew text header
    const verseTextDiv = document.getElementById('verseText');
    if (verseTextDiv) {
        verseTextDiv.innerHTML = `
            <h4>${data.book} ${data.chapter}:${data.verse}</h4>
            <p class="fs-3">${data.hebrew_text}</p>
        `;
    }
    
    // Clear and populate word analysis accordion
    const accordion = document.getElementById('wordAnalysisAccordion');
    if (accordion) {
        accordion.innerHTML = '';
        
        // Create accordion item for each word analysis
        data.analysis_results.forEach((analysis, index) => {
            const accordionItem = createWordAccordionItem(analysis, index);
            accordion.appendChild(accordionItem);
        });
    }
    
    // Update statistics
    updateVerseStatistics(data);
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function createWordAccordionItem(analysis, index) {
    const item = document.createElement('div');
    item.className = 'accordion-item';
    
    const confidenceColor = getConfidenceColor(analysis.confidence);
    
    item.innerHTML = `
        <h2 class="accordion-header" id="heading${index}">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                    data-bs-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">
                <span class="hebrew-text fs-4 me-3">${analysis.word}</span>
                <span class="badge bg-${confidenceColor} me-2">${(analysis.confidence * 100).toFixed(0)}%</span>
                <span class="text-muted">${analysis.translation}</span>
            </button>
        </h2>
        <div id="collapse${index}" class="accordion-collapse collapse" 
             aria-labelledby="heading${index}" data-bs-parent="#wordAnalysisAccordion">
            <div class="accordion-body">
                <div class="row">
                    <div class="col-md-6">
                        <h6>📚 Translation & Meaning:</h6>
                        <p class="mb-2"><strong>${analysis.translation}</strong></p>
                        
                        <h6>🔤 Grammar Analysis:</h6>
                        <ul class="list-unstyled">
                            ${analysis.grammar_info.hebrew_root ? 
                              `<li><strong>Root:</strong> ${analysis.grammar_info.hebrew_root}</li>` : ''}
                            ${analysis.grammar_info.morphological_analysis ? 
                              `<li><strong>Structure:</strong> ${analysis.grammar_info.morphological_analysis}</li>` : ''}
                            ${analysis.grammar_info.word_type ? 
                              `<li><strong>Type:</strong> ${analysis.grammar_info.word_type}</li>` : ''}
                            ${analysis.grammar_info.biblical_context ? 
                              `<li><strong>Context:</strong> ${analysis.grammar_info.biblical_context}</li>` : ''}
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h6>🤖 AI Analysis Details:</h6>
                        <ul class="list-unstyled">
                            <li><strong>Model:</strong> ${analysis.model_used}</li>
                            <li><strong>Confidence:</strong> 
                                <span class="badge bg-${confidenceColor}">${(analysis.confidence * 100).toFixed(1)}%</span>
                            </li>
                            <li><strong>Device:</strong> ${analysis.grammar_info.device_used || 'CPU'}</li>
                            <li><strong>Processing:</strong> ${analysis.grammar_info.processing_time || 'N/A'}</li>
                        </ul>
                        
                        <div class="mt-2">
                            <small class="text-muted">
                                Analyzed: ${new Date(analysis.timestamp).toLocaleString()}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    return item;
}

function updateVerseStatistics(data) {
    const wordsCountEl = document.getElementById('wordsCount');
    const studyTimeEl = document.getElementById('studyTime');
    const avgConfidenceEl = document.getElementById('avgConfidence');
    
    if (wordsCountEl) wordsCountEl.textContent = data.words_analyzed;
    if (studyTimeEl) studyTimeEl.textContent = new Date(data.timestamp).toLocaleTimeString();
    
    if (avgConfidenceEl && data.analysis_results && data.analysis_results.length > 0) {
        const avgConf = data.analysis_results.reduce((sum, a) => sum + a.confidence, 0) / data.analysis_results.length;
        avgConfidenceEl.textContent = (avgConf * 100).toFixed(1) + '%';
    }
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

function getConfidenceColor(confidence) {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'danger';
}

async function fetchWithRetry(url, options = {}, retries = CONFIG.MAX_RETRIES) {
    for (let i = 0; i < retries; i++) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), CONFIG.DEFAULT_TIMEOUT);
            
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return response;
            
        } catch (error) {
            console.warn(`Attempt ${i + 1} failed:`, error.message);
            
            if (i === retries - 1) throw error;
            
            // Wait before retrying
            await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY * (i + 1)));
        }
    }
}

// =============================================================================
// UI HELPER FUNCTIONS
// =============================================================================

// Word Analysis UI
function showWordLoading() {
    const loadingEl = document.getElementById('wordLoadingIndicator');
    if (loadingEl) loadingEl.style.display = 'block';
}

function hideWordLoading() {
    const loadingEl = document.getElementById('wordLoadingIndicator');
    if (loadingEl) loadingEl.style.display = 'none';
}

function showWordResults() {
    const resultsEl = document.getElementById('wordResults');
    if (resultsEl) resultsEl.style.display = 'block';
}

function hideWordResults() {
    const resultsEl = document.getElementById('wordResults');
    if (resultsEl) resultsEl.style.display = 'none';
}

function showWordError(message) {
    const errorEl = document.getElementById('wordErrorDisplay');
    const messageEl = document.getElementById('wordErrorMessage');
    if (errorEl && messageEl) {
        messageEl.textContent = message;
        errorEl.style.display = 'block';
    }
}

function hideWordError() {
    const errorEl = document.getElementById('wordErrorDisplay');
    if (errorEl) errorEl.style.display = 'none';
}

// Verse Study UI
function showVerseLoading() {
    const loadingEl = document.getElementById('loadingIndicator');
    if (loadingEl) loadingEl.style.display = 'block';
}

function hideVerseLoading() {
    const loadingEl = document.getElementById('loadingIndicator');
    if (loadingEl) loadingEl.style.display = 'none';
}

function showVerseResults() {
    const resultsEl = document.getElementById('verseResults');
    if (resultsEl) resultsEl.style.display = 'block';
}

function hideVerseResults() {
    const resultsEl = document.getElementById('verseResults');
    if (resultsEl) resultsEl.style.display = 'none';
}

function showVerseError(message) {
    const errorEl = document.getElementById('errorDisplay');
    const messageEl = document.getElementById('errorMessage');
    if (errorEl && messageEl) {
        messageEl.textContent = message;
        errorEl.style.display = 'block';
    }
}

function hideVerseError() {
    const errorEl = document.getElementById('errorDisplay');
    if (errorEl) errorEl.style.display = 'none';
}

// General UI
function showError(message) {
    // Try multiple error display elements
    showWordError(message);
    showVerseError(message);
    console.error('❌ Error:', message);
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('📋 Copied to clipboard:', text);
            // Could add toast notification here
        }).catch(err => {
            console.error('Failed to copy text:', err);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            console.log('📋 Copied to clipboard (fallback):', text);
        } catch (err) {
            console.error('Failed to copy text (fallback):', err);
        }
        document.body.removeChild(textArea);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to submit active form
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const activeForm = document.querySelector('form:focus-within') || 
                          document.getElementById('verseStudyForm') || 
                          document.getElementById('wordAnalysisForm');
        if (activeForm) {
            activeForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to close modals or clear results
    if (event.key === 'Escape') {
        hideWordResults();
        hideVerseResults();
        hideWordError();
        hideVerseError();
    }
});

// Export functions for global access
window.HebrewAI = {
    analyzeWord,
    studyVerse,
    copyToClipboard,
    getConfidenceColor,
    displayWordResults,
    displayVerseResults
};

console.log('✅ Hebrew AI helpers loaded successfully');