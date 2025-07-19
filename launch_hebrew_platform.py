# launch_hebrew_platform.py
"""
Professional Hebrew AI Learning Platform Launcher
Week 3 Day 5 - Fixed Import Issues
"""

import sys
import os
from pathlib import Path
import subprocess

def setup_python_path():
    """Setup Python path for proper module imports"""
    project_root = Path(__file__).parent.absolute()
    
    # Add project directories to Python path
    paths_to_add = [
        str(project_root),
        str(project_root / "src"),
        str(project_root / "src" / "core"),
        str(project_root / "src" / "web")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Set PYTHONPATH environment variable
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    new_pythonpath = os.pathsep.join(paths_to_add)
    if current_pythonpath:
        new_pythonpath = f"{new_pythonpath}{os.pathsep}{current_pythonpath}"
    
    os.environ['PYTHONPATH'] = new_pythonpath
    
    print(f"✅ Python path configured:")
    for path in paths_to_add:
        print(f"   📁 {path}")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = {
        'fastapi': 'FastAPI web framework',
        'uvicorn': 'ASGI server',
        'jinja2': 'Template engine',
        'torch': 'PyTorch for AI models',
        'transformers': 'Hugging Face transformers',
        'numpy': 'Numerical computing'
    }
    
    missing = []
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'src/core/hebrew_analyzers.py',
        'src/core/enhanced_alephbert_analyzer.py',
        'src/core/hebrew_database.py',
        'src/core/tanakh_learning_session.py',
        'src/web/hebrew_api.py',
        'data/tanakh/hebrew_bible_with_nikkud.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (MISSING)")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def create_directories():
    """Create required directories"""
    directories = [
        'src/web/templates',
        'src/web/static/css',
        'src/web/static/js',
        'data',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure verified")

def main():
    """Main launcher function"""
    print("🚀 Hebrew AI Learning Platform Launcher")
    print("=" * 50)
    
    # Setup Python path
    setup_python_path()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing dependencies. Please install them and try again.")
        return False
    
    # Check file structure
    if not check_file_structure():
        print("\n❌ Missing required files. Please ensure all components are in place.")
        return False
    
    # Create directories
    create_directories()
    
    print("\n🌐 Starting Hebrew AI Learning Platform...")
    print("📖 Features:")
    print("   - Hebrew word analysis with Enhanced AlephBERT")
    print("   - Biblical verse study with AI insights")
    print("   - User progress tracking and analytics")
    print("   - REST API for programmatic access")
    print("\n🔗 Platform will be available at:")
    print("   - Main Interface: http://localhost:8000")
    print("   - API Documentation: http://localhost:8000/api/docs")
    print("\n⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        # Import and run the FastAPI app
        setup_python_path()  # Ensure path is set
        
        # Try to import and verify our modules work
        print("🔍 Testing module imports...")
        try:
            from src.core.hebrew_analyzers import HebrewAnalyzer
            print("   ✅ Hebrew analyzers imported")
        except ImportError as e:
            print(f"   ❌ Hebrew analyzers import failed: {e}")
            return False
        
        # Launch with uvicorn
        import uvicorn
        
        # Set environment variables for the web app
        os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
        
        uvicorn.run(
            "src.web.hebrew_api:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Hebrew AI Platform stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error starting platform: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Verify all source files are present")
        print("3. Check Python path configuration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
