#!/usr/bin/env python3
"""Version checking script for development."""

import sys
import subprocess
import re
from pathlib import Path

# Add the package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from simple_global_logging import __version__


def get_git_tag():
    """Get current git tag if available."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--exact-match"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_pyproject_version():
    """Get version from pyproject.toml."""
    pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    try:
        content = pyproject_file.read_text(encoding='utf-8')
        match = re.search(r'version = "([^"]*)"', content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def main():
    """Main function to check version information."""
    print(f"Package version (__init__.py): {__version__}")
    
    pyproject_version = get_pyproject_version()
    if pyproject_version:
        print(f"pyproject.toml version: {pyproject_version}")
        
        if __version__ != pyproject_version:
            print("❌ Version mismatch between __init__.py and pyproject.toml!")
            print("   Run 'python scripts/sync_versions.py' to fix this")
            sys.exit(1)
    
    git_tag = get_git_tag()
    if git_tag:
        print(f"Git tag: {git_tag}")
        
        # Remove 'v' prefix if present
        tag_version = git_tag[1:] if git_tag.startswith('v') else git_tag
        
        if tag_version == __version__:
            print("✅ Version consistency: OK")
        else:
            print("❌ Version mismatch detected!")
            print(f"   Tag version: {tag_version}")
            print(f"   Package version: {__version__}")
            print("   Run 'python scripts/sync_versions.py' to fix this")
            sys.exit(1)
    else:
        print("No git tag found (development mode)")
        if __version__.endswith('.dev0'):
            print("✅ Development version: OK")
        else:
            print("⚠️  Warning: Not on a tagged commit but version doesn't indicate development")
            print("   Consider running 'python scripts/sync_versions.py' after creating a tag")


if __name__ == "__main__":
    main() 