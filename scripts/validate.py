#!/usr/bin/env python3
"""
Validation script for MkDocs content.
Checks for broken links, markdown issues, and content consistency.
"""
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

class ContentValidator:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.errors = []
        self.warnings = []
        
    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("🔍 Starting content validation...\n")
        
        self.check_markdown_files()
        self.check_internal_links()
        self.check_required_metadata()
        
        return self.report_results()
    
    def check_markdown_files(self):
        """Check for common markdown issues."""
        print("📝 Checking markdown files...")
        
        for md_file in self.docs_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Check for empty files
                if not content.strip():
                    self.warnings.append(f"Empty file: {md_file}")
                
                # Check for missing title (# heading)
                if not re.search(r'^#\s+.+', content, re.MULTILINE):
                    self.warnings.append(f"Missing title heading: {md_file}")
                
                # Check for unclosed code blocks
                code_blocks = re.findall(r'```', content)
                if len(code_blocks) % 2 != 0:
                    self.errors.append(f"Unclosed code block: {md_file}")
                    
            except Exception as e:
                self.errors.append(f"Error reading {md_file}: {e}")
        
        print(f"   ✓ Checked {len(list(self.docs_dir.rglob('*.md')))} markdown files")
    
    def check_internal_links(self):
        """Check for broken internal links."""
        print("🔗 Checking internal links...")
        
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        checked_links = 0
        
        for md_file in self.docs_dir.rglob("*.md"):
            # Skip template files - they contain placeholder links
            if 'templates' in md_file.parts:
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                links = link_pattern.findall(content)
                
                for link_text, link_url in links:
                    # Skip external links and anchors
                    if link_url.startswith(('http://', 'https://', '#')):
                        continue
                    
                    # Skip placeholder links
                    if '[' in link_url or ']' in link_url:
                        continue
                    
                    checked_links += 1
                    
                    # Resolve relative path
                    link_path = (md_file.parent / link_url).resolve()
                    
                    if not link_path.exists():
                        self.errors.append(
                            f"Broken link in {md_file}: [{link_text}]({link_url})"
                        )
                        
            except Exception as e:
                self.errors.append(f"Error checking links in {md_file}: {e}")
        
        print(f"   ✓ Checked {checked_links} internal links")
    
    def check_required_metadata(self):
        """Check for required metadata in content files."""
        print("📋 Checking page metadata...")
        
        checked_files = 0
        for md_file in self.docs_dir.rglob("*.md"):
            # Skip files that don't need metadata
            if (md_file.name == "index.md" or 
                'templates' in md_file.parts or
                'includes' in md_file.parts or
                md_file.name in ['tags.md', 'glossary.md', 'test-code-highlighting.md']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                checked_files += 1
                
                # Check for YAML frontmatter
                if not content.startswith('---'):
                    self.warnings.append(
                        f"Missing metadata frontmatter: {md_file}"
                    )
                    
            except Exception as e:
                self.errors.append(f"Error checking metadata in {md_file}: {e}")
        
        print(f"   ✓ Checked metadata in {checked_files} files")
    
    def report_results(self) -> bool:
        """Print validation results."""
        print("\n" + "=" * 60)
        print("Validation Results")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  Found {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ All validation checks passed!")
            return True
        elif not self.errors:
            print("\n✅ No errors found (warnings can be ignored)")
            return True
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} error(s)")
            return False

def main():
    """Main validation process."""
    # Change to project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    validator = ContentValidator()
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
