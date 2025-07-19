#!/usr/bin/env python3
"""
Hebrew AI Tutor - Main Application Entry Point
A comprehensive Agentic AI system for learning biblical Hebrew
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🔥 Hebrew AI Tutor Starting...")
    print("Welcome to your Agentic Hebrew Learning System!")
    
    # Future: Initialize all AI components
    # from src.core.hebrew_processor import HebrewProcessor
    # from src.ai.agents.pronunciation_coach import PronunciationCoach
    # from src.ai.agents.rabbi_qa import HebRabbAI
    
    print("✅ System initialized successfully!")
    print("Ready to begin Hebrew learning journey! 🚀")

if __name__ == "__main__":
    main()
