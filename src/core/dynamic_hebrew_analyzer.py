# src/core/dynamic_hebrew_analyzer.py
"""
Dynamic Hebrew Analyzer - Week 3 Day 3 Enhancement
No hard-coded dictionaries - uses algorithmic analysis
"""

import re
import json
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import logging

class DynamicHebrewAnalyzer:
    """Analyzes Hebrew words dynamically without hard-coded dictionaries"""
    
    def __init__(self):
        self.logger = logging.getLogger("DynamicHebrew")
        self.hebrew_patterns = self._create_pattern_database()
        self.morpheme_database = self._load_morpheme_database()
        
    def analyze_word_dynamically(self, word: str) -> Dict[str, Any]:
        """Analyze Hebrew word using algorithmic pattern recognition"""
        clean_word = self._clean_hebrew_word(word)
        
        analysis = {
            'original_word': word,
            'clean_word': clean_word,
            'detected_morphemes': self._detect_morphemes(clean_word),
            'grammatical_category': self._classify_grammatically(clean_word),
            'root_extraction': self._extract_root_algorithmically(clean_word),
            'morphological_features': self._detect_morphological_features(clean_word),
            'confidence_score': self._calculate_dynamic_confidence(clean_word)
        }
        
        return analysis
    
    def _detect_morphemes(self, word: str) -> Dict[str, Any]:
        """Detect Hebrew morphemes (prefixes, stems, suffixes) algorithmically"""
        morphemes = {
            'prefixes': [],
            'stem': '',
            'suffixes': [],
            'analysis_method': 'algorithmic'
        }
        
        working_word = word
        
        # Detect common prefixes
        prefix_patterns = {
            'ה': 'definite_article',
            'ו': 'conjunction_waw',
            'ב': 'preposition_in',
            'כ': 'preposition_like',
            'ל': 'preposition_to',
            'מ': 'preposition_from',
            'ש': 'relative_pronoun'
        }
        
        # Check for prefixes
        for prefix, meaning in prefix_patterns.items():
            if working_word.startswith(prefix) and len(working_word) > 1:
                morphemes['prefixes'].append({
                    'morpheme': prefix,
                    'function': meaning,
                    'position': 'prefix'
                })
                working_word = working_word[1:]  # Remove prefix
        
        # Detect common suffixes
        suffix_patterns = {
            'ים': 'masculine_plural',
            'ות': 'feminine_plural',
            'ת': 'feminine_singular_or_construct',
            'י': 'construct_or_possessive',
            'ה': 'feminine_or_directional',
            'ן': 'final_nun_energicum',
            'נו': 'our_suffix',
            'כם': 'your_masculine_plural',
            'כן': 'your_feminine_plural'
        }
        
        # Check for suffixes (longest first)
        for suffix in sorted(suffix_patterns.keys(), key=len, reverse=True):
            if working_word.endswith(suffix) and len(working_word) > len(suffix):
                morphemes['suffixes'].append({
                    'morpheme': suffix,
                    'function': suffix_patterns[suffix],
                    'position': 'suffix'
                })
                working_word = working_word[:-len(suffix)]  # Remove suffix
                break  # Only take one suffix for now
        
        # Remaining part is likely the stem
        morphemes['stem'] = working_word
        
        return morphemes
    
    def _classify_grammatically(self, word: str) -> Dict[str, str]:
        """Classify word grammatically using pattern analysis"""
        classification = {
            'primary_category': 'unknown',
            'secondary_features': [],
            'reasoning': ''
        }
        
        # Verb pattern recognition
        if self._matches_verb_patterns(word):
            classification['primary_category'] = 'verb'
            classification['secondary_features'] = self._detect_verbal_features(word)
            classification['reasoning'] = 'matches Hebrew verbal morphology patterns'
        
        # Noun pattern recognition
        elif self._matches_noun_patterns(word):
            classification['primary_category'] = 'noun'
            classification['secondary_features'] = self._detect_nominal_features(word)
            classification['reasoning'] = 'matches Hebrew nominal morphology patterns'
        
        # Particle/function word recognition
        elif len(word) <= 3:  # Most Hebrew function words are short
            classification['primary_category'] = 'particle'
            classification['secondary_features'] = ['short_function_word']
            classification['reasoning'] = 'short word likely function/grammatical particle'
        
        else:
            classification['reasoning'] = 'pattern not clearly identified'
        
        return classification
    
    def _extract_root_algorithmically(self, word: str) -> Dict[str, Any]:
        """Extract Hebrew root using algorithmic methods"""
        # Remove known prefixes and suffixes
        morphemes = self._detect_morphemes(word)
        potential_root = morphemes['stem']
        
        # Hebrew roots are typically 3 consonants (sometimes 2 or 4)
        # Remove vowel points (nikkud) to find consonantal root
        consonant_root = self._extract_consonants(potential_root)
        
        root_info = {
            'extracted_root': consonant_root,
            'root_length': len(consonant_root),
            'extraction_method': 'algorithmic_morpheme_analysis',
            'confidence': 'medium' if 2 <= len(consonant_root) <= 4 else 'low'
        }
        
        return root_info
    
    def _extract_consonants(self, text: str) -> str:
        """Extract Hebrew consonants by removing vowel points"""
        # Hebrew vowel points (nikkud) unicode ranges
        nikkud_pattern = r'[\u0591-\u05C7]'  # Hebrew accents and points
        consonants_only = re.sub(nikkud_pattern, '', text)
        return consonants_only
    
    def _matches_verb_patterns(self, word: str) -> bool:
        """Check if word matches Hebrew verbal patterns"""
        consonants = self._extract_consonants(word)
        
        # Common Hebrew verbal patterns (simplified)
        verb_indicators = [
            len(consonants) >= 3,  # Most Hebrew verbs have 3+ consonants
            bool(re.search(r'[תיאנה]$', word)),  # Common verbal endings
            bool(re.search(r'^[אתינה]', word)),  # Common verbal prefixes
        ]
        
        return sum(verb_indicators) >= 2  # At least 2 indicators
    
    def _matches_noun_patterns(self, word: str) -> bool:
        """Check if word matches Hebrew nominal patterns"""
        # Definite article
        if word.startswith('ה'):
            return True
        
        # Common noun endings
        noun_endings = ['ים', 'ות', 'ת', 'ה', 'י']
        if any(word.endswith(ending) for ending in noun_endings):
            return True
        
        return False
    
    def _detect_verbal_features(self, word: str) -> List[str]:
        """Detect specific verbal features"""
        features = []
        
        if word.startswith('ה'):
            features.append('possible_hiphil')
        if word.startswith('נ'):
            features.append('possible_niphal')
        if word.startswith('ת'):
            features.append('possible_hithpael_or_future')
        if word.startswith('י'):
            features.append('possible_future_3ms')
        if word.startswith('א'):
            features.append('possible_future_1s')
        
        return features
    
    def _detect_nominal_features(self, word: str) -> List[str]:
        """Detect specific nominal features"""
        features = []
        
        if word.startswith('ה'):
            features.append('definite_article')
        if word.endswith('ים'):
            features.append('masculine_plural')
        if word.endswith('ות'):
            features.append('feminine_plural')
        if word.endswith('ת'):
            features.append('feminine_or_construct')
        
        return features
    
    def _detect_morphological_features(self, word: str) -> Dict[str, Any]:
        """Detect detailed morphological features"""
        features = {
            'syllable_count': self._estimate_syllables(word),
            'vowel_pattern': self._extract_vowel_pattern(word),
            'consonant_pattern': self._extract_consonant_pattern(word),
            'special_features': self._detect_special_features(word)
        }
        
        return features
    
    def _estimate_syllables(self, word: str) -> int:
        """Estimate syllable count in Hebrew word"""
        # Simplified: count vowel-bearing units
        vowel_points = r'[\u05B0-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]'
        vowel_count = len(re.findall(vowel_points, word))
        # Hebrew words typically have at least one syllable
        return max(1, vowel_count)
    
    def _extract_vowel_pattern(self, word: str) -> str:
        """Extract vowel pattern from Hebrew word"""
        vowel_points = r'[\u05B0-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]'
        vowels = re.findall(vowel_points, word)
        return ''.join(vowels)
    
    def _extract_consonant_pattern(self, word: str) -> str:
        """Extract consonant pattern"""
        return self._extract_consonants(word)
    
    def _detect_special_features(self, word: str) -> List[str]:
        """Detect special Hebrew features"""
        features = []
        
        # Gemination (dagesh forte)
        if '\u05BC' in word:  # Dagesh
            features.append('contains_dagesh')
        
        # Final forms
        final_letters = 'ךםןףץ'
        if any(letter in word for letter in final_letters):
            features.append('contains_final_form')
        
        # Cantillation marks
        cantillation_pattern = r'[\u0591-\u05AF]'
        if re.search(cantillation_pattern, word):
            features.append('contains_cantillation')
        
        return features
    
    def _calculate_dynamic_confidence(self, word: str) -> float:
        """Calculate confidence based on pattern recognition success"""
        confidence_factors = []
        
        # Length factor (Hebrew words are typically 2-8 characters)
        length_score = 1.0 if 2 <= len(word) <= 8 else 0.5
        confidence_factors.append(length_score)
        
        # Pattern recognition success
        if self._matches_verb_patterns(word) or self._matches_noun_patterns(word):
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Morpheme detection success
        morphemes = self._detect_morphemes(word)
        if morphemes['stem']:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.3)
        
        # Average confidence
        return round(sum(confidence_factors) / len(confidence_factors), 2)
    
    def _clean_hebrew_word(self, word: str) -> str:
        """Clean Hebrew word for analysis"""
        # Remove final punctuation
        cleaned = re.sub(r'[׃.,;!?\s]+$', '', word)
        return cleaned.strip()
    
    def _create_pattern_database(self) -> Dict[str, Any]:
        """Create pattern database for Hebrew analysis"""
        return {
            'verb_prefixes': ['א', 'ת', 'י', 'נ'],
            'noun_definite': 'ה',
            'prepositions': ['ב', 'כ', 'ל', 'מ'],
            'conjunctions': ['ו'],
            'common_suffixes': ['ים', 'ות', 'ת', 'ה', 'י']
        }
    
    def _load_morpheme_database(self) -> Dict[str, Any]:
        """Load morpheme database (could be from external file)"""
        return {
            'prefixes': {
                'ה': {'type': 'definite_article', 'frequency': 'very_high'},
                'ו': {'type': 'conjunction', 'frequency': 'very_high'},
                'ב': {'type': 'preposition', 'meaning': 'in/with', 'frequency': 'high'}
            },
            'suffixes': {
                'ים': {'type': 'plural_marker', 'gender': 'masculine', 'frequency': 'high'},
                'ות': {'type': 'plural_marker', 'gender': 'feminine', 'frequency': 'high'}
            }
        }

# Demo function
def demo_dynamic_analysis():
    """Demonstrate dynamic Hebrew analysis"""
    print("🎓 Dynamic Hebrew Analysis Demo")
    print("=" * 40)
    
    analyzer = DynamicHebrewAnalyzer()
    
    test_words = ["בְּרֵאשִׁ֖ית", "בָּרָ֣א", "אֱלֹהִ֑ים", "הַשָּׁמַ֖יִם"]
    
    for word in test_words:
        print(f"\n📖 Dynamic analysis of: {word}")
        print("-" * 25)
        
        analysis = analyzer.analyze_word_dynamically(word)
        
        print(f"Clean word: {analysis['clean_word']}")
        print(f"Category: {analysis['grammatical_category']['primary_category']}")
        print(f"Extracted root: {analysis['root_extraction']['extracted_root']}")
        print(f"Prefixes: {[p['morpheme'] for p in analysis['detected_morphemes']['prefixes']]}")
        print(f"Stem: {analysis['detected_morphemes']['stem']}")
        print(f"Suffixes: {[s['morpheme'] for s in analysis['detected_morphemes']['suffixes']]}")
        print(f"Confidence: {analysis['confidence_score']}")
    
    print("\n✅ Dynamic analysis complete!")

if __name__ == "__main__":
    demo_dynamic_analysis()
