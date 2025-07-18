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
  %(prog)s JA "Hello, world!"        # Translate text directly
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
        'input_text',
        nargs='?',
        help='Text to translate or input file path'
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
        if not sys.stdin.isatty():
            return sys.stdin.read()

        # Direct text or file mode
        if args.input_text:
            # Check if it's a file path
            file_path = Path(args.input_text)

            if file_path.exists() and file_path.is_file():
                # It's a file, read it
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if not content.strip():
                        raise CLIError(f"Input file is empty: {args.input_text}")
                    return content
                except PermissionError:
                    raise CLIError(f"Permission denied reading file: {args.input_text}")
                except UnicodeDecodeError:
                    raise CLIError(
                        f"Unable to decode file as UTF-8: {args.input_text}\n"
                        f"Please ensure the file is saved with UTF-8 encoding"
                    )
            else:
                # It's direct text input
                return args.input_text

        raise CLIError(
            "No input provided. Use one of:\n"
            "  - Provide text directly: deepl-cli JA \"Hello, world!\"\n"
            "  - Provide input file path: deepl-cli JA input.txt\n"
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
        print(text)

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
    print("\nUsage: deepl-cli <TARGET_LANG> [input_text or file]")
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
