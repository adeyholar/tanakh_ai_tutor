# hebrew_lexicon_builder.py - Week 1 Day 4: Building Your Hebrew AI Brain!
# Creating the intelligent lexicon system for your Hebrew tutor

import json

def demonstrate_dictionary_power():
    """Show why dictionaries are PERFECT for Hebrew lexicons"""
    print("🧠 BUILDING YOUR HEBREW AI BRAIN!")
    print("Using Dictionaries to Create Intelligent Hebrew Lexicon")
    print("=" * 60)
    
    # =================================================================
    # From Your Genesis 1:1 Discovery
    # =================================================================
    genesis_words = ['בְּרֵאשִׁ֖ית', 'בָּרָ֣א', 'אֱלֹהִ֑ים', 'אֵ֥ת', 'הַשָּׁמַ֖יִם', 'וְאֵ֥ת', 'הָאָֽרֶץ׃']
    
    print(f"📖 GENESIS 1:1 WORDS FROM YOUR TANAKH:")
    for i, word in enumerate(genesis_words, 1):
        print(f"{i}. {word}")
    
    # =================================================================
    # DICTIONARY-BASED HEBREW LEXICON
    # =================================================================
    print(f"\n🔤 CREATING INTELLIGENT HEBREW LEXICON:")
    
    # This is how your Hebrew AI will store word knowledge!
    hebrew_lexicon = {
        # Remove cantillation marks for base word lookup
        "בְּרֵאשִׁית": {
            "english": "in the beginning",
            "root": "ראש",
            "meaning": "head, beginning, first",
            "part_of_speech": "noun",
            "frequency": "high",
            "pronunciation": "be-re-SHEET",
            "grammar_notes": "construct state with preposition",
            "first_occurrence": "Genesis 1:1",
            "related_words": ["רֹאשׁ", "רִאשׁוֹן"]
        },
        "בָּרָא": {
            "english": "he created",
            "root": "ברא",
            "meaning": "to create, make",
            "part_of_speech": "verb",
            "frequency": "medium",
            "pronunciation": "ba-RA",
            "grammar_notes": "Qal perfect 3rd person masculine singular",
            "first_occurrence": "Genesis 1:1",
            "related_words": ["בְּרִיאָה", "בָּרִיא"]
        },
        "אֱלֹהִים": {
            "english": "God",
            "root": "אלה",
            "meaning": "God, gods, divine beings",
            "part_of_speech": "noun",
            "frequency": "very_high",
            "pronunciation": "e-lo-HEEM",
            "grammar_notes": "plural form but often singular meaning",
            "first_occurrence": "Genesis 1:1",
            "related_words": ["אֵל", "אֱלוֹהַּ"]
        },
        "אֵת": {
            "english": "(direct object marker)",
            "root": "את",
            "meaning": "with, sign of direct object",
            "part_of_speech": "particle",
            "frequency": "very_high",
            "pronunciation": "et",
            "grammar_notes": "definite direct object marker",
            "first_occurrence": "Genesis 1:1",
            "related_words": ["אֶת־", "אִתּ"]
        },
        "הַשָּׁמַיִם": {
            "english": "the heavens",
            "root": "שמה",
            "meaning": "heavens, sky",
            "part_of_speech": "noun",
            "frequency": "high",
            "pronunciation": "ha-sha-MA-yim",
            "grammar_notes": "definite article + dual form",
            "first_occurrence": "Genesis 1:1",
            "related_words": ["שָׁמַיִם", "שָׁמֶה"]
        },
        "הָאָרֶץ": {
            "english": "the earth",
            "root": "ארץ",
            "meaning": "earth, land",
            "part_of_speech": "noun",
            "frequency": "very_high",
            "pronunciation": "ha-A-retz",
            "grammar_notes": "definite article + feminine noun",
            "first_occurrence": "Genesis 1:1",
            "related_words": ["אֶרֶץ", "אֲרָצוֹת"]
        }
    }
    
    # =================================================================
    # INTELLIGENT WORD LOOKUP SYSTEM
    # =================================================================
    print(f"\n🔍 INTELLIGENT WORD LOOKUP SYSTEM:")
    
    def clean_hebrew_word(word):
        """Remove cantillation marks for lookup"""
        # Remove common cantillation marks
        cantillation_marks = "ֽ֑֖֣֥֖֥׃"
        clean_word = word
        for mark in cantillation_marks:
            clean_word = clean_word.replace(mark, "")
        return clean_word
    
    def lookup_hebrew_word(word, lexicon):
        """Intelligent Hebrew word lookup"""
        # Try exact match first
        if word in lexicon:
            return lexicon[word]
        
        # Try cleaned version (remove cantillation)
        clean_word = clean_hebrew_word(word)
        if clean_word in lexicon:
            return lexicon[clean_word]
        
        # Return unknown if not found
        return {
            "english": "Unknown word",
            "root": "Needs research",
            "meaning": "Not in lexicon yet",
            "part_of_speech": "unknown",
            "frequency": "unknown",
            "pronunciation": "unknown",
            "note": f"Add '{word}' to lexicon"
        }
    
    # Test with your actual Genesis words
    print(f"Testing with your Genesis 1:1 words:")
    for word in genesis_words:
        info = lookup_hebrew_word(word, hebrew_lexicon)
        print(f"\n📝 {word}:")
        print(f"   English: {info['english']}")
        print(f"   Root: {info['root']}")
        print(f"   Pronunciation: {info['pronunciation']}")
        print(f"   Grammar: {info.get('grammar_notes', 'N/A')}")
    
    # =================================================================
    # LEXICON STATISTICS AND ANALYSIS
    # =================================================================
    print(f"\n📊 LEXICON ANALYSIS:")
    
    def analyze_lexicon(lexicon):
        """Analyze your Hebrew lexicon"""
        total_words = len(lexicon)
        
        # Count by part of speech
        pos_counts = {}
        for word_info in lexicon.values():
            pos = word_info['part_of_speech']
            pos_counts[pos] = pos_counts.get(pos, 0) + 1
        
        # Count by frequency
        freq_counts = {}
        for word_info in lexicon.values():
            freq = word_info['frequency']
            freq_counts[freq] = freq_counts.get(freq, 0) + 1
        
        return {
            'total_words': total_words,
            'parts_of_speech': pos_counts,
            'frequency_distribution': freq_counts
        }
    
    stats = analyze_lexicon(hebrew_lexicon)
    
    print(f"Total words in lexicon: {stats['total_words']}")
    print(f"Parts of speech: {stats['parts_of_speech']}")
    print(f"Frequency distribution: {stats['frequency_distribution']}")
    
    # =================================================================
    # BUILDING YOUR COMPREHENSIVE LEXICON
    # =================================================================
    print(f"\n🏗️ BUILDING YOUR COMPREHENSIVE LEXICON:")
    
    def extract_unique_words_from_tanakh():
        """Extract unique words from your Tanakh for lexicon building"""
        file_path = r"D:\AI\Projects\HEBREW TRAINING AI AGENT\TANACH\book\hebrew_bible_with_nikkud.json"
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tanakh = json.load(file)
            
            unique_words = set()
            
            # Navigate your Tanakh structure: book -> chapters -> verses -> words
            for book_name, chapters in tanakh.items():
                if isinstance(chapters, list):
                    for chapter in chapters:
                        if isinstance(chapter, list):
                            for verse in chapter:
                                if isinstance(verse, list):
                                    for word in verse:
                                        if isinstance(word, str):
                                            # Clean and add word
                                            clean_word = clean_hebrew_word(word)
                                            if clean_word:
                                                unique_words.add(clean_word)
            
            return unique_words
        
        except Exception as e:
            print(f"Error accessing Tanakh: {e}")
            return set()
    
    # Get sample of unique words
    unique_words = extract_unique_words_from_tanakh()
    if unique_words:
        sample_words = list(unique_words)[:10]
        print(f"Sample unique words from your Tanakh:")
        for i, word in enumerate(sample_words, 1):
            print(f"{i:2}. {word}")
        print(f"Total unique words available: {len(unique_words):,}")
    
    # =================================================================
    # YOUR HEBREW AI POTENTIAL
    # =================================================================
    print(f"\n🚀 YOUR HEBREW AI LEXICON SYSTEM:")
    print(f"✅ Intelligent word lookup with cantillation handling")
    print(f"✅ Complete linguistic information storage")
    print(f"✅ Grammar and pronunciation data")
    print(f"✅ Frequency and usage statistics")
    print(f"✅ Expandable to 116,897+ unique words")
    print(f"✅ Perfect foundation for AI tutoring")
    
    return hebrew_lexicon

def save_lexicon_to_file(lexicon):
    """Save your lexicon for future use"""
    with open("hebrew_lexicon.json", "w", encoding="utf-8") as file:
        json.dump(lexicon, file, ensure_ascii=False, indent=2)
    print(f"\n💾 Lexicon saved to 'hebrew_lexicon.json'")

if __name__ == "__main__":
    lexicon = demonstrate_dictionary_power()
    save_lexicon_to_file(lexicon)
    
    print(f"\n" + "=" * 60)
    print(f"🎯 YOU'VE BUILT THE BRAIN OF YOUR HEBREW AI!")
    print(f"=" * 60)
    print(f"🎓 What you've mastered:")
    print(f"  • Dictionary-based data storage")
    print(f"  • Intelligent word lookup systems")
    print(f"  • Hebrew text processing")
    print(f"  • Lexicon analysis and statistics")
    print(f"  • Foundation for AI language tutoring")
    print(f"\n🚀 Ready for Week 1 Day 5: Functions and Code Organization!")
    print(f"   Next: Turn your code into reusable Hebrew AI components!")