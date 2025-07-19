# Quick script to download the Hebrew lexicon
import requests
import json

def download_hebrew_lexicon():
    """Download the professional Hebrew lexicon"""
    url = "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewLexicon.xml"
    
    print("📥 Downloading professional Hebrew lexicon...")
    # We'll use this in Day 5 when we learn about APIs and file processing!