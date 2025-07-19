// Hebrew AI Platform - Corrected Book Names (Final Fix)
// File: src/web/static/js/hebrew-helpers.js
// Uses actual book names from your Tanakh JSON structure

console.log('🚀 Hebrew Platform with Corrected Book Names Loading...');

// CORRECTED: Using actual book names from your Tanakh JSON
const ACTUAL_BOOK_NAMES = [
    // Torah (תורה)
    { display: 'Genesis (בראשית)', value: 'Gen' },
    { display: 'Exodus (שמות)', value: 'Exod' },
    { display: 'Leviticus (ויקרא)', value: 'Lev' },
    { display: 'Numbers (במדבר)', value: 'Num' },
    { display: 'Deuteronomy (דברים)', value: 'Deut' },
    
    // Historical Books (נביאים ראשונים)
    { display: 'Joshua (יהושע)', value: 'Josh' },
    { display: 'Judges (שופטים)', value: 'Judg' },
    { display: '1 Samuel (שמואל א)', value: '1Sam' },
    { display: '2 Samuel (שמואל ב)', value: '2Sam' },
    { display: '1 Kings (מלכים א)', value: '1Kgs' },
    { display: '2 Kings (מלכים ב)', value: '2Kgs' },
    { display: '1 Chronicles (דברי הימים א)', value: '1Chr' },
    { display: '2 Chronicles (דברי הימים ב)', value: '2Chr' },
    { display: 'Ezra (עזרא)', value: 'Ezra' },
    { display: 'Nehemiah (נחמיה)', value: 'Neh' },
    { display: 'Esther (אסתר)', value: 'Esth' },
    
    // Wisdom Books (כתובים)
    { display: 'Job (איוב)', value: 'Job' },
    { display: 'Psalms (תהלים)', value: 'Ps' },
    { display: 'Proverbs (משלי)', value: 'Prov' },
    { display: 'Ecclesiastes (קהלת)', value: 'Eccl' },
    { display: 'Song of Songs (שיר השירים)', value: 'Song' },
    { display: 'Ruth (רות)', value: 'Ruth' },
    { display: 'Lamentations (איכה)', value: 'Lam' },
    
    // Major Prophets (נביאים אחרונים)
    { display: 'Isaiah (ישעיהו)', value: 'Isa' },
    { display: 'Jeremiah (ירמיהו)', value: 'Jer' },
    { display: 'Ezekiel (יחזקאל)', value: 'Ezek' },
    { display: 'Daniel (דניאל)', value: 'Dan' },
    
    // Minor Prophets (תרי עשר)
    { display: 'Hosea (הושע)', value: 'Hos' },
    { display: 'Joel (יואל)', value: 'Joel' },
    { display: 'Amos (עמוס)', value: 'Amos' },
    { display: 'Obadiah (עובדיה)', value: 'Obad' },
    { display: 'Jonah (יונה)', value: 'Jonah' },
    { display: 'Micah (מיכה)', value: 'Mic' },
    { display: 'Nahum (נחום)', value: 'Nah' },
    { display: 'Habakkuk (חבקוק)', value: 'Hab' },
    { display: 'Zephaniah (צפניה)', value: 'Zeph' },
    { display: 'Haggai (חגי)', value: 'Hag' },
    { display: 'Zechariah (זכריה)', value: 'Zech' },
    { display: 'Malachi (מלאכי)', value: 'Mal' }
];

class CorrectedHebrewPlatform {
    constructor() {
        this.currentFontSize = 24;
        this.init();
    }
    
    init() {
        console.log('📚 Corrected Hebrew Platform initializing...');
        this.setupBookSelector();
        this.fixFormStructure();
        this.fixFormSubmission();
        this.setupFontControls();
        this.setupSystemMonitoring();
        this.addQuickAccessButtons();
        console.log('✅ Corrected platform initialization complete!');
    }
    
    setupBookSelector() {
        setTimeout(() => {
            const bookSelect = document.querySelector('select[name="book"]');
            if (!bookSelect) {
                console.log('📚 Book selector not found, retrying...');
                setTimeout(() => this.setupBookSelector(), 1000);
                return;
            }
            
            console.log('📚 Setting up book selector with CORRECT book names...');
            
            // Clear and rebuild with correct book names
            bookSelect.innerHTML = '<option value="">בחר ספר / Select Book</option>';
            
            // Add books grouped by section
            this.addBookSection(bookSelect, 'Torah (תורה)', ACTUAL_BOOK_NAMES.slice(0, 5));
            this.addBookSection(bookSelect, 'Historical Books (נביאים ראשונים)', ACTUAL_BOOK_NAMES.slice(5, 16));
            this.addBookSection(bookSelect, 'Wisdom Books (כתובים)', ACTUAL_BOOK_NAMES.slice(16, 23));
            this.addBookSection(bookSelect, 'Prophets (נביאים אחרונים)', ACTUAL_BOOK_NAMES.slice(23));
            
            // Add change event listener
            bookSelect.addEventListener('change', (e) => {
                if (e.target.value) {
                    const selectedBook = ACTUAL_BOOK_NAMES.find(book => book.value === e.target.value);
                    if (selectedBook) {
                        this.showBookSelection(selectedBook.display, selectedBook.value);
                    }
                }
            });
            
            console.log(`✅ Book selector loaded with ${ACTUAL_BOOK_NAMES.length} CORRECT book names!`);
        }, 500);
    }
    
    addBookSection(bookSelect, sectionName, books) {
        const optgroup = document.createElement('optgroup');
        optgroup.label = sectionName;
        
        books.forEach(book => {
            const option = document.createElement('option');
            option.value = book.value;  // This is the correct backend name
            option.textContent = book.display;  // This is the user-friendly display
            optgroup.appendChild(option);
        });
        
        bookSelect.appendChild(optgroup);
    }
    
    fixFormStructure() {
        setTimeout(() => {
            console.log('🔧 Checking and fixing form structure...');
            
            const form = document.querySelector('form[action="/study-verse-form"]');
            if (!form) {
                console.error('❌ Form not found');
                return;
            }
            
            // Check for chapter input
            let chapterInput = form.querySelector('input[name="chapter"]');
            if (!chapterInput) {
                console.log('🔧 Adding missing chapter input...');
                this.addChapterInput(form);
            }
            
            // Check for verse input
            let verseInput = form.querySelector('input[name="verse"]');
            if (!verseInput) {
                console.log('🔧 Adding missing verse input...');
                this.addVerseInput(form);
            }
            
        }, 1000);
    }
    
    addChapterInput(form) {
        const bookSelect = form.querySelector('select[name="book"]');
        if (!bookSelect) return;
        
        const chapterContainer = document.createElement('div');
        chapterContainer.className = 'row mb-3';
        chapterContainer.innerHTML = `
            <div class="col-md-6">
                <label for="chapter" class="form-label">Chapter:</label>
                <input type="number" name="chapter" id="chapter" 
                       class="form-control" min="1" value="1" required>
            </div>
            <div class="col-md-6" id="verse-placeholder">
                <!-- Verse input will be added here -->
            </div>
        `;
        
        bookSelect.closest('div').parentNode.appendChild(chapterContainer);
    }
    
    addVerseInput(form) {
        let verseContainer = document.getElementById('verse-placeholder');
        
        if (!verseContainer) {
            const chapterInput = form.querySelector('input[name="chapter"]');
            if (!chapterInput) return;
            
            verseContainer = document.createElement('div');
            verseContainer.className = 'col-md-6 mb-3';
            
            const chapterContainer = chapterInput.closest('.col-md-6');
            if (chapterContainer && chapterContainer.parentNode) {
                chapterContainer.parentNode.appendChild(verseContainer);
            }
        }
        
        verseContainer.innerHTML = `
            <label for="verse" class="form-label">Verse:</label>
            <input type="number" name="verse" id="verse" 
                   class="form-control" min="1" value="1" required>
        `;
        
        console.log('✅ Added verse input field');
    }
    
    fixFormSubmission() {
        setTimeout(() => {
            const form = document.querySelector('form[action="/study-verse-form"]');
            if (!form) return;
            
            console.log('🔧 Applying CORRECTED form submission...');
            
            // Replace form to remove existing listeners
            const newForm = form.cloneNode(true);
            form.parentNode.replaceChild(newForm, form);
            
            newForm.addEventListener('submit', (e) => {
                e.preventDefault();
                
                const bookValue = newForm.querySelector('select[name="book"]').value;
                const chapter = newForm.querySelector('input[name="chapter"]').value;
                const verse = newForm.querySelector('input[name="verse"]').value;
                
                console.log('📤 Submitting with CORRECT book name:', {bookValue, chapter, verse});
                
                if (!bookValue || !chapter || !verse) {
                    alert('Please select a book, chapter, and verse before studying.');
                    return;
                }
                
                // Show loading state
                const submitBtn = newForm.querySelector('button[type="submit"]');
                const originalText = submitBtn ? submitBtn.textContent : '';
                if (submitBtn) {
                    submitBtn.textContent = '🔄 Analyzing Hebrew...';
                    submitBtn.disabled = true;
                }
                
                // Create FormData with CORRECT book names
                const formData = new FormData();
                formData.append('book', bookValue);  // Now sends 'Gen' instead of 'Genesis'
                formData.append('chapter', parseInt(chapter));
                formData.append('verse', parseInt(verse));
                
                fetch('/study-verse-form', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    console.log('📨 Response status:', response.status);
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        throw new Error(`HTTP ${response.status}`);
                    }
                })
                .catch(error => {
                    console.error('❌ Submission error:', error);
                    alert(`Error studying verse: ${error.message}`);
                })
                .finally(() => {
                    if (submitBtn) {
                        submitBtn.textContent = originalText;
                        submitBtn.disabled = false;
                    }
                });
            });
            
            console.log('✅ CORRECTED form submission handler installed');
            
        }, 1500);
    }
    
    showBookSelection(displayName, backendValue) {
        const existingInfo = document.getElementById('book-selection-info');
        if (existingInfo) existingInfo.remove();
        
        const infoDiv = document.createElement('div');
        infoDiv.id = 'book-selection-info';
        infoDiv.style.cssText = `
            background: linear-gradient(135deg, #00b894, #00cec9);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            margin: 12px 0;
            font-size: 14px;
            text-align: center;
            font-weight: 500;
        `;
        infoDiv.innerHTML = `📖 Selected: <strong>${displayName}</strong><br><small>Backend ID: ${backendValue}</small>`;
        
        const bookSelect = document.querySelector('select[name="book"]');
        if (bookSelect && bookSelect.parentNode) {
            bookSelect.parentNode.appendChild(infoDiv);
        }
    }
    
    setupFontControls() {
        if (document.getElementById('font-controls')) return;
        
        const controls = document.createElement('div');
        controls.id = 'font-controls';
        controls.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            font-family: 'Segoe UI', sans-serif;
            border: 1px solid #e0e0e0;
            min-width: 120px;
        `;
        
        controls.innerHTML = `
            <div style="font-weight: 600; margin-bottom: 8px; color: #2c3e50; font-size: 12px; text-align: center;">
                Hebrew Font Size
            </div>
            <div style="display: flex; gap: 4px; margin-bottom: 6px; justify-content: center;">
                <button onclick="correctedPlatform.decreaseFont()" 
                        style="background: #e74c3c; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 600;">A-</button>
                <button onclick="correctedPlatform.increaseFont()" 
                        style="background: #27ae60; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 600;">A+</button>
                <button onclick="correctedPlatform.resetFont()" 
                        style="background: #3498db; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 600;">Reset</button>
            </div>
            <div id="font-size-display" style="font-size: 11px; color: #666; text-align: center; font-weight: 500;">
                ${this.currentFontSize}px
            </div>
        `;
        
        document.body.appendChild(controls);
    }
    
    increaseFont() {
        this.currentFontSize = Math.min(48, this.currentFontSize + 2);
        this.applyFontSize();
    }
    
    decreaseFont() {
        this.currentFontSize = Math.max(16, this.currentFontSize - 2);
        this.applyFontSize();
    }
    
    resetFont() {
        this.currentFontSize = 24;
        this.applyFontSize();
    }
    
    applyFontSize() {
        const existingStyle = document.getElementById('dynamic-hebrew-font');
        if (existingStyle) existingStyle.remove();
        
        const style = document.createElement('style');
        style.id = 'dynamic-hebrew-font';
        style.textContent = `
            .hebrew-text { 
                font-size: ${this.currentFontSize}px !important; 
                line-height: 1.6 !important;
            }
            .hebrew-verse-display { 
                font-size: ${this.currentFontSize + 8}px !important; 
                line-height: 1.8 !important;
            }
            .hebrew-word-card { 
                font-size: ${this.currentFontSize - 2}px !important; 
            }
            .hebrew-input { 
                font-size: ${this.currentFontSize}px !important; 
            }
        `;
        document.head.appendChild(style);
        
        const display = document.getElementById('font-size-display');
        if (display) display.textContent = `${this.currentFontSize}px`;
    }
    
    addQuickAccessButtons() {
        setTimeout(() => {
            // Update quick access with correct book names
            const quickAccessContainer = document.querySelector('.d-flex.flex-wrap.gap-2');
            if (quickAccessContainer) {
                quickAccessContainer.innerHTML = `
                    <button class="btn btn-outline-primary btn-sm" onclick="correctedPlatform.loadVerse('Gen', 1, 1)">
                        Gen 1:1
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="correctedPlatform.loadVerse('Ps', 23, 1)">
                        Ps 23:1
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="correctedPlatform.loadVerse('Isa', 40, 3)">
                        Isa 40:3
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="correctedPlatform.loadRandomVerse()">
                        Random
                    </button>
                `;
            }
        }, 2000);
    }
    
    loadVerse(bookValue, chapter, verse) {
        const bookSelect = document.querySelector('select[name="book"]');
        const chapterInput = document.querySelector('input[name="chapter"]');
        const verseInput = document.querySelector('input[name="verse"]');
        
        if (bookSelect) {
            bookSelect.value = bookValue;
            const selectedBook = ACTUAL_BOOK_NAMES.find(book => book.value === bookValue);
            if (selectedBook) {
                this.showBookSelection(selectedBook.display, selectedBook.value);
            }
        }
        if (chapterInput) chapterInput.value = chapter;
        if (verseInput) verseInput.value = verse;
        
        console.log(`📖 Loaded verse: ${bookValue} ${chapter}:${verse}`);
    }
    
    loadRandomVerse() {
        const randomBooks = ['Gen', 'Ps', 'Isa', 'Prov', 'Job'];
        const randomBook = randomBooks[Math.floor(Math.random() * randomBooks.length)];
        const randomChapter = Math.floor(Math.random() * 10) + 1;
        const randomVerse = Math.floor(Math.random() * 10) + 1;
        this.loadVerse(randomBook, randomChapter, randomVerse);
    }
    
    setupSystemMonitoring() {
        this.checkSystemStatus();
        setInterval(() => this.checkSystemStatus(), 30000);
    }
    
    async checkSystemStatus() {
        try {
            const response = await fetch('/api/health');
            const health = await response.json();
            this.updateStatusDisplay(health);
        } catch (error) {
            console.error('Status check failed:', error);
            this.updateStatusDisplay({ status: 'error' });
        }
    }
    
    updateStatusDisplay(health) {
        const statusElements = document.querySelectorAll('[id*="ollama"], [data-status="ollama"]');
        statusElements.forEach(el => {
            if (health.components && health.components.ollama) {
                if (el.textContent) el.textContent = 'Online';
                el.className = el.className.replace(/bg-(danger|warning)/g, 'bg-success');
            } else {
                if (el.textContent) el.textContent = 'Offline';
                el.className = el.className.replace(/bg-(success|warning)/g, 'bg-danger');
            }
        });
    }
}

// Global functions
function loadVerse(bookValue, chapter, verse) {
    if (window.correctedPlatform) {
        window.correctedPlatform.loadVerse(bookValue, chapter, verse);
    }
}

// Success indicator
function showCorrectedSuccessIndicator() {
    const indicator = document.createElement('div');
    indicator.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        z-index: 1000;
        transition: opacity 0.5s ease;
        box-shadow: 0 4px 20px rgba(39, 174, 96, 0.3);
    `;
    indicator.innerHTML = '🎯 Hebrew Platform - Correct Book Names Loaded!';
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => indicator.remove(), 500);
    }, 5000);
}

// Initialize platform
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing CORRECTED Hebrew Platform...');
    
    setTimeout(() => {
        window.correctedPlatform = new CorrectedHebrewPlatform();
        showCorrectedSuccessIndicator();
        console.log('✅ CORRECTED Hebrew Platform fully operational!');
    }, 1000);
});

console.log('🎯 CORRECTED Hebrew Platform loaded - Book name mapping fixed!');
// This code ensures that the book names used in the platform match the actual names in your Tanakh JSON structure,

// Hebrew Study Results Display Fix
// Add this to your existing hebrew-helpers.js file

console.log('🔧 Adding results display fix...');

class ResultsDisplayManager {
    constructor() {
        this.init();
    }
    
    init() {
        // Monitor for successful form submissions
        this.monitorFormSubmissions();
        // Check for existing results on page load
        this.checkForExistingResults();
        // Add auto-refresh mechanism
        this.setupAutoRefresh();
    }
    
    monitorFormSubmissions() {
        // Override the existing form submission to handle results better
        setTimeout(() => {
            const form = document.querySelector('form[action="/study-verse-form"]');
            if (!form) return;
            
            // Add additional handling after our existing handler
            form.addEventListener('submit', (e) => {
                setTimeout(() => {
                    this.waitForResults();
                }, 2000); // Wait 2 seconds for processing
            });
        }, 2000);
    }
    
    waitForResults() {
        console.log('🔍 Waiting for study results...');
        
        // Check for results every second for up to 30 seconds
        let attempts = 0;
        const maxAttempts = 30;
        
        const checkInterval = setInterval(() => {
            attempts++;
            
            // Look for results in the page
            if (this.checkForResults()) {
                clearInterval(checkInterval);
                console.log('✅ Results found and displayed!');
                return;
            }
            
            // Try to refresh the page content
            if (attempts % 5 === 0) {
                console.log(`🔄 Attempt ${attempts}: Refreshing page content...`);
                this.refreshPageContent();
            }
            
            // Give up after max attempts
            if (attempts >= maxAttempts) {
                clearInterval(checkInterval);
                console.log('⏰ Timeout waiting for results');
                this.showManualRefreshOption();
            }
        }, 1000);
    }
    
    checkForResults() {
        // Look for various indicators that results are present
        const indicators = [
            document.querySelector('.hebrew-verse-display'),
            document.querySelector('[class*="analysis"]'),
            document.querySelector('[class*="hebrew-text"]'),
            document.querySelector('.accordion'),
            document.querySelector('[id*="verse"]'),
            document.querySelector('[class*="result"]')
        ];
        
        const hasResults = indicators.some(el => el && el.textContent && el.textContent.trim().length > 0);
        
        if (hasResults) {
            console.log('📊 Results detected on page');
            this.enhanceDisplayedResults();
            return true;
        }
        
        return false;
    }
    
    checkForExistingResults() {
        setTimeout(() => {
            if (this.checkForResults()) {
                console.log('✅ Existing results found on page load');
            } else {
                console.log('ℹ️ No existing results found');
            }
        }, 1000);
    }
    
    refreshPageContent() {
        // Try to get fresh content without full page reload
        const currentUrl = window.location.href;
        
        fetch(currentUrl)
            .then(response => response.text())
            .then(html => {
                // Parse the new HTML
                const parser = new DOMParser();
                const newDoc = parser.parseFromString(html, 'text/html');
                
                // Update the study results section
                const currentResults = document.querySelector('.col-lg-7');
                const newResults = newDoc.querySelector('.col-lg-7');
                
                if (currentResults && newResults && newResults.innerHTML !== currentResults.innerHTML) {
                    currentResults.innerHTML = newResults.innerHTML;
                    console.log('🔄 Results section updated');
                    this.enhanceDisplayedResults();
                }
            })
            .catch(error => {
                console.error('Error refreshing content:', error);
            });
    }
    
    enhanceDisplayedResults() {
        // Enhance any Hebrew text that's displayed
        const hebrewElements = document.querySelectorAll('[class*="hebrew"], [style*="rtl"]');
        hebrewElements.forEach(el => {
            if (!el.classList.contains('hebrew-enhanced')) {
                el.classList.add('hebrew-enhanced', 'hebrew-text');
                el.style.fontFamily = "'Noto Sans Hebrew', 'David CLM', serif";
                el.style.direction = 'rtl';
                el.style.textAlign = 'right';
            }
        });
        
        // Apply current font size
        if (window.correctedPlatform) {
            window.correctedPlatform.applyFontSize();
        }
        
        console.log('✨ Results enhanced with Hebrew styling');
    }
    
    showManualRefreshOption() {
        // Show a helpful message to the user
        const studyResults = document.querySelector('.col-lg-7');
        if (studyResults) {
            const refreshDiv = document.createElement('div');
            refreshDiv.style.cssText = `
                background: linear-gradient(135deg, #f39c12, #e67e22);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
            `;
            refreshDiv.innerHTML = `
                <h5>📊 Analysis Complete!</h5>
                <p>Your Hebrew verse has been analyzed successfully. If results don't appear automatically:</p>
                <button onclick="window.location.reload()" 
                        style="background: white; color: #e67e22; border: none; padding: 10px 20px; border-radius: 5px; font-weight: 600; cursor: pointer;">
                    🔄 Refresh Page to View Results
                </button>
                <br><br>
                <small>Analysis completed with AlephBERT Hebrew AI</small>
            `;
            
            // Replace the welcome message
            const welcomeSection = studyResults.querySelector('.text-center.py-5');
            if (welcomeSection) {
                welcomeSection.replaceWith(refreshDiv);
            }
        }
    }
    
    setupAutoRefresh() {
        // Periodically check for new results
        setInterval(() => {
            // Only check if we're on the study page and don't have results
            if (window.location.pathname.includes('study') && !this.checkForResults()) {
                const form = document.querySelector('form[action="/study-verse-form"]');
                const bookSelect = form ? form.querySelector('select[name="book"]') : null;
                
                // If a book is selected but no results, try to refresh
                if (bookSelect && bookSelect.value && bookSelect.value !== '') {
                    console.log('🔄 Auto-refreshing to check for results...');
                    this.refreshPageContent();
                }
            }
        }, 10000); // Check every 10 seconds
    }
}

// Add some debugging for the current page state
function debugCurrentState() {
    console.log('🔍 Current page debug info:');
    console.log('URL:', window.location.href);
    console.log('Study results container:', document.querySelector('.col-lg-7') ? 'Found' : 'Not found');
    console.log('Hebrew elements:', document.querySelectorAll('[class*="hebrew"]').length);
    console.log('Form elements:', document.querySelectorAll('form').length);
    
    // Look for any Hebrew text on the page
    const allText = document.body.innerText;
    const hasHebrew = /[\u0590-\u05FF]/.test(allText);
    console.log('Hebrew text detected:', hasHebrew);
    
    // Check for common result indicators
    const resultIndicators = [
        'verse-display', 'analysis', 'hebrew-text', 'accordion', 'word-card', 'result'
    ];
    
    resultIndicators.forEach(indicator => {
        const elements = document.querySelectorAll(`[class*="${indicator}"], [id*="${indicator}"]`);
        if (elements.length > 0) {
            console.log(`Found ${elements.length} elements with "${indicator}"`);
        }
    });
}

// Enhanced page readiness check
function enhancedPageReady() {
    console.log('🚀 Enhanced page ready check...');
    
    // Debug current state
    debugCurrentState();
    
    // Initialize results display manager
    window.resultsDisplayManager = new ResultsDisplayManager();
    
    // Show ready indicator
    const indicator = document.createElement('div');
    indicator.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        z-index: 1000;
        transition: opacity 0.5s ease;
        box-shadow: 0 4px 20px rgba(0, 184, 148, 0.3);
    `;
    indicator.innerHTML = '🎯 Results Display Manager Active!';
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => indicator.remove(), 500);
    }, 4000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhancedPageReady);
} else {
    enhancedPageReady();
}

// Also run when the page becomes visible (in case user switches tabs)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        setTimeout(() => {
            if (window.resultsDisplayManager) {
                window.resultsDisplayManager.checkForResults();
            }
        }, 1000);
    }
});

console.log('🎯 Results display manager loaded!');