#!/usr/bin/env python3
"""Test script for prerelease version handling."""

import re


def validate_version(version):
    """Validate version format (semver with prerelease support)."""
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$'
    return re.match(pattern, version) is not None


def test_versions():
    """Test various version formats."""
    test_cases = [
        # Valid versions
        ("1.0.0", True),
        ("0.1.0", True),
        ("10.20.30", True),
        ("1.0.0-dev", True),
        ("1.0.0-alpha", True),
        ("1.0.0-alpha.1", True),
        ("1.0.0-beta.2", True),
        ("1.0.0-rc.1", True),
        ("2.1.0-dev.20231201", True),
        ("1.0.0-alpha.beta", True),
        ("1.0.0-0.3.7", True),
        ("1.0.0-x.7.z.92", True),
        
        # Invalid versions
        ("1.0", False),
        ("1.0.0-", False),
        ("1.0.0-.", False),
        ("1.0.0-.alpha", False),
        ("1.0.0-alpha.", False),
        ("v1.0.0", False),  # 'v' prefix should be removed before validation
        ("1.0.0-alpha..1", False),
        ("1.0.0-α", False),  # Non-ASCII characters
    ]
    
    print("Testing version validation:")
    print("=" * 50)
    
    all_passed = True
    for version, expected in test_cases:
        result = validate_version(version)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} {version:<20} -> {result} (expected: {expected})")
        if result != expected:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        return False
    
    return True


def test_tag_processing():
    """Test tag processing (removing 'v' prefix)."""
    print("\nTesting tag processing:")
    print("=" * 50)
    
    test_cases = [
        ("v1.0.0", "1.0.0"),
        ("v1.0.0-dev", "1.0.0-dev"),
        ("v2.1.0-alpha.1", "2.1.0-alpha.1"),
        ("1.0.0", "1.0.0"),  # No 'v' prefix
        ("1.0.0-beta", "1.0.0-beta"),  # No 'v' prefix
    ]
    
    all_passed = True
    for tag, expected in test_cases:
        # Simulate tag processing
        processed = tag[1:] if tag.startswith('v') else tag
        status = "✅ PASS" if processed == expected else "❌ FAIL"
        print(f"{status} {tag:<15} -> {processed:<15} (expected: {expected})")
        if processed != expected:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✅ All tag processing tests passed!")
    else:
        print("❌ Some tag processing tests failed!")
        return False
    
    return True


def main():
    """Main function."""
    print("Prerelease Version Testing")
    print("=" * 50)
    
    success = True
    success &= test_versions()
    success &= test_tag_processing()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Prerelease versions are supported.")
    else:
        print("💥 Some tests failed!")
        exit(1)


if __name__ == "__main__":
    main() 