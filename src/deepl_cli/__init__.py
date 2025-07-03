"""DeepL CLI - Command-line interface for DeepL translation"""

__version__ = "0.1.0"
__author__ = "MASAMI Mashino"
__email__ = "mashi.zzz@gmail.com"

from .translator import DeepLTranslator
from .clipboard import ClipboardManager

__all__ = ["DeepLTranslator", "ClipboardManager"]
