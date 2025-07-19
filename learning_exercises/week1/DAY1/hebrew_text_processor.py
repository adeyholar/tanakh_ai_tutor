# hebrew_text_processor.py - Week 1: Variables & Hebrew Text Basics
# Your first step toward building the Hebrew Learning AI Agent!

# =============================================================================
# WEEK 1: PYTHON VARIABLES FOR HEBREW TEXT PROCESSING
# =============================================================================

def main():
    print("🔥 HEBREW AI TUTOR - Week 1: Variables & Text Processing")
    print("=" * 60)
    
    # =================================================================
    # CONCEPT 1: String Variables for Hebrew Text
    # =================================================================
    print("\n📚 CONCEPT 1: Hebrew Text Variables")
    
    # Hebrew text samples (from Genesis 1:1)
    hebrew_verse = "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ"
    english_translation = "In the beginning God created the heavens and the earth"
    verse_reference = "Genesis 1:1"
    
    # Display the text
    print(f"Hebrew: {hebrew_verse}")
    print(f"English: {english_translation}")
    print(f"Reference: {verse_reference}")
    
    # =================================================================
    # CONCEPT 2: String Operations for Hebrew Analysis
    # =================================================================
    print("\n🔍 CONCEPT 2: Hebrew Text Analysis")
    
    # Basic text analysis
    word_count = len(hebrew_verse.split())
    character_count = len(hebrew_verse)
    character_count_no_spaces = len(hebrew_verse.replace(" ", ""))
    
    print(f"Words in verse: {word_count}")
    print(f"Total characters: {character_count}")
    print(f"Characters (no spaces): {character_count_no_spaces}")
    
    # =================================================================
    # CONCEPT 3: Lists for Hebrew Word Processing
    # =================================================================
    print("\n📝 CONCEPT 3: Breaking Down Hebrew Words")
    
    # Split into individual words
    hebrew_words = hebrew_verse.split()
    
    print("Individual Hebrew words:")
    for i, word in enumerate(hebrew_words, 1):
        print(f"{i}. {word}")
    
    # =================================================================
    # CONCEPT 4: Dictionaries for Hebrew-English Mapping
    # =================================================================
    print("\n🗂️ CONCEPT 4: Hebrew Word Dictionary")
    
    # Create a simple Hebrew-English dictionary
    hebrew_lexicon = {
        "בְּרֵאשִׁית": {"english": "in the beginning", "root": "ראש", "meaning": "head/beginning"},
        "בָּרָא": {"english": "created", "root": "ברא", "meaning": "to create"},
        "אֱלֹהִים": {"english": "God", "root": "אלה", "meaning": "God/gods"},
        "אֵת": {"english": "(direct object marker)", "root": "את", "meaning": "with/sign"},
        "הַשָּׁמַיִם": {"english": "the heavens", "root": "שמה", "meaning": "heaven/sky"},
        "וְאֵת": {"english": "and (direct object marker)", "root": "ואת", "meaning": "and with"},
        "הָאָרֶץ": {"english": "the earth", "root": "ארץ", "meaning": "earth/land"}
    }
    
    # Analyze each word
    print("\nWord-by-word analysis:")
    for word in hebrew_words:
        if word in hebrew_lexicon:
            info = hebrew_lexicon[word]
            print(f"{word} → {info['english']} (root: {info['root']})")
        else:
            print(f"{word} → (not in our dictionary yet)")
    
    # =================================================================
    # CONCEPT 5: Functions for Reusable Hebrew Processing
    # =================================================================
    print("\n⚙️ CONCEPT 5: Hebrew Processing Functions")
    
    def analyze_hebrew_text(text):
        """Analyze Hebrew text and return statistics"""
        analysis = {
            'text': text,
            'word_count': len(text.split()),
            'char_count': len(text),
            'char_count_no_spaces': len(text.replace(" ", "")),
            'words': text.split()
        }
        return analysis
    
    def lookup_word(word, lexicon):
        """Look up a Hebrew word in our lexicon"""
        if word in lexicon:
            return lexicon[word]
        else:
            return {"english": "Unknown", "root": "Unknown", "meaning": "Not in lexicon"}
    
    # Test our functions
    analysis = analyze_hebrew_text(hebrew_verse)
    print(f"\nFunction analysis results:")
    print(f"Text: {analysis['text']}")
    print(f"Words: {analysis['word_count']}")
    print(f"Characters: {analysis['char_count']}")
    
    # =================================================================
    # YOUR FIRST HEBREW AI COMPONENT!
    # =================================================================
    print("\n🎯 YOUR FIRST AI COMPONENT: Smart Hebrew Lookup")
    
    def smart_hebrew_lookup(text, lexicon):
        """
        This is the beginning of your Hebrew learning AI!
        It processes Hebrew text and provides intelligent analysis.
        """
        results = []
        words = text.split()
        
        for word in words:
            word_info = lookup_word(word, lexicon)
            results.append({
                'hebrew': word,
                'english': word_info['english'],
                'root': word_info['root'],
                'meaning': word_info['meaning']
            })
        
        return results
    
    # Use your AI component!
    ai_analysis = smart_hebrew_lookup(hebrew_verse, hebrew_lexicon)
    
    print("\n🤖 AI Analysis Results:")
    for result in ai_analysis:
        print(f"Hebrew: {result['hebrew']}")
        print(f"English: {result['english']}")
        print(f"Root: {result['root']}")
        print(f"Meaning: {result['meaning']}")
        print("-" * 30)
    
    # =================================================================
    # CHALLENGE: Process Your Own Hebrew Text!
    # =================================================================
    print("\n🏆 CHALLENGE: Try Another Verse!")
    
    # Psalm 23:1
    psalm_text = "יְהוָה רֹעִי לֹא אֶחְסָר"
    psalm_translation = "The LORD is my shepherd; I shall not want"
    
    print(f"Hebrew: {psalm_text}")
    print(f"English: {psalm_translation}")
    
    psalm_analysis = analyze_hebrew_text(psalm_text)
    print(f"This verse has {psalm_analysis['word_count']} words")
    print(f"Individual words: {psalm_analysis['words']}")
    
    print("\n🎉 CONGRATULATIONS!")
    print("You just built your first Hebrew text processing component!")
    print("This is the foundation of your AI Hebrew tutor!")

# =============================================================================
# UNDERSTANDING CHECK - Answer these to show you understand!
# =============================================================================

def understanding_check():
    """
    Before we move to the next concept, answer these questions:
    
    1. What's the difference between a string and a list in Python?
    2. How would you add a new word to our hebrew_lexicon dictionary?
    3. What does the split() method do to Hebrew text?
    4. How could we expand the smart_hebrew_lookup function?
    
    Think about these, then tell me your answers!
    """
    pass

if __name__ == "__main__":
    main()
    print("\n" + "="*60)
    print("🤔 UNDERSTANDING CHECK - Think about these questions:")
    print("1. What's the difference between a string and a list?")
    print("2. How would you add new words to hebrew_lexicon?")
    print("3. What does split() do to Hebrew text?")
    print("4. How could we make smart_hebrew_lookup even smarter?")
    print("="*60)