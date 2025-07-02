"""Command-line interface implementation"""

import sys
import os
import argparse
import logging
from typing import Optional

from .translator import DeepLTranslator
from .clipboard import ClipboardManager


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
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
    
    return parser


def read_input(args) -> str:
    """Read input text based on arguments"""
    # Clipboard mode
    if args.clipboard:
        return ClipboardManager.read()
    
    # Stdin mode (pipe or redirect)
    if not sys.stdin.isatty() or args.input_file == '-':
        return sys.stdin.read()
    
    # File mode
    if args.input_file:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read file: {e}")
    
    raise ValueError("No input provided. Use --help for usage information.")


def write_output(text: str, args):
    """Write output text based on arguments"""
    # Clipboard mode
    if args.clipboard:
        ClipboardManager.write(text)
        print("Translation copied to clipboard!")
        return
    
    # File output mode
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Translation saved to: {args.output}")
            return
        except Exception as e:
            raise ValueError(f"Failed to write file: {e}")
    
    # Default: stdout
    print(text)


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    try:
        # Handle special commands
        if args.list_languages:
            print("Supported language codes:")
            for lang in DeepLTranslator.list_languages():
                print(f"  {lang}")
            return 0
        
        # Initialize translator
        api_key = args.api_key or os.environ.get('DEEPL_API_KEY')
        translator = DeepLTranslator(api_key)
        
        # Show usage info
        if args.usage:
            usage = translator.get_usage()
            print(f"API Usage:")
            print(f"  Characters used: {usage['character_count']:,}")
            print(f"  Character limit: {usage['character_limit']:,}")
            print(f"  Remaining: {usage['character_limit'] - usage['character_count']:,}")
            return 0
        
        # Validate target language
        if not args.target_lang:
            parser.error("target_lang is required for translation")
        
        if args.target_lang.upper() not in translator.list_languages():
            parser.error(f"Unsupported language: {args.target_lang}")
        
        # Read input
        input_text = read_input(args)
        
        # Translate
        logging.info("Translating...")
        translated_text = translator.translate(
            input_text,
            args.target_lang.upper(),
            args.source_lang.upper() if args.source_lang else None
        )
        
        # Write output
        write_output(translated_text, args)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130
    except Exception as e:
        logging.error(str(e))
        return 1
