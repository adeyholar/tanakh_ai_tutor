# split_method_demo.py - Master the split() method for Hebrew AI
# This is CRUCIAL for your Hebrew text processing AI!

def demonstrate_split_method():
    print("✂️ MASTERING split() FOR HEBREW TEXT AI!")
    print("=" * 50)
    
    # =================================================================
    # BASIC split() - The Foundation
    # =================================================================
    print("\n🔤 BASIC split() - Breaking Text Apart")
    
    # Hebrew sentence (Genesis 1:3)
    hebrew_sentence = "וַיֹּאמֶר אֱלֹהִים יְהִי אוֹר"
    english_sentence = "And God said let there be light"
    
    print(f"Original Hebrew: {hebrew_sentence}")
    print(f"Type: {type(hebrew_sentence)}")
    
    # split() breaks it into individual words
    hebrew_words = hebrew_sentence.split()
    print(f"After split(): {hebrew_words}")
    print(f"Type: {type(hebrew_words)}")
    print(f"Number of words: {len(hebrew_words)}")
    
    # =================================================================
    # WHY split() IS MAGIC FOR AI
    # =================================================================
    print("\n🤖 WHY split() IS CRUCIAL FOR YOUR AI:")
    
    print("Before split() - Can't analyze individual words:")
    print(f"  '{hebrew_sentence}' ← One big chunk")
    
    print("After split() - Can analyze each word:")
    for i, word in enumerate(hebrew_words, 1):
        print(f"  {i}. '{word}' ← Separate analyzable word")
    
    # =================================================================
    # ADVANCED split() - Custom Separators
    # =================================================================
    print("\n🔧 ADVANCED split() - Custom Separators")
    
    # Sometimes Hebrew text has different separators
    verse_with_punctuation = "וַיֹּאמֶר,אֱלֹהִים;יְהִי:אוֹר"
    print(f"Text with punctuation: {verse_with_punctuation}")
    
    # Split by comma
    by_comma = verse_with_punctuation.split(',')
    print(f"Split by comma: {by_comma}")
    
    # Split by semicolon
    by_semicolon = verse_with_punctuation.split(';')
    print(f"Split by semicolon: {by_semicolon}")
    
    # =================================================================
    # REAL-WORLD HEBREW PROCESSING
    # =================================================================
    print("\n📚 REAL HEBREW TEXT PROCESSING")
    
    # Multi-verse text (like what your AI will process)
    multi_verse = """בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ
וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ
וַיֹּאמֶר אֱלֹהִים יְהִי אוֹר וַיְהִי אוֹר"""
    
    print("Multi-verse Hebrew text:")
    print(multi_verse)
    
    # Split by lines first
    verses = multi_verse.split('\n')
    print(f"\nSplit into {len(verses)} verses:")
    
    for i, verse in enumerate(verses, 1):
        print(f"\nVerse {i}: {verse}")
        words = verse.split()
        print(f"  Words: {words}")
        print(f"  Word count: {len(words)}")
    
    # =================================================================
    # BUILDING YOUR HEBREW AI PROCESSOR
    # =================================================================
    print("\n🎯 BUILDING YOUR HEBREW TEXT PROCESSOR")
    
    def process_hebrew_text(text):
        """
        This is how your AI will process Hebrew text!
        Real function you'll use in your Hebrew tutor.
        """
        # Handle multi-line text
        if '\n' in text:
            verses = text.split('\n')
            all_words = []
            for verse in verses:
                if verse.strip():  # Skip empty lines
                    words = verse.split()
                    all_words.extend(words)
        else:
            # Single line text
            all_words = text.split()
        
        return {
            'original_text': text,
            'total_words': len(all_words),
            'words': all_words,
            'unique_words': list(set(all_words)),
            'unique_count': len(set(all_words))
        }
    
    # Test your processor!
    result = process_hebrew_text(multi_verse)
    
    print(f"\n🤖 AI PROCESSING RESULTS:")
    print(f"Total words: {result['total_words']}")
    print(f"Unique words: {result['unique_count']}")
    print(f"All words: {result['words'][:5]}... (showing first 5)")
    print(f"Unique words: {result['unique_words'][:5]}... (showing first 5)")
    
    # =================================================================
    # CHALLENGE: Process Your Own Text
    # =================================================================
    print("\n🏆 CHALLENGE: Try Psalm 23:1")
    
    psalm = "יְהוָה רֹעִי לֹא אֶחְסָר"
    psalm_result = process_hebrew_text(psalm)
    
    print(f"Psalm text: {psalm}")
    print(f"Words: {psalm_result['words']}")
    print(f"Total: {psalm_result['total_words']} words")
    
    print("\n✅ NOW YOU UNDERSTAND split()!")
    print("• Breaks strings into lists of words")
    print("• Essential for analyzing individual Hebrew words")
    print("• Foundation of ALL text AI processing")
    print("• Your Hebrew AI will use this constantly!")

if __name__ == "__main__":
    demonstrate_split_method()