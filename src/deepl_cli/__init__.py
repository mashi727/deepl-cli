"""DeepL CLI - Command-line interface for DeepL translation"""

__version__ = "0.1.0"
__author__ = "MASAMI Mashino"
__email__ = "mashi.zzz@gmail.com"
__description__ = "A command-line interface for DeepL translation API"
__url__ = "https://github.com/${GITHUB_USERNAME}/deepl-cli"

from .translator import DeepLTranslator
from .clipboard import ClipboardManager, ClipboardError

__all__ = [
    "DeepLTranslator", 
    "ClipboardManager", 
    "ClipboardError",
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "__url__"
]