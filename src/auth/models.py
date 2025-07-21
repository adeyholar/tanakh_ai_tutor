# src/auth/models.py - Authentication Database Models
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timezone
import os

Base = declarative_base()

class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=True)
    
    # Hebrew learning specific fields
    learning_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    total_study_time = Column(Integer, default=0)  # in minutes
    words_learned = Column(Integer, default=0)
    current_book = Column(String, default="genesis")
    current_chapter = Column(Integer, default=1)

class UserSession(Base):
    """Track user sessions for analytics and security"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

# Database setup
DATABASE_URL = "sqlite:///./data/hebrew_ai_users.db"

# Create database directory if it doesn't exist
os.makedirs("./data", exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database helper functions
def create_user_table():
    """Initialize user tables - call this once"""
    Base.metadata.create_all(bind=engine)
    print("✅ User authentication database created successfully!")

if __name__ == "__main__":
    create_user_table()