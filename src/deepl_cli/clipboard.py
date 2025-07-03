"""Clipboard management functionality"""

import logging
from typing import Optional

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


logger = logging.getLogger(__name__)


class ClipboardError(Exception):
    """Custom exception for clipboard-related errors"""
    pass


class ClipboardManager:
    """Manage clipboard operations with enhanced error handling"""
    
    @staticmethod
    def is_available() -> bool:
        """
        Check if clipboard operations are available
        
        Returns:
            True if pyperclip is installed and functional, False otherwise
        """
        if not CLIPBOARD_AVAILABLE:
            return False
        
        # Additional check to see if clipboard actually works
        try:
            # Try a simple operation to verify clipboard functionality
            test_text = pyperclip.paste()
            return True
        except Exception as e:
            logger.debug(f"Clipboard not functional: {e}")
            return False
    
    @staticmethod
    def read() -> str:
        """
        Read text from clipboard
        
        Returns:
            Text content from clipboard
            
        Raises:
            ClipboardError: If clipboard operations fail or pyperclip is not installed
        """
        if not CLIPBOARD_AVAILABLE:
            raise ClipboardError(
                "Clipboard support not available. "
                "Install with: pip install deepl-cli[clipboard]"
            )
        
        try:
            text = pyperclip.paste()
            logger.debug(f"Read {len(text)} characters from clipboard")
            
            if not text:
                raise ClipboardError(
                    "Clipboard is empty. "
                    "Please copy some text to translate and try again."
                )
            
            return text
            
        except ClipboardError:
            raise
        except Exception as e:
            raise ClipboardError(f"Failed to read from clipboard: {e}")
    
    @staticmethod
    def write(text: str) -> None:
        """
        Write text to clipboard
        
        Args:
            text: Text to copy to clipboard
            
        Raises:
            ClipboardError: If clipboard operations fail or pyperclip is not installed
        """
        if not CLIPBOARD_AVAILABLE:
            raise ClipboardError(
                "Clipboard support not available. "
                "Install with: pip install deepl-cli[clipboard]"
            )
        
        if not isinstance(text, str):
            raise ClipboardError("Only string text can be copied to clipboard")
        
        try:
            pyperclip.copy(text)
            logger.debug(f"Copied {len(text)} characters to clipboard")
            
        except Exception as e:
            raise ClipboardError(f"Failed to write to clipboard: {e}")
    
    @staticmethod
    def get_clipboard_info() -> Optional[dict]:
        """
        Get information about clipboard content
        
        Returns:
            Dictionary with clipboard info, or None if not available
        """
        if not ClipboardManager.is_available():
            return None
        
        try:
            text = pyperclip.paste()
            return {
                'length': len(text),
                'lines': text.count('\n') + 1 if text else 0,
                'has_content': bool(text and text.strip())
            }
        except Exception:
            return None