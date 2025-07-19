# Hebrew AI Tutor Setup Guide

## Prerequisites
- Python 3.11+ 
- Git
- VS Code (recommended)
- 4GB+ free disk space for Hebrew data

## Installation

1. **Clone the repository:**
`ash
git clone <your-repo-url>
cd tanakh_ai_tutor
`

2. **Create virtual environment:**
`ash
conda create -n tanakh_ai_3.11.9 python=3.11.9
conda activate tanakh_ai_3.11.9
`

3. **Install dependencies:**
`ash
pip install -r requirements.txt
`

4. **Download Hebrew data:**
`ash
python scripts/download_lexicon.py
`

5. **Run the application:**
`ash
python main.py
`

## Directory Structure
See docs/ARCHITECTURE.md for detailed project structure.

## Development
Follow the 32-week curriculum in learning_exercises/ directory.
