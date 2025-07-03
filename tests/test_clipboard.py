"""Tests for clipboard functionality"""

import pytest
from unittest.mock import Mock, patch
from deepl_cli.clipboard import ClipboardManager, ClipboardError


class TestClipboardManager:
    """Test cases for ClipboardManager"""
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_is_available_success(self, mock_pyperclip):
        """Test clipboard availability check when functional"""
        mock_pyperclip.paste.return_value = "test"
        
        assert ClipboardManager.is_available()
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', False)
    def test_is_available_not_installed(self):
        """Test clipboard availability when pyperclip not installed"""
        assert not ClipboardManager.is_available()
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_is_available_exception(self, mock_pyperclip):
        """Test clipboard availability when pyperclip raises exception"""
        mock_pyperclip.paste.side_effect = Exception("Clipboard error")
        
        assert not ClipboardManager.is_available()
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_read_success(self, mock_pyperclip):
        """Test successful clipboard read"""
        mock_pyperclip.paste.return_value = "Hello from clipboard"
        
        result = ClipboardManager.read()
        assert result == "Hello from clipboard"
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', False)
    def test_read_not_available(self):
        """Test clipboard read when not available"""
        with pytest.raises(ClipboardError) as exc_info:
            ClipboardManager.read()
        
        assert "not available" in str(exc_info.value)
        assert "pip install" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_read_empty_clipboard(self, mock_pyperclip):
        """Test reading from empty clipboard"""
        mock_pyperclip.paste.return_value = ""
        
        with pytest.raises(ClipboardError) as exc_info:
            ClipboardManager.read()
        
        assert "Clipboard is empty" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_read_exception(self, mock_pyperclip):
        """Test clipboard read with exception"""
        mock_pyperclip.paste.side_effect = Exception("Read error")
        
        with pytest.raises(ClipboardError) as exc_info:
            ClipboardManager.read()
        
        assert "Failed to read from clipboard" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_write_success(self, mock_pyperclip):
        """Test successful clipboard write"""
        ClipboardManager.write("Test text")
        
        mock_pyperclip.copy.assert_called_once_with("Test text")
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', False)
    def test_write_not_available(self):
        """Test clipboard write when not available"""
        with pytest.raises(ClipboardError) as exc_info:
            ClipboardManager.write("Test text")
        
        assert "not available" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    def test_write_invalid_type(self):
        """Test clipboard write with invalid type"""
        with pytest.raises(ClipboardError) as exc_info:
            ClipboardManager.write(123)  # Not a string
        
        assert "Only string text" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_write_exception(self, mock_pyperclip):
        """Test clipboard write with exception"""
        mock_pyperclip.copy.side_effect = Exception("Write error")
        
        with pytest.raises(ClipboardError) as exc_info:
            ClipboardManager.write("Test text")
        
        assert "Failed to write to clipboard" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_get_clipboard_info_success(self, mock_pyperclip):
        """Test getting clipboard information"""
        mock_pyperclip.paste.return_value = "Hello\nWorld\nTest"
        
        info = ClipboardManager.get_clipboard_info()
        
        assert info is not None
        assert info['length'] == 16  # "Hello\nWorld\nTest"
        assert info['lines'] == 3
        assert info['has_content'] is True
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', False)
    def test_get_clipboard_info_not_available(self):
        """Test getting clipboard info when not available"""
        info = ClipboardManager.get_clipboard_info()
        assert info is None
    
    @patch('deepl_cli.clipboard.CLIPBOARD_AVAILABLE', True)
    @patch('deepl_cli.clipboard.pyperclip')
    def test_get_clipboard_info_empty(self, mock_pyperclip):
        """Test getting clipboard info for empty clipboard"""
        mock_pyperclip.paste.return_value = ""
        
        info = ClipboardManager.get_clipboard_info()
        
        assert info is not None
        assert info['length'] == 0
        assert info['lines'] == 0
        assert info['has_content'] is False