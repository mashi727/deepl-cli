"""DeepL CLI - Command-line interface for DeepL translation"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .translator import DeepLTranslator
from .clipboard import ClipboardManager

__all__ = ["DeepLTranslator", "ClipboardManager"]
