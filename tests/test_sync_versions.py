"""
Tests for scripts/sync_versions.py
"""

import pytest
import subprocess
import sys
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Import sync_versions from scripts package
from scripts import sync_versions


class TestGetGitVersion:
    """Test cases for get_git_version function."""
    
    @patch('subprocess.run')
    def test_get_git_version_exact_match(self, mock_run):
        """Test getting version from exact git tag match."""
        # Mock successful exact match
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "v1.2.3\n"
        mock_run.return_value = mock_result
        
        version = sync_versions.get_git_version()
        
        assert version == "1.2.3"
        mock_run.assert_called_once_with(
            ["git", "describe", "--tags", "--exact-match"],
            capture_output=True,
            text=True,
            check=False
        )
    
    @patch('subprocess.run')
    def test_get_git_version_fallback_to_latest(self, mock_run):
        """Test fallback to latest tag when no exact match."""
        # Mock first call (exact match) fails, second call (latest) succeeds
        mock_results = [
            MagicMock(returncode=1, stdout=""),  # No exact match
            MagicMock(returncode=0, stdout="v2.0.0\n")  # Latest tag
        ]
        mock_run.side_effect = mock_results
        
        with patch('builtins.print') as mock_print:
            version = sync_versions.get_git_version()
        
        assert version == "2.0.0"
        assert mock_run.call_count == 2
        mock_print.assert_called_with("No exact tag match for current commit, using latest tag: v2.0.0")
    
    @patch('subprocess.run')
    def test_get_git_version_no_v_prefix(self, mock_run):
        """Test version without 'v' prefix."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "1.0.0\n"
        mock_run.return_value = mock_result
        
        version = sync_versions.get_git_version()
        
        assert version == "1.0.0"
    
    @patch('subprocess.run')
    def test_get_git_version_prerelease(self, mock_run):
        """Test version with prerelease suffix."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "v1.0.0-alpha.1\n"
        mock_run.return_value = mock_result
        
        version = sync_versions.get_git_version()
        
        assert version == "1.0.0-alpha.1"
    
    @patch('subprocess.run')
    def test_get_git_version_invalid_format(self, mock_run):
        """Test invalid version format returns None."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "invalid-version\n"
        mock_run.return_value = mock_result
        
        version = sync_versions.get_git_version()
        
        assert version is None
    
    @patch('subprocess.run')
    def test_get_git_version_subprocess_error(self, mock_run):
        """Test subprocess error handling."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        version = sync_versions.get_git_version()
        
        assert version is None
    
    @patch('subprocess.run')
    def test_get_git_version_file_not_found(self, mock_run):
        """Test FileNotFoundError handling."""
        mock_run.side_effect = FileNotFoundError()
        
        version = sync_versions.get_git_version()
        
        assert version is None


class TestSetVersionInInit:
    """Test cases for set_version_in_init function."""
    
    @patch('pathlib.Path.read_text')
    @patch('pathlib.Path.write_text')
    @patch('builtins.print')
    def test_set_version_in_init_success(self, mock_print, mock_write, mock_read):
        """Test successful version update in __init__.py."""
        mock_read.return_value = '__version__ = "0.1.0"\nother_content = "test"'
        
        result = sync_versions.set_version_in_init("1.2.3")
        
        assert result is True
        mock_write.assert_called_once_with('__version__ = "1.2.3"\nother_content = "test"', encoding='utf-8')
        mock_print.assert_called()
    
    @patch('pathlib.Path.read_text')
    @patch('builtins.print')
    def test_set_version_in_init_pattern_not_found(self, mock_print, mock_read):
        """Test when version pattern is not found in __init__.py."""
        mock_read.return_value = 'no_version_here = "test"'
        
        result = sync_versions.set_version_in_init("1.2.3")
        
        assert result is False
        # Check that warning message was printed (don't check exact path)
        mock_print.assert_called()
        call_args = mock_print.call_args[0][0]
        assert "Warning: Version pattern not found" in call_args
        assert "__init__.py" in call_args


class TestSetVersionInPyproject:
    """Test cases for set_version_in_pyproject function."""
    
    @patch('builtins.open', new_callable=mock_open, read_data='[tool.poetry]\nversion = "0.1.0"\nname = "test"')
    @patch('builtins.print')
    def test_set_version_in_pyproject_success(self, mock_print, mock_file):
        """Test successful version update in pyproject.toml."""
        result = sync_versions.set_version_in_pyproject("1.2.3")
        
        assert result is True
        # Check that file was written with updated version
        handle = mock_file()
        written_content = ''.join(call.args[0] for call in handle.write.call_args_list)
        assert 'version = "1.2.3"' in written_content
        mock_print.assert_called()
    
    @patch('builtins.open', new_callable=mock_open, read_data='[tool.poetry]\nname = "test"')
    @patch('builtins.print')
    def test_set_version_in_pyproject_pattern_not_found(self, mock_print, mock_file):
        """Test when version pattern is not found in pyproject.toml."""
        result = sync_versions.set_version_in_pyproject("1.2.3")
        
        assert result is False
        # Check that warning message was printed (don't check exact path)
        mock_print.assert_called()
        call_args = mock_print.call_args[0][0]
        assert "Warning: Version pattern not found" in call_args
        assert "pyproject.toml" in call_args
    
    @patch('builtins.open', side_effect=Exception("File error"))
    @patch('builtins.print')
    def test_set_version_in_pyproject_exception(self, mock_print, mock_file):
        """Test exception handling in pyproject.toml update."""
        result = sync_versions.set_version_in_pyproject("1.2.3")
        
        assert result is False
        mock_print.assert_called_with("Error updating pyproject.toml: File error")


class TestMain:
    """Test cases for main function."""
    
    @patch('scripts.sync_versions.get_git_version')
    @patch('scripts.sync_versions.set_version_in_init')
    @patch('scripts.sync_versions.set_version_in_pyproject')
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_set_pyproject, mock_set_init, mock_get_version):
        """Test successful main execution."""
        mock_get_version.return_value = "1.2.3"
        mock_set_init.return_value = True
        mock_set_pyproject.return_value = True
        
        sync_versions.main()
        
        mock_get_version.assert_called_once()
        mock_set_init.assert_called_once_with("1.2.3")
        mock_set_pyproject.assert_called_once_with("1.2.3")
        mock_print.assert_any_call("Setting version to: 1.2.3")
        mock_print.assert_any_call("Successfully synchronized version to 1.2.3")
    
    @patch('scripts.sync_versions.get_git_version')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_git_version(self, mock_exit, mock_print, mock_get_version):
        """Test main when no git version is found."""
        mock_get_version.return_value = None
        
        sync_versions.main()
        
        mock_print.assert_any_call("Error: No valid git tag found")
        mock_print.assert_any_call("Please create a tag first: git tag v1.0.0")
        mock_exit.assert_called_with(1)
    
    @patch('scripts.sync_versions.get_git_version')
    @patch('scripts.sync_versions.set_version_in_init')
    @patch('scripts.sync_versions.set_version_in_pyproject')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_init_update_fails(self, mock_exit, mock_print, mock_set_pyproject, mock_set_init, mock_get_version):
        """Test main when init file update fails."""
        mock_get_version.return_value = "1.2.3"
        mock_set_init.return_value = False
        mock_set_pyproject.return_value = True
        
        sync_versions.main()
        
        mock_exit.assert_called_with(1)
    
    @patch('scripts.sync_versions.get_git_version')
    @patch('scripts.sync_versions.set_version_in_init')
    @patch('scripts.sync_versions.set_version_in_pyproject')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_pyproject_update_fails(self, mock_exit, mock_print, mock_set_pyproject, mock_set_init, mock_get_version):
        """Test main when pyproject.toml update fails."""
        mock_get_version.return_value = "1.2.3"
        mock_set_init.return_value = True
        mock_set_pyproject.return_value = False
        
        sync_versions.main()
        
        mock_exit.assert_called_with(1)


# Integration test (optional - requires actual git repository)
class TestIntegration:
    """Integration tests that require actual git repository."""
    
    def test_actual_git_version_retrieval(self):
        """Test actual git version retrieval (requires git repository with tags)."""
        # This test uses the actual git repository
        # It might fail if no tags exist, which is expected
        version = sync_versions.get_git_version()
        
        # This test might fail if no tags exist, which is expected
        if version is not None:
            # If version exists, it should match semver pattern
            import re
            assert re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$', version) 