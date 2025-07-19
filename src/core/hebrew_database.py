# src/core/hebrew_database.py
"""
Hebrew AI Database System - Week 3 Day 4
Professional SQLite database for user progress, vocabulary, and learning analytics
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
import asyncio

@dataclass
class UserProfile:
    """User profile information"""
    user_id: str
    username: str
    email: str
    learning_level: str  # beginner, intermediate, advanced
    preferred_translation: str  # JPS, ESV, NIV, etc.
    study_goals: List[str]
    created_date: datetime
    last_active: datetime
    total_study_time: int  # minutes
    
@dataclass
class VocabularyEntry:
    """Individual vocabulary word tracking"""
    word_id: str
    user_id: str
    hebrew_word: str
    translation: str
    root: str
    part_of_speech: str
    first_encountered: datetime
    times_studied: int
    times_correct: int
    times_incorrect: int
    mastery_level: float  # 0.0 to 1.0
    last_studied: datetime
    next_review: datetime
    tags: List[str]
    
@dataclass
class StudySession:
    """Study session tracking"""
    session_id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime]
    session_type: str  # verse_study, vocabulary_review, quiz
    content_studied: str  # book:chapter:verse or topic
    words_learned: int
    words_reviewed: int
    accuracy_rate: float
    notes: str

@dataclass
class LearningAnalytics:
    """Learning analytics and insights"""
    user_id: str
    date: datetime
    total_vocabulary: int
    mastered_words: int
    words_in_progress: int
    average_session_length: float
    study_streak: int
    weekly_goal_progress: float
    strengths: List[str]
    areas_for_improvement: List[str]

class HebrewDatabaseManager:
    """Professional database manager for Hebrew AI learning system"""
    
    def __init__(self, db_path: str = "data/hebrew_learning.db"):
        self.db_path = Path(db_path)
        self.logger = logging.getLogger("HebrewDB")
        self.connection: Optional[sqlite3.Connection] = None
        
    async def initialize_database(self) -> bool:
        """Initialize database with all required tables"""
        try:
            # Ensure directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Connect to database
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            
            # Create all tables
            await self._create_tables()
            
            self.logger.info(f"✅ Hebrew database initialized: {self.db_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize database: {e}")
            return False
    
    async def _create_tables(self):
        """Create all database tables"""
        
        # Users table
        await self._execute_sql("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            learning_level TEXT DEFAULT 'beginner',
            preferred_translation TEXT DEFAULT 'JPS',
            study_goals TEXT,  -- JSON array
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_study_time INTEGER DEFAULT 0,
            settings TEXT  -- JSON for user preferences
        )
        """)
        
        # Vocabulary table
        await self._execute_sql("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            word_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            hebrew_word TEXT NOT NULL,
            translation TEXT NOT NULL,
            root TEXT,
            part_of_speech TEXT,
            first_encountered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            times_studied INTEGER DEFAULT 0,
            times_correct INTEGER DEFAULT 0,
            times_incorrect INTEGER DEFAULT 0,
            mastery_level REAL DEFAULT 0.0,
            last_studied TIMESTAMP,
            next_review TIMESTAMP,
            tags TEXT,  -- JSON array
            analysis_data TEXT,  -- JSON for full analysis
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        # Study sessions table
        await self._execute_sql("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            session_type TEXT NOT NULL,
            content_studied TEXT,
            words_learned INTEGER DEFAULT 0,
            words_reviewed INTEGER DEFAULT 0,
            accuracy_rate REAL DEFAULT 0.0,
            notes TEXT,
            session_data TEXT,  -- JSON for detailed session info
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        # Learning analytics table
        await self._execute_sql("""
        CREATE TABLE IF NOT EXISTS learning_analytics (
            analytics_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            total_vocabulary INTEGER DEFAULT 0,
            mastered_words INTEGER DEFAULT 0,
            words_in_progress INTEGER DEFAULT 0,
            average_session_length REAL DEFAULT 0.0,
            study_streak INTEGER DEFAULT 0,
            weekly_goal_progress REAL DEFAULT 0.0,
            strengths TEXT,  -- JSON array
            areas_for_improvement TEXT,  -- JSON array
            analytics_data TEXT,  -- JSON for additional metrics
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        # Verse study tracking
        await self._execute_sql("""
        CREATE TABLE IF NOT EXISTS verse_studies (
            study_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            book TEXT NOT NULL,
            chapter INTEGER NOT NULL,
            verse INTEGER NOT NULL,
            study_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            time_spent INTEGER,  -- seconds
            words_analyzed INTEGER,
            comprehension_score REAL,
            notes TEXT,
            analysis_results TEXT,  -- JSON
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        # Create indexes for performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_vocabulary_user_id ON vocabulary(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_vocabulary_hebrew_word ON vocabulary(hebrew_word)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON study_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_date ON study_sessions(start_time)",
            "CREATE INDEX IF NOT EXISTS idx_verse_studies_user_id ON verse_studies(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_verse_studies_reference ON verse_studies(book, chapter, verse)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
        
        self.logger.info("✅ All database tables and indexes created")
    
    async def _execute_sql(self, sql: str, params: tuple = ()):
        """Execute SQL with error handling"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            self.connection.commit()
            return cursor
        except Exception as e:
            self.logger.error(f"SQL execution failed: {sql[:50]}... Error: {e}")
            raise
    
    async def create_user(self, user_profile: UserProfile) -> bool:
        """Create a new user profile"""
        try:
            sql = """
            INSERT INTO users (user_id, username, email, learning_level, 
                             preferred_translation, study_goals, created_date, 
                             last_active, total_study_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            await self._execute_sql(sql, (
                user_profile.user_id,
                user_profile.username,
                user_profile.email,
                user_profile.learning_level,
                user_profile.preferred_translation,
                json.dumps(user_profile.study_goals),
                user_profile.created_date.isoformat(),
                user_profile.last_active.isoformat(),
                user_profile.total_study_time
            ))
            
            self.logger.info(f"✅ Created user: {user_profile.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create user: {e}")
            return False
    
    async def add_vocabulary_word(self, vocab_entry: VocabularyEntry) -> bool:
        """Add a new vocabulary word to user's collection"""
        try:
            sql = """
            INSERT OR REPLACE INTO vocabulary 
            (word_id, user_id, hebrew_word, translation, root, part_of_speech,
             first_encountered, times_studied, times_correct, times_incorrect,
             mastery_level, last_studied, next_review, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            next_review = vocab_entry.next_review.isoformat() if vocab_entry.next_review else None
            last_studied = vocab_entry.last_studied.isoformat() if vocab_entry.last_studied else None
            
            await self._execute_sql(sql, (
                vocab_entry.word_id,
                vocab_entry.user_id,
                vocab_entry.hebrew_word,
                vocab_entry.translation,
                vocab_entry.root,
                vocab_entry.part_of_speech,
                vocab_entry.first_encountered.isoformat(),
                vocab_entry.times_studied,
                vocab_entry.times_correct,
                vocab_entry.times_incorrect,
                vocab_entry.mastery_level,
                last_studied,
                next_review,
                json.dumps(vocab_entry.tags)
            ))
            
            self.logger.debug(f"✅ Added vocabulary: {vocab_entry.hebrew_word}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to add vocabulary: {e}")
            return False
    
    async def start_study_session(self, user_id: str, session_type: str, content: str) -> str:
        """Start a new study session"""
        try:
            session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            sql = """
            INSERT INTO study_sessions (session_id, user_id, session_type, content_studied)
            VALUES (?, ?, ?, ?)
            """
            
            await self._execute_sql(sql, (session_id, user_id, session_type, content))
            
            self.logger.info(f"✅ Started session: {session_id}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start session: {e}")
            return ""
    
    async def end_study_session(self, session_id: str, words_learned: int = 0, 
                               words_reviewed: int = 0, accuracy: float = 0.0, 
                               notes: str = "") -> bool:
        """End a study session with results"""
        try:
            sql = """
            UPDATE study_sessions 
            SET end_time = CURRENT_TIMESTAMP, words_learned = ?, 
                words_reviewed = ?, accuracy_rate = ?, notes = ?
            WHERE session_id = ?
            """
            
            await self._execute_sql(sql, (words_learned, words_reviewed, accuracy, notes, session_id))
            
            self.logger.info(f"✅ Ended session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to end session: {e}")
            return False
    
    async def get_user_vocabulary(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user's vocabulary with progress information"""
        try:
            sql = """
            SELECT * FROM vocabulary 
            WHERE user_id = ? 
            ORDER BY last_studied DESC, mastery_level ASC
            LIMIT ?
            """
            
            cursor = await self._execute_sql(sql, (user_id, limit))
            rows = cursor.fetchall()
            
            vocabulary = []
            for row in rows:
                vocab_dict = dict(row)
                # Parse JSON fields
                vocab_dict['tags'] = json.loads(vocab_dict['tags']) if vocab_dict['tags'] else []
                vocabulary.append(vocab_dict)
            
            self.logger.debug(f"Retrieved {len(vocabulary)} vocabulary words for {user_id}")
            return vocabulary
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get vocabulary: {e}")
            return []
    
    async def get_learning_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive learning analytics"""
        try:
            # Get basic stats
            vocab_stats = await self._get_vocabulary_stats(user_id)
            session_stats = await self._get_session_stats(user_id, days)
            progress_stats = await self._get_progress_stats(user_id, days)
            
            analytics = {
                'user_id': user_id,
                'report_date': datetime.now().isoformat(),
                'vocabulary_stats': vocab_stats,
                'session_stats': session_stats,
                'progress_stats': progress_stats,
                'recommendations': await self._generate_recommendations(user_id, vocab_stats, session_stats)
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate analytics: {e}")
            return {}
    
    async def _get_vocabulary_stats(self, user_id: str) -> Dict[str, Any]:
        """Get vocabulary statistics"""
        sql = """
        SELECT 
            COUNT(*) as total_words,
            COUNT(CASE WHEN mastery_level >= 0.8 THEN 1 END) as mastered_words,
            COUNT(CASE WHEN mastery_level BETWEEN 0.3 AND 0.79 THEN 1 END) as learning_words,
            COUNT(CASE WHEN mastery_level < 0.3 THEN 1 END) as beginner_words,
            AVG(mastery_level) as average_mastery,
            SUM(times_studied) as total_reviews
        FROM vocabulary WHERE user_id = ?
        """
        
        cursor = await self._execute_sql(sql, (user_id,))
        row = cursor.fetchone()
        
        return dict(row) if row else {}
    
    async def _get_session_stats(self, user_id: str, days: int) -> Dict[str, Any]:
        """Get study session statistics"""
        sql = """
        SELECT 
            COUNT(*) as total_sessions,
            AVG(words_learned) as avg_words_per_session,
            AVG(accuracy_rate) as average_accuracy,
            SUM(words_learned) as total_words_learned,
            COUNT(DISTINCT DATE(start_time)) as study_days
        FROM study_sessions 
        WHERE user_id = ? AND start_time >= datetime('now', '-{} days')
        """.format(days)
        
        cursor = await self._execute_sql(sql, (user_id,))
        row = cursor.fetchone()
        
        return dict(row) if row else {}
    
    async def _get_progress_stats(self, user_id: str, days: int) -> Dict[str, Any]:
        """Get learning progress statistics"""
        # Calculate study streak
        sql = """
        SELECT DATE(start_time) as study_date
        FROM study_sessions 
        WHERE user_id = ? 
        ORDER BY start_time DESC
        """
        
        cursor = await self._execute_sql(sql, (user_id,))
        dates = [row[0] for row in cursor.fetchall()]
        
        study_streak = self._calculate_study_streak(dates)
        
        return {
            'study_streak': study_streak,
            'last_study_date': dates[0] if dates else None,
            'consistency_score': min(1.0, len(set(dates)) / days) if days > 0 else 0.0
        }
    
    def _calculate_study_streak(self, study_dates: List[str]) -> int:
        """Calculate consecutive study days"""
        if not study_dates:
            return 0
        
        streak = 1
        current_date = datetime.strptime(study_dates[0], '%Y-%m-%d').date()
        
        for date_str in study_dates[1:]:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if (current_date - date).days == 1:
                streak += 1
                current_date = date
            else:
                break
        
        return streak
    
    async def _generate_recommendations(self, user_id: str, vocab_stats: Dict, 
                                      session_stats: Dict) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        # Vocabulary-based recommendations
        if vocab_stats.get('total_words', 0) < 50:
            recommendations.append("Focus on building core vocabulary - aim for 5-10 new words per session")
        
        if vocab_stats.get('average_mastery', 0) < 0.5:
            recommendations.append("Review existing vocabulary more frequently to improve retention")
        
        # Session-based recommendations
        if session_stats.get('average_accuracy', 0) < 0.7:
            recommendations.append("Spend more time on each word to improve comprehension")
        
        if session_stats.get('study_days', 0) < 5:
            recommendations.append("Try to study more consistently - daily practice yields better results")
        
        # Default recommendations
        if not recommendations:
            recommendations.append("Great progress! Continue your current study pattern")
            recommendations.append("Consider exploring more challenging biblical texts")
        
        return recommendations
    
    async def backup_database(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of the database"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f"data/backups/hebrew_learning_backup_{timestamp}.db"
            
            backup_path = Path(backup_path)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Simple file copy for SQLite
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            self.logger.info(f"✅ Database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to backup database: {e}")
            return False
    
    async def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

# Demo function
async def demo_database_system():
    """Demonstrate the Hebrew database system"""
    print("🎓 Hebrew Database System Demo - Week 3 Day 4")
    print("=" * 50)
    
    # Initialize database
    db = HebrewDatabaseManager("data/demo_hebrew_learning.db")
    if not await db.initialize_database():
        print("❌ Failed to initialize database")
        return
    
    # Create a demo user
    user = UserProfile(
        user_id="demo_user_001",
        username="HebrewLearner",
        email="learner@example.com",
        learning_level="beginner",
        preferred_translation="JPS",
        study_goals=["Master Genesis 1", "Learn 500 vocabulary words"],
        created_date=datetime.now(),
        last_active=datetime.now(),
        total_study_time=120  # 2 hours
    )
    
    success = await db.create_user(user)
    print(f"{'✅' if success else '❌'} User creation: {user.username}")
    
    # Add vocabulary words
    vocab_words = [
        VocabularyEntry(
            word_id="word_001",
            user_id="demo_user_001",
            hebrew_word="בְּרֵאשִׁ֖ית",
            translation="in the beginning",
            root="ראש",
            part_of_speech="prepositional phrase",
            first_encountered=datetime.now(),
            times_studied=3,
            times_correct=2,
            times_incorrect=1,
            mastery_level=0.6,
            last_studied=datetime.now(),
            next_review=datetime.now() + timedelta(days=1),
            tags=["Genesis", "creation", "temporal"]
        ),
        VocabularyEntry(
            word_id="word_002",
            user_id="demo_user_001",
            hebrew_word="אֱלֹהִ֑ים",
            translation="God",
            root="אלה",
            part_of_speech="noun",
            first_encountered=datetime.now(),
            times_studied=5,
            times_correct=5,
            times_incorrect=0,
            mastery_level=0.9,
            last_studied=datetime.now(),
            next_review=datetime.now() + timedelta(days=3),
            tags=["Genesis", "deity", "theological"]
        )
    ]
    
    for vocab in vocab_words:
        success = await db.add_vocabulary_word(vocab)
        print(f"{'✅' if success else '❌'} Added vocabulary: {vocab.hebrew_word}")
    
    # Start and end a study session
    session_id = await db.start_study_session("demo_user_001", "verse_study", "Genesis 1:1")
    print(f"✅ Started session: {session_id}")
    
    # Simulate study time
    await asyncio.sleep(1)
    
    success = await db.end_study_session(session_id, words_learned=2, words_reviewed=0, accuracy=0.8)
    print(f"{'✅' if success else '❌'} Ended session")
    
    # Get user vocabulary
    vocabulary = await db.get_user_vocabulary("demo_user_001")
    print(f"📖 Retrieved {len(vocabulary)} vocabulary words")
    
    # Generate analytics
    analytics = await db.get_learning_analytics("demo_user_001")
    print(f"📊 Generated analytics for user")
    print(f"   Total vocabulary: {analytics.get('vocabulary_stats', {}).get('total_words', 0)}")
    print(f"   Mastered words: {analytics.get('vocabulary_stats', {}).get('mastered_words', 0)}")
    print(f"   Study sessions: {analytics.get('session_stats', {}).get('total_sessions', 0)}")
    
    # Show recommendations
    recommendations = analytics.get('recommendations', [])
    if recommendations:
        print("💡 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    # Backup database
    success = await db.backup_database()
    print(f"{'✅' if success else '❌'} Database backup")
    
    # Close connection
    await db.close_connection()
    print("✅ Database demo complete!")

if __name__ == "__main__":
    asyncio.run(demo_database_system())
