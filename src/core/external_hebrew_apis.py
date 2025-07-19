# src/core/external_hebrew_apis.py
"""
External Hebrew API Integrations - Week 3 Day 3
Professional API integrations for enhanced Hebrew analysis
"""

import asyncio
import aiohttp
import requests
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import logging
import json
from pathlib import Path

# Import our base analyzer
from hebrew_analyzers import HebrewAnalyzer, AnalysisResult

@dataclass
class HebrewAPIResult:
    """Result from external Hebrew API"""
    word: str
    source: str
    translation: str
    transliteration: str
    grammar_info: Dict[str, Any]
    morphology: Dict[str, Any]
    confidence: float
    timestamp: datetime

class SefariaMockAPI(HebrewAnalyzer):
    """Mock integration with Sefaria-style Hebrew text API"""
    
    def __init__(self):
        super().__init__("Sefaria-Mock")
        self.base_url = "https://www.sefaria.org/api"
        self.cache_path = Path("data/api_cache/sefaria_cache.json")
        self.cache = {}
        self._load_cache()
        
    def initialize(self) -> bool:
        """Initialize the Sefaria API connection"""
        try:
            # Test connection (mock for now since we don't want to spam real API)
            self.is_available = True
            self.logger.info("✅ Sefaria Mock API initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Sefaria API: {e}")
            return False
    
    async def analyze_word(self, word: str) -> AnalysisResult:
        """Analyze Hebrew word using Sefaria-style resources"""
        try:
            # Check cache first
            if word in self.cache:
                cached_result = self.cache[word]
                self.logger.debug(f"Using cached result for {word}")
                return AnalysisResult(
                    word=word,
                    translation=cached_result.get('translation', 'Unknown'),
                    grammar_info=cached_result.get('grammar_info', {}),
                    confidence=0.70,
                    model_used="Sefaria-Mock",
                    timestamp=datetime.now()
                )
            
            # Mock API call (replace with real API in production)
            mock_data = await self._mock_sefaria_lookup(word)
            
            # Create analysis result
            analysis = AnalysisResult(
                word=word,
                translation=mock_data.get('translation', 'Unknown'),
                grammar_info={
                    'root': mock_data.get('root', 'Unknown'),
                    'part_of_speech': mock_data.get('pos', 'Unknown'),
                    'tense': mock_data.get('tense', 'N/A'),
                    'source': 'Sefaria Hebrew Lexicon'
                },
                confidence=0.70,
                model_used="Sefaria-Mock",
                timestamp=datetime.now()
            )
            
            # Cache the result
            self.cache[word] = {
                'translation': analysis.translation,
                'grammar_info': analysis.grammar_info,
                'timestamp': analysis.timestamp.isoformat()
            }
            self._save_cache()
            
            self.analysis_count += 1
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error with Sefaria API for '{word}': {e}")
            raise
    
    async def _mock_sefaria_lookup(self, word: str) -> Dict[str, str]:
        """Mock Sefaria API lookup - replace with real API calls"""
        # Hebrew word dictionary for common biblical words
        mock_lexicon = {
            'בְּרֵאשִׁ֖ית': {
                'translation': 'in the beginning',
                'root': 'ראש',
                'pos': 'prepositional phrase',
                'tense': 'N/A'
            },
            'בָּרָ֣א': {
                'translation': 'created',
                'root': 'ברא',
                'pos': 'verb',
                'tense': 'qal perfect'
            },
            'אֱלֹהִ֑ים': {
                'translation': 'God',
                'root': 'אלה',
                'pos': 'noun',
                'tense': 'N/A'
            },
            'אֵ֥ת': {
                'translation': '(direct object marker)',
                'root': 'את',
                'pos': 'particle',
                'tense': 'N/A'
            },
            'הַשָּׁמַ֖יִם': {
                'translation': 'the heavens',
                'root': 'שמה',
                'pos': 'noun',
                'tense': 'N/A'
            }
        }
        
        # Clean the word for lookup
        clean_word = self._clean_hebrew_for_lookup(word)
        
        # Return mock data
        if clean_word in mock_lexicon:
            return mock_lexicon[clean_word]
        else:
            return {
                'translation': f'[Unknown: {word}]',
                'root': 'Unknown',
                'pos': 'Unknown',
                'tense': 'N/A'
            }
    
    def _clean_hebrew_for_lookup(self, word: str) -> str:
        """Clean Hebrew word for API lookup"""
        # Remove final punctuation but keep nikkud for now
        import re
        cleaned = re.sub(r'[׃.,;!?]$', '', word)
        return cleaned.strip()
    
    def _load_cache(self):
        """Load API response cache"""
        try:
            if self.cache_path.exists():
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
                self.logger.debug(f"Loaded {len(self.cache)} cached entries")
        except Exception as e:
            self.logger.warning(f"Could not load cache: {e}")
            self.cache = {}
    
    def _save_cache(self):
        """Save API response cache"""
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save cache: {e}")

class HebrewMorphologyAPI(HebrewAnalyzer):
    """Hebrew morphological analysis API integration"""
    
    def __init__(self):
        super().__init__("HebrewMorphology")
        self.api_timeout = 10
        
    def initialize(self) -> bool:
        """Initialize morphology analyzer"""
        try:
            # Mock initialization for now
            self.is_available = True
            self.logger.info("✅ Hebrew Morphology API initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Morphology API: {e}")
            return False
    
    async def analyze_word(self, word: str) -> AnalysisResult:
        """Perform morphological analysis of Hebrew word"""
        try:
            # Mock morphological analysis
            morphology_data = await self._mock_morphological_analysis(word)
            
            analysis = AnalysisResult(
                word=word,
                translation=morphology_data.get('lemma', 'Unknown'),
                grammar_info={
                    'morphology': morphology_data.get('morphology', {}),
                    'word_form': morphology_data.get('word_form', 'Unknown'),
                    'parsing': morphology_data.get('parsing', 'Unknown'),
                    'strong_number': morphology_data.get('strong_number', 'N/A')
                },
                confidence=0.75,
                model_used="HebrewMorphology",
                timestamp=datetime.now()
            )
            
            self.analysis_count += 1
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error with Morphology API for '{word}': {e}")
            raise
    
    async def _mock_morphological_analysis(self, word: str) -> Dict[str, Any]:
        """Mock morphological analysis - replace with real API"""
        # Simplified morphology for common words
        morphology_db = {
            'בְּרֵאשִׁ֖ית': {
                'lemma': 'beginning',
                'morphology': {
                    'prefix': 'ב',
                    'stem': 'ראש',
                    'suffix': 'ית'
                },
                'word_form': 'construct',
                'parsing': 'prep + noun fs construct',
                'strong_number': 'H7225'
            },
            'בָּרָ֣א': {
                'lemma': 'create',
                'morphology': {
                    'stem': 'ברא',
                    'binyan': 'qal',
                    'person': '3ms',
                    'tense': 'perfect'
                },
                'word_form': 'verb',
                'parsing': 'qal perfect 3ms',
                'strong_number': 'H1254'
            }
        }
        
        clean_word = word.rstrip('׃.,;!?')
        return morphology_db.get(clean_word, {
            'lemma': f'[Morphology unknown for {word}]',
            'morphology': {},
            'word_form': 'Unknown',
            'parsing': 'Unknown',
            'strong_number': 'N/A'
        })

class EnhancedHebrewAI:
    """Enhanced Hebrew AI combining local and external resources"""
    
    def __init__(self):
        self.local_analyzers = []
        self.external_apis = []
        self.logger = logging.getLogger("EnhancedHebrewAI")
        
    async def initialize_all_sources(self):
        """Initialize all available Hebrew analysis sources"""
        self.logger.info("🚀 Initializing Enhanced Hebrew AI...")
        
        # Import and initialize local analyzers
        try:
            from hebrew_analyzers import AlephBertAnalyzer, OllamaAnalyzer
            
            alephbert = AlephBertAnalyzer()
            if alephbert.initialize():
                self.local_analyzers.append(alephbert)
                self.logger.info("✅ AlephBERT local analyzer ready")
            
            ollama = OllamaAnalyzer()
            if ollama.initialize():
                self.local_analyzers.append(ollama)
                self.logger.info("✅ Ollama local analyzer ready")
                
        except Exception as e:
            self.logger.warning(f"Some local analyzers failed: {e}")
        
        # Initialize external APIs
        sefaria = SefariaMockAPI()
        if sefaria.initialize():
            self.external_apis.append(sefaria)
            self.logger.info("✅ Sefaria API ready")
        
        morphology = HebrewMorphologyAPI()
        if morphology.initialize():
            self.external_apis.append(morphology)
            self.logger.info("✅ Morphology API ready")
        
        total_sources = len(self.local_analyzers) + len(self.external_apis)
        self.logger.info(f"🎯 Enhanced Hebrew AI ready with {total_sources} sources")
    
    async def comprehensive_analysis(self, word: str) -> Dict[str, AnalysisResult]:
        """Get comprehensive analysis from all available sources"""
        results = {}
        
        # Analyze with local models
        for analyzer in self.local_analyzers:
            try:
                result = await analyzer.analyze_word(word)
                results[analyzer.name] = result
            except Exception as e:
                self.logger.warning(f"Local analysis failed with {analyzer.name}: {e}")
        
        # Analyze with external APIs
        for api in self.external_apis:
            try:
                result = await api.analyze_word(word)
                results[api.name] = result
            except Exception as e:
                self.logger.warning(f"External API failed with {api.name}: {e}")
        
        return results

# Demo function
async def demo_enhanced_hebrew_ai():
    """Demonstrate the enhanced Hebrew AI system"""
    print("🎓 Enhanced Hebrew AI Demo - Week 3 Day 3")
    print("=" * 50)
    
    # Initialize enhanced system
    enhanced_ai = EnhancedHebrewAI()
    await enhanced_ai.initialize_all_sources()
    
    # Test word
    test_word = "בְּרֵאשִׁ֖ית"
    print(f"\n📖 Comprehensive analysis of: {test_word}")
    print("-" * 30)
    
    # Get comprehensive analysis
    results = await enhanced_ai.comprehensive_analysis(test_word)
    
    # Display results
    for source, result in results.items():
        print(f"\n🔍 {source}:")
        print(f"   Translation: {result.translation}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Grammar: {result.grammar_info}")
    
    print(f"\n📊 Total analysis sources: {len(results)}")
    print("✅ Enhanced Hebrew AI demo complete!")

if __name__ == "__main__":
    asyncio.run(demo_enhanced_hebrew_ai())
