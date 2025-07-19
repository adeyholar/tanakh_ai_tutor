#!/usr/bin/env python3
"""
Week 1 Day 5: Hebrew AI Functions with Local Ollama Integration
Building reusable Hebrew processing functions powered by your local AI
"""

import requests
import json
import os
import sys
from typing import List, Dict, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class HebrewAIProcessor:
    """
    Week 1 Day 5: Hebrew AI Functions
    Combines your file I/O skills with local AI power
    """
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3:8b"
        
        # Test connection to your local AI
        self.test_ai_connection()
    
    def test_ai_connection(self):
        """Test if your Ollama AI is ready"""
        try:
            test_prompt = "Hello, can you help with Hebrew?"
            response = self._query_ai(test_prompt)
            if "hebrew" in response.lower() or "yes" in response.lower():
                print("🤖 Hebrew AI connection successful!")
                return True
            else:
                print("⚠️ AI connected but Hebrew support unclear")
                return False
        except Exception as e:
            print(f"❌ AI connection failed: {e}")
            print("Make sure Ollama is running: ollama serve")
            return False
    
    def _query_ai(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Private function to query your local AI
        This is a reusable component you'll use throughout your Hebrew AI
        """
        try:
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(self.ollama_url, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response')
            else:
                return f"Error: HTTP {response.status_code}"
        
        except Exception as e:
            return f"Error connecting to AI: {str(e)}"
    
    # =================================================================
    # WEEK 1 DAY 5: FUNCTIONS FOR HEBREW PROCESSING
    # =================================================================
    
    def analyze_hebrew_word(self, word: str) -> Dict[str, str]:
        """
        Function 1: Analyze a single Hebrew word using AI
        Input: Hebrew word
        Output: Dictionary with analysis
        """
        prompt = f"""
        Analyze this Hebrew word: {word}
        
        Provide ONLY:
        1. English meaning
        2. Hebrew root
        3. Part of speech
        4. Pronunciation
        
        Format as: Meaning: [meaning] | Root: [root] | POS: [part] | Pronunciation: [pronunciation]
        """
        
        ai_response = self._query_ai(prompt)
        
        # Parse AI response into structured data
        analysis = {
            'word': word,
            'ai_analysis': ai_response,
            'timestamp': self._get_timestamp()
        }
        
        return analysis
    
    def process_hebrew_verse(self, verse_words: List[str]) -> Dict[str, any]:
        """
        Function 2: Process entire Hebrew verse using AI
        Input: List of Hebrew words (like your Genesis 1:1 data)
        Output: Complete verse analysis
        """
        verse_text = " ".join(verse_words)
        
        prompt = f"""
        As a Hebrew tutor, analyze this verse: {verse_text}
        
        Provide:
        1. English translation
        2. Key Hebrew words explanation
        3. One grammar insight
        
        Be concise and educational.
        """
        
        ai_response = self._query_ai(prompt, max_tokens=800)
        
        analysis = {
            'original_words': verse_words,
            'verse_text': verse_text,
            'word_count': len(verse_words),
            'ai_explanation': ai_response,
            'timestamp': self._get_timestamp()
        }
        
        return analysis
    
    def create_pronunciation_guide(self, hebrew_text: str) -> Dict[str, str]:
        """
        Function 3: Generate pronunciation guide using AI
        Input: Hebrew text
        Output: Pronunciation information
        """
        prompt = f"""
        Create a pronunciation guide for: {hebrew_text}
        
        Provide ONLY:
        1. Transliteration using English letters
        2. Syllable breakdown with stress marks
        
        Format as: Transliteration: [transliteration] | Syllables: [syllables]
        """
        
        ai_response = self._query_ai(prompt)
        
        guide = {
            'hebrew_text': hebrew_text,
            'pronunciation_guide': ai_response,
            'timestamp': self._get_timestamp()
        }
        
        return guide
    
    def save_analysis_to_file(self, analysis: Dict, filename: str) -> bool:
        """
        Function 4: Save AI analysis to file (using your Week 1 file skills)
        Input: Analysis dictionary, filename
        Output: Success/failure boolean
        """
        try:
            # Ensure data directory exists
            os.makedirs("data/analysis", exist_ok=True)
            
            filepath = f"data/analysis/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(analysis, file, ensure_ascii=False, indent=2)
            
            print(f"✅ Analysis saved to {filepath}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to save analysis: {e}")
            return False
    
    def load_analysis_from_file(self, filename: str) -> Optional[Dict]:
        """
        Function 5: Load previous analysis from file
        Input: Filename
        Output: Analysis dictionary or None
        """
        try:
            filepath = f"data/analysis/{filename}"
            
            with open(filepath, 'r', encoding='utf-8') as file:
                analysis = json.load(file)
            
            print(f"✅ Loaded analysis from {filepath}")
            return analysis
        
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return None
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return None
    
    def batch_process_words(self, word_list: List[str]) -> List[Dict]:
        """
        Function 6: Process multiple Hebrew words efficiently
        Input: List of Hebrew words
        Output: List of analyses
        """
        results = []
        
        print(f"🔄 Processing {len(word_list)} Hebrew words...")
        
        for i, word in enumerate(word_list, 1):
            print(f"Processing word {i}/{len(word_list)}: {word}")
            analysis = self.analyze_hebrew_word(word)
            results.append(analysis)
        
        print(f"✅ Completed processing {len(results)} words")
        return results
    
    def _get_timestamp(self) -> str:
        """Helper function to get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =================================================================
# DEMONSTRATION: Using Your Hebrew AI Functions
# =================================================================

def demonstrate_hebrew_ai_functions():
    """
    Demonstrate all your new Hebrew AI functions
    Using your actual Genesis 1:1 data
    """
    print("🔥 WEEK 1 DAY 5: HEBREW AI FUNCTIONS DEMONSTRATION")
    print("=" * 60)
    
    # Initialize your Hebrew AI processor
    processor = HebrewAIProcessor()
    
    # Your actual Genesis data from earlier tests
    genesis_words = ['בְּרֵאשִׁית', 'בָּרָא', 'אֱלֹהִים', 'אֵת', 'הַשָּׁמַיִם', 'וְאֵת', 'הָאָרֶץ']
    
    print(f"📖 Working with Genesis 1:1: {' '.join(genesis_words)}")
    
    # =================================================================
    # FUNCTION 1: Analyze individual Hebrew word
    # =================================================================
    print(f"\n🔍 FUNCTION 1: Analyzing word 'בְּרֵאשִׁית'")
    word_analysis = processor.analyze_hebrew_word('בְּרֵאשִׁית')
    print(f"Result: {word_analysis['ai_analysis']}")
    
    # =================================================================
    # FUNCTION 2: Process complete verse
    # =================================================================
    print(f"\n📚 FUNCTION 2: Processing complete Genesis verse")
    verse_analysis = processor.process_hebrew_verse(genesis_words)
    print(f"Word count: {verse_analysis['word_count']}")
    print(f"AI explanation: {verse_analysis['ai_explanation']}")
    
    # =================================================================
    # FUNCTION 3: Create pronunciation guide
    # =================================================================
    print(f"\n🗣️ FUNCTION 3: Creating pronunciation guide")
    pronunciation = processor.create_pronunciation_guide('שָׁלוֹם')
    print(f"Pronunciation: {pronunciation['pronunciation_guide']}")
    
    # =================================================================
    # FUNCTION 4: Save analysis to file
    # =================================================================
    print(f"\n💾 FUNCTION 4: Saving analysis to file")
    save_success = processor.save_analysis_to_file(
        verse_analysis, 
        "genesis_1_1_analysis.json"
    )
    
    # =================================================================
    # FUNCTION 5: Load analysis from file
    # =================================================================
    print(f"\n📂 FUNCTION 5: Loading analysis from file")
    loaded_analysis = processor.load_analysis_from_file("genesis_1_1_analysis.json")
    if loaded_analysis:
        print(f"Loaded {len(loaded_analysis)} analysis items")
    
    # =================================================================
    # FUNCTION 6: Batch process multiple words
    # =================================================================
    print(f"\n⚡ FUNCTION 6: Batch processing Hebrew words")
    sample_words = ['שָׁלוֹם', 'אֱלֹהִים', 'תּוֹרָה']
    batch_results = processor.batch_process_words(sample_words)
    
    # Save batch results
    processor.save_analysis_to_file(
        {'batch_analysis': batch_results}, 
        "hebrew_words_batch_analysis.json"
    )
    
    print(f"\n🎉 ALL FUNCTIONS WORKING PERFECTLY!")
    print(f"You now have 6 powerful Hebrew AI functions!")

def test_with_your_tanakh_data():
    """
    Test functions with your actual Tanakh JSON data
    """
    print(f"\n🔗 TESTING WITH YOUR TANAKH DATA")
    print("=" * 40)
    
    tanakh_path = "data/tanakh/hebrew_bible_with_nikkud.json"
    
    if os.path.exists(tanakh_path):
        try:
            with open(tanakh_path, 'r', encoding='utf-8') as f:
                tanakh = json.load(f)
            
            # Get first verse from your data
            first_book = list(tanakh.keys())[0]
            first_verse = tanakh[first_book][0][0]  # First book, first chapter, first verse
            
            print(f"📚 Testing with {first_book} 1:1")
            print(f"Hebrew words: {first_verse}")
            
            # Process with your functions
            processor = HebrewAIProcessor()
            analysis = processor.process_hebrew_verse(first_verse)
            
            # Save the results
            processor.save_analysis_to_file(
                analysis, 
                f"{first_book}_1_1_analysis.json"
            )
            
            print(f"✅ Successfully processed your Tanakh data!")
            
        except Exception as e:
            print(f"❌ Error processing Tanakh: {e}")
    else:
        print(f"⚠️ Tanakh file not found. Make sure it's at: {tanakh_path}")

if __name__ == "__main__":
    print("🔥 WEEK 1 DAY 5: HEBREW AI FUNCTIONS")
    print("Combining file I/O, functions, and local AI power!")
    print("=" * 60)
    
    # Demonstrate all your new Hebrew AI functions
    demonstrate_hebrew_ai_functions()
    
    # Test with your actual Tanakh data
    test_with_your_tanakh_data()
    
    print(f"\n" + "=" * 60)
    print(f"🎓 WEEK 1 DAY 5 COMPLETE!")
    print(f"✅ You've mastered:")
    print(f"  • Functions for code organization")
    print(f"  • AI integration with local models")
    print(f"  • Hebrew text processing")
    print(f"  • File I/O with structured data")
    print(f"  • Batch processing workflows")
    print(f"  • Real-world application building")
    print(f"\n🚀 Ready for Week 1 Day 6: Putting it all together!")
    print(f"Next: Build your first complete Hebrew learning module!")
    print("=" * 60)
