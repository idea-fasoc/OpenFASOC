#!/usr/bin/env python3
"""
Installation verification and fix script for OpenFASOC transmission gate dataset generation.
Checks and installs missing dependencies, specifically handling the PrettyPrint issue.
"""

import subprocess
import sys
import importlib.util

def check_and_install_package(package_name, import_name=None):
    """Check if a package is installed, and install if missing"""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            print(f"✅ {package_name} is already installed")
            return True
    except ImportError:
        pass
    
    print(f"❌ {package_name} is missing. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def main():
    """Main installation verification function"""
    print("🔧 OpenFASOC Dependency Checker and Installer")
    print("=" * 50)
    
    # Check gdsfactory version
    try:
        import gdsfactory
        version = gdsfactory.__version__
        print(f"📦 gdsfactory version: {version}")
        
        # Parse version to check if it's 7.16.0+
        version_parts = [int(x) for x in version.split('.')]
        if version_parts[0] > 7 or (version_parts[0] == 7 and version_parts[1] >= 16):
            print("ℹ️  Using gdsfactory 7.16.0+ with strict Pydantic validation")
            print("ℹ️  The updated fix handles this version properly")
        else:
            print("ℹ️  Using older gdsfactory version with relaxed validation")
    except ImportError:
        print("❌ gdsfactory not found")
        return False
    
    # Check required packages
    packages_to_check = [
        ("prettyprinttree", "prettyprinttree"),
        ("prettyprint", "prettyprint"),
        ("gymnasium", "gymnasium"),  # Also check for gymnasium
    ]
    
    print("\n📋 Checking required packages...")
    all_good = True
    
    for package_name, import_name in packages_to_check:
        success = check_and_install_package(package_name, import_name)
        if not success:
            all_good = False
    
    # Special check for PrettyPrint import issue
    print("\n🔍 Testing PrettyPrint imports...")
    try:
        from prettyprinttree import PrettyPrintTree
        print("✅ prettyprinttree import works correctly")
    except ImportError:
        try:
            from PrettyPrint import PrettyPrintTree
            print("✅ PrettyPrint import works (older style)")
        except ImportError:
            print("❌ Neither prettyprinttree nor PrettyPrint imports work")
            print("💡 Installing prettyprinttree...")
            success = check_and_install_package("prettyprinttree")
            if not success:
                all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All dependencies are properly installed!")
        print("✅ Your environment should now work with the transmission gate dataset generation")
        print("\n📝 Next steps:")
        print("1. Run the test script: python test_comprehensive_fix.py")
        print("2. If tests pass, run: python generate_tg_1000_dataset.py")
    else:
        print("⚠️  Some dependencies are missing or failed to install")
        print("💡 Please install them manually:")
        print("   pip install prettyprinttree prettyprint gymnasium")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
