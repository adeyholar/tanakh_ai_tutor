# create_hebrew_ai_structure.ps1
# PowerShell script to create complete Hebrew AI project structure
# Run this in your tanakh_ai_tutor directory

Write-Host "🏗️ Creating Hebrew AI Project Structure..." -ForegroundColor Green
Write-Host "Building professional directory layout..." -ForegroundColor Yellow

# Define all folders to create
$folders = @(
    # Main source code structure
    "src",
    "src\core",
    "src\ai", 
    "src\ai\agents",
    "src\ai\models",
    "src\ai\rag",
    "src\ui",
    "src\ui\components",
    "src\ui\static",
    "src\utils",
    
    # Data directories
    "data",
    "data\tanakh",
    "data\lexicon", 
    "data\audio",
    "data\audio\pronunciation",
    "data\audio\readings",
    "data\embeddings",
    
    # Development directories
    "tests",
    "docs",
    "scripts",
    "config",
    
    # Learning and reference
    "learning_exercises",
    "learning_exercises\week1",
    "learning_exercises\week2",
    "learning_exercises\week3",
    "learning_exercises\week4",
    "learning_exercises\week5",
    "learning_exercises\week6"
)

# Create all folders
foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "✅ Created: $folder" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Already exists: $folder" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🐍 Creating Python __init__.py files..." -ForegroundColor Cyan

# Python package init files
$initFiles = @(
    "src\__init__.py",
    "src\core\__init__.py", 
    "src\ai\__init__.py",
    "src\ai\agents\__init__.py",
    "src\ai\models\__init__.py",
    "src\ai\rag\__init__.py",
    "src\ui\__init__.py",
    "src\utils\__init__.py"
)

# Create __init__.py files
foreach ($initFile in $initFiles) {
    if (!(Test-Path $initFile)) {
        New-Item -ItemType File -Path $initFile -Force | Out-Null
        Add-Content -Path $initFile -Value "# Hebrew AI Package"
        Write-Host "✅ Created: $initFile" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "📁 Creating essential project files..." -ForegroundColor Cyan

# Create essential project files
$projectFiles = @{
    "README.md" = @"
# Hebrew AI Tutor - Agentic Hebrew Learning System

A comprehensive AI-powered Hebrew learning application with:
- Voice recognition and pronunciation coaching
- Interactive reading with word highlighting  
- RAG-based Tanakh Q&A system (HebRabbAI)
- Adaptive learning and memorization

## Project Structure
- `src/` - Main application source code
- `data/` - Hebrew texts, lexicons, and audio files
- `tests/` - Unit tests for all components
- `docs/` - Documentation and API references

## Setup
See `docs/SETUP.md` for installation instructions.

## Development
This project is built using a 32-week curriculum from beginner to Hebrew AI expert.
"@

    "requirements.txt" = @"
# Hebrew AI Tutor Dependencies
# Install with: pip install -r requirements.txt

# Core Python packages
requests>=2.31.0
beautifulsoup4>=4.12.0
pandas>=2.0.0

# File processing
json5>=0.9.0
xmltodict>=0.13.0

# Hebrew text processing
hebrew-tokenizer>=2.3.0
transliterate>=1.10.0

# Audio processing (for future weeks)
# speechrecognition>=3.10.0
# pydub>=0.25.0
# pygame>=2.5.0

# AI/ML (for future weeks)  
# openai>=1.0.0
# langchain>=0.1.0
# transformers>=4.30.0

# Web interface (for future weeks)
# streamlit>=1.28.0
# flask>=2.3.0

# Development tools
pytest>=7.4.0
black>=23.0.0
"@

    "main.py" = @"
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
"@

    "config\settings.json" = @"
{
  "project": {
    "name": "Hebrew AI Tutor",
    "version": "1.0.0",
    "description": "Agentic AI Hebrew Learning System"
  },
  "data_paths": {
    "tanakh_file": "data/tanakh/hebrew_bible_with_nikkud.json",
    "lexicon_dir": "data/lexicon/",
    "audio_dir": "data/audio/",
    "embeddings_dir": "data/embeddings/"
  },
  "ai_settings": {
    "model_provider": "openai",
    "embedding_model": "text-embedding-ada-002",
    "chat_model": "gpt-4"
  },
  "learning_settings": {
    "difficulty_levels": ["beginner", "intermediate", "advanced"],
    "pronunciation_threshold": 0.85,
    "progress_save_interval": 300
  }
}
"@

    "docs\SETUP.md" = @"
# Hebrew AI Tutor Setup Guide

## Prerequisites
- Python 3.11+ 
- Git
- VS Code (recommended)
- 4GB+ free disk space for Hebrew data

## Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd tanakh_ai_tutor
```

2. **Create virtual environment:**
```bash
conda create -n tanakh_ai_3.11.9 python=3.11.9
conda activate tanakh_ai_3.11.9
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download Hebrew data:**
```bash
python scripts/download_lexicon.py
```

5. **Run the application:**
```bash
python main.py
```

## Directory Structure
See `docs/ARCHITECTURE.md` for detailed project structure.

## Development
Follow the 32-week curriculum in `learning_exercises/` directory.
"@

    "scripts\download_lexicon.py" = @"
#!/usr/bin/env python3
"""
Download Hebrew lexicon data from OpenScriptures
"""
import requests
import json
import os

def download_hebrew_lexicon():
    '''Download professional Hebrew lexicon'''
    print("📥 Downloading Hebrew lexicon from OpenScriptures...")
    
    # Create lexicon directory if it doesn't exist
    os.makedirs("data/lexicon", exist_ok=True)
    
    # Future: Download actual lexicon files
    print("ℹ️  Lexicon download will be implemented in Week 2")
    print("✅ Ready for lexicon integration!")

if __name__ == "__main__":
    download_hebrew_lexicon()
"@
}

# Create project files
foreach ($file in $projectFiles.Keys) {
    if (!(Test-Path $file)) {
        $directory = Split-Path $file -Parent
        if ($directory -and !(Test-Path $directory)) {
            New-Item -ItemType Directory -Path $directory -Force | Out-Null
        }
        
        Set-Content -Path $file -Value $projectFiles[$file] -Encoding UTF8
        Write-Host "✅ Created: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Already exists: $file" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📊 Project Structure Summary:" -ForegroundColor Magenta
Write-Host "┌─ src/                 (Source code)" -ForegroundColor White
Write-Host "├─ data/               (Hebrew texts & audio)" -ForegroundColor White  
Write-Host "├─ tests/              (Unit tests)" -ForegroundColor White
Write-Host "├─ docs/               (Documentation)" -ForegroundColor White
Write-Host "├─ scripts/            (Utility scripts)" -ForegroundColor White
Write-Host "├─ config/             (Configuration)" -ForegroundColor White
Write-Host "├─ learning_exercises/ (Weekly exercises)" -ForegroundColor White
Write-Host "├─ main.py            (Application entry)" -ForegroundColor White
Write-Host "└─ requirements.txt    (Dependencies)" -ForegroundColor White

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Move your Tanakh JSON to data/tanakh/" -ForegroundColor White
Write-Host "2. Move your week exercises to learning_exercises/" -ForegroundColor White  
Write-Host "3. Run: python main.py" -ForegroundColor White
Write-Host "4. Continue with Week 1 Day 5!" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Professional Hebrew AI project structure created!" -ForegroundColor Green
Write-Host "Ready to build world-class Hebrew learning software! ✨" -ForegroundColor Yellow