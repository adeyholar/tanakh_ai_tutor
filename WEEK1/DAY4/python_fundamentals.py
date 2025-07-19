# python_fundamentals.py - Understanding 'def' and Python Code Organization
# Essential concepts for writing real Python applications

def explain_def_keyword():
    """
    This explains what 'def' means and why it's crucial
    """
    print("🔧 UNDERSTANDING 'def' - The Foundation of Python Code")
    print("=" * 55)
    
    print("""
📝 WHAT IS 'def'?
• 'def' stands for 'define'
• It creates a FUNCTION - a reusable piece of code
• Think of it as creating a custom tool you can use over and over
    """)
    
    # =================================================================
    # WITHOUT FUNCTIONS (Your Current Approach)
    # =================================================================
    print("\n❌ WITHOUT FUNCTIONS - Repetitive Code:")
    print("If you want to process Hebrew words multiple times...")
    
    # Repetitive approach
    hebrew_words1 = ["שָׁלוֹם", "אֱלֹהִים"]
    print(f"Processing list 1: {hebrew_words1}")
    total1 = len(hebrew_words1)
    print(f"Count: {total1}")
    
    hebrew_words2 = ["בְּרֵאשִׁית", "בָּרָא"]  
    print(f"Processing list 2: {hebrew_words2}")
    total2 = len(hebrew_words2)
    print(f"Count: {total2}")
    
    print("😩 Problem: You're writing the SAME code over and over!")
    
    # =================================================================
    # WITH FUNCTIONS (Better Approach)
    # =================================================================
    print("\n✅ WITH FUNCTIONS - Reusable Code:")
    
    def process_hebrew_words(word_list):
        """This function can process ANY list of Hebrew words"""
        print(f"Processing: {word_list}")
        count = len(word_list)
        print(f"Count: {count}")
        return count
    
    # Now use the function multiple times
    result1 = process_hebrew_words(["שָׁלוֹם", "אֱלֹהִים"])
    result2 = process_hebrew_words(["בְּרֵאשִׁית", "בָּרָא"])
    result3 = process_hebrew_words(["יְהוָה", "רֹעִי", "לֹא", "אֶחְסָר"])
    
    print(f"😊 Much better! One function, multiple uses!")

def demonstrate_function_benefits():
    """Show why functions are essential for your Hebrew AI"""
    print("\n🚀 WHY FUNCTIONS ARE ESSENTIAL FOR YOUR HEBREW AI:")
    print("=" * 50)
    
    # =================================================================
    # FUNCTION FOR HEBREW WORD ANALYSIS
    # =================================================================
    def analyze_hebrew_word(word):
        """Analyze a single Hebrew word - reusable component"""
        analysis = {
            'word': word,
            'length': len(word),
            'has_vowels': any(char in 'ֱֲֳִֵֶַָֹֻ' for char in word),
            'character_count': len([c for c in word if c.isalpha()])
        }
        return analysis
    
    print("📊 Hebrew Word Analysis Function:")
    test_words = ["בְּרֵאשִׁית", "אֱלֹהִים", "שָׁלוֹם"]
    
    for word in test_words:
        result = analyze_hebrew_word(word)
        print(f"  {word}: {result['length']} chars, vowels: {result['has_vowels']}")
    
    # =================================================================
    # FUNCTION FOR FILE OPERATIONS
    # =================================================================
    def save_hebrew_data(data, filename):
        """Save Hebrew data to file - reusable for any data"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                if isinstance(data, list):
                    for item in data:
                        file.write(f"{item}\n")
                else:
                    file.write(str(data))
            print(f"✅ Saved data to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving: {e}")
            return False
    
    # Use the function for different data
    save_hebrew_data(test_words, "hebrew_words.txt")
    save_hebrew_data(["Genesis 1:1", "Psalm 23:1"], "verses.txt")
    
    print("💡 One function, multiple uses - that's the power!")

def explain_function_parts():
    """Break down the parts of a function"""
    print("\n🔍 ANATOMY OF A FUNCTION:")
    print("=" * 30)
    
    print("""
def function_name(parameters):
    ↑        ↑          ↑
    |        |          └─ Input values (optional)
    |        └─ Name you choose (descriptive!)
    └─ 'def' keyword starts function definition
    
    \"\"\"Optional description of what function does\"\"\"
    
    # Code that does the work
    result = some_calculation
    
    return result  # Send result back (optional)
    ↑
    └─ Give back a value to whoever called the function
    """)

def demonstrate_real_world_functions():
    """Show functions you'll actually use in your Hebrew AI"""
    print("\n🤖 REAL FUNCTIONS FOR YOUR HEBREW AI:")
    print("=" * 40)
    
    def load_hebrew_lexicon(file_path):
        """Load Hebrew lexicon from the OpenScriptures data"""
        # This would load your actual lexicon file
        print(f"Loading lexicon from: {file_path}")
        # Simplified for demo
        return {"שָׁלוֹם": "peace", "אֱלֹהִים": "God"}
    
    def lookup_hebrew_word(word, lexicon):
        """Look up Hebrew word in lexicon"""
        return lexicon.get(word, "Word not found")
    
    def clean_hebrew_text(text):
        """Remove cantillation marks from Hebrew text"""
        cantillation = "ֽ֑֖֣֥׃"
        clean_text = text
        for mark in cantillation:
            clean_text = clean_text.replace(mark, "")
        return clean_text
    
    def extract_words_from_verse(verse):
        """Extract individual words from Hebrew verse"""
        if isinstance(verse, list):
            # Your Tanakh format: already a list of words
            return [clean_hebrew_text(word) for word in verse]
        else:
            # String format: split into words
            return verse.split()
    
    # Demo using these functions together
    print("🔧 Using Functions Together:")
    
    lexicon = load_hebrew_lexicon("hebrew_lexicon.json")
    sample_verse = ['בְּרֵאשִׁ֖ית', 'בָּרָ֣א', 'אֱלֹהִ֑ים']
    
    clean_words = extract_words_from_verse(sample_verse)
    print(f"Clean words: {clean_words}")
    
    for word in clean_words:
        meaning = lookup_hebrew_word(word, lexicon)
        print(f"  {word} → {meaning}")
    
    print("✨ Each function does ONE job well, but together they're powerful!")

def explain_main_and_init():
    """Explain __main__ and __init__ that you've seen"""
    print("\n🎯 SPECIAL PYTHON PATTERNS:")
    print("=" * 30)
    
    print("""
📌 if __name__ == "__main__":
   • This runs ONLY when you run the file directly
   • Not when file is imported by another program
   • Think of it as the "start here" section
   
📌 __init__ (you'll learn more later):
   • Special function for creating objects/classes
   • Sets up initial values when creating something
   • More advanced - we'll cover this in Week 7-8
    """)

if __name__ == "__main__":
    print("🐍 PYTHON FUNDAMENTALS: Functions and Code Organization")
    print("Essential knowledge for your Hebrew AI development")
    print("=" * 65)
    
    explain_def_keyword()
    demonstrate_function_benefits()
    explain_function_parts()
    demonstrate_real_world_functions()
    explain_main_and_init()
    
    print("\n" + "=" * 65)
    print("🎓 KEY TAKEAWAYS:")
    print("✅ 'def' creates reusable functions")
    print("✅ Functions eliminate repetitive code")  
    print("✅ Functions make code organized and testable")
    print("✅ Functions are essential for real applications")
    print("✅ Your Hebrew AI will be built with many functions working together")
    
    print("\n🚀 NEXT: Let's download that Hebrew lexicon and build real functions!")
    print("Ready to move from toy examples to professional Hebrew AI components?")
    print("=" * 65)