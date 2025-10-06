"""
Setup and Installation Script for Document Q&A Chatbot
Run this after installing requirements to verify your setup
"""
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'openai',
        'fitz',  # PyMuPDF
        'docx',  # python-docx
        'chardet',
        'faiss',
        'chromadb',
        'numpy',
        'dotenv'
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        try:
            if package == 'fitz':
                __import__('fitz')
            elif package == 'docx':
                __import__('docx')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            installed.append(package)
        except ImportError:
            missing.append(package)
    
    print(f"\n📦 Package Check:")
    for pkg in installed:
        print(f"   ✅ {pkg}")
    
    if missing:
        print(f"\n❌ Missing packages:")
        for pkg in missing:
            print(f"   ❌ {pkg}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages installed!")
    return True


def check_directories():
    """Check if required directories exist"""
    base_dir = Path(__file__).parent
    required_dirs = [
        'src',
        'src/document_processor',
        'src/embedding',
        'src/vector_store',
        'src/retrieval',
        'src/llm',
        'src/ui',
        'data',
        'data/uploads',
        'data/vector_db'
    ]
    
    print("\n📁 Directory Check:")
    all_exist = True
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} (missing)")
            all_exist = False
            # Create missing directory
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"      Created {dir_path}")
    
    return all_exist


def check_env_file():
    """Check if .env file exists and has API key"""
    base_dir = Path(__file__).parent
    env_file = base_dir / '.env'
    env_example = base_dir / '.env.example'
    
    print("\n🔑 Environment Configuration:")
    
    if not env_file.exists():
        print("   ⚠️  .env file not found")
        if env_example.exists():
            print("   💡 Copy .env.example to .env and add your API key:")
            print("      copy .env.example .env")
        else:
            print("   💡 Create a .env file with:")
            print("      OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=' in content:
            # Check if it's not the placeholder
            if 'your_openai_api_key_here' in content or 'your_api_key_here' in content:
                print("   ⚠️  .env file exists but API key is placeholder")
                print("   💡 Update .env with your actual OpenAI API key")
                return False
            print("   ✅ .env file exists with API key")
            return True
        else:
            print("   ⚠️  .env file missing OPENAI_API_KEY")
            return False


def check_files():
    """Check if core files exist"""
    base_dir = Path(__file__).parent
    core_files = [
        'src/config.py',
        'src/ui/streamlit_app.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("\n📄 Core Files Check:")
    all_exist = True
    for file_path in core_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            all_exist = False
    
    return all_exist


def main():
    """Run all setup checks"""
    print("=" * 60)
    print("🚀 Document Q&A Chatbot - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Directories", check_directories()),
        ("Core Files", check_files()),
        ("Environment", check_env_file())
    ]
    
    print("\n" + "=" * 60)
    print("📊 Setup Summary:")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 Setup Complete! You're ready to go!")
        print("\n🚀 Next Steps:")
        print("   1. Make sure your .env has a valid OpenAI API key")
        print("   2. Run: streamlit run src/ui/streamlit_app.py")
        print("   3. Upload documents and start chatting!")
    else:
        print("⚠️  Setup incomplete. Please fix the issues above.")
        print("\n💡 Quick Fix:")
        print("   1. pip install -r requirements.txt")
        print("   2. copy .env.example .env")
        print("   3. Edit .env and add your OpenAI API key")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
