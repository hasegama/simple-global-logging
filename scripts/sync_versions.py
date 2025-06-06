#!/usr/bin/env python3
"""Sync version across pyproject.toml and __init__.py based on git tag."""

import subprocess
import re
import sys
import toml
from pathlib import Path


def get_git_version():
    """Get version from git tag."""
    try:
        # Try to get version from git tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--exact-match"],
            capture_output=True,
            text=True,
            check=True
        )
        tag = result.stdout.strip()
        
        # Remove 'v' prefix if present (e.g., v1.0.0 -> 1.0.0)
        if tag.startswith('v'):
            tag = tag[1:]
            
        # Validate version format (semver with prerelease support)
        # Matches: 1.0.0, 1.0.0-dev, 1.0.0-alpha.1, 1.0.0-beta.2, 1.0.0-rc.1, etc.
        if re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$', tag):
            return tag
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return None


def set_version_in_init(version):
    """Set version in __init__.py file."""
    init_file = Path(__file__).parent.parent / "simple_global_logging" / "__init__.py"
    
    # Read current content
    content = init_file.read_text(encoding='utf-8')
    
    # Replace version line
    pattern = r'__version__ = "[^"]*"'
    replacement = f'__version__ = "{version}"'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print(f"Warning: Version pattern not found in {init_file}")
        return False
    
    # Write back
    init_file.write_text(new_content, encoding='utf-8')
    print(f"Version set to {version} in {init_file}")
    return True


def set_version_in_pyproject(version):
    """Set version in pyproject.toml file."""
    pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    
    try:
        # Read current content
        with open(pyproject_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace version line using regex (more reliable than toml parsing for this case)
        pattern = r'version = "[^"]*"'
        replacement = f'version = "{version}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content == content:
            print(f"Warning: Version pattern not found in {pyproject_file}")
            return False
        
        # Write back
        with open(pyproject_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Version set to {version} in {pyproject_file}")
        return True
        
    except Exception as e:
        print(f"Error updating pyproject.toml: {e}")
        return False


def main():
    """Main function."""
    # Get version from git tag
    version = get_git_version()
    
    if version is None:
        print("Error: No valid git tag found")
        print("Please create a tag first: git tag v1.0.0")
        sys.exit(1)
    
    print(f"Setting version to: {version}")
    
    # Set version in both files
    success = True
    success = success and set_version_in_init(version)
    success = success and set_version_in_pyproject(version)
    
    if not success:
        sys.exit(1)
    
    print(f"Successfully synchronized version to {version}")


if __name__ == "__main__":
    main() 