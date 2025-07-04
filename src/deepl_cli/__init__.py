"""DeepL CLI - Command-line interface for DeepL translation"""

__version__ = "0.2.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A powerful command-line interface for DeepL translation API"
__url__ = "https://github.com/YOUR_USERNAME/deepl-cli"

# Core modules
from .translator import DeepLTranslator
from .clipboard import ClipboardManager, ClipboardError
from .cli import CLIError, main

# Utility modules
from .utils import (
    BatchTranslator,
    TextProcessor,
    SubtitleTranslator,
    format_file_size,
    estimate_translation_time
)

# Configuration modules
from .config import (
    TranslationConfig,
    ConfigManager,
    LanguagePreferences
)

__all__ = [
    # Core
    "DeepLTranslator",
    "ClipboardManager",
    "ClipboardError",
    "CLIError",
    "main",

    # Utils
    "BatchTranslator",
    "TextProcessor",
    "SubtitleTranslator",
    "format_file_size",
    "estimate_translation_time",

    # Config
    "TranslationConfig",
    "ConfigManager",
    "LanguagePreferences",

    # Meta
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "__url__"
]
