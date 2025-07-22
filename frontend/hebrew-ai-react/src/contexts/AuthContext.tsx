// src/contexts/AuthContext.tsx - Authentication Context for React
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define types
interface User {
  id: number;
  username: string;
  email: string;
  learning_level: string;
  total_study_time?: number;
  words_learned?: number;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  token: string | null;
  register: (userData: { username: string; email: string; password: string; learning_level?: string }) => Promise<{ success: boolean; user?: User; error?: string }>;
  login: (credentials: { username: string; password: string }) => Promise<{ success: boolean; user?: User; error?: string }>;
  logout: () => void;
  verifyToken: () => Promise<void>;
  getUserProfile: () => Promise<User | null>;
  updateProfile: (updates: Partial<User>) => Promise<{ success: boolean; error?: string }>;
  changePassword: (passwordData: { currentPassword: string; newPassword: string }) => Promise<{ success: boolean; error?: string }>;
  getUserStats: () => Promise<User | null>;
  analyzeText: (text: string) => Promise<any>;
  analyzeWord: (word: string) => Promise<any>;
  getBooks: () => Promise<{ books: string[]; user_authenticated: boolean; total_books: number }>;
  startStudySession: (book: string, chapter: number) => Promise<any>;
  endStudySession: (sessionData: { sessionId: number; wordsReviewed: number; versesStudied: number }) => Promise<any>;
  getStudyProgress: () => Promise<User | null>;
  apiCall: (endpoint: string, options?: RequestInit) => Promise<any>;
}

// Create Authentication Context
const AuthContext = createContext<AuthContextType | null>(null);

// API Base URL
const API_BASE = 'http://localhost:8000';

// Authentication Provider Component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(localStorage.getItem('auth_token'));

  // Set up axios defaults if token exists
  useEffect(() => {
    if (token) {
      verifyToken();
    } else {
      setLoading(false);
    }
  }, [token]);

  // API call helper with automatic token handling
  const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers as { [key: string]: string }),
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
  const register = async (userData: { username: string; email: string; password: string; learning_level?: string }) => {
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
        setUser(response.user);
        return { success: true, user: response.user };
      }
      
      return { success: false, error: 'Registration failed' };
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: (error as Error).message };
    } finally {
      setLoading(false);
    }
  };

  // Login existing user
  const login = async (credentials: { username: string; password: string }) => {
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
        setUser(response.user);
        return { success: true, user: response.user };
      }
      
      return { success: false, error: 'Login failed' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: (error as Error).message || 'Login failed' };
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
      const response = await apiCall('/auth/profile');
      if (response) {
        setUser(response);
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
  const updateProfile = async (updates: Partial<User>) => {
    try {
      await apiCall('/auth/profile', {
        method: 'PUT',
        body: JSON.stringify(updates),
      });
      await getUserProfile();
      return { success: true };
    } catch (error) {
      console.error('Profile update failed:', error);
      return { success: false, error: (error as Error).message };
    }
  };

  // Change password
  const changePassword = async (passwordData: { currentPassword: string; newPassword: string }) => {
    try {
      await apiCall('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify(passwordData),
      });
      return { success: true };
    } catch (error) {
      console.error('Password change failed:', error);
      return { success: false, error: (error as Error).message };
    }
  };

  // Get user statistics
  const getUserStats = async () => {
    try {
      return await apiCall('/auth/profile');
    } catch (error) {
      console.error('Failed to get user stats:', error);
      return null;
    }
  };

  // Analyze text
  const analyzeText = async (text: string) => {
    try {
      return await apiCall('/api/analyze', {
        method: 'POST',
        body: JSON.stringify({ text, analysis_type: "comprehensive" }),
      });
    } catch (error) {
      console.error('Text analysis failed:', error);
      throw error;
    }
  };

  // Analyze word
  const analyzeWord = async (word: string) => {
    try {
      return await apiCall('/api/analyze-word', {
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
      return await apiCall('/api/books');
    } catch (error) {
      console.error('Failed to get books:', error);
      throw error;
    }
  };

  // Start study session
  const startStudySession = async (book: string, chapter: number) => {
    try {
      return await apiCall('/auth/start-session', {
        method: 'POST',
        body: JSON.stringify({ book, chapter }),
      });
    } catch (error) {
      console.error('Failed to start study session:', error);
      throw error;
    }
  };

  // End study session
  const endStudySession = async (sessionData: { sessionId: number; wordsReviewed: number; versesStudied: number }) => {
    try {
      return await apiCall('/auth/end-session', {
        method: 'POST',
        body: JSON.stringify({
          session_id: sessionData.sessionId,
          words_reviewed: sessionData.wordsReviewed,
          verses_studied: sessionData.versesStudied,
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
      return await apiCall('/auth/profile');
    } catch (error) {
      console.error('Failed to get study progress:', error);
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    token,
    register,
    login,
    logout,
    verifyToken,
    getUserProfile,
    updateProfile,
    changePassword,
    getUserStats,
    analyzeText,
    analyzeWord,
    getBooks,
    startStudySession,
    endStudySession,
    getStudyProgress,
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
export const withAuth = (Component: React.ComponentType<any>) => {
  return function AuthenticatedComponent(props: any) {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
      return (
        <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '200px' }}>
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