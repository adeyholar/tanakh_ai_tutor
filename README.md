# 🔥 Hebrew AI Tutor - Agentic Hebrew Learning System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()

An intelligent AI-powered Hebrew learning application featuring:

## 🎯 Features

### 🗣️ **Voice Recognition & Pronunciation Coaching**
- Real-time Hebrew pronunciation analysis
- Personalized feedback and correction
- Progress tracking and improvement suggestions

### 📖 **Interactive Reading System**
- Word-by-word highlighting during reading
- AI-guided read-along sessions
- Adaptive difficulty progression

### 🤖 **HebRabbAI - Tanakh Q&A System**
- RAG-powered biblical Hebrew questions
- Contextual explanations and commentary
- Historical and linguistic insights

### 🧠 **Adaptive Learning Engine**
- Personalized learning paths
- Spaced repetition for memorization
- Performance analytics and insights

## 🏗️ Project Structure

# 🚀 Week 4: React Frontend & JWT Authentication

## Mission: Transform Your Hebrew AI into a Modern React Application

**Achievement Goal:** Professional React frontend with JWT authentication, beautiful Hebrew display, and production-ready architecture.

---

## 📋 Week 4 Learning Objectives

### **Day 1-2: React Foundation & Project Setup**
- ✅ React fundamentals and component architecture
- ✅ Create React app for Hebrew AI platform
- ✅ Set up development environment with Vite
- ✅ Component-based Hebrew text display
- ✅ Connect React frontend to your FastAPI backend

### **Day 3-4: JWT Authentication System**
- ✅ JWT token-based authentication
- ✅ User registration and login system
- ✅ Protected routes and authentication middleware
- ✅ User session management
- ✅ Secure API communication

### **Day 5-6: Advanced React Features**
- ✅ State management with Context API
- ✅ React Router for navigation
- ✅ Beautiful Hebrew text rendering with proper fonts
- ✅ Responsive design with Tailwind CSS
- ✅ Production build and deployment preparation

---

## 🛠️ Technical Stack for Week 4

### **Frontend Stack:**
```bash
- React 18 (Latest version)
- Vite (Super fast build tool)
- TypeScript (Type safety)
- Tailwind CSS (Beautiful styling)
- React Router (Navigation)
- Axios (API communication)
- React Query (Data fetching)
- Zustand (Simple state management)
```

### **Authentication Stack:**
```bash
- JWT Tokens (Secure authentication)
- FastAPI-Users (Backend auth framework)
- Secure HTTP-only cookies
- Password hashing with bcrypt
- Protected API routes
```

### **Development Tools:**
```bash
- Vite (Lightning fast development)
- ESLint + Prettier (Code quality)
- PostCSS (CSS processing)
- React DevTools (Debugging)
```

---

## 🚀 Day 1: React Project Setup

### **Step 1: Create React Project Structure**

```bash
# Create React frontend directory
mkdir src/frontend
cd src/frontend

# Initialize React project with Vite + TypeScript
npm create vite@latest hebrew-ai-frontend -- --template react-ts
cd hebrew-ai-frontend

# Install additional dependencies
npm install @types/react @types/react-dom
npm install tailwindcss postcss autoprefixer
npm install react-router-dom axios react-query
npm install zustand
npm install @headlessui/react @heroicons/react
npm install react-hook-form
npm install js-cookie @types/js-cookie
npm install classnames

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### **Step 2: Configure Tailwind for Hebrew Fonts**

```typescript
// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'hebrew': ['SBL Hebrew', 'Ezra SIL', 'Taamey David CLM', 'serif'],
      },
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}
```

### **Step 3: Project Structure Setup**

```
src/frontend/hebrew-ai-frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # Reusable UI components
│   │   ├── auth/         # Authentication components
│   │   ├── hebrew/       # Hebrew analysis components
│   │   └── layout/       # Layout components
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── AnalyzePage.tsx
│   │   ├── StudyPage.tsx
│   │   ├── LoginPage.tsx
│   │   └── RegisterPage.tsx
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API services
│   ├── store/            # State management
│   ├── types/            # TypeScript types
│   └── utils/            # Utility functions
├── public/
└── index.html
```

---

## 🔐 Day 2-3: JWT Authentication Implementation

### **Backend JWT Setup (FastAPI)**

```python
# Install additional packages for JWT
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# src/auth/jwt_auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import BaseModel

class JWTManager:
    def __init__(self):
        self.SECRET_KEY = "your-secret-key-change-this"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            return username
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
```

### **React Authentication Hook**

```typescript
// src/hooks/useAuth.ts
import { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';

interface User {
  id: string;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password,
      });
      
      const { access_token, user } = response.data;
      localStorage.setItem('token', access_token);
      setUser(user);
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const register = async (username: string, email: string, password: string): Promise<boolean> => {
    try {
      const response = await axios.post('/api/auth/register', {
        username,
        email,
        password,
      });
      
      const { access_token, user } = response.data;
      localStorage.setItem('token', access_token);
      setUser(user);
      return true;
    } catch (error) {
      console.error('Registration failed:', error);
      return false;
    }
  };

  // ... rest of implementation
  
  return (
    <AuthContext.Provider value={{ user, login, logout, register, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

---

## 🎨 Day 4-5: Beautiful Hebrew Components

### **Hebrew Text Display Component**

```typescript
// src/components/hebrew/HebrewText.tsx
import React from 'react';
import classNames from 'classnames';

interface HebrewTextProps {
  text: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  className?: string;
  onClick?: () => void;
}

export const HebrewText: React.FC<HebrewTextProps> = ({
  text,
  size = 'md',
  className,
  onClick
}) => {
  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-xl',
    xl: 'text-2xl',
    '2xl': 'text-4xl'
  };

  return (
    <span
      className={classNames(
        'font-hebrew',
        'direction-rtl',
        'text-right',
        'leading-relaxed',
        sizeClasses[size],
        onClick && 'cursor-pointer hover:text-blue-600 transition-colors',
        className
      )}
      dir="rtl"
      onClick={onClick}
    >
      {text}
    </span>
  );
};
```

### **Word Analysis Component**

```typescript
// src/components/hebrew/WordAnalysis.tsx
import React, { useState } from 'react';
import { HebrewText } from './HebrewText';
import { AnalysisResult } from '../../types/hebrew';

interface WordAnalysisProps {
  analysis: AnalysisResult;
  index: number;
}

export const WordAnalysis: React.FC<WordAnalysisProps> = ({ analysis, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const confidenceColor = analysis.confidence >= 0.8 ? 'green' : 
                         analysis.confidence >= 0.6 ? 'yellow' : 'red';

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <button
        className="w-full p-4 text-left hover:bg-gray-50 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <HebrewText text={analysis.word} size="lg" />
            <span className={`px-2 py-1 rounded text-sm bg-${confidenceColor}-100 text-${confidenceColor}-800`}>
              {(analysis.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <span className="text-gray-600">{analysis.translation}</span>
        </div>
      </button>
      
      {isExpanded && (
        <div className="p-4 bg-gray-50 border-t">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold mb-2">📚 Translation & Meaning</h4>
              <p className="text-gray-700 mb-3">{analysis.translation}</p>
              
              <h4 className="font-semibold mb-2">🔤 Grammar Analysis</h4>
              <ul className="space-y-1 text-sm">
                {analysis.grammar_info.hebrew_root && (
                  <li><strong>Root:</strong> {analysis.grammar_info.hebrew_root}</li>
                )}
                {analysis.grammar_info.morphological_analysis && (
                  <li><strong>Structure:</strong> {analysis.grammar_info.morphological_analysis}</li>
                )}
                {analysis.grammar_info.word_type && (
                  <li><strong>Type:</strong> {analysis.grammar_info.word_type}</li>
                )}
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">🤖 AI Analysis</h4>
              <ul className="space-y-1 text-sm">
                <li><strong>Model:</strong> {analysis.model_used}</li>
                <li><strong>Device:</strong> {analysis.grammar_info.device_used}</li>
                <li><strong>Processing:</strong> {analysis.grammar_info.processing_time}</li>
              </ul>
              
              <p className="text-xs text-gray-500 mt-2">
                Analyzed: {new Date(analysis.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## 🎯 Your Decision Point

**Do you want to:**

**A) 🚀 Jump into Week 4 React Development** (Recommended)
- Modern, professional frontend
- JWT authentication
- Beautiful Hebrew components
- Production-ready architecture

**B) 🔧 Quick HTML Template Fix** (5 minutes)
- Fix current display issue
- Continue with basic HTML templates
- Move to React later

**I strongly recommend Option A** - your backend is solid, and React will give you a much more impressive and professional platform!

**What's your choice?** Let's build something amazing! 🌟