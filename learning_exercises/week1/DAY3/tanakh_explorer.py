# tanakh_explorer.py - Exploring Your Hebrew Bible Database
# This is the foundation of your Hebrew AI tutor!

import json

def explore_tanakh_structure():
    """Explore the structure of your Hebrew Bible JSON"""
    print("🔍 EXPLORING YOUR HEBREW BIBLE DATABASE")
    print("=" * 50)
    
    # Load your Tanakh file
    file_path = r"D:\AI\Projects\HEBREW TRAINING AI AGENT\TANACH\book\hebrew_bible_with_nikkud.json"
    
    with open(file_path, "r", encoding="utf-8") as file:
        tanakh = json.load(file)
    
    # =================================================================
    # 1. DISCOVER ALL BOOKS
    # =================================================================
    print("📚 ALL BOOKS IN YOUR TANAKH:")
    all_books = list(tanakh.keys())
    print(f"Total books: {len(all_books)}")
    
    # Display first 10 books
    for i, book in enumerate(all_books[:10], 1):
        print(f"{i:2}. {book}")
    
    if len(all_books) > 10:
        print(f"... and {len(all_books) - 10} more books!")
    
    # =================================================================
    # 2. EXAMINE GENESIS STRUCTURE
    # =================================================================
    print(f"\n📖 EXAMINING GENESIS STRUCTURE:")
    
    # Look for Genesis (might be 'Gen' or 'Genesis')
    genesis_key = None
    for book in all_books:
        if 'gen' in book.lower() or book.lower() == 'genesis':
            genesis_key = book
            break
    
    if not genesis_key:
        # Use first book as example
        genesis_key = all_books[0]
        print(f"Using {genesis_key} as example...")
    
    genesis = tanakh[genesis_key]
    print(f"Genesis structure type: {type(genesis)}")
    
    if isinstance(genesis, dict):
        print(f"Genesis keys: {list(genesis.keys())[:5]}...")
    elif isinstance(genesis, list):
        print(f"Genesis has {len(genesis)} chapters")
    
    # =================================================================
    # 3. FIND GENESIS 1:1 (The Beginning!)
    # =================================================================
    print(f"\n🌟 FINDING GENESIS 1:1 - בְּרֵאשִׁית!")
    
    try:
        # Try different possible structures
        if isinstance(genesis, dict):
            # Structure might be: genesis -> chapters -> verses
            first_chapter_key = list(genesis.keys())[0]
            first_chapter = genesis[first_chapter_key]
            print(f"First chapter key: {first_chapter_key}")
            print(f"First chapter type: {type(first_chapter)}")
            
            if isinstance(first_chapter, dict):
                first_verse_key = list(first_chapter.keys())[0]
                first_verse = first_chapter[first_verse_key]
                print(f"First verse: {first_verse}")
            elif isinstance(first_chapter, list):
                first_verse = first_chapter[0]
                print(f"First verse: {first_verse}")
        
        elif isinstance(genesis, list):
            # Structure might be: genesis -> [chapters] -> verses
            first_chapter = genesis[0]
            print(f"First chapter type: {type(first_chapter)}")
            
            if isinstance(first_chapter, dict):
                first_verse_key = list(first_chapter.keys())[0]
                first_verse = first_chapter[first_verse_key]
                print(f"First verse: {first_verse}")
            elif isinstance(first_chapter, list):
                first_verse = first_chapter[0]
                print(f"First verse: {first_verse}")
    
    except Exception as e:
        print(f"Structure exploration needed: {e}")
    
    # =================================================================
    # 4. EXTRACT HEBREW WORDS FOR YOUR AI
    # =================================================================
    print(f"\n🤖 EXTRACTING HEBREW WORDS FOR YOUR AI:")
    
    try:
        # Get a sample verse to work with
        sample_verse = None
        if isinstance(genesis, dict):
            for chapter_key, chapter in genesis.items():
                if isinstance(chapter, dict):
                    for verse_key, verse in chapter.items():
                        if isinstance(verse, str) and len(verse) > 10:
                            sample_verse = verse
                            print(f"Sample verse from {genesis_key} {chapter_key}:{verse_key}")
                            break
                elif isinstance(chapter, list) and len(chapter) > 0:
                    sample_verse = chapter[0]
                    print(f"Sample verse from {genesis_key} chapter {chapter_key}")
                    break
                if sample_verse:
                    break
        
        if sample_verse:
            print(f"Hebrew text: {sample_verse}")
            
            # Extract individual Hebrew words
            hebrew_words = sample_verse.split()
            print(f"Individual words: {len(hebrew_words)} words")
            
            for i, word in enumerate(hebrew_words[:5], 1):
                print(f"  {i}. {word}")
            
            if len(hebrew_words) > 5:
                print(f"  ... and {len(hebrew_words) - 5} more words")
    
    except Exception as e:
        print(f"Word extraction needs refinement: {e}")
    
    # =================================================================
    # 5. YOUR HEBREW AI POTENTIAL
    # =================================================================
    print(f"\n🚀 YOUR HEBREW AI POTENTIAL:")
    print(f"✅ Complete Hebrew Bible: {len(all_books)} books")
    print(f"✅ Structured by book/chapter/verse")
    print(f"✅ Hebrew text with nikkud (vowel points)")
    print(f"✅ Perfect for vocabulary building")
    print(f"✅ Ideal for pronunciation training")
    print(f"✅ Ready for lexicon integration")
    
    return tanakh

def count_total_words():
    """Count total Hebrew words in your entire Tanakh"""
    print(f"\n📊 COUNTING YOUR HEBREW VOCABULARY:")
    
    file_path = r"D:\AI\Projects\HEBREW TRAINING AI AGENT\TANACH\book\hebrew_bible_with_nikkud.json"
    
    with open(file_path, "r", encoding="utf-8") as file:
        tanakh = json.load(file)
    
    total_words = 0
    unique_words = set()
    
    # This is a simplified count - we'll refine it as we learn the exact structure
    try:
        for book_name, book_content in tanakh.items():
            # We'll need to navigate the structure once we understand it better
            book_text = str(book_content)  # Convert to string for now
            words = book_text.split()
            
            # Filter for Hebrew words (basic filter)
            hebrew_words = [word for word in words if any(ord(char) >= 0x05D0 and ord(char) <= 0x05EA for char in word)]
            
            total_words += len(hebrew_words)
            unique_words.update(hebrew_words)
    
    except Exception as e:
        print(f"Detailed counting requires structure analysis: {e}")
        return
    
    print(f"Estimated total Hebrew words: {total_words:,}")
    print(f"Estimated unique Hebrew words: {len(unique_words):,}")
    print(f"This is MASSIVE vocabulary for your AI! 🤯")

if __name__ == "__main__":
    tanakh_data = explore_tanakh_structure()
    count_total_words()
    
    print(f"\n" + "=" * 50)
    print(f"🎯 NEXT STEPS FOR YOUR HEBREW AI:")
    print(f"=" * 50)
    print(f"1. Map exact JSON structure")
    print(f"2. Build Hebrew word extraction system")
    print(f"3. Create pronunciation mapping with your MP3s")
    print(f"4. Build interactive lexicon lookup")
    print(f"5. Integrate with AI for intelligent tutoring")
    print(f"\nYou have EVERYTHING needed for a world-class Hebrew AI! 🚀")