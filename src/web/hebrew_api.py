# src/web/hebrew_api.py
"""
FastAPI Web Interface for Hebrew AI Learning Platform - Week 3 Day 5
Professional REST API with HTML interface for Hebrew Bible study
"""

from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import json
from datetime import datetime
from pathlib import Path
import logging

# Import our Hebrew AI components
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "src" / "core"))

from src.core.hebrew_database import HebrewDatabaseManager, UserProfile, VocabularyEntry, StudySession
from src.core.enhanced_alephbert_analyzer import EnhancedAlephBertAnalyzer
from src.core.tanakh_learning_session import TanakhLearningSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HebrewAPI")

# Create FastAPI app
app = FastAPI(
    title="Hebrew AI Learning Platform",
    description="Professional Biblical Hebrew Learning System with AI Analysis",
    version="0.3.5",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates and static files
templates = Jinja2Templates(directory="src/web/templates")
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

# Global components
db_manager: Optional[HebrewDatabaseManager] = None
alephbert_analyzer: Optional[EnhancedAlephBertAnalyzer] = None
tanakh_session: Optional[TanakhLearningSession] = None

# Pydantic models for API
class WordAnalysisRequest(BaseModel):
    word: str = Field(..., description="Hebrew word to analyze")
    user_id: Optional[str] = Field(None, description="User ID for personalized analysis")

class WordAnalysisResponse(BaseModel):
    word: str
    translation: str
    grammar_info: Dict[str, Any]
    confidence: float
    model_used: str
    timestamp: str
    analysis_sources: List[str]

class VerseStudyRequest(BaseModel):
    book: str = Field(..., description="Book name (e.g., 'Gen')")
    chapter: int = Field(..., description="Chapter number")
    verse: int = Field(..., description="Verse number")
    user_id: str = Field(..., description="User ID")

class UserStatsResponse(BaseModel):
    user_id: str
    total_vocabulary: int
    mastered_words: int
    study_streak: int
    last_study_date: Optional[str]
    recommendations: List[str]

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize all Hebrew AI components"""
    global db_manager, alephbert_analyzer, tanakh_session
    
    logger.info("🚀 Starting Hebrew AI Learning Platform...")
    
    try:
        # Initialize database
        db_manager = HebrewDatabaseManager("data/hebrew_learning.db")
        await db_manager.initialize_database()
        logger.info("✅ Database initialized")
        
        # Initialize AlephBERT analyzer
        alephbert_analyzer = EnhancedAlephBertAnalyzer()
        if alephbert_analyzer.initialize():
            logger.info("✅ Enhanced AlephBERT ready")
        else:
            logger.warning("⚠️ AlephBERT initialization failed")
        
        # Initialize Tanakh session
        tanakh_session = TanakhLearningSession()
        await tanakh_session.initialize()
        logger.info("✅ Tanakh learning session ready")
        
        logger.info("🎯 Hebrew AI Platform startup complete!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    if db_manager:
        await db_manager.close_connection()
    logger.info("👋 Hebrew AI Platform shutdown complete")

# Web Routes (HTML Interface)
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Main learning interface"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Hebrew AI Learning Platform",
        "system_status": await get_system_status()
    })

@app.get("/analyze", response_class=HTMLResponse)
async def analyze_page(request: Request):
    """Word analysis interface"""
    return templates.TemplateResponse("analyze.html", {
        "request": request,
        "title": "Hebrew Word Analysis"
    })

@app.get("/study", response_class=HTMLResponse)
async def study_page(request: Request):
    """Verse study interface"""
    return templates.TemplateResponse("study.html", {
        "request": request,
        "title": "Biblical Hebrew Study"
    })

@app.get("/progress", response_class=HTMLResponse)
async def progress_page(request: Request):
    """User progress dashboard"""
    return templates.TemplateResponse("progress.html", {
        "request": request,
        "title": "Learning Progress"
    })

# API Routes (JSON Interface)
@app.get("/api/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": await get_system_status()
    }

@app.post("/api/analyze-word", response_model=WordAnalysisResponse)
async def analyze_word_api(request: WordAnalysisRequest):
    """Analyze a Hebrew word using Enhanced AlephBERT"""
    if not alephbert_analyzer or not alephbert_analyzer.is_available:
        raise HTTPException(status_code=503, detail="AlephBERT analyzer not available")
    
    try:
        # Perform analysis
        result = await alephbert_analyzer.analyze_word(request.word)
        
        # If user provided, save to their vocabulary
        if request.user_id and db_manager:
            vocab_entry = VocabularyEntry(
                word_id=f"{request.user_id}_{request.word}_{int(datetime.now().timestamp())}",
                user_id=request.user_id,
                hebrew_word=result.translation, # Assuming translation is the English word here for vocab
                translation=result.translation,
                root=result.grammar_info.get('hebrew_root', 'unknown'),
                part_of_speech=result.grammar_info.get('word_type', 'unknown'),
                first_encountered=datetime.now(),
                times_studied=1,
                times_correct=0,
                times_incorrect=0,
                mastery_level=0.1,
                last_studied=datetime.now(),
                next_review=datetime.now(),
                tags=["api_analysis"]
            )
            await db_manager.add_vocabulary_word(vocab_entry)
        
        return WordAnalysisResponse(
            word=result.word,
            translation=result.translation,
            grammar_info=result.grammar_info,
            confidence=result.confidence,
            model_used=result.model_used,
            timestamp=result.timestamp.isoformat(),
            analysis_sources=["Enhanced AlephBERT", "Hebrew Grammar Patterns", "Biblical Context"]
        )
        
    except Exception as e:
        logger.error(f"Analysis failed for '{request.word}': {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/study-verse")
async def study_verse_api(request: VerseStudyRequest):
    """Study a biblical verse with comprehensive analysis"""
    if not tanakh_session:
        raise HTTPException(status_code=503, detail="Tanakh session not available")
    
    try:
        # Perform verse study
        verse_study = await tanakh_session.study_verse(request.book, request.chapter, request.verse)
        
        if not verse_study:
            raise HTTPException(status_code=404, detail=f"Verse not found: {request.book} {request.chapter}:{request.verse}")
        
        # Return comprehensive results
        return {
            "verse_reference": f"{request.book} {request.chapter}:{request.verse}",
            "hebrew_text": verse_study.hebrew_text,
            "analysis_results": [
                {
                    "word": result.word,
                    "translation": result.translation,
                    "confidence": result.confidence,
                    "model": result.model_used
                }
                for result in verse_study.analysis_results
            ],
            "words_learned": len(verse_study.words_learned),
            "study_time": verse_study.study_time.isoformat(),
            "session_notes": verse_study.session_notes
        }
        
    except Exception as e:
        logger.error(f"Verse study failed: {e}")
        raise HTTPException(status_code=500, detail=f"Verse study failed: {str(e)}")

@app.get("/api/user/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_stats(user_id: str):
    """Get user learning statistics"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        analytics = await db_manager.get_learning_analytics(user_id)
        
        vocab_stats = analytics.get('vocabulary_stats', {})
        progress_stats = analytics.get('progress_stats', {})
        
        return UserStatsResponse(
            user_id=user_id,
            total_vocabulary=vocab_stats.get('total_words', 0),
            mastered_words=vocab_stats.get('mastered_words', 0),
            study_streak=progress_stats.get('study_streak', 0),
            last_study_date=progress_stats.get('last_study_date'),
            recommendations=analytics.get('recommendations', [])
        )
        
    except Exception as e:
        logger.error(f"Failed to get user stats: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

@app.get("/api/user/{user_id}/vocabulary")
async def get_user_vocabulary(user_id: str, limit: int = 50):
    """Get user's vocabulary with progress"""
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        vocabulary = await db_manager.get_user_vocabulary(user_id, limit)
        return {
            "user_id": user_id,
            "vocabulary_count": len(vocabulary),
            "vocabulary": vocabulary
        }
        
    except Exception as e:
        logger.error(f"Failed to get vocabulary: {e}")
        raise HTTPException(status_code=500, detail=f"Vocabulary retrieval failed: {str(e)}")

# Form handlers for HTML interface
@app.post("/analyze-word-form")
async def analyze_word_form(request: Request, hebrew_word: str = Form(...), user_id: str = Form("demo_user")):
    """Handle word analysis form submission"""
    try:
        # Use the API endpoint
        analysis_request = WordAnalysisRequest(word=hebrew_word, user_id=user_id)
        result = await analyze_word_api(analysis_request)
        
        return templates.TemplateResponse("analyze.html", {
            "request": request,
            "title": "Hebrew Word Analysis",
            "analysis_result": result,
            "analyzed_word": hebrew_word
        })
        
    except Exception as e:
        return templates.TemplateResponse("analyze.html", {
            "request": request,
            "title": "Hebrew Word Analysis",
            "error": str(e),
            "analyzed_word": hebrew_word
        })

# Frontend Template Fix - Update your hebrew_api.py study_verse_form_handler
@app.post("/study-verse-form", response_class=HTMLResponse)
async def study_verse_form_handler(
    request: Request,
    book: str = Form(...),
    chapter: int = Form(...),
    verse: int = Form(...)
):
    """
    Handle verse study form submission and return results
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"📖 Processing verse study request: {book} {chapter}:{verse}")
        
        # Study the verse using your existing session
        verse_study_result = await tanakh_session.study_verse(book, chapter, verse)
        
        logger.info(f"✅ Verse study completed for {book} {chapter}:{verse}")
        
        # Get hebrew_text and handle both string and array formats
        hebrew_text_raw = getattr(verse_study_result, 'hebrew_text', [])
        
        # Convert array to string for display
        if isinstance(hebrew_text_raw, list):
            hebrew_text_display = " ".join(hebrew_text_raw)
        else:
            hebrew_text_display = str(hebrew_text_raw)
        
        # Get analysis results
        analysis_results = getattr(verse_study_result, 'analysis_results', [])
        
        # Prepare template data with proper structure
        template_data = {
            "request": request,
            "verse_data": {
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "hebrew_text": hebrew_text_display,  # Now a proper string
                "words_analyzed": len(analysis_results),
                "analysis_results": analysis_results,
                "study_successful": True
            }
        }
        
        # Debug logging
        logger.info(f"📊 Template data prepared:")
        logger.info(f"   - Hebrew text: {hebrew_text_display}")
        logger.info(f"   - Words analyzed: {len(analysis_results)}")
        logger.info(f"   - Analysis results: {len(analysis_results)} items")
        
        return templates.TemplateResponse("study.html", template_data)
        
    except Exception as e:
        logger.error(f"❌ Error in verse study: {str(e)}")
        
        # Return error template
        error_data = {
            "request": request,
            "verse_data": None,
            "error_message": f"Error studying {book} {chapter}:{verse} - {str(e)}"
        }
        
        return templates.TemplateResponse("study.html", error_data)

# Also update the API endpoint for consistency
@app.get("/api/study/{book}/{chapter}/{verse}")
async def api_study_verse(book: str, chapter: int, verse: int):
    """
    Direct API endpoint to test verse study functionality
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"🔍 API verse study request: {book} {chapter}:{verse}")
        
        # Study the verse
        result = await tanakh_session.study_verse(book, chapter, verse)
        
        # Get hebrew_text and handle both string and array formats
        hebrew_text_raw = getattr(result, 'hebrew_text', [])
        
        # For API, provide both formats
        if isinstance(hebrew_text_raw, list):
            hebrew_text_string = " ".join(hebrew_text_raw)
            hebrew_words_array = hebrew_text_raw
        else:
            hebrew_text_string = str(hebrew_text_raw)
            hebrew_words_array = hebrew_text_raw.split() if hebrew_text_raw else []
        
        # Access VerseStudy object attributes directly
        response = {
            "success": True,
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "hebrew_text": hebrew_text_string,  # String for display
            "hebrew_words": hebrew_words_array,  # Array for processing
            "analysis_results": getattr(result, 'analysis_results', []),
            "words_analyzed": len(getattr(result, 'analysis_results', [])),
            "timestamp": datetime.now().isoformat(),
            "result_type": type(result).__name__,
            "session_notes": getattr(result, 'session_notes', ''),
            "study_time": str(getattr(result, 'study_time', '')),
            "words_learned": getattr(result, 'words_learned', [])
        }
        
        logger.info(f"✅ API response prepared: {len(response['analysis_results'])} analyses")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ API verse study error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "error_type": type(e).__name__
        }

@app.get("/api/debug/tanakh-session")
async def debug_tanakh_session():
    """
    Debug endpoint to check tanakh session status
    """
    try:
        # Get basic info about the session
        session_info = {
            "session_exists": tanakh_session is not None,
            "session_type": type(tanakh_session).__name__ if tanakh_session else None,
            "session_attributes": [attr for attr in dir(tanakh_session) if not attr.startswith('_')] if tanakh_session else []
        }
        
        # Try to get books if possible
        if hasattr(tanakh_session, 'tanakh_data'):
            books_available = list(tanakh_session.tanakh_data.keys())
            session_info.update({
                "books_available": books_available[:10],
                "total_books": len(books_available)
            })
        
        # Try to get analyzers info
        if hasattr(tanakh_session, 'analyzers'):
            session_info["analyzers_count"] = len(tanakh_session.analyzers)
        
        return session_info
        
    except Exception as e:
        return {
            "error": str(e),
            "session_ready": False,
            "error_type": type(e).__name__
        }

@app.get("/api/test/genesis")
async def test_genesis():
    """
    Test endpoint for Genesis 1:1 specifically
    """
    try:
        result = await tanakh_session.study_verse("Gen", 1, 1)
        
        return {
            "test": "Genesis 1:1",
            "success": True,
            "result_type": type(result).__name__,
            "result_attributes": [attr for attr in dir(result) if not attr.startswith('_')],
            "hebrew_text": getattr(result, 'hebrew_text', 'Not found'),
            "analysis_results_count": len(getattr(result, 'analysis_results', [])),
            "has_analysis_results": hasattr(result, 'analysis_results'),
            "result_preview": str(result)[:300] if result else "No result"
        }
    except Exception as e:
        return {
            "test": "Genesis 1:1",
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

# Utility functions
async def get_system_status() -> Dict[str, str]:
    """Get current system component status"""
    status = {}
    
    if db_manager:
        status["database"] = "✅ Connected"
    else:
        status["database"] = "❌ Not available"
    
    if alephbert_analyzer and alephbert_analyzer.is_available:
        status["alephbert"] = "✅ Ready"
    else:
        status["alephbert"] = "❌ Not available"
    
    if tanakh_session:
        status["tanakh_data"] = "✅ Loaded"
    else:
        status["tanakh_data"] = "❌ Not available"
    
    return status

# Development server runner
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Hebrew AI Learning Platform Web Server...")
    print("📖 Features:")
    print("  - Word analysis with Enhanced AlephBERT")
    print("  - Biblical verse study")
    print("  - User progress tracking")
    print("  - Learning analytics")
    print("\n🌐 Access the platform at: http://localhost:8000")
    print("📊 API documentation at: http://localhost:8000/api/docs")
    
    uvicorn.run(
        "hebrew_api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )