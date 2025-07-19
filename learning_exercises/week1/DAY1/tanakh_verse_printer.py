# Simple Python script using variables to print Biblical Hebrew Tanakh verses
# Part of your Biblical Hebrew Tanakh Agentic AI Tutor
# Note: Hebrew is right-to-left; \u202B ensures RTL display
# Future capstone goal: Develop a tutor with read-along, feedback, BDB, toggles

# Store verses and roots in variables
verse_genesis = "\u202Bבְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ"
root_genesis = "ב-ר-א (meaning 'create')"
verse_deut = "\u202Bשְׁמַע יִשְׂרָאֵל יְהוָה אֱלֹהֵינוּ יְהוָה אֶחָד"
root_deut = "שׁ-מ-ע (meaning 'hear')"

# Print the verses and their roots
print("Tanakh Verse (Genesis 1:1):")
print(verse_genesis)
print("Root word:", root_genesis)
print("\nTanakh Verse (Deuteronomy 6:4):")
print(verse_deut)
print("Root word:", root_deut)