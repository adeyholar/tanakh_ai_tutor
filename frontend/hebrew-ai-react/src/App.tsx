// src/App.tsx
// UPDATED VERSION - Enhanced with Dynamic Book Loading Study Component

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axios from 'axios';

// Import the new enhanced Study component
import Study from './pages/Study';

// Create QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000,
    },
  },
});

// Enhanced Home Page with better system status
const HomePage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          🔯 Hebrew AI Learning Platform
        </h1>
        <p className="text-xl text-gray-600 mb-2">
          Advanced Biblical Hebrew analysis powered by AlephBERT AI
        </p>
        <p className="text-sm text-gray-500">
          GPU-accelerated processing • Complete Hebrew Bible • Real-time analysis
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-3">
            <span className="text-2xl mr-2">📝</span>
            <h3 className="text-lg font-semibold">Word Analysis</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Analyze individual Hebrew words with AI-powered grammar insights and root analysis
          </p>
          <a href="/analyze" className="btn-primary">Analyze Words</a>
        </div>
        
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-3">
            <span className="text-2xl mr-2">📖</span>
            <h3 className="text-lg font-semibold">Verse Study</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Study Biblical verses from all 39 books with comprehensive word-by-word analysis
          </p>
          <a href="/study" className="btn-primary">Study Verses</a>
        </div>
        
        <div className="card hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-3">
            <span className="text-2xl mr-2">📊</span>
            <h3 className="text-lg font-semibold">Progress</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Track your Hebrew learning progress and vocabulary growth over time
          </p>
          <a href="/progress" className="btn-primary">View Progress</a>
        </div>
      </div>
      
      <div className="mt-12 card bg-blue-50 border-blue-200">
        <h3 className="text-lg font-semibold mb-2 flex items-center">
          <span className="text-2xl mr-2">🚀</span>
          System Status
        </h3>
        <SystemStatus />
      </div>
      
      {/* Quick Stats Section */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">999+</div>
          <div className="text-sm text-green-700">Tokens/Second</div>
          <div className="text-xs text-green-600">GPU Performance</div>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">39</div>
          <div className="text-sm text-blue-700">Books Available</div>
          <div className="text-xs text-blue-600">Complete Hebrew Bible</div>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-600">~0.48GB</div>
          <div className="text-sm text-purple-700">GPU Memory</div>
          <div className="text-xs text-purple-600">Efficient Processing</div>
        </div>
      </div>
    </div>
  );
};

// Enhanced System Status Component
const SystemStatus = () => {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const checkStatus = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/health');
      setStatus(response.data);
    } catch (error) {
      console.error('Health check failed:', error);
      setStatus({ error: 'Backend not available' });
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    checkStatus();
    // Auto-refresh every 30 seconds
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center text-gray-600">
        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
        Checking system status...
      </div>
    );
  }

  if (status?.error) {
    return (
      <div className="text-red-600">
        <div className="flex items-center mb-2">
          <span className="text-lg mr-2">❌</span>
          <span className="font-medium">Backend not connected</span>
        </div>
        <p className="text-sm">
          Make sure your FastAPI server is running at localhost:8000
        </p>
        <button
          onClick={checkStatus}
          className="mt-2 text-sm bg-red-100 hover:bg-red-200 px-3 py-1 rounded transition-colors"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  if (status?.status === 'healthy' || status?.status === 'partial') {
    const components = status.components || {};
    return (
      <div className="space-y-3">
        <div className="flex items-center text-green-600 mb-3">
          <span className="text-lg mr-2">✅</span>
          <span className="font-medium">Hebrew AI Backend Connected!</span>
          {status.gpu_performance?.tokens_per_second && (
            <span className="ml-2 text-xs bg-green-100 px-2 py-1 rounded">
              {status.gpu_performance.tokens_per_second} tokens/sec
            </span>
          )}
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <span>🤖 AlephBERT:</span>
              <span className={components.alephbert?.status ? 'text-green-600' : 'text-red-600'}>
                {components.alephbert?.status ? '✅ Ready' : '❌ Offline'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span>🎮 GPU:</span>
              <span className={components.gpu?.status ? 'text-green-600' : 'text-red-600'}>
                {components.gpu?.status ? '✅ Active' : '❌ Offline'}
              </span>
            </div>
          </div>
          
          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <span>📚 Tanakh:</span>
              <span className={components.tanakh_data?.status ? 'text-green-600' : 'text-red-600'}>
                {components.tanakh_data?.status ? 
                  `✅ ${components.tanakh_data.book_count} books` : 
                  '❌ Not loaded'
                }
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span>💾 Database:</span>
              <span className={components.database?.status ? 'text-green-600' : 'text-red-600'}>
                {components.database?.status ? '✅ Connected' : '❌ Offline'}
              </span>
            </div>
          </div>
        </div>
        
        {status.gpu_performance && (
          <div className="mt-3 pt-3 border-t border-blue-200">
            <div className="text-xs text-gray-600 space-y-1">
              <div>GPU Memory: {status.gpu_performance.memory_usage}</div>
              <div>Last checked: {new Date(status.timestamp).toLocaleTimeString()}</div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return <div className="text-gray-600">System status unknown</div>;
};

// Enhanced Word Analysis Page
const AnalyzePage = () => {
  const [word, setWord] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<string[]>([]);

  const analyzeWord = async () => {
    if (!word.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/analyze-word', {
        word: word.trim()
      });
      setResult(response.data);
      
      // Add to history (keep last 5)
      setHistory(prev => [word.trim(), ...prev.slice(0, 4)]);
    } catch (error) {
      console.error('Analysis failed:', error);
      setResult({ error: 'Analysis failed. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !loading) {
      analyzeWord();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">📝 Hebrew Word Analysis</h1>
        <p className="text-gray-600">
          Analyze individual Hebrew words with AI-powered grammar and root analysis
        </p>
      </div>
      
      <div className="card mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter Hebrew word (e.g., בְּרֵאשִׁית)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hebrew-text"
            dir="rtl"
          />
          <button
            onClick={analyzeWord}
            disabled={loading || !word.trim()}
            className="btn-primary disabled:opacity-50 flex items-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Analyzing...
              </>
            ) : (
              'Analyze'
            )}
          </button>
        </div>
        
        {/* Quick access buttons */}
        {history.length > 0 && (
          <div className="mt-4 pt-4 border-t">
            <p className="text-sm text-gray-600 mb-2">Recent words:</p>
            <div className="flex flex-wrap gap-2">
              {history.map((historyWord, index) => (
                <button
                  key={index}
                  onClick={() => setWord(historyWord)}
                  className="text-sm bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded hebrew-text"
                  dir="rtl"
                >
                  {historyWord}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {result && (
        <div className="card">
          {result.error ? (
            <div className="text-red-600 flex items-center">
              <span className="text-lg mr-2">❌</span>
              {result.error}
            </div>
          ) : (
            <div>
              <div className="flex items-center gap-4 mb-6">
                <span className="hebrew-text text-4xl font-bold">{result.word}</span>
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded text-sm ${
                    result.confidence > 0.8 ? 'bg-green-100 text-green-800' :
                    result.confidence > 0.6 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {Math.round(result.confidence * 100)}% confidence
                  </span>
                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                    GPU Accelerated
                  </span>
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Translation:</h3>
                    <p className="text-gray-700 text-lg">{result.translation}</p>
                  </div>
                  
                  {result.grammar_info?.hebrew_root && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">Hebrew Root:</h3>
                      <p className="text-gray-700 hebrew-text text-xl">{result.grammar_info.hebrew_root}</p>
                    </div>
                  )}
                  
                  {result.grammar_info?.word_type && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">Word Type:</h3>
                      <p className="text-gray-700">{result.grammar_info.word_type}</p>
                    </div>
                  )}
                </div>
                
                <div className="space-y-4">
                  {result.grammar_info?.morphological_analysis && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">Grammar Structure:</h3>
                      <p className="text-gray-700">{result.grammar_info.morphological_analysis}</p>
                    </div>
                  )}
                  
                  {result.grammar_info?.biblical_context && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">Biblical Context:</h3>
                      <p className="text-gray-700">{result.grammar_info.biblical_context}</p>
                    </div>
                  )}
                  
                  <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded">
                    <div>Model: {result.model_used}</div>
                    <div>Device: {result.grammar_info?.device_used || 'GPU'}</div>
                    <div>Analyzed: {new Date(result.timestamp).toLocaleString()}</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Progress Page Enhanced
const ProgressPage = () => (
  <div className="max-w-4xl mx-auto">
    <div className="mb-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">📊 Learning Progress</h1>
      <p className="text-gray-600">
        Track your Hebrew learning journey and vocabulary development
      </p>
    </div>
    <div className="card">
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🚧</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Progress Tracking Coming Soon</h3>
        <p className="text-gray-600 mb-6">
          We're building comprehensive learning analytics to track your Hebrew study progress.
        </p>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-2xl mb-2">📈</div>
            <div className="font-medium">Vocabulary Growth</div>
            <div className="text-gray-600">Track new words learned</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-2xl mb-2">🎯</div>
            <div className="font-medium">Study Streaks</div>
            <div className="text-gray-600">Daily learning consistency</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-2xl mb-2">📚</div>
            <div className="font-medium">Biblical Coverage</div>
            <div className="text-gray-600">Books and chapters studied</div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// Main App Component
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          {/* Enhanced Navigation */}
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <a href="/" className="text-xl font-bold text-gray-900 flex items-center">
                    <span className="text-2xl mr-2">🔯</span>
                    Hebrew AI Platform
                  </a>
                </div>
                <div className="flex items-center space-x-6">
                  <a href="/" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">
                    Home
                  </a>
                  <a href="/analyze" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">
                    Analyze
                  </a>
                  <a href="/study" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">
                    Study
                  </a>
                  <a href="/progress" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">
                    Progress
                  </a>
                </div>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/analyze" element={<AnalyzePage />} />
              <Route path="/study" element={<Study />} />
              <Route path="/progress" element={<ProgressPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;