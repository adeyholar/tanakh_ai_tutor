// App.tsx - Enhanced App with Authentication and Your Existing Features
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth, withAuth } from './contexts/AuthContext';
import { AuthPage, AuthModal, UserProfile } from './components/auth/AuthComponents';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

// Type definitions for compatibility
interface User {
  id?: number;
  username?: string;
  total_study_time?: number;
  words_learned?: number;
  learning_level?: string;
  current_chapter?: number;
  email?: string; // Added for completeness from login response
}

interface Book {
  id: string;
  name: string;
  hebrew_name?: string;
}

interface AnalysisResult {
  text?: string;
  word?: string;
  analysis?: any;
  user_level?: string;
  translation?: string;
  grammar_info?: {
    hebrew_root?: string;
    word_type?: string;
    morphological_analysis?: string;
  };
  confidence?: number;
  model_used?: string;
}

// Main App Component
const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <AppContent />
        </div>
      </Router>
    </AuthProvider>
  );
};

// App Content with Routing
const AppContent: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // Sync hash with router state
  useEffect(() => {
    const hash = location.hash.slice(1) || 'home';
    // No need to set state here; router handles it
  }, [location]);

  // Show loading spinner during authentication check
  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary mb-3" role="status" style={{ width: '3rem', height: '3rem' }}>
            <span className="visually-hidden">Loading...</span>
          </div>
          <h5>Loading Hebrew AI Platform...</h5>
        </div>
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/login" element={<AuthPage />} />
          <Route path="/register" element={<AuthPage />} />
          <Route path="/study" element={<StudyPageWrapper />} />
          <Route path="/profile" element={<ProfilePageWrapper />} />
          <Route path="/" element={isAuthenticated ? <HomePage /> : <Navigate to="/login" />} />
          <Route path="*" element={<Navigate to={isAuthenticated ? "/" : "/login"} />} />
        </Routes>
      </main>
    </>
  );
};

// Navigation Bar Component
const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const [showProfile, setShowProfile] = useState<boolean>(false);

  const handleLogout = () => {
    logout();
    window.location.href = '/'; // Use router navigation
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <a className="navbar-brand fw-bold" href="/">
            🎯 Hebrew AI Platform
          </a>
          
          <button 
            className="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <a className="nav-link" href="/">
                  <i className="bi bi-house-fill me-1"></i>Home
                </a>
              </li>
              {isAuthenticated && (
                <li className="nav-item">
                  <a className="nav-link" href="/study">
                    <i className="bi bi-book me-1"></i>Study
                  </a>
                </li>
              )}
            </ul>
            
            <ul className="navbar-nav">
              {isAuthenticated ? (
                <li className="nav-item dropdown">
                  <a 
                    className="nav-link dropdown-toggle" 
                    href="#" 
                    role="button" 
                    data-bs-toggle="dropdown"
                  >
                    <i className="bi bi-person-circle me-1"></i>
                    {user?.username || 'User'}
                  </a>
                  <ul className="dropdown-menu">
                    <li>
                      <button 
                        className="dropdown-item"
                        onClick={() => setShowProfile(true)}
                      >
                        <i className="bi bi-person me-2"></i>Profile
                      </button>
                    </li>
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <button 
                        className="dropdown-item text-danger"
                        onClick={handleLogout}
                      >
                        <i className="bi bi-box-arrow-right me-2"></i>Logout
                      </button>
                    </li>
                  </ul>
                </li>
              ) : (
                <>
                  <li className="nav-item">
                    <a className="nav-link" href="/login">
                      <i className="bi bi-box-arrow-in-right me-1"></i>Login
                    </a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="/register">
                      <i className="bi bi-person-plus me-1"></i>Register
                    </a>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </nav>

      {/* Profile Modal */}
      {showProfile && (
        <UserProfile onClose={() => setShowProfile(false)} />
      )}
    </>
  );
};

// Home Page Component
const HomePage: React.FC = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-lg-8 mx-auto">
          {isAuthenticated ? (
            // Authenticated Home Page
            <div className="text-center">
              <h1 className="display-4 mb-4">
                Welcome back, <span className="text-primary">{user?.username}</span>! 🎉
              </h1>
              <p className="lead mb-4">
                Your Hebrew AI Learning Platform is ready. Continue your journey to Biblical Hebrew mastery!
              </p>
              
              <div className="row mb-5">
                <div className="col-md-4 mb-3">
                  <div className="card h-100">
                    <div className="card-body text-center">
                      <i className="bi bi-clock-history display-4 text-primary mb-3"></i>
                      <h5>Study Time</h5>
                      <h3 className="text-success">{user?.total_study_time || 0} min</h3>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 mb-3">
                  <div className="card h-100">
                    <div className="card-body text-center">
                      <i className="bi bi-journal-text display-4 text-info mb-3"></i>
                      <h5>Words Learned</h5>
                      <h3 className="text-success">{user?.words_learned || 0}</h3>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 mb-3">
                  <div className="card h-100">
                    <div className="card-body text-center">
                      <i className="bi bi-trophy display-4 text-warning mb-3"></i>
                      <h5>Level</h5>
                      <h3 className="text-capitalize text-success">{user?.learning_level || 'Beginner'}</h3>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="d-grid gap-2 d-md-block">
                <a href="/study" className="btn btn-primary btn-lg me-md-2">
                  <i className="bi bi-play-fill me-2"></i>
                  Continue Learning
                </a>
                <a href="/profile" className="btn btn-outline-primary btn-lg">
                  <i className="bi bi-person me-2"></i>
                  View Profile
                </a>
              </div>
            </div>
          ) : (
            // Public Home Page - Your Original Working Hebrew AI Interface
            <PublicHomePage />
          )}
        </div>
      </div>
    </div>
  );
};

// Public Home Page - Restore Your Working Hebrew AI Interface
const PublicHomePage: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [inputWord, setInputWord] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const { analyzeWord } = useAuth(); // Destructure analyzeWord from useAuth hook

  useEffect(() => {
    checkSystemHealth();
  }, []);

  const checkSystemHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      setHealthStatus(data);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({
        status: 'error',
        components: {
          database: 'Connection failed'
        }
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!inputWord.trim()) {
      setError('Please enter a Hebrew word');
      return;
    }

    setAnalyzing(true);
    setError('');

    try {
      const result = await analyzeWord(inputWord.trim());
      setAnalysisResult(result);
    } catch (error) {
      setError('Analysis failed. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const quickWords = ['בראשית', 'אלהים', 'שלום', 'תורה', 'ישראל'];

  if (loading) {
    return (
      <div className="text-center">
        <div className="spinner-border text-primary mb-3" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <h5>Loading Hebrew AI Platform...</h5>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Section */}
      <div className="text-center mb-5">
        <h1 className="display-4 mb-4">
          Hebrew AI Learning Platform 🎯
        </h1>
        <p className="lead mb-4">
          Master Biblical Hebrew with AI-powered analysis and personalized learning
        </p>
      </div>

      {/* System Status */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">🖥️ System Status</h5>
            </div>
            <div className="card-body">
              <div className="row text-center">
                <div className="col-md-3 mb-3">
                  <div className={`p-3 rounded ${healthStatus?.status === 'healthy' ? 'bg-success' : 'bg-danger'} text-white`}>
                    <h6>Backend API</h6>
                    <p className="mb-0">{healthStatus?.status === 'healthy' ? '✅ Connected' : '❌ Offline'}</p>
                  </div>
                </div>
                <div className="col-md-3 mb-3">
                  <div className={`p-3 rounded ${healthStatus?.components?.database === 'Connected' ? 'bg-success' : 'bg-warning'} text-white`}>
                    <h6>Database</h6>
                    <p className="mb-0">{healthStatus?.components?.database === 'Connected' ? '✅ Ready' : '⚠️ Loading'}</p>
                  </div>
                </div>
                <div className="col-md-3 mb-3">
                  <div className={`p-3 rounded ${healthStatus?.components?.alephbert ? 'bg-success' : 'bg-warning'} text-white`}>
                    <h6>AlephBERT AI</h6>
                    <p className="mb-0">{healthStatus?.components?.alephbert ? '✅ Ready' : '⚠️ Loading'}</p>
                  </div>
                </div>
                <div className="col-md-3 mb-3">
                  <div className={`p-3 rounded ${healthStatus?.components?.tanakh_data ? 'bg-success' : 'bg-warning'} text-white`}>
                    <h6>Hebrew Data</h6>
                    <p className="mb-0">{healthStatus?.components?.tanakh_data ? '✅ Loaded' : '⚠️ Loading'}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Hebrew Analysis - Your Original Working Feature */}
      <div className="row mb-5">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">⚡ Quick Hebrew Analysis</h5>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <div className="mb-3">
                <label className="form-label">Hebrew Word:</label>
                <input
                  type="text"
                  value={inputWord}
                  onChange={(e) => setInputWord(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                  className="form-control"
                  placeholder="Enter Hebrew word (e.g., בראשית)"
                  style={{ direction: 'rtl', textAlign: 'right' }}
                />
              </div>

              <div className="d-grid gap-2 mb-3">
                <button
                  onClick={handleAnalyze}
                  disabled={analyzing || !inputWord.trim()}
                  className="btn btn-primary"
                >
                  {analyzing ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-search me-2"></i>
                      Analyze Word
                    </>
                  )}
                </button>
              </div>

              <div className="mb-3">
                <label className="form-label">Quick Words:</label>
                <div className="d-flex flex-wrap gap-2">
                  {quickWords.map((word, index) => (
                    <button
                      key={index}
                      onClick={() => setInputWord(word)}
                      className="btn btn-outline-secondary btn-sm"
                    >
                      {word}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">🤖 Analysis Results</h5>
            </div>
            <div className="card-body">
              {analysisResult ? (
                <div>
                  <div className="mb-3">
                    <h6>Hebrew Word:</h6>
                    <p className="fs-5 fw-bold" style={{ direction: 'rtl', textAlign: 'right' }}>
                      {analysisResult.word}
                    </p>
                  </div>

                  {analysisResult.translation && (
                    <div className="mb-3">
                      <h6>Translation:</h6>
                      <p>{analysisResult.translation}</p>
                    </div>
                  )}

                  {analysisResult.grammar_info && (
                    <div className="mb-3">
                      <h6>Grammar Analysis:</h6>
                      <div className="bg-light p-3 rounded">
                        {analysisResult.grammar_info.hebrew_root && (
                          <p className="mb-2"><strong>Root:</strong> {analysisResult.grammar_info.hebrew_root}</p>
                        )}
                        {analysisResult.grammar_info.word_type && (
                          <p className="mb-2"><strong>Type:</strong> {analysisResult.grammar_info.word_type}</p>
                        )}
                        {analysisResult.grammar_info.morphological_analysis && (
                          <p className="mb-0"><strong>Analysis:</strong> {analysisResult.grammar_info.morphological_analysis}</p>
                        )}
                      </div>
                    </div>
                  )}

                  {analysisResult.confidence && (
                    <div className="mb-3">
                      <h6>Confidence:</h6>
                      <div className="progress">
                        <div
                          className="progress-bar bg-success"
                          style={{ width: `${(analysisResult.confidence * 100)}%` }}
                        ></div>
                      </div>
                      <p className="small mt-1 mb-0">
                        {Math.round(analysisResult.confidence * 100)}% ({analysisResult.model_used || 'AI Model'})
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center text-muted py-4">
                  <i className="bi bi-search display-3 mb-3"></i>
                  <p>Enter a Hebrew word to see AI-powered analysis</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="row mb-5">
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <i className="bi bi-cpu display-4 text-primary mb-3"></i>
              <h5>AI-Powered Analysis</h5>
              <p>Advanced AlephBERT + Llama 3 hybrid intelligence for accurate Biblical Hebrew understanding</p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <i className="bi bi-book display-4 text-success mb-3"></i>
              <h5>Complete Hebrew Bible</h5>
              <p>Full Tanakh with all 39 books, chapters, and verses with cantillation marks</p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <i className="bi bi-graph-up display-4 text-info mb-3"></i>
              <h5>Progress Tracking</h5>
              <p>Personal dashboard to monitor your learning journey and vocabulary growth</p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center">
        <div className="d-grid gap-2 d-md-block mb-4">
          <a href="/register" className="btn btn-primary btn-lg me-md-2">
            <i className="bi bi-person-plus me-2"></i>
            Start Learning
          </a>
          <a href="/login" className="btn btn-outline-primary btn-lg">
            <i className="bi bi-box-arrow-in-right me-2"></i>
            Login
          </a>
        </div>

        <div className="bg-light p-4 rounded">
          <h4>🚀 Platform Features</h4>
          <div className="row text-start">
            <div className="col-md-6">
              <ul className="list-unstyled">
                <li><i className="bi bi-check-circle text-success me-2"></i>Real-time Hebrew text analysis</li>
                <li><i className="bi bi-check-circle text-success me-2"></i>Individual word breakdown</li>
                <li><i className="bi bi-check-circle text-success me-2"></i>Biblical context explanations</li>
                <li><i className="bi bi-check-circle text-success me-2"></i>Pronunciation guides</li>
              </ul>
            </div>
            <div className="col-md-6">
              <ul className="list-unstyled">
                <li><i className="bi bi-check-circle text-success me-2"></i>Personal progress tracking</li>
                <li><i className="bi bi-check-circle text-success me-2"></i>Study session management</li>
                <li><i className="bi bi-check-circle text-success me-2"></i>Adaptive learning levels</li>
                <li><i className="bi bi-check-circle text-success me-2"></i>GPU-accelerated AI processing</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Protected Study Page Wrapper
const StudyPageWrapper = withAuth(() => {
  return <StudyPage />;
});

// Study Page Component
const StudyPage: React.FC = () => {
  const { user, analyzeText, analyzeWord, getBooks, startStudySession, endStudySession } = useAuth();
  const [books, setBooks] = useState<Book[]>([]);
  const [selectedBook, setSelectedBook] = useState<string>('');
  const [selectedChapter, setSelectedChapter] = useState<number>(1);
  const [inputText, setInputText] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [studySessionActive, setStudySessionActive] = useState<boolean>(false);
  const [sessionStartTime, setSessionStartTime] = useState<Date | null>(null);

  // Load books on component mount
  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      const response = await getBooks();
      const bookList: Book[] = (response.books || []).map((bookId: string) => ({
        id: bookId,
        name: bookId, // Adjust if you have hebrew_name data
      }));
      setBooks(bookList);
      if (bookList.length > 0) setSelectedBook(bookList[0].id);
    } catch (error) {
      console.error('Failed to load books:', error);
      setError('Failed to load Hebrew books');
    }
  };

  const handleStartSession = async () => {
    try {
      await startStudySession(selectedBook, selectedChapter);
      setStudySessionActive(true);
      setSessionStartTime(new Date());
      setError('');
    } catch (error) {
      setError('Failed to start study session');
    }
  };

  const handleEndSession = async () => {
    if (!sessionStartTime) return;
    
    try {
      const studyMinutes = Math.floor((new Date().getTime() - sessionStartTime.getTime()) / 60000);
      const wordsAnalyzed = analysisResult ? inputText.split(' ').length : 0;
      
      await endStudySession({ sessionId: 1, wordsReviewed: studyMinutes, versesStudied: wordsAnalyzed });
      setStudySessionActive(false);
      setSessionStartTime(null);
      setError('');
    } catch (error) {
      setError('Failed to end study session');
    }
  };

  const handleAnalyze = async () => {
    if (!inputText.trim()) {
      setError('Please enter Hebrew text to analyze');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const result = await analyzeText(inputText.trim());
      setAnalysisResult(result);
    } catch (error) {
      setError('Analysis failed. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleWordAnalyze = async (word: string) => {
    if (!word.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const result = await analyzeWord(word.trim());
      setAnalysisResult(result);
    } catch (error) {
      setError('Word analysis failed. Please try again.');
      console.error('Word analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickWords = ['בראשית', 'אלהים', 'שלום', 'תורה', 'ישראל'];

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h2>📚 Hebrew AI Study Center</h2>
              <p className="text-muted mb-0">
                Welcome, <strong>{user?.username}</strong> | Level: <span className="badge bg-primary">{user?.learning_level}</span>
              </p>
            </div>
            <div>
              {!studySessionActive ? (
                <button className="btn btn-success" onClick={handleStartSession}>
                  <i className="bi bi-play-fill me-2"></i>
                  Start Session
                </button>
              ) : (
                <button className="btn btn-warning" onClick={handleEndSession}>
                  <i className="bi bi-stop-fill me-2"></i>
                  End Session
                </button>
              )}
            </div>
          </div>

          {studySessionActive && sessionStartTime && (
            <div className="alert alert-info mb-4">
              <i className="bi bi-clock me-2"></i>
              Study session active since {sessionStartTime.toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>

      <div className="row">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">🔍 Hebrew Text Analysis</h5>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <div className="mb-3">
                <label htmlFor="hebrewInput" className="form-label">
                  Enter Hebrew Text:
                </label>
                <textarea
                  id="hebrewInput"
                  className="form-control"
                  rows={3}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Type Hebrew text here... (e.g., בראשית ברא אלהים)"
                  style={{ direction: 'rtl', textAlign: 'right' }}
                />
              </div>

              <div className="d-grid gap-2">
                <button
                  className="btn btn-primary"
                  onClick={handleAnalyze}
                  disabled={loading || !inputText.trim()}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-search me-2"></i>
                      Analyze Text
                    </>
                  )}
                </button>
              </div>

              <hr />

              <div className="mb-3">
                <label className="form-label">Quick Hebrew Words:</label>
                <div className="d-flex flex-wrap gap-2">
                  {quickWords.map((word, index) => (
                    <button
                      key={index}
                      className="btn btn-outline-secondary btn-sm"
                      onClick={() => handleWordAnalyze(word)}
                      disabled={loading}
                    >
                      {word}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="card mt-4">
            <div className="card-header">
              <h5 className="mb-0">📖 Book Selection</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-8">
                  <label className="form-label">Hebrew Bible Book:</label>
                  <select
                    className="form-select"
                    value={selectedBook}
                    onChange={(e) => setSelectedBook(e.target.value)}
                  >
                    {books.map((book) => (
                      <option key={book.id} value={book.id}>
                        {book.name} ({book.hebrew_name || book.id})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="form-label">Chapter:</label>
                  <input
                    type="number"
                    className="form-control"
                    min="1"
                    max="150"
                    value={selectedChapter}
                    onChange={(e) => setSelectedChapter(parseInt(e.target.value) || 1)}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">🤖 AI Analysis Results</h5>
            </div>
            <div className="card-body">
              {analysisResult ? (
                <div>
                  <div className="mb-3">
                    <h6>Text Analyzed:</h6>
                    <div 
                      className="p-2 bg-light rounded"
                      style={{ direction: 'rtl', textAlign: 'right' }}
                    >
                      <strong>{analysisResult.text || analysisResult.word}</strong>
                    </div>
                  </div>

                  <div className="mb-3">
                    <h6>AI Analysis:</h6>
                    <div className="p-3 border rounded">
                      {typeof analysisResult.analysis === 'string' ? (
                        <p className="mb-0">{analysisResult.analysis}</p>
                      ) : (
                        <pre className="mb-0" style={{ whiteSpace: 'pre-wrap', fontSize: '0.9em' }}>
                          {JSON.stringify(analysisResult.analysis, null, 2)}
                        </pre>
                      )}
                    </div>
                  </div>

                  {analysisResult.user_level && (
                    <div className="alert alert-info">
                      <small>
                        <i className="bi bi-info-circle me-1"></i>
                        Analysis tailored for your level: <strong>{analysisResult.user_level}</strong>
                      </small>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center text-muted py-5">
                  <i className="bi bi-search display-1 mb-3"></i>
                  <p>Enter Hebrew text and click "Analyze" to see AI-powered insights</p>
                </div>
              )}
            </div>
          </div>

          <div className="card mt-4">
            <div className="card-header">
              <h5 className="mb-0">📊 Your Progress</h5>
            </div>
            <div className="card-body">
              <div className="row text-center">
                <div className="col-4">
                  <div className="border rounded p-3">
                    <h4 className="text-primary mb-1">{user?.total_study_time || 0}</h4>
                    <small className="text-muted">Minutes</small>
                  </div>
                </div>
                <div className="col-4">
                  <div className="border rounded p-3">
                    <h4 className="text-success mb-1">{user?.words_learned || 0}</h4>
                    <small className="text-muted">Words</small>
                  </div>
                </div>
                <div className="col-4">
                  <div className="border rounded p-3">
                    <h4 className="text-info mb-1">{user?.current_chapter || 1}</h4>
                    <small className="text-muted">Chapter</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Protected Profile Page Wrapper
const ProfilePageWrapper = withAuth(() => {
  const [showProfile, setShowProfile] = useState<boolean>(true);
  
  return showProfile ? (
    <UserProfile onClose={() => window.location.href = '/home'} />
  ) : (
    <div>Loading...</div>
  );
});

export default App;