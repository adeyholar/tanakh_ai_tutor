# strings_vs_lists_demo.py - Understanding Strings vs Lists for Hebrew AI
# Let's see the difference with REAL Hebrew text processing!

def demonstrate_strings_vs_lists():
    print("🔤 STRINGS vs LISTS - Hebrew AI Style!")
    print("=" * 50)
    
    # =================================================================
    # STRINGS: Complete text as ONE piece
    # =================================================================
    print("\n📝 STRINGS - Complete Hebrew Text")
    
    # This is a STRING - one complete piece of text
    hebrew_string = "שָׁלוֹם עֲלֵיכֶם"
    print(f"String: {hebrew_string}")
    print(f"Type: {type(hebrew_string)}")
    print(f"Length: {len(hebrew_string)} characters")
    
    # You can access individual characters by position
    print(f"First character: {hebrew_string[0]}")
    print(f"Last character: {hebrew_string[-1]}")
    
    # =================================================================
    # LISTS: Multiple separate items
    # =================================================================
    print("\n📚 LISTS - Separate Hebrew Words")
    
    # This is a LIST - multiple separate items
    hebrew_list = ["שָׁלוֹם", "עֲלֵיכֶם"]
    print(f"List: {hebrew_list}")
    print(f"Type: {type(hebrew_list)}")
    print(f"Length: {len(hebrew_list)} items")
    
    # You can access individual items by position
    print(f"First word: {hebrew_list[0]}")
    print(f"Second word: {hebrew_list[1]}")
    
    # =================================================================
    # THE MAGIC: Converting Between Them!
    # =================================================================
    print("\n✨ CONVERTING: String ↔ List")
    
    # String to List (splitting)
    sentence = "בְּרֵאשִׁית בָּרָא אֱלֹהִים"
    words = sentence.split()  # This converts string to list!
    print(f"Original string: {sentence}")
    print(f"After split(): {words}")
    print(f"Now it's a: {type(words)}")
    
    # List to String (joining)
    rejoined = " ".join(words)  # This converts list back to string!
    print(f"Rejoined string: {rejoined}")
    
    # =================================================================
    # WHY THIS MATTERS FOR YOUR HEBREW AI
    # =================================================================
    print("\n🤖 FOR YOUR HEBREW AI:")
    print("• String = Complete verse or sentence")
    print("• List = Individual words you can analyze")
    print("• split() = Break sentence into analyzable words")
    print("• join() = Rebuild sentence after processing")

if __name__ == "__main__":
    demonstrate_strings_vs_lists()