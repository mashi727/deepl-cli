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
