#!/usr/bin/env python3
"""
Build script for MkDocs site with validation and error handling.
"""
import subprocess
import sys
import os
import shutil

def clean_build():
    """Remove existing build directory."""
    site_dir = "site"
    if os.path.exists(site_dir):
        print(f"🧹 Cleaning existing build directory: {site_dir}")
        shutil.rmtree(site_dir)

def build_site():
    """Build the MkDocs site."""
    print("🔨 Building MkDocs site...")
    try:
        result = subprocess.run(
            ["mkdocs", "build", "--strict"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Build completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        if e.stderr:
            print(e.stderr)
        if e.stdout:
            print(e.stdout)
        return False

def main():
    """Main build process."""
    # Change to project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    print("=" * 60)
    print("MkDocs Build Process")
    print("=" * 60)
    
    # Clean previous build
    clean_build()
    
    # Build site
    success = build_site()
    
    if success:
        print("\n✅ Build process completed successfully!")
        print(f"📁 Site generated in: {os.path.join(project_root, 'site')}")
        sys.exit(0)
    else:
        print("\n❌ Build process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
