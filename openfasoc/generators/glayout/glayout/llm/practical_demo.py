#!/usr/bin/env python3
"""
Practical LLM Demo Script
=========================

This script provides a working demonstration of the prompt → strict syntax flow.
Run this from the glayout/llm directory.

Usage:
    export HF_TOKEN='your_huggingface_token'
    python practical_demo.py
"""

import os
import sys

def check_environment():
    """Check if we're in the right environment"""
    current_dir = os.getcwd()
    
    if not current_dir.endswith('glayout/llm'):
        print("❌ Please run this script from the glayout/llm directory")
        print(f"Current directory: {current_dir}")
        print("Expected to end with: glayout/llm")
        return False
    
    # Check for key files
    required_files = ['train_and_run.py', 'rag.py', 'manage_data.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ Environment check passed")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'transformers', 'torch', 'langchain', 'sentence_transformers', 
        'peft', 'trl', 'chromadb'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.ml.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def get_hf_token():
    """Get HuggingFace token"""
    token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_HUB_TOKEN')
    
    if not token:
        print("\n🔑 HuggingFace Token Required")
        print("=" * 40)
        print("1. Go to: https://huggingface.co/settings/tokens")
        print("2. Create a new token with 'Read' permission")
        print("3. Set it as environment variable:")
        print("   export HF_TOKEN='your_token_here'")
        print("\nOr enter it now:")
        
        token = input("HF Token: ").strip()
        
        if not token:
            print("❌ No token provided")
            return None
    
    return token

def test_basic_import():
    """Test if we can import the LLM modules"""
    try:
        from train_and_run import GlayoutLLMSessionHandler
        print("✅ Successfully imported LLM modules")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and PYTHONPATH is set")
        return False

def run_mini_demo(hf_token):
    """Run a minimal demonstration"""
    print("\n🚀 Mini LLM Demo")
    print("=" * 30)
    
    try:
        from train_and_run import GlayoutLLMSessionHandler
        
        print("📡 Initializing LLM session...")
        print("   (This will download models on first run - may take time)")
        
        # Initialize with the smallest model for demo
        session = GlayoutLLMSessionHandler(
            model="7b",  # Use 7b model
            accesstoken=hf_token
        )
        
        print("✅ LLM session initialized!")
        
        # Single test prompt
        test_prompt = "Create a simple NMOS current mirror"
        
        print(f"\n📝 Test prompt: '{test_prompt}'")
        print("🤔 Generating strict syntax...")
        
        result = session.generate(test_prompt)
        
        print("\n📄 Generated Strict Syntax:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        # Save result
        output_file = "demo_current_mirror.convo"
        with open(output_file, "w") as f:
            f.write("DemoCurrentMirror\n")
            f.write(result)
        
        print(f"\n💾 Output saved to: {output_file}")
        print("\n✅ Demo completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nPossible issues:")
        print("- Invalid HF token")
        print("- Network/download issues")
        print("- Insufficient memory/disk space")
        print("- Missing dependencies")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n🎯 Next Steps")
    print("=" * 20)
    print("1. Try more prompts:")
    print("   - 'Make a P-type differential pair'")
    print("   - 'Create a common source amplifier'")
    print("   - 'Build an inverter with CMOS'")
    print()
    print("2. Convert to layout:")
    print("   ```python")
    print("   from glayout.syntaxer.dynamic_load import run_session")
    print("   code = run_session('demo_current_mirror.convo', restore_and_exit=True)")
    print("   ```")
    print()
    print("3. Explore the system:")
    print("   - Check rag_data/ for knowledge base")
    print("   - Look at syntax_data/ for training examples")  
    print("   - Read FLOW_GUIDE.md for complete documentation")

def main():
    """Main function"""
    print("🔬 OpenFASoC LLM Practical Demo")
    print("=" * 40)
    
    # Environment checks
    if not check_environment():
        return 1
        
    if not check_dependencies():
        return 1
    
    # Test imports
    if not test_basic_import():
        return 1
    
    # Get HF token
    hf_token = get_hf_token()
    if not hf_token:
        return 1
    
    # Run demo
    print("\n⚠️  WARNING: First run will download large models!")
    print("This may take 10-30 minutes depending on your connection.")
    
    proceed = input("\nProceed with demo? (y/N): ").strip().lower()
    if proceed != 'y':
        print("Demo cancelled")
        return 0
    
    success = run_mini_demo(hf_token)
    
    if success:
        show_next_steps()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
