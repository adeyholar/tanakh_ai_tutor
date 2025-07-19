# Your challenge: Create this system yourself!

# Hebrew words from Genesis 1:1
hebrew_words = ["בְּרֵאשִׁית", "בָּרָא", "אֱלֹהִים", "אֵת", "הַשָּׁמַיִם", "וְאֵת", "הָאָרֶץ"]

# Can you write code to:
# 1. Count total words
total_words = len(hebrew_words)
print (f"Total words: (total_words)")

# 2. Display each word with a number
    # I find it difficut to figure out.

# 3. Add a new Hebrew word to the list
hebrew_words.append("וְהָאָרֶץ")
print(f"Updated word list: {hebrew_words}")

# 4. Find if a specific word exists
     # I don't know how.

# 5. Save the word list to a file
file = open ("hebrew_words.txt", "w")
file.write("\nhebrew_words")
file.close()

print (hebrew_words)
