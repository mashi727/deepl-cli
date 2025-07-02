"""Clipboard management functionality"""

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class ClipboardManager:
    """Manage clipboard operations"""
    
    @staticmethod
    def is_available() -> bool:
        """Check if clipboard operations are available"""
        return CLIPBOARD_AVAILABLE
    
    @staticmethod
    def read() -> str:
        """Read text from clipboard"""
        if not CLIPBOARD_AVAILABLE:
            raise RuntimeError("pyperclip is not installed. Please run: pip install deepl-cli[clipboard]")
        
        try:
            text = pyperclip.paste()
            if not text:
                raise ValueError("Clipboard is empty")
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to read from clipboard: {e}")
    
    @staticmethod
    def write(text: str):
        """Write text to clipboard"""
        if not CLIPBOARD_AVAILABLE:
            raise RuntimeError("pyperclip is not installed. Please run: pip install deepl-cli[clipboard]")
        
        try:
            pyperclip.copy(text)
        except Exception as e:
            raise RuntimeError(f"Failed to write to clipboard: {e}")
