# Quick test to see your Tanakh data structure
import json

with open(r"D:\AI\Projects\HEBREW TRAINING AI AGENT\TANACH\book\hebrew_bible_with_nikkud.json", "r", encoding="utf-8") as file:
    tanakh_data = json.load(file)
    
# Let's see what treasures you have!
print("Keys in your Tanakh file:", list(tanakh_data.keys())[:5])  # First 5 keys