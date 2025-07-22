# auth_system.py - Complete JWT Authentication System
# Week 4 Day 4: Backend Authentication Implementation

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import json
from dataclasses import dataclass
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define User and TokenData as top-level dataclasses
@dataclass
class User:
    """User data model"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    learning_level: str = "beginner"
    total_study_time: int = 0
    words_learned: int = 0
    created_at: Optional[str] = None
    last_login: Optional[str] = None
    is_active: bool = True

@dataclass
class TokenData:
    """JWT token data model"""
    username: Optional[str] = None
    user_id: Optional[int] = None

# JWT Configuration (moved to class for instance access)
class AuthenticationSystem:
    SECRET_KEY = secrets.token_urlsafe(32)  # Generate secure random key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days

    # Password hashing configuration
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, database_path: str = "data/hebrew_learning.db"):
        self.database_path = database_path
        self.setup_database()
        logger.info("Authentication system initialized")
    
    def setup_database(self):
        """Initialize user tables in the database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Create users table with all required columns
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        hashed_password TEXT NOT NULL,
                        learning_level TEXT DEFAULT 'beginner',
                        total_study_time INTEGER DEFAULT 0,
                        words_learned INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """)
                
                # Create user_sessions table for tracking study sessions
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        session_end TIMESTAMP,
                        duration_minutes INTEGER,
                        words_reviewed INTEGER DEFAULT 0,
                        verses_studied INTEGER DEFAULT 0,
                        book_studied TEXT,
                        chapter_studied INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create user_progress table for detailed tracking
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        word_hebrew TEXT NOT NULL,
                        word_english TEXT,
                        times_reviewed INTEGER DEFAULT 1,
                        last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        mastery_level INTEGER DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        UNIQUE(user_id, word_hebrew)
                    )
                """)
                
                conn.commit()
                logger.info("Database tables created successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Database setup error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database initialization failed"
            )
    
    # Password Management
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password for storage"""
        return self.pwd_context.hash(password)
    
    # User Management
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, username, email, hashed_password, learning_level,
                           total_study_time, words_learned, created_at, last_login, is_active
                    FROM users WHERE username = ? AND is_active = 1
                """, (username,))
                
                row = cursor.fetchone()
                if row:
                    return User(
                        id=row[0], username=row[1], email=row[2], 
                        hashed_password=row[3], learning_level=row[4],
                        total_study_time=row[5], words_learned=row[6],
                        created_at=row[7], last_login=row[8], is_active=bool(row[9])
                    )
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting user {username}: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, username, email, hashed_password, learning_level,
                           total_study_time, words_learned, created_at, last_login, is_active
                    FROM users WHERE email = ? AND is_active = 1
                """, (email,))
                
                row = cursor.fetchone()
                if row:
                    return User(
                        id=row[0], username=row[1], email=row[2], 
                        hashed_password=row[3], learning_level=row[4],
                        total_study_time=row[5], words_learned=row[6],
                        created_at=row[7], last_login=row[8], is_active=bool(row[9])
                    )
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        self.update_last_login(user.id)
        return user
    
    def create_user(self, username: str, email: str, password: str, 
                   learning_level: str = "beginner") -> Tuple[bool, str]:
        """Create a new user"""
        try:
            # Check if user already exists
            if self.get_user(username):
                return False, "Username already exists"
            
            if self.get_user_by_email(email):
                return False, "Email already registered"
            
            # Validate input
            if len(username) < 3:
                return False, "Username must be at least 3 characters"
            
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            
            if "@" not in email or "." not in email:
                return False, "Invalid email format"
            
            # Hash password and create user
            hashed_password = self.get_password_hash(password)
            
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, hashed_password, learning_level)
                    VALUES (?, ?, ?, ?)
                """, (username, email, hashed_password, learning_level))
                
                conn.commit()
                logger.info(f"User created successfully: {username}")
                return True, "User created successfully"
                
        except sqlite3.IntegrityError as e:
            logger.error(f"User creation integrity error: {e}")
            return False, "Username or email already exists"
        except sqlite3.Error as e:
            logger.error(f"User creation error: {e}")
            return False, "Failed to create user"
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (user_id,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error updating last login for user {user_id}: {e}")
    
    # JWT Token Management
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            
            if username is None:
                return None
            
            return TokenData(username=username, user_id=user_id)
            
        except JWTError:
            return None
    
    # User Progress Tracking
    def track_word_study(self, user_id: int, hebrew_word: str, english_translation: str):
        """Track a word that user has studied"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Check if word already exists for this user
                cursor.execute("""
                    SELECT id, times_reviewed FROM user_progress 
                    WHERE user_id = ? AND word_hebrew = ?
                """, (user_id, hebrew_word))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing word
                    cursor.execute("""
                        UPDATE user_progress 
                        SET times_reviewed = times_reviewed + 1,
                            last_reviewed = CURRENT_TIMESTAMP,
                            mastery_level = MIN(5, mastery_level + 1)
                        WHERE id = ?
                    """, (existing[0],))
                else:
                    # Insert new word
                    cursor.execute("""
                        INSERT INTO user_progress (user_id, word_hebrew, word_english)
                        VALUES (?, ?, ?)
                    """, (user_id, hebrew_word, english_translation))
                
                # Update user's total words learned count
                cursor.execute("""
                    UPDATE users 
                    SET words_learned = (
                        SELECT COUNT(*) FROM user_progress WHERE user_id = ?
                    )
                    WHERE id = ?
                """, (user_id, user_id))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Error tracking word study: {e}")
    
    def start_study_session(self, user_id: int, book: str = "", chapter: int = 0) -> int:
        """Start a new study session and return session ID"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_sessions (user_id, book_studied, chapter_studied)
                    VALUES (?, ?, ?)
                """, (user_id, book, chapter))
                
                session_id = cursor.lastrowid
                conn.commit()
                return session_id
                
        except sqlite3.Error as e:
            logger.error(f"Error starting study session: {e}")
            return 0
    
    def end_study_session(self, session_id: int, words_reviewed: int = 0, verses_studied: int = 0):
        """End a study session with statistics"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Calculate session duration
                cursor.execute("""
                    UPDATE user_sessions 
                    SET session_end = CURRENT_TIMESTAMP,
                        words_reviewed = ?,
                        verses_studied = ?,
                        duration_minutes = (
                            (julianday(CURRENT_TIMESTAMP) - julianday(session_start)) * 24 * 60
                        )
                    WHERE id = ?
                """, (words_reviewed, verses_studied, session_id))
                
                # Update user's total study time
                cursor.execute("""
                    UPDATE users 
                    SET total_study_time = (
                        SELECT COALESCE(SUM(duration_minutes), 0) 
                        FROM user_sessions 
                        WHERE user_id = users.id
                    )
                    WHERE id = (
                        SELECT user_id FROM user_sessions WHERE id = ?
                    )
                """, (session_id,))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Error ending study session: {e}")
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Get basic user stats
                cursor.execute("""
                    SELECT username, learning_level, total_study_time, words_learned,
                           created_at, last_login
                    FROM users WHERE id = ?
                """, (user_id,))
                
                user_data = cursor.fetchone()
                if not user_data:
                    return {}
                
                # Get recent study sessions
                cursor.execute("""
                    SELECT COUNT(*) as session_count,
                           AVG(duration_minutes) as avg_session_length,
                           SUM(words_reviewed) as total_words_reviewed
                    FROM user_sessions 
                    WHERE user_id = ? AND session_end IS NOT NULL
                """, (user_id,))
                
                session_stats = cursor.fetchone()
                
                # Get learning progress
                cursor.execute("""
                    SELECT AVG(mastery_level) as avg_mastery,
                           COUNT(*) as unique_words
                    FROM user_progress 
                    WHERE user_id = ?
                """, (user_id,))
                
                progress_stats = cursor.fetchone()
                
                return {
                    "username": user_data[0],
                    "learning_level": user_data[1],
                    "total_study_time": user_data[2] or 0,
                    "words_learned": user_data[3] or 0,
                    "member_since": user_data[4],
                    "last_login": user_data[5],
                    "total_sessions": session_stats[0] or 0,
                    "avg_session_length": round(session_stats[1] or 0, 1),
                    "total_words_reviewed": session_stats[2] or 0,
                    "avg_mastery_level": round(progress_stats[0] or 0, 1),
                    "unique_words_learned": progress_stats[1] or 0
                }
                
        except sqlite3.Error as e:
            logger.error(f"Error getting user stats: {e}")
            return {}

# Initialize the authentication system
auth_system = AuthenticationSystem()

# Export the main functions for use in FastAPI
def get_auth_system():
    """Get the authentication system instance"""
    return auth_system