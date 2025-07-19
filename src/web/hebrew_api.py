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
                hebrew_word=request.word,
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

@app.post("/study-verse-form")
async def study_verse_form(request: Request, book: str = Form(...), chapter: int = Form(...), 
                          verse: int = Form(...), user_id: str = Form("demo_user")):
    """Handle verse study form submission"""
    try:
        # Use the API endpoint
        study_request = VerseStudyRequest(book=book, chapter=chapter, verse=verse, user_id=user_id)
        result = await study_verse_api(study_request)
        
        return templates.TemplateResponse("study.html", {
            "request": request,
            "title": "Biblical Hebrew Study",
            "study_result": result,
            "verse_reference": f"{book} {chapter}:{verse}"
        })
        
    except Exception as e:
        return templates.TemplateResponse("study.html", {
            "request": request,
            "title": "Biblical Hebrew Study",
            "error": str(e),
            "verse_reference": f"{book} {chapter}:{verse}"
        })

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