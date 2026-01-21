#!/usr/bin/env python3
"""
Local development server script for MkDocs.
Starts the development server with live reload functionality.
"""
import subprocess
import sys
import os

def main():
    """Start the MkDocs development server."""
    print("🚀 Starting MkDocs development server...")
    print("📝 Server will be available at http://127.0.0.1:8000")
    print("🔄 Live reload is enabled - changes will be reflected automatically")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        # Change to project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_root)
        
        # Start MkDocs development server
        subprocess.run(["mkdocs", "serve"], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Development server stopped")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting development server: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ MkDocs not found. Please install dependencies:")
        print("   pipenv install")
        sys.exit(1)

if __name__ == "__main__":
    main()
