# Super simple Python script for novices to print Biblical Hebrew Tanakh verses
# Starting point for your Biblical Hebrew Tanakh Agentic AI Tutor
# Note: Hebrew is right-to-left; \u202B ensures RTL display
# Future capstone: Add read-along, repeat-after, feedback, BDB lookup, root/suffix toggles

# Verse from Genesis 1:1 (Biblical Hebrew with nikkud)
verse1 = "\u202Bבְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ"
message1 = "Root word: ב-ר-א (meaning 'create')"

# Verse from Deuteronomy 6:4 (Biblical Hebrew with nikkud)
verse2 = "\u202Bשְׁמַע יִשְׂרָאֵל יְהוָה אֱלֹהֵינוּ יְהוָה אֶחָד"
message2 = "Root word: שׁ-מ-ע (meaning 'hear')"

# Print the verses and messages about the roots
print("Tanakh Verse (Genesis 1:1):")
print(verse1)
print(message1)
print("\nTanakh Verse (Deuteronomy 6:4):")
print(verse2)
print(message2)