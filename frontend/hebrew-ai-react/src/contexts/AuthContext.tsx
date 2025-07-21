// src/contexts/AuthContext.jsx - Authentication Context for React
import React, { createContext, useContext, useState, useEffect } from 'react';

// Create Authentication Context
const AuthContext = createContext({});

// API Base URL
const API_BASE = 'http://localhost:8000';

// Authentication Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));

  // Set up axios defaults if token exists
  useEffect(() => {
    if (token) {
      // Verify token on app start
      verifyToken();
    } else {
      setLoading(false);
    }
  }, [token]);

  // API call helper with automatic token handling
  const apiCall = async (endpoint, options = {}) => {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token expired or invalid
          logout();
          throw new Error('Authentication required');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API call failed for ${endpoint}:`, error);
      throw error;
    }
  };

  // Register new user
  const register = async (userData) => {
    try {
      setLoading(true);
      const response = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      });

      if (response.access_token) {
        const newToken = response.access_token;
        setToken(newToken);
        localStorage.setItem('auth_token', newToken);
        setUser(response.user_info);
        return { success: true, user: response.user_info };
      }
      
      return { success: false, error: 'Registration failed' };
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  // Login existing user
  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });

      if (response.access_token) {
        const newToken = response.access_token;
        setToken(newToken);
        localStorage.setItem('auth_token', newToken);
        setUser(response.user_info);
        return { success: true, user: response.user_info };
      }
      
      return { success: false, error: 'Login failed' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message || 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  // Logout user
  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token');
  };

  // Verify token validity
  const verifyToken = async () => {
    try {
      const response = await apiCall('/auth/verify-token');
      if (response.valid) {
        // Get full user profile
        const profile = await getUserProfile();
        setUser(profile);
      } else {
        logout();
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  // Get user profile
  const getUserProfile = async () => {
    try {
      const profile = await apiCall('/auth/profile');
      setUser(profile);
      return profile;
    } catch (error) {
      console.error('Failed to get user profile:', error);
      return null;
    }
  };

  // Update user profile
  const updateProfile = async (updates) => {
    try {
      await apiCall('/auth/profile', {
        method: 'PUT',
        body: JSON.stringify(updates),
      });
      
      // Refresh user profile
      await getUserProfile();
      return { success: true };
    } catch (error) {
      console.error('Profile update failed:', error);
      return { success: false, error: error.message };
    }
  };

  // Change password
  const changePassword = async (passwordData) => {
    try {
      await apiCall('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify(passwordData),
      });
      return { success: true };
    } catch (error) {
      console.error('Password change failed:', error);
      return { success: false, error: error.message };
    }
  };

  // Get user statistics
  const getUserStats = async () => {
    try {
      return await apiCall('/auth/stats');
    } catch (error) {
      console.error('Failed to get user stats:', error);
      return null;
    }
  };

  // Protected API call for Hebrew analysis
  const analyzeText = async (text) => {
    try {
      return await apiCall('/analyze/text', {
        method: 'POST',
        body: JSON.stringify({ text }),
      });
    } catch (error) {
      console.error('Text analysis failed:', error);
      throw error;
    }
  };

  // Protected API call for word analysis
  const analyzeWord = async (word) => {
    try {
      return await apiCall('/analyze/word', {
        method: 'POST',
        body: JSON.stringify({ word }),
      });
    } catch (error) {
      console.error('Word analysis failed:', error);
      throw error;
    }
  };

  // Get Hebrew books
  const getBooks = async () => {
    try {
      return await apiCall('/books');
    } catch (error) {
      console.error('Failed to get books:', error);
      throw error;
    }
  };

  // Start study session
  const startStudySession = async (book, chapter) => {
    try {
      return await apiCall('/study/session/start', {
        method: 'POST',
        body: JSON.stringify({ book, chapter }),
      });
    } catch (error) {
      console.error('Failed to start study session:', error);
      throw error;
    }
  };

  // End study session
  const endStudySession = async (minutes, wordsReviewed) => {
    try {
      return await apiCall('/study/session/end', {
        method: 'POST',
        body: JSON.stringify({ 
          minutes: minutes,
          words_reviewed: wordsReviewed 
        }),
      });
    } catch (error) {
      console.error('Failed to end study session:', error);
      throw error;
    }
  };

  // Get study progress
  const getStudyProgress = async () => {
    try {
      return await apiCall('/study/progress');
    } catch (error) {
      console.error('Failed to get study progress:', error);
      throw error;
    }
  };

  const value = {
    // State
    user,
    loading,
    isAuthenticated: !!user,
    token,

    // Authentication methods
    register,
    login,
    logout,
    verifyToken,

    // Profile methods
    getUserProfile,
    updateProfile,
    changePassword,
    getUserStats,

    // Hebrew AI methods
    analyzeText,
    analyzeWord,
    getBooks,

    // Study session methods
    startStudySession,
    endStudySession,
    getStudyProgress,

    // Utility
    apiCall,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Higher-order component for protected routes
export const withAuth = (Component) => {
  return function AuthenticatedComponent(props) {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
      return (
        <div className="d-flex justify-content-center align-items-center" style={{minHeight: '200px'}}>
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      );
    }

    if (!isAuthenticated) {
      return <AuthRequired />;
    }

    return <Component {...props} />;
  };
};

// Component to show when authentication is required
const AuthRequired = () => {
  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body text-center">
              <h3 className="card-title">🔐 Authentication Required</h3>
              <p className="card-text">
                Please log in to access the Hebrew AI Learning Platform.
              </p>
              <div className="d-grid gap-2">
                <button 
                  className="btn btn-primary"
                  onClick={() => window.location.hash = '#login'}
                >
                  Login
                </button>
                <button 
                  className="btn btn-outline-primary"
                  onClick={() => window.location.hash = '#register'}
                >
                  Create Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthContext;