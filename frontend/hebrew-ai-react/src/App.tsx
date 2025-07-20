// src/App.tsx
// WORKING VERSION - Connected to your Hebrew AI Backend

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axios from 'axios';

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

// Simple Home Page
const HomePage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          🔯 Hebrew AI Learning Platform
        </h1>
        <p className="text-xl text-gray-600">
          Advanced Biblical Hebrew analysis powered by AlephBERT AI
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold mb-2">📝 Word Analysis</h3>
          <p className="text-gray-600 mb-4">Analyze individual Hebrew words with AI-powered grammar insights</p>
          <a href="/analyze" className="btn-primary">Analyze Words</a>
        </div>
        
        <div className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold mb-2">📖 Verse Study</h3>
          <p className="text-gray-600 mb-4">Study Biblical verses word-by-word with comprehensive analysis</p>
          <a href="/study" className="btn-primary">Study Verses</a>
        </div>
        
        <div className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold mb-2">📊 Progress</h3>
          <p className="text-gray-600 mb-4">Track your Hebrew learning progress and vocabulary growth</p>
          <a href="/progress" className="btn-primary">View Progress</a>
        </div>
      </div>
      
      <div className="mt-12 card bg-blue-50 border-blue-200">
        <h3 className="text-lg font-semibold mb-2">🚀 System Status</h3>
        <SystemStatus />
      </div>
    </div>
  );
};

// System Status Component
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
  }, []);

  if (loading) {
    return <div className="text-gray-600">Checking system status...</div>;
  }

  if (status?.error) {
    return (
      <div className="text-red-600">
        ❌ Backend not connected. Make sure your FastAPI server is running at localhost:8000
      </div>
    );
  }

  if (status?.status === 'healthy') {
    return (
      <div className="text-green-600">
        ✅ Hebrew AI Backend Connected! 
        <ul className="mt-2 text-sm">
          <li>🤖 AlephBERT: {status.components?.alephbert ? '✅' : '❌'}</li>
          <li>🏃‍♂️ GPU: {status.components?.gpu ? '✅' : '❌'}</li>
          <li>📚 Tanakh Data: {status.components?.tanakh_data ? '✅' : '❌'}</li>
          <li>💾 Database: {status.components?.database ? '✅' : '❌'}</li>
        </ul>
      </div>
    );
  }

  return <div className="text-gray-600">System status unknown</div>;
};

// Simple Word Analysis Page
const AnalyzePage = () => {
  const [word, setWord] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyzeWord = async () => {
    if (!word.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/analyze-word', {
        word: word.trim()
      });
      setResult(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
      setResult({ error: 'Analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">📝 Hebrew Word Analysis</h1>
      
      <div className="card mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            placeholder="Enter Hebrew word (e.g., בְּרֵאשִׁית)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 hebrew-text"
            dir="rtl"
          />
          <button
            onClick={analyzeWord}
            disabled={loading || !word.trim()}
            className="btn-primary disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>

      {result && (
        <div className="card">
          {result.error ? (
            <div className="text-red-600">❌ {result.error}</div>
          ) : (
            <div>
              <div className="flex items-center gap-4 mb-4">
                <span className="hebrew-text text-3xl">{result.word}</span>
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                  {Math.round(result.confidence * 100)}% confidence
                </span>
              </div>
              
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold">Translation:</h3>
                  <p className="text-gray-700">{result.translation}</p>
                </div>
                
                {result.grammar_info?.hebrew_root && (
                  <div>
                    <h3 className="font-semibold">Hebrew Root:</h3>
                    <p className="text-gray-700 hebrew-text">{result.grammar_info.hebrew_root}</p>
                  </div>
                )}
                
                {result.grammar_info?.morphological_analysis && (
                  <div>
                    <h3 className="font-semibold">Grammar Structure:</h3>
                    <p className="text-gray-700">{result.grammar_info.morphological_analysis}</p>
                  </div>
                )}
                
                <div className="text-sm text-gray-500">
                  Analyzed by: {result.model_used} • Device: {result.grammar_info?.device_used}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Simple Verse Study Page
const StudyPage = () => {
  const [book, setBook] = useState('Gen');
  const [chapter, setChapter] = useState(1);
  const [verse, setVerse] = useState(1);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const studyVerse = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/study/${book}/${chapter}/${verse}`);
      setResult(response.data);
    } catch (error) {
      console.error('Verse study failed:', error);
      setResult({ error: 'Verse study failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">📖 Biblical Verse Study</h1>
      
      <div className="card mb-8">
        <div className="grid grid-cols-3 gap-4 mb-4">
          <select
            value={book}
            onChange={(e) => setBook(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="Gen">Genesis</option>
            <option value="Exod">Exodus</option>
            <option value="Ps">Psalms</option>
            <option value="Isa">Isaiah</option>
          </select>
          
          <input
            type="number"
            value={chapter}
            onChange={(e) => setChapter(Number(e.target.value))}
            placeholder="Chapter"
            min="1"
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
          
          <input
            type="number"
            value={verse}
            onChange={(e) => setVerse(Number(e.target.value))}
            placeholder="Verse"
            min="1"
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>
        
        <button
          onClick={studyVerse}
          disabled={loading}
          className="btn-primary disabled:opacity-50"
        >
          {loading ? 'Studying...' : 'Study Verse'}
        </button>
      </div>

      {result && (
        <div className="space-y-6">
          {result.error ? (
            <div className="card">
              <div className="text-red-600">❌ {result.error}</div>
            </div>
          ) : (
            <>
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">{result.book} {result.chapter}:{result.verse}</h2>
                <div className="hebrew-text text-2xl mb-4 p-4 bg-gray-50 rounded">
                  {result.hebrew_text}
                </div>
                <div className="text-sm text-gray-600">
                  {result.words_analyzed} words analyzed • {result.model_used || 'Enhanced AlephBERT'}
                </div>
              </div>

              {result.analysis_results && result.analysis_results.map((analysis: any, index: number) => (
                <div key={index} className="card">
                  <div className="flex items-center gap-4 mb-4">
                    <span className="hebrew-text text-2xl">{analysis.word}</span>
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                      {Math.round(analysis.confidence * 100)}% confidence
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold mb-2">Translation & Meaning:</h4>
                      <p className="text-gray-700 mb-4">{analysis.translation}</p>
                      
                      {analysis.grammar_info?.hebrew_root && (
                        <div className="mb-2">
                          <span className="font-medium">Root: </span>
                          <span className="hebrew-text">{analysis.grammar_info.hebrew_root}</span>
                        </div>
                      )}
                      
                      {analysis.grammar_info?.word_type && (
                        <div className="mb-2">
                          <span className="font-medium">Type: </span>
                          <span>{analysis.grammar_info.word_type}</span>
                        </div>
                      )}
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-2">Grammar Analysis:</h4>
                      {analysis.grammar_info?.morphological_analysis && (
                        <p className="text-gray-700 mb-2">{analysis.grammar_info.morphological_analysis}</p>
                      )}
                      
                      {analysis.grammar_info?.biblical_context && (
                        <div className="mb-2">
                          <span className="font-medium">Context: </span>
                          <span className="text-gray-700">{analysis.grammar_info.biblical_context}</span>
                        </div>
                      )}
                      
                      <div className="text-sm text-gray-500 mt-4">
                        Model: {analysis.model_used} • Device: {analysis.grammar_info?.device_used}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
};

// Progress Page Placeholder
const ProgressPage = () => (
  <div className="max-w-4xl mx-auto">
    <h1 className="text-3xl font-bold text-gray-900 mb-8">📊 Learning Progress</h1>
    <div className="card">
      <p className="text-gray-600">Progress tracking coming soon...</p>
    </div>
  </div>
);

// Main App Component
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          {/* Navigation */}
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <a href="/" className="text-xl font-bold text-gray-900">
                    🔯 Hebrew AI Platform
                  </a>
                </div>
                <div className="flex items-center space-x-6">
                  <a href="/" className="text-gray-600 hover:text-gray-900 transition-colors">
                    Home
                  </a>
                  <a href="/analyze" className="text-gray-600 hover:text-gray-900 transition-colors">
                    Analyze
                  </a>
                  <a href="/study" className="text-gray-600 hover:text-gray-900 transition-colors">
                    Study
                  </a>
                  <a href="/progress" className="text-gray-600 hover:text-gray-900 transition-colors">
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
              <Route path="/study" element={<StudyPage />} />
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