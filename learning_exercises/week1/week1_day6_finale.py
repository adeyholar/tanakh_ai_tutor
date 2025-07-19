#!/usr/bin/env python3
"""
WEEK 1 DAY 6: COMPLETE HEBREW LEARNING MODULE - GRAND FINALE
Combining ALL Week 1 skills into a complete Hebrew learning system
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class CompleteHebrewLearningModule:
    """
    Week 1 Grand Finale: Complete Hebrew Learning System
    Integrates: Variables, Lists, Dictionaries, Functions, File I/O, and AI
    """
    
    def __init__(self):
        print("🔥 INITIALIZING COMPLETE HEBREW LEARNING MODULE")
        print("=" * 60)
        
        # Core components (Week 1 skills)
        self.tanakh_data = self.load_tanakh_database()
        self.user_progress = self.initialize_user_progress()
        self.ai_processor = self.setup_ai_processor()
        self.session_stats = {
            'words_learned': 0,
            'verses_studied': 0,
            'ai_queries': 0,
            'session_start': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print("✅ Hebrew Learning Module initialized successfully!")
        print(f"📚 Loaded {len(self.tanakh_data)} books from Tanakh")
        print(f"🤖 AI processor ready with Llama 3 8B")
    
    def load_tanakh_database(self) -> Dict:
        """Load your complete Hebrew Bible database"""
        tanakh_path = "data/tanakh/hebrew_bible_with_nikkud.json"
        
        try:
            with open(tanakh_path, 'r', encoding='utf-8') as f:
                tanakh = json.load(f)
            
            print(f"📖 Loaded {len(tanakh)} books from Hebrew Bible")
            return tanakh
        
        except FileNotFoundError:
            print(f"❌ Tanakh file not found at {tanakh_path}")
            return {}
        except Exception as e:
            print(f"❌ Error loading Tanakh: {e}")
            return {}
    
    def initialize_user_progress(self) -> Dict:
        """Initialize or load user learning progress"""
        progress_file = "data/progress/user_progress.json"
        
        # Create progress directory if needed
        os.makedirs("data/progress", exist_ok=True)
        
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
            print("📈 Loaded existing user progress")
        except FileNotFoundError:
            # Create new progress file
            progress = {
                'level': 'beginner',
                'words_mastered': [],
                'verses_completed': [],
                'total_study_time': 0,
                'achievements': [],
                'current_book': 'Genesis',
                'current_chapter': 1,
                'current_verse': 1
            }
            print("🆕 Created new user progress file")
        
        return progress
    
    def setup_ai_processor(self) -> Dict:
        """Setup AI processing configuration"""
        return {
            'url': "http://localhost:11434/api/generate",
            'model': "llama3:8b",
            'available': self.test_ai_connection()
        }
    
    def test_ai_connection(self) -> bool:
        """Test connection to your local AI"""
        try:
            response = requests.post("http://localhost:11434/api/generate", 
                json={
                    "model": "llama3:8b",
                    "prompt": "Hello",
                    "stream": False
                }, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    # =================================================================
    # COMPLETE LEARNING EXPERIENCE METHODS
    # =================================================================
    
    def start_interactive_learning_session(self):
        """
        Main learning interface - combines all Week 1 skills
        """
        print(f"\n🎓 STARTING INTERACTIVE HEBREW LEARNING SESSION")
        print("=" * 50)
        
        while True:
            print(f"\n📚 HEBREW LEARNING MENU:")
            print(f"1. 📖 Study a specific verse")
            print(f"2. 🔍 Analyze Hebrew words")
            print(f"3. 📊 View learning progress")
            print(f"4. 🎯 Take a quiz")
            print(f"5. 🗣️ Practice pronunciation")
            print(f"6. 💾 Save and exit")
            
            choice = input(f"\nChoose an option (1-6): ").strip()
            
            if choice == '1':
                self.study_verse_interactive()
            elif choice == '2':
                self.analyze_words_interactive()
            elif choice == '3':
                self.show_progress_report()
            elif choice == '4':
                self.take_hebrew_quiz()
            elif choice == '5':
                self.practice_pronunciation()
            elif choice == '6':
                self.save_progress_and_exit()
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def study_verse_interactive(self):
        """Interactive verse study session"""
        print(f"\n📖 INTERACTIVE VERSE STUDY")
        print("-" * 30)
        
        # Show available books
        books = list(self.tanakh_data.keys())[:10]  # First 10 books
        print(f"Available books: {', '.join(books)}")
        
        book = input(f"Enter book name (or press Enter for {self.user_progress['current_book']}): ").strip()
        if not book:
            book = self.user_progress['current_book']
        
        # Find book in your data
        matching_books = [b for b in self.tanakh_data.keys() if book.lower() in b.lower()]
        
        if not matching_books:
            print(f"❌ Book '{book}' not found")
            return
        
        selected_book = matching_books[0]
        
        try:
            chapter = int(input(f"Enter chapter (1-{len(self.tanakh_data[selected_book])}): ") or 1)
            verse = int(input(f"Enter verse (1-{len(self.tanakh_data[selected_book][chapter-1])}): ") or 1)
            
            # Get the verse
            hebrew_verse = self.tanakh_data[selected_book][chapter-1][verse-1]
            
            print(f"\n📜 {selected_book} {chapter}:{verse}")
            print(f"Hebrew: {' '.join(hebrew_verse)}")
            
            # AI Analysis
            if self.ai_processor['available']:
                print(f"\n🤖 AI ANALYSIS:")
                analysis = self.get_ai_verse_analysis(hebrew_verse, f"{selected_book} {chapter}:{verse}")
                print(analysis)
                self.session_stats['ai_queries'] += 1
            
            # Update progress
            verse_id = f"{selected_book}_{chapter}_{verse}"
            if verse_id not in self.user_progress['verses_completed']:
                self.user_progress['verses_completed'].append(verse_id)
                self.session_stats['verses_studied'] += 1
                print(f"\n✅ Verse added to your completed studies!")
        
        except (ValueError, IndexError) as e:
            print(f"❌ Invalid chapter/verse number: {e}")
    
    def analyze_words_interactive(self):
        """Interactive word analysis session"""
        print(f"\n🔍 INTERACTIVE WORD ANALYSIS")
        print("-" * 30)
        
        while True:
            hebrew_word = input(f"Enter Hebrew word to analyze (or 'back' to return): ").strip()
            
            if hebrew_word.lower() == 'back':
                break
            
            if not hebrew_word:
                print("❌ Please enter a Hebrew word")
                continue
            
            # Analyze with AI
            if self.ai_processor['available']:
                analysis = self.get_ai_word_analysis(hebrew_word)
                print(f"\n📝 Analysis of '{hebrew_word}':")
                print(analysis)
                
                # Add to mastered words
                if hebrew_word not in self.user_progress['words_mastered']:
                    self.user_progress['words_mastered'].append(hebrew_word)
                    self.session_stats['words_learned'] += 1
                    print(f"\n✅ '{hebrew_word}' added to your vocabulary!")
                
                self.session_stats['ai_queries'] += 1
            else:
                print("❌ AI not available for analysis")
    
    def show_progress_report(self):
        """Display comprehensive learning progress"""
        print(f"\n📊 YOUR HEBREW LEARNING PROGRESS")
        print("=" * 40)
        
        print(f"🎯 Level: {self.user_progress['level'].title()}")
        print(f"📚 Words Mastered: {len(self.user_progress['words_mastered'])}")
        print(f"📖 Verses Completed: {len(self.user_progress['verses_completed'])}")
        print(f"🏆 Achievements: {len(self.user_progress['achievements'])}")
        
        print(f"\n📈 Current Session Stats:")
        print(f"  • Words learned: {self.session_stats['words_learned']}")
        print(f"  • Verses studied: {self.session_stats['verses_studied']}")
        print(f"  • AI queries: {self.session_stats['ai_queries']}")
        print(f"  • Session started: {self.session_stats['session_start']}")
        
        # Recent words
        if self.user_progress['words_mastered']:
            recent_words = self.user_progress['words_mastered'][-5:]
            print(f"\n🔤 Recently Mastered Words:")
            for word in recent_words:
                print(f"  • {word}")
    
    def take_hebrew_quiz(self):
        """Interactive Hebrew quiz using your Tanakh data"""
        print(f"\n🎯 HEBREW VOCABULARY QUIZ")
        print("-" * 25)
        
        if len(self.user_progress['words_mastered']) < 3:
            print("❌ You need to study at least 3 words before taking a quiz")
            return
        
        import random
        
        # Create quiz from mastered words
        quiz_words = random.sample(self.user_progress['words_mastered'], min(3, len(self.user_progress['words_mastered'])))
        score = 0
        
        for i, word in enumerate(quiz_words, 1):
            print(f"\nQuestion {i}: What does '{word}' mean?")
            
            if self.ai_processor['available']:
                # Get AI answer for comparison
                analysis = self.get_ai_word_analysis(word)
                user_answer = input("Your answer: ").strip()
                
                print(f"🤖 AI Analysis: {analysis}")
                
                # Simple scoring (user gets point for attempting)
                if user_answer:
                    score += 1
                    print("✅ Good effort!")
        
        print(f"\n🏆 Quiz Complete! Score: {score}/{len(quiz_words)}")
        
        # Award achievement
        if score == len(quiz_words):
            achievement = f"Perfect Quiz Score - {datetime.now().strftime('%Y-%m-%d')}"
            if achievement not in self.user_progress['achievements']:
                self.user_progress['achievements'].append(achievement)
                print("🎉 Achievement Unlocked: Perfect Quiz Score!")
    
    def practice_pronunciation(self):
        """Pronunciation practice session"""
        print(f"\n🗣️ PRONUNCIATION PRACTICE")
        print("-" * 25)
        
        if not self.user_progress['words_mastered']:
            print("❌ Study some words first before practicing pronunciation")
            return
        
        import random
        word = random.choice(self.user_progress['words_mastered'])
        
        print(f"Practice pronouncing: {word}")
        
        if self.ai_processor['available']:
            pronunciation_guide = self.get_ai_pronunciation_guide(word)
            print(f"\n🔊 Pronunciation Guide:")
            print(pronunciation_guide)
        
        input(f"\nPress Enter when you've practiced the pronunciation...")
        print("✅ Great practice session!")
    
    def save_progress_and_exit(self):
        """Save all progress and exit gracefully"""
        print(f"\n💾 SAVING YOUR PROGRESS...")
        
        # Update total study time (simplified)
        session_duration = 5  # Assume 5 minutes per session
        self.user_progress['total_study_time'] += session_duration
        
        # Save progress file
        try:
            with open("data/progress/user_progress.json", 'w', encoding='utf-8') as f:
                json.dump(self.user_progress, f, ensure_ascii=False, indent=2)
            
            # Save session summary
            session_summary = {
                'session_date': self.session_stats['session_start'],
                'stats': self.session_stats,
                'progress_snapshot': self.user_progress.copy()
            }
            
            session_file = f"data/progress/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_summary, f, ensure_ascii=False, indent=2)
            
            print("✅ Progress saved successfully!")
            print(f"📊 Session Summary:")
            print(f"  • Words learned: {self.session_stats['words_learned']}")
            print(f"  • Verses studied: {self.session_stats['verses_studied']}")
            print(f"  • Total vocabulary: {len(self.user_progress['words_mastered'])} words")
            
        except Exception as e:
            print(f"❌ Error saving progress: {e}")
        
        print(f"\n🎉 Thank you for using the Hebrew Learning Module!")
        print(f"🚀 Keep building your Hebrew AI journey!")
    
    # =================================================================
    # AI INTEGRATION METHODS (Week 1 Day 5 Skills)
    # =================================================================
    
    def get_ai_verse_analysis(self, hebrew_words: List[str], reference: str) -> str:
        """Get AI analysis of Hebrew verse"""
        verse_text = " ".join(hebrew_words)
        prompt = f"""
        Analyze this Hebrew verse from {reference}: {verse_text}
        
        Provide:
        1. English translation
        2. Two key Hebrew words with meanings
        3. One interesting grammar point
        
        Keep it educational and encouraging for Hebrew learners.
        """
        
        return self.query_ai(prompt)
    
    def get_ai_word_analysis(self, word: str) -> str:
        """Get AI analysis of Hebrew word"""
        prompt = f"""
        Analyze the Hebrew word: {word}
        
        Provide: Meaning | Root | Pronunciation
        Format: [word] means [meaning]. Root: [root]. Pronounced: [pronunciation]
        """
        
        return self.query_ai(prompt)
    
    def get_ai_pronunciation_guide(self, word: str) -> str:
        """Get AI pronunciation guide"""
        prompt = f"""
        Create a pronunciation guide for Hebrew word: {word}
        
        Provide transliteration and simple pronunciation tips.
        """
        
        return self.query_ai(prompt)
    
    def query_ai(self, prompt: str) -> str:
        """Query your local Llama 3 8B AI"""
        try:
            response = requests.post(self.ai_processor['url'], 
                json={
                    "model": self.ai_processor['model'],
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": 300}
                }, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            else:
                return f"AI Error: {response.status_code}"
        
        except Exception as e:
            return f"AI Connection Error: {str(e)}"

# =================================================================
# WEEK 1 DEMONSTRATION AND TESTING
# =================================================================

def demonstrate_complete_system():
    """
    Demonstrate the complete Hebrew learning system
    Showcasing ALL Week 1 skills in action
    """
    print("🔥 WEEK 1 DAY 6: COMPLETE HEBREW LEARNING MODULE")
    print("Demonstrating ALL Week 1 skills in action!")
    print("=" * 60)
    
    # Initialize the complete system
    learning_module = CompleteHebrewLearningModule()
    
    if not learning_module.tanakh_data:
        print("❌ Cannot demonstrate without Tanakh data")
        return
    
    print(f"\n🎯 AUTOMATIC DEMONSTRATION MODE")
    print("(Showing what your system can do)")
    print("-" * 40)
    
    # Demo 1: Process a verse automatically
    print(f"\n📖 DEMO 1: Processing Genesis-like verse")
    first_book = list(learning_module.tanakh_data.keys())[0]
    first_verse = learning_module.tanakh_data[first_book][0][0]
    
    print(f"Hebrew: {' '.join(first_verse)}")
    
    if learning_module.ai_processor['available']:
        analysis = learning_module.get_ai_verse_analysis(first_verse, f"{first_book} 1:1")
        print(f"AI Analysis: {analysis}")
    
    # Demo 2: Word analysis
    print(f"\n🔍 DEMO 2: Analyzing Hebrew word")
    if first_verse:
        demo_word = first_verse[0]
        word_analysis = learning_module.get_ai_word_analysis(demo_word)
        print(f"Word: {demo_word}")
        print(f"Analysis: {word_analysis}")
    
    # Demo 3: Save progress
    print(f"\n💾 DEMO 3: Saving learning progress")
    learning_module.user_progress['words_mastered'].extend(first_verse[:2])
    learning_module.session_stats['words_learned'] = 2
    learning_module.session_stats['verses_studied'] = 1
    
    # Save demo progress
    os.makedirs("data/progress", exist_ok=True)
    with open("data/progress/demo_progress.json", 'w', encoding='utf-8') as f:
        json.dump({
            'demo_stats': learning_module.session_stats,
            'sample_progress': learning_module.user_progress
        }, f, ensure_ascii=False, indent=2)
    
    print("✅ Demo progress saved to data/progress/demo_progress.json")
    
    print(f"\n🎉 COMPLETE SYSTEM DEMONSTRATION FINISHED!")
    print(f"Your Hebrew AI learning module is fully operational!")

if __name__ == "__main__":
    print("🔥 WEEK 1 DAY 6: COMPLETE HEBREW LEARNING MODULE")
    print("The Grand Finale of Week 1 - ALL skills combined!")
    print("=" * 60)
    
    # Run automatic demonstration
    demonstrate_complete_system()
    
    print(f"\n" + "=" * 60)
    print(f"🏆 WEEK 1 COMPLETE - INCREDIBLE ACHIEVEMENT!")
    print(f"=" * 60)
    print(f"✅ SKILLS MASTERED:")
    print(f"  • Python fundamentals with Hebrew focus")
    print(f"  • File I/O operations for Hebrew texts")
    print(f"  • Data structures (lists, dictionaries)")
    print(f"  • Functions and code organization")
    print(f"  • Local AI integration (Llama 3 8B)")
    print(f"  • Real-world Hebrew text processing")
    print(f"  • Interactive learning systems")
    print(f"  • Progress tracking and data persistence")
    print(f"  • Professional project structure")
    print(f"  • Security-aware development")
    
    print(f"\n🚀 READY FOR WEEK 2!")
    print(f"Next: Advanced programming concepts and expanded Hebrew AI features!")
    print(f"You've built an incredible foundation! 🎓✨")
    print("=" * 60)
    
    # Offer to run interactive mode
    print(f"\n🎯 Want to try the interactive learning module?")
    choice = input("Type 'yes' to start interactive session (or Enter to finish): ").strip().lower()
    
    if choice == 'yes':
        learning_module = CompleteHebrewLearningModule()
        learning_module.start_interactive_learning_session()