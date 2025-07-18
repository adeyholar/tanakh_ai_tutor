# lexicon_builder_demo.py - How to Add Words to Hebrew Lexicon
# Building your Hebrew AI vocabulary database!

def demonstrate_lexicon_building():
    print("📚 BUILDING YOUR HEBREW LEXICON!")
    print("=" * 40)
    
    # =================================================================
    # START WITH BASIC LEXICON
    # =================================================================
    print("\n🏗️ STARTING LEXICON:")
    
    # Our starting dictionary
    hebrew_lexicon = {
        "שָׁלוֹם": {"english": "peace/hello", "root": "שלם", "meaning": "complete/whole"},
        "אֱלֹהִים": {"english": "God", "root": "אלה", "meaning": "God/gods"}
    }
    
    print("Current words in lexicon:")
    for hebrew_word, info in hebrew_lexicon.items():
        print(f"  {hebrew_word} → {info['english']}")
    
    # =================================================================
    # METHOD 1: Add One Word at a Time
    # =================================================================
    print("\n➕ METHOD 1: Adding Single Words")
    
    # Add a new word using dictionary syntax
    hebrew_lexicon["תּוֹרָה"] = {
        "english": "Torah/Law", 
        "root": "ירה", 
        "meaning": "to teach/instruct"
    }
    
    print("✅ Added תּוֹרָה (Torah)")
    
    # Add another word
    hebrew_lexicon["אוֹר"] = {
        "english": "light", 
        "root": "אור", 
        "meaning": "to give light"
    }
    
    print("✅ Added אוֹר (light)")
    
    # =================================================================
    # METHOD 2: Add Multiple Words at Once
    # =================================================================
    print("\n➕ METHOD 2: Adding Multiple Words")
    
    # Create new words to add
    new_words = {
        "מַיִם": {"english": "water", "root": "מים", "meaning": "water"},
        "רוּחַ": {"english": "spirit/wind", "root": "רוח", "meaning": "breath/wind"},
        "יוֹם": {"english": "day", "root": "יום", "meaning": "day/time"}
    }
    
    # Add them all using update()
    hebrew_lexicon.update(new_words)
    print("✅ Added 3 new words using update()")
    
    # =================================================================
    # METHOD 3: Smart Adding with Checks
    # =================================================================
    print("\n🧠 METHOD 3: Smart Adding (Prevents Duplicates)")
    
    def add_word_safely(lexicon, hebrew, english, root, meaning):
        """Add word only if it doesn't exist"""
        if hebrew not in lexicon:
            lexicon[hebrew] = {
                "english": english,
                "root": root, 
                "meaning": meaning
            }
            print(f"✅ Added new word: {hebrew}")
            return True
        else:
            print(f"⚠️ Word {hebrew} already exists!")
            return False
    
    # Try to add a new word
    add_word_safely(hebrew_lexicon, "אֶרֶץ", "earth/land", "ארץ", "earth/land")
    
    # Try to add a duplicate
    add_word_safely(hebrew_lexicon, "שָׁלוֹם", "peace", "שלם", "complete")
    
    # =================================================================
    # SEE YOUR COMPLETE LEXICON
    # =================================================================
    print(f"\n📖 FINAL LEXICON ({len(hebrew_lexicon)} words):")
    
    for i, (hebrew_word, info) in enumerate(hebrew_lexicon.items(), 1):
        print(f"{i:2}. {hebrew_word} → {info['english']} (root: {info['root']})")
    
    # =================================================================
    # FOR YOUR HEBREW AI: File-Based Lexicon
    # =================================================================
    print("\n💾 FOR YOUR AI: Save/Load from File")
    
    import json
    
    # Save lexicon to file (for your AI to use later)
    def save_lexicon(lexicon, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lexicon, f, ensure_ascii=False, indent=2)
        print(f"✅ Lexicon saved to {filename}")
    
    # Load lexicon from file
    def load_lexicon(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ File {filename} not found")
            return {}
    
    # Demo saving (creates file in your project!)
    save_lexicon(hebrew_lexicon, "hebrew_lexicon.json")
    
    print("\n🎯 NOW YOU CAN:")
    print("• Add words one at a time")
    print("• Add multiple words at once") 
    print("• Check for duplicates")
    print("• Save/load your lexicon")
    print("• Build a growing Hebrew database for your AI!")

if __name__ == "__main__":
    demonstrate_lexicon_building()