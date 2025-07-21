// frontend/hebrew-ai-react/src/pages/Study.tsx
// FIXED VERSION - Handles JSON abbreviations correctly
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Book {
  abbreviation: string;
  full_name: string;
  display_name: string;
}

interface VerseData {
  book: string;
  chapter: number;
  verse: number;
  hebrew_text: string;
  words_analyzed: number;
  analysis_results: Array<{
    word: string;
    translation: string;
    confidence: number;
    model: string;
  }>;
  study_successful: boolean;
}

interface BooksAPIResponse {
  total_books: number;
  books: Book[];
  book_abbreviations: string[];
  book_full_names: string[];
  mapping_info: string;
}

interface ChaptersAPIResponse {
  book_abbreviation: string;
  book_full_name: string;
  book_requested: string;
  total_chapters: number;
  chapters: number[];
  max_chapter: number;
}

const API_BASE = 'http://localhost:8000';

export default function Study() {
  const [books, setBooks] = useState<Book[]>([]);
  const [chapters, setChapters] = useState<number[]>([]);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [selectedChapter, setSelectedChapter] = useState(1);
  const [selectedVerse, setSelectedVerse] = useState(1);
  const [verseData, setVerseData] = useState<VerseData | null>(null);
  const [loading, setLoading] = useState(false);
  const [booksLoading, setBooksLoading] = useState(true);
  const [chaptersLoading, setChaptersLoading] = useState(false);
  const [error, setError] = useState('');

  // Load all available books on component mount
  useEffect(() => {
    loadBooks();
  }, []);

  // Load chapters when book changes
  useEffect(() => {
    if (selectedBook) {
      loadChapters(selectedBook.abbreviation);
    }
  }, [selectedBook]);

  const loadBooks = async () => {
    setBooksLoading(true);
    setError('');
    
    try {
      console.log('📚 Loading books from API...');
      const response = await axios.get<BooksAPIResponse>(`${API_BASE}/api/books`);
      const bookData = response.data;
      
      console.log(`✅ Loaded ${bookData.total_books} books successfully`);
      console.log('📋 Mapping info:', bookData.mapping_info);
      console.log('📖 First 5 books:', bookData.books.slice(0, 5));
      
      setBooks(bookData.books);
      
      // Set default to Genesis if available
      if (bookData.books.length > 0) {
        const genesis = bookData.books.find(b => b.abbreviation === 'Gen') || bookData.books[0];
        setSelectedBook(genesis);
      }
      
    } catch (err: any) {
      console.error('❌ Failed to load books:', err);
      setError(`Failed to load books: ${err.response?.data?.detail || err.message}`);
    } finally {
      setBooksLoading(false);
    }
  };

  const loadChapters = async (bookAbbreviation: string) => {
    setChaptersLoading(true);
    setError('');
    
    try {
      console.log(`📖 Loading chapters for ${bookAbbreviation}...`);
      
      const response = await axios.get<ChaptersAPIResponse>(
        `${API_BASE}/api/books/${encodeURIComponent(bookAbbreviation)}/chapters`
      );
      
      console.log(`✅ Loaded ${response.data.total_chapters} chapters for ${response.data.book_full_name}`);
      
      setChapters(response.data.chapters);
      setSelectedChapter(1); // Reset to chapter 1
      setSelectedVerse(1);   // Reset to verse 1
      
    } catch (err: any) {
      console.error('❌ Failed to load chapters:', err);
      setError(`Failed to load chapters: ${err.response?.data?.detail || err.message}`);
      setChapters([]);
    } finally {
      setChaptersLoading(false);
    }
  };

  const studyVerse = async () => {
    if (!selectedBook || !selectedChapter || !selectedVerse) {
      setError('Please select a book, chapter, and verse');
      return;
    }

    setLoading(true);
    setError('');
    setVerseData(null);
    
    try {
      console.log(`🔍 Studying ${selectedBook.full_name} (${selectedBook.abbreviation}) ${selectedChapter}:${selectedVerse}`);
      
      // Use the abbreviation for the API call (this is what the JSON uses)
      const response = await axios.get(
        `${API_BASE}/api/study/${encodeURIComponent(selectedBook.abbreviation)}/${selectedChapter}/${selectedVerse}`
      );
      
      console.log('📊 API Response:', response.data);
      
      if (response.data.success) {
        setVerseData({
          book: selectedBook.full_name, // Display full name
          chapter: selectedChapter,
          verse: selectedVerse,
          hebrew_text: response.data.hebrew_text,
          words_analyzed: response.data.words_analyzed,
          analysis_results: response.data.analysis_results || [],
          study_successful: true
        });
        
        console.log(`✅ Successfully analyzed ${response.data.words_analyzed} words`);
      } else {
        setError(response.data.error || 'Failed to study verse');
      }
      
    } catch (err: any) {
      console.error('❌ Verse study failed:', err);
      setError(err.response?.data?.detail || 'Failed to study verse. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAccess = (bookAbbrev: string, chapter: number, verse: number) => {
    const book = books.find(b => b.abbreviation === bookAbbrev);
    if (book) {
      setSelectedBook(book);
      setSelectedChapter(chapter);
      setSelectedVerse(verse);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !loading) {
      studyVerse();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Header */}
          <div className="flex items-center mb-8">
            <div className="bg-blue-100 p-3 rounded-lg mr-4">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Biblical Verse Study</h1>
              <p className="text-gray-600 mt-1">
                Study any verse from the complete Hebrew Bible with AI-powered analysis
              </p>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              <div className="flex items-center">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                {error}
              </div>
            </div>
          )}

          {/* Debug Info */}
          {selectedBook && (
            <div className="bg-blue-50 border border-blue-200 p-3 rounded mb-6 text-sm">
              <strong>Debug:</strong> Selected "{selectedBook.full_name}" (JSON key: "{selectedBook.abbreviation}") 
              • {chapters.length} chapters available
            </div>
          )}

          {/* Verse Selection */}
          <div className="grid lg:grid-cols-3 gap-6 mb-8">
            {/* Book Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Book {booksLoading ? '(Loading...)' : `(${books.length} available)`}
              </label>
              <select
                value={selectedBook?.abbreviation || ''}
                onChange={(e) => {
                  const book = books.find(b => b.abbreviation === e.target.value);
                  setSelectedBook(book || null);
                }}
                onKeyPress={handleKeyPress}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
                disabled={booksLoading}
              >
                <option value="">
                  {booksLoading ? 'Loading books...' : 'Select a book...'}
                </option>
                {books.map((book) => (
                  <option key={book.abbreviation} value={book.abbreviation}>
                    {book.display_name}
                  </option>
                ))}
              </select>
              {booksLoading && (
                <div className="mt-2 flex items-center text-sm text-gray-500">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
                  Loading all 39 books...
                </div>
              )}
            </div>

            {/* Chapter Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Chapter {chaptersLoading ? '(Loading...)' : `(${chapters.length} available)`}
              </label>
              <select
                value={selectedChapter}
                onChange={(e) => setSelectedChapter(parseInt(e.target.value))}
                onKeyPress={handleKeyPress}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
                disabled={!selectedBook || chaptersLoading}
              >
                {chapters.length === 0 && !chaptersLoading && (
                  <option value="">Select a book first</option>
                )}
                {chaptersLoading && (
                  <option value="">Loading chapters...</option>
                )}
                {chapters.map((chapter) => (
                  <option key={chapter} value={chapter}>
                    Chapter {chapter}
                  </option>
                ))}
              </select>
              {chaptersLoading && (
                <div className="mt-2 flex items-center text-sm text-gray-500">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
                  Loading chapters...
                </div>
              )}
            </div>

            {/* Verse Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Verse
              </label>
              <input
                type="number"
                min="1"
                max="200"
                value={selectedVerse}
                onChange={(e) => setSelectedVerse(parseInt(e.target.value) || 1)}
                onKeyPress={handleKeyPress}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                disabled={!selectedBook || chaptersLoading}
                placeholder="Enter verse number"
              />
            </div>
          </div>

          {/* Study Button */}
          <div className="text-center mb-8">
            <button
              onClick={studyVerse}
              disabled={loading || !selectedBook || booksLoading || chaptersLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-8 rounded-lg transition-colors flex items-center justify-center mx-auto"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Analyzing with AlephBERT...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Study This Verse
                </>
              )}
            </button>
            
            {selectedBook && selectedChapter && selectedVerse && !loading && (
              <p className="text-sm text-gray-500 mt-2">
                Ready to study: {selectedBook.full_name} {selectedChapter}:{selectedVerse}
              </p>
            )}
          </div>

          {/* Results */}
          {verseData && (
            <div className="border-t pt-8">
              <div className="mb-6">
                <h2 className="text-2xl font-bold mb-2 text-gray-800">
                  {verseData.book} {verseData.chapter}:{verseData.verse}
                </h2>
                <div className="flex items-center text-sm text-gray-500 space-x-4">
                  <span>{verseData.words_analyzed} words analyzed</span>
                  <span>•</span>
                  <span>Enhanced AlephBERT</span>
                  <span>•</span>
                  <span className="flex items-center">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                    GPU Accelerated
                  </span>
                </div>
              </div>
              
              {/* Hebrew Text */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg mb-6 border">
                <div 
                  className="text-3xl font-hebrew text-right leading-relaxed text-gray-800"
                  dir="rtl"
                  style={{ 
                    fontFamily: 'SBL Hebrew, Ezra SIL, David, Times New Roman',
                    lineHeight: '1.8'
                  }}
                >
                  {verseData.hebrew_text}
                </div>
              </div>

              {/* Word Analysis Results */}
              {verseData.analysis_results && verseData.analysis_results.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold mb-4 text-gray-800">
                    Word-by-Word Analysis
                  </h3>
                  <div className="grid gap-4">
                    {verseData.analysis_results.map((result, index) => (
                      <div key={index} className="bg-gray-50 hover:bg-gray-100 p-4 rounded-lg border transition-colors">
                        <div className="flex justify-between items-start mb-3">
                          <span 
                            className="text-xl font-hebrew text-gray-800"
                            dir="rtl"
                            style={{ fontFamily: 'SBL Hebrew, Ezra SIL, David, Times New Roman' }}
                          >
                            {result.word}
                          </span>
                          <div className="flex items-center text-sm text-gray-500">
                            <div className={`w-2 h-2 rounded-full mr-1 ${
                              result.confidence > 0.8 ? 'bg-green-500' : 
                              result.confidence > 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                            }`}></div>
                            {Math.round(result.confidence * 100)}% confidence
                          </div>
                        </div>
                        <p className="text-gray-700 font-medium mb-1">{result.translation}</p>
                        <p className="text-sm text-gray-500">
                          Analyzed by: {result.model}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {(!verseData.analysis_results || verseData.analysis_results.length === 0) && (
                <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                  <p className="text-yellow-800">
                    No detailed analysis available for this verse. The verse was found but analysis results are empty.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Quick Access */}
          {!verseData && !loading && (
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">Quick Access</h3>
              <div className="grid md:grid-cols-3 gap-4">
                <button
                  onClick={() => handleQuickAccess('Gen', 1, 1)}
                  className="p-3 bg-white border rounded-lg hover:bg-blue-50 transition-colors text-left"
                >
                  <div className="font-medium">Genesis 1:1</div>
                  <div className="text-sm text-gray-500">In the beginning...</div>
                </button>
                <button
                  onClick={() => handleQuickAccess('Ps', 23, 1)}
                  className="p-3 bg-white border rounded-lg hover:bg-blue-50 transition-colors text-left"
                >
                  <div className="font-medium">Psalms 23:1</div>
                  <div className="text-sm text-gray-500">The Lord is my shepherd...</div>
                </button>
                <button
                  onClick={() => handleQuickAccess('Isa', 6, 3)}
                  className="p-3 bg-white border rounded-lg hover:bg-blue-50 transition-colors text-left"
                >
                  <div className="font-medium">Isaiah 6:3</div>
                  <div className="text-sm text-gray-500">Holy, holy, holy...</div>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}