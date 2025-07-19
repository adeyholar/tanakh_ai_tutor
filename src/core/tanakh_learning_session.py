# src/core/tanakh_learning_session.py
"""
Tanakh Learning Session Manager - Week 3 Day 2
Object-Oriented Hebrew Bible Learning System
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import logging

# Import our new OOP analyzers
from src.core.hebrew_analyzers import HebrewAnalyzer, AlephBertAnalyzer, OllamaAnalyzer, AnalysisResult

@dataclass
class WordLearning:
    """Tracks learning progress for a specific Hebrew word"""
    word: str
    first_seen: datetime
    times_studied: int
    confidence_level: float
    translations_learned: List[str]
    last_studied: datetime
    mastery_level: str  # "beginner", "intermediate", "advanced", "mastered"

@dataclass
class VerseStudy:
    """Represents a complete verse study session"""
    book: str
    chapter: int
    verse: int
    hebrew_text: List[str]
    analysis_results: List[AnalysisResult]
    study_time: datetime
    words_learned: List[str]
    session_notes: str

class TanakhLearningSession:
    """Professional Hebrew Bible learning session manager"""
    
    def __init__(self, data_path: str = "data/tanakh/hebrew_bible_with_nikkud.json"):
        self.data_path = Path(data_path)
        self.progress_path = Path("data/progress/learning_progress.json")
        self.tanakh_data: Dict[str, Any] = {}
        self.vocabulary: Dict[str, WordLearning] = {}
        self.study_history: List[VerseStudy] = []
        
        # Initialize analyzers
        self.alephbert = AlephBertAnalyzer()
        self.ollama = OllamaAnalyzer()
        self.available_analyzers: List[HebrewAnalyzer] = []
        
        # Session statistics
        self.session_start = datetime.now()
        self.words_studied_today = 0
        self.verses_studied_today = 0
        
        # Setup logging
        self.logger = logging.getLogger("TanakhLearning")
        
    async def initialize(self) -> bool:
        """Initialize the learning session"""
        try:
            self.logger.info("🚀 Initializing Tanakh Learning Session...")
            
            # Load Tanakh data
            if not await self._load_tanakh_data():
                return False
            
            # Initialize AI analyzers
            await self._initialize_analyzers()
            
            # Load user progress
            await self._load_progress()
            
            self.logger.info("✅ Tanakh Learning Session ready!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize learning session: {e}")
            return False
    
    async def _load_tanakh_data(self) -> bool:
        """Load the complete Hebrew Bible data"""
        try:
            if not self.data_path.exists():
                self.logger.error(f"Tanakh data file not found: {self.data_path}")
                return False
            
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.tanakh_data = json.load(f)
            
            book_count = len(self.tanakh_data)
            self.logger.info(f"📚 Loaded {book_count} books of the Hebrew Bible")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load Tanakh data: {e}")
            return False
    
    async def _initialize_analyzers(self):
        """Initialize available AI analyzers"""
        self.logger.info("🤖 Initializing AI analyzers...")
        
        # Try AlephBERT
        if self.alephbert.initialize():
            self.available_analyzers.append(self.alephbert)
            self.logger.info("✅ AlephBERT ready for Biblical Hebrew analysis")
        else:
            self.logger.warning("⚠️ AlephBERT not available")
        
        # Try Ollama (but don't fail if it's not working)
        try:
            if self.ollama.initialize():
                self.available_analyzers.append(self.ollama)
                self.logger.info("✅ Ollama ready for educational explanations")
            else:
                self.logger.warning("⚠️ Ollama not available")
        except Exception as e:
            self.logger.warning(f"⚠️ Ollama initialization failed: {e}")
        
        self.logger.info(f"🎯 {len(self.available_analyzers)} analyzers available")
    
    async def _load_progress(self):
        """Load user learning progress"""
        try:
            if self.progress_path.exists():
                with open(self.progress_path, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
                
                # Load vocabulary progress
                for word, data in progress_data.get('vocabulary', {}).items():
                    self.vocabulary[word] = WordLearning(
                        word=data['word'],
                        first_seen=datetime.fromisoformat(data['first_seen']),
                        times_studied=data['times_studied'],
                        confidence_level=data['confidence_level'],
                        translations_learned=data['translations_learned'],
                        last_studied=datetime.fromisoformat(data['last_studied']),
                        mastery_level=data['mastery_level']
                    )
                
                self.logger.info(f"📖 Loaded progress for {len(self.vocabulary)} words")
            else:
                self.logger.info("📝 Starting fresh learning journey")
                
        except Exception as e:
            self.logger.warning(f"Could not load progress: {e}")
    
    async def study_verse(self, book: str, chapter: int, verse: int) -> Optional[VerseStudy]:
        """Study a specific verse with AI analysis"""
        try:
            self.logger.info(f"📖 Studying {book} {chapter}:{verse}")
            
            # Get verse data
            verse_data = self._get_verse_data(book, chapter, verse)
            if not verse_data:
                return None
            
            hebrew_words = verse_data.get('text', [])
            if not hebrew_words:
                self.logger.warning("No Hebrew text found for this verse")
                return None
            
            # Analyze each word
            analysis_results = []
            words_learned = []
            
            for word in hebrew_words:
                # Clean the word (remove punctuation for analysis)
                clean_word = self._clean_hebrew_word(word)
                if not clean_word:
                    continue
                
                # Get analysis from available analyzers
                word_analysis = await self._analyze_word_with_available_models(clean_word)
                if word_analysis:
                    analysis_results.extend(word_analysis)
                    words_learned.append(clean_word)
                    
                    # Update vocabulary tracking
                    await self._update_word_learning(clean_word, word_analysis[0])
            
            # Create verse study record
            verse_study = VerseStudy(
                book=book,
                chapter=chapter,
                verse=verse,
                hebrew_text=hebrew_words,
                analysis_results=analysis_results,
                study_time=datetime.now(),
                words_learned=words_learned,
                session_notes=f"Studied {len(words_learned)} words"
            )
            
            self.study_history.append(verse_study)
            self.verses_studied_today += 1
            self.words_studied_today += len(words_learned)
            
            self.logger.info(f"✅ Completed study of {book} {chapter}:{verse}")
            return verse_study
            
        except Exception as e:
            self.logger.error(f"Error studying verse: {e}")
            return None
    
    def _get_verse_data(self, book: str, chapter: int, verse: int) -> Optional[Dict]:
        """Get specific verse data from Tanakh"""
        try:
            book_data = self.tanakh_data.get(book)
            if not book_data:
                available_books = list(self.tanakh_data.keys())[:5]  # Show first 5
                self.logger.error(f"Book '{book}' not found. Available: {available_books}...")
                return None
            
            # Handle the actual data structure: book_data is an array of chapters
            if not isinstance(book_data, list):
                self.logger.error(f"Unexpected book data structure for {book}")
                return None
                
            if chapter > len(book_data) or chapter < 1:
                self.logger.error(f"Chapter {chapter} not found in {book} (has {len(book_data)} chapters)")
                return None
            
            chapter_data = book_data[chapter - 1]  # Arrays are 0-indexed
            if not isinstance(chapter_data, list):
                self.logger.error(f"Unexpected chapter data structure")
                return None
                
            if verse > len(chapter_data) or verse < 1:
                self.logger.error(f"Verse {verse} not found in {book} {chapter} (has {len(chapter_data)} verses)")
                return None
            
            verse_data = chapter_data[verse - 1]  # Arrays are 0-indexed
            if not isinstance(verse_data, list):
                self.logger.error(f"Unexpected verse data structure")
                return None
            
            # Return in the expected format
            return {
                "text": verse_data,
                "book": book,
                "chapter": chapter, 
                "verse": verse
            }
            
        except Exception as e:
            self.logger.error(f"Error getting verse data: {e}")
            return None
    
    def _clean_hebrew_word(self, word: str) -> str:
        """Clean Hebrew word for analysis"""
        # Remove common punctuation but keep Hebrew text and nikkud
        import re
        # Keep Hebrew letters, nikkud (diacritics), and basic punctuation
        cleaned = re.sub(r'[^\u0590-\u05FF\u0600-\u06FF]', '', word)
        return cleaned.strip()
    
    async def _analyze_word_with_available_models(self, word: str) -> List[AnalysisResult]:
        """Analyze word with all available models"""
        results = []
        
        for analyzer in self.available_analyzers:
            try:
                result = await analyzer.analyze_word(word)
                results.append(result)
            except Exception as e:
                self.logger.warning(f"Analysis failed with {analyzer.name}: {e}")
        
        return results
    
    async def _update_word_learning(self, word: str, analysis: AnalysisResult):
        """Update learning progress for a word"""
        now = datetime.now()
        
        if word in self.vocabulary:
            # Update existing word
            word_learning = self.vocabulary[word]
            word_learning.times_studied += 1
            word_learning.last_studied = now
            word_learning.confidence_level = min(1.0, word_learning.confidence_level + 0.1)
            
            # Update mastery level
            if word_learning.times_studied >= 10:
                word_learning.mastery_level = "mastered"
            elif word_learning.times_studied >= 5:
                word_learning.mastery_level = "advanced"
            elif word_learning.times_studied >= 3:
                word_learning.mastery_level = "intermediate"
        else:
            # New word
            self.vocabulary[word] = WordLearning(
                word=word,
                first_seen=now,
                times_studied=1,
                confidence_level=0.2,
                translations_learned=[analysis.translation],
                last_studied=now,
                mastery_level="beginner"
            )
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics"""
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "verses_studied_today": self.verses_studied_today,
            "words_studied_today": self.words_studied_today,
            "total_vocabulary": len(self.vocabulary),
            "available_analyzers": [a.name for a in self.available_analyzers],
            "mastery_distribution": self._get_mastery_distribution()
        }
    
    def _get_mastery_distribution(self) -> Dict[str, int]:
        """Get distribution of word mastery levels"""
        distribution = {"beginner": 0, "intermediate": 0, "advanced": 0, "mastered": 0}
        for word_learning in self.vocabulary.values():
            distribution[word_learning.mastery_level] += 1
        return distribution
    
    async def save_progress(self):
        """Save learning progress to file"""
        try:
            # Ensure progress directory exists
            self.progress_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert vocabulary to serializable format
            vocabulary_data = {}
            for word, learning in self.vocabulary.items():
                vocabulary_data[word] = {
                    "word": learning.word,
                    "first_seen": learning.first_seen.isoformat(),
                    "times_studied": learning.times_studied,
                    "confidence_level": learning.confidence_level,
                    "translations_learned": learning.translations_learned,
                    "last_studied": learning.last_studied.isoformat(),
                    "mastery_level": learning.mastery_level
                }
            
            progress_data = {
                "vocabulary": vocabulary_data,
                "last_saved": datetime.now().isoformat(),
                "session_stats": self.get_session_stats()
            }
            
            with open(self.progress_path, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"💾 Progress saved: {len(self.vocabulary)} words")
            
        except Exception as e:
            self.logger.error(f"Failed to save progress: {e}")


# Demo function to test the system
async def demo_learning_session():
    """Demonstrate the Tanakh learning system"""
    print("🎓 Starting Tanakh Learning Session Demo...")
    
    # Create and initialize session
    session = TanakhLearningSession()
    if not await session.initialize():
        print("❌ Failed to initialize session")
        return
    
    # Study Genesis 1:1
    print("\n📖 Studying Genesis 1:1...")
    verse_study = await session.study_verse("Gen", 1, 1)
    
    if verse_study:
        print(f"✅ Studied verse with {len(verse_study.words_learned)} words")
        print(f"📊 Analysis results: {len(verse_study.analysis_results)}")
        
        # Show some results
        for i, result in enumerate(verse_study.analysis_results[:3]):  # First 3 words
            print(f"  Word {i+1}: {result.word} -> {result.model_used}")
    
    # Show session statistics
    print("\n📊 Session Statistics:")
    stats = session.get_session_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Save progress
    await session.save_progress()
    print("\n💾 Progress saved!")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_learning_session())