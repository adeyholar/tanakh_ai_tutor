# launch_hebrew_platform.py - Hebrew AI Platform with JWT Authentication
# Week 4 Day 4: Complete Authentication and Analysis Integration

import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import traceback
import sqlite3

# FastAPI imports
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import your existing Hebrew AI components and new auth system
try:
    from src.core.enhanced_alephbert_analyzer import EnhancedAlephBertAnalyzer
    from src.core.tanakh_learning_session import TanakhLearningSession
    from src.core.auth_system import AuthenticationSystem, User
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are available in src/core/")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hebrew AI Learning Platform",
    description="Advanced Hebrew learning with AI-powered analysis and user authentication",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Authentication system
auth_system = AuthenticationSystem(database_path="data/hebrew_learning.db")

# Request/Response Models
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    learning_level: str = "beginner"

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserProfile(BaseModel):
    username: str
    email: str
    learning_level: str
    total_study_time: int
    words_learned: int

class HebrewAnalysisRequest(BaseModel):
    text: str
    analysis_type: str = "comprehensive"

class StudySessionStart(BaseModel):
    book: str = ""
    chapter: int = 0

class StudySessionEnd(BaseModel):
    session_id: int
    words_reviewed: int = 0
    verses_studied: int = 0

# Global variables for AI components
enhanced_analyzer = None
learning_session = None

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    token_data = auth_system.verify_token(token)
    
    if token_data is None or token_data.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = auth_system.get_user(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user.__dict__  # Convert dataclass to dict for consistency

# Optional authentication (for endpoints that work with or without auth)
async def get_current_user_optional(request: Request):
    """Get current user if token is provided, otherwise return None"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    try:
        token = authorization.split(" ")[1]
        token_data = auth_system.verify_token(token)
        
        if token_data is None or token_data.username is None:
            return None
        
        user = auth_system.get_user(token_data.username)
        return user.__dict__ if user else None
    except:
        return None

# Initialize AI components
async def initialize_ai_components():
    """Initialize Hebrew AI analysis components"""
    global enhanced_analyzer, learning_session
    
    try:
        logger.info("Initializing Enhanced AlephBERT Analyzer...")
        enhanced_analyzer = EnhancedAlephBertAnalyzer()
        if not enhanced_analyzer.initialize():
            logger.warning("Enhanced AlephBERT initialization failed, using fallback mode")
        
        logger.info("Initializing Tanakh Learning Session...")
        learning_session = TanakhLearningSession(data_path="data/tanakh/hebrew_bible_with_nikkud.json")
        if not await learning_session.initialize():
            logger.warning("Tanakh Learning Session initialization failed")
        
        logger.info("✅ All AI components initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI components: {e}")
        traceback.print_exc()
        return False

# Startup event using lifespan (replacing deprecated on_event)
async def lifespan(app: FastAPI):
    await initialize_ai_components()
    yield
    # Cleanup if needed
    if enhanced_analyzer:
        enhanced_analyzer.cleanup()
    logger.info("Application shutdown complete")

app.add_event_handler("startup", initialize_ai_components)  # Temporary fallback for older FastAPI versions
app.add_event_handler("shutdown", lambda: logger.info("Application shutdown"))

# Health check endpoint (public)
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global enhanced_analyzer, learning_session
    
    status_info = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "enhanced_alephbert": enhanced_analyzer is not None and enhanced_analyzer.is_available,
            "learning_session": learning_session is not None,
            "authentication": True,
            "database": os.path.exists("data/hebrew_learning.db")
        }
    }
    
    if enhanced_analyzer:
        status_info["enhanced_alephbert_stats"] = enhanced_analyzer.get_performance_stats()
    
    return status_info

# AUTHENTICATION ENDPOINTS

@app.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegistration):
    """Register a new user"""
    try:
        success, message = auth_system.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            learning_level=user_data.learning_level
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Authenticate the newly created user
        user = auth_system.authenticate_user(user_data.username, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User created but authentication failed"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=auth_system.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_system.create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "learning_level": user.learning_level
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@app.post("/auth/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """Authenticate user and return JWT token"""
    try:
        user = auth_system.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=auth_system.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_system.create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "learning_level": user.learning_level,
                "total_study_time": user.total_study_time,
                "words_learned": user.words_learned
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@app.get("/auth/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile with statistics"""
    try:
        user_id = current_user["id"]
        user_stats = auth_system.get_user_stats(user_id)
        return user_stats
        
    except Exception as e:
        logger.error(f"Profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )

@app.post("/auth/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user)
):
    """Change user password"""
    try:
        # Verify current password
        user = auth_system.get_user(current_user["username"])
        if not user or not auth_system.verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password
        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters"
            )
        
        # Update password
        success, message = auth_system.create_user(
            username=current_user["username"],
            email=current_user["email"],
            password=new_password,
            learning_level=current_user["learning_level"]
        )
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
        
        return {"message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

@app.post("/auth/start-session")
async def start_study_session(
    session_data: StudySessionStart,
    current_user: dict = Depends(get_current_user)
):
    """Start a new study session"""
    try:
        session_id = auth_system.start_study_session(
            user_id=current_user["id"],
            book=session_data.book,
            chapter=session_data.chapter
        )
        
        # Initiate study in learning session
        if learning_session:
            await learning_session.study_verse(session_data.book, session_data.chapter, 1, current_user["id"])  # Start with verse 1
        
        return {
            "session_id": session_id,
            "message": "Study session started",
            "book": session_data.book,
            "chapter": session_data.chapter
        }
        
    except Exception as e:
        logger.error(f"Start session error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start study session"
        )

@app.post("/auth/end-session")
async def end_study_session(
    session_data: StudySessionEnd,
    current_user: dict = Depends(get_current_user)
):
    """End a study session with statistics"""
    try:
        auth_system.end_study_session(
            session_id=session_data.session_id,
            words_reviewed=session_data.words_reviewed,
            verses_studied=session_data.verses_studied
        )
        
        # Save progress if learning session is active
        if learning_session:
            await learning_session.save_progress()
        
        return {
            "message": "Study session completed",
            "words_reviewed": session_data.words_reviewed,
            "verses_studied": session_data.verses_studied
        }
        
    except Exception as e:
        logger.error(f"End session error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to end study session"
        )

@app.post("/api/analyze")
async def analyze_hebrew_text(
    request: HebrewAnalysisRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Analyze Hebrew text with optional user tracking"""
    global enhanced_analyzer
    
    if not enhanced_analyzer:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Hebrew analyzer not available"
        )
    
    try:
        # Perform Hebrew analysis (using analyze_word for single text input)
        analysis_result = await enhanced_analyzer.analyze_word(request.text)  # Await the coroutine
        if not analysis_result:
            raise ValueError("Analysis failed to produce result")
        
        # Track word study if user is authenticated
        if current_user and "english" in analysis_result.grammar_info:
            auth_system.track_word_study(
                user_id=current_user["id"],
                hebrew_word=request.text,
                english_translation=analysis_result.grammar_info["english"] if "english" in analysis_result.grammar_info else analysis_result.translation
            )
        
        return {
            "analysis": analysis_result.__dict__,
            "user_authenticated": current_user is not None,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/api/analyze-word")
async def analyze_hebrew_word(
    word: str,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Analyze individual Hebrew word with optional user tracking"""
    global enhanced_analyzer
    
    if not enhanced_analyzer:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Hebrew analyzer not available"
        )
    
    try:
        # Perform word analysis
        word_analysis = await enhanced_analyzer.analyze_word(word)  # Await the coroutine
        
        # Track word study if user is authenticated
        if current_user and "english" in word_analysis.grammar_info:
            auth_system.track_word_study(
                user_id=current_user["id"],
                hebrew_word=word,
                english_translation=word_analysis.grammar_info["english"] if "english" in word_analysis.grammar_info else word_analysis.translation
            )
        
        return {
            "word": word,
            "analysis": word_analysis.__dict__,
            "user_authenticated": current_user is not None,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Word analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Word analysis failed: {str(e)}"
        )

@app.get("/api/books")
async def get_books(current_user: Optional[dict] = Depends(get_current_user_optional)):
    """Get list of available books"""
    global learning_session
    
    if not learning_session:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Learning session not available"
        )
    
    try:
        books = learning_session.tanakh_data.keys()  # Using dictionary keys as book names
        return {
            "books": list(books),
            "user_authenticated": current_user is not None,
            "total_books": len(books)
        }
        
    except Exception as e:
        logger.error(f"Books error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get books: {str(e)}"
        )

@app.get("/api/verse/{book}/{chapter}/{verse}")
async def get_verse(
    book: str, 
    chapter: int, 
    verse: int,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get specific verse with analysis"""
    global learning_session
    
    if not learning_session:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Learning session not available"
        )
    
    try:
        verse_data = learning_session._get_verse_data(book, chapter, verse)
        if not verse_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Verse {book} {chapter}:{verse} not found")
        
        # Analyze each word in the verse
        hebrew_words = verse_data["text"]
        analysis_results = []
        for word in hebrew_words:
            analysis = await enhanced_analyzer.analyze_word(word)  # Await the coroutine
            if analysis:
                analysis_results.append(analysis.__dict__)
        
        # Track verse study if user is authenticated
        if current_user:
            await learning_session.study_verse(book, chapter, verse, current_user["id"])
        
        return {
            "verse": {"text": hebrew_words, **verse_data},
            "analysis": analysis_results,
            "user_authenticated": current_user is not None,
            "reference": f"{book} {chapter}:{verse}"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Verse error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get verse: {str(e)}"
        )

@app.get("/admin/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    """List all users (admin only - in production, add role checking)"""
    try:
        # In production, you'd check if current_user has admin role
        # For now, any authenticated user can see this for development
        with sqlite3.connect("data/hebrew_learning.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users")
            users = [{"id": row[0], "username": row[1]} for row in cursor.fetchall()]
        
        return {
            "message": "User listing would require admin privileges",
            "current_user": current_user["username"],
            "users": users,
            "note": "Admin functionality to be implemented"
        }
        
    except Exception as e:
        logger.error(f"Admin error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin operation failed"
        )

@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "message": "Hebrew AI Learning Platform",
        "version": "2.0.0",
        "features": [
            "JWT Authentication",
            "Enhanced AlephBERT Analysis",
            "User Progress Tracking",
            "Study Session Management",
            "Hebrew Text Processing"
        ],
        "endpoints": {
            "health": "/health",
            "register": "/auth/register",
            "login": "/auth/login",
            "analyze": "/api/analyze",
            "books": "/api/books"
        }
    }

@app.get("/debug/status")
async def debug_status():
    """Debug endpoint to check system status"""
    global enhanced_analyzer, learning_session
    
    return {
        "enhanced_alephbert_loaded": enhanced_analyzer is not None and enhanced_analyzer.is_available,
        "learning_session_loaded": learning_session is not None,
        "authentication_system": "active",
        "database_status": os.path.exists("data/hebrew_learning.db"),
        "python_version": sys.version,
        "platform": sys.platform,
        "enhanced_alephbert_stats": enhanced_analyzer.get_performance_stats() if enhanced_analyzer else {},
        "learning_session_stats": learning_session.get_session_stats() if learning_session else {}
    }

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
   )

# Main execution
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Hebrew AI Learning Platform with Authentication...")
    print("📚 Features: JWT Auth, Enhanced AlephBERT Analysis, User Tracking")
    print("🔗 Frontend: http://localhost:5173")
    print("🔗 Backend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "launch_hebrew_platform:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )