# DeepL CLI

[![PyPI version](https://badge.fury.io/py/deepl-cli.svg)](https://badge.fury.io/py/deepl-cli)
[![Python Version](https://img.shields.io/pypi/pyversions/deepl-cli.svg)](https://pypi.org/project/deepl-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/${GITHUB_USERNAME}/deepl-cli/workflows/Tests/badge.svg)](https://github.com/${GITHUB_USERNAME}/deepl-cli/actions)

A simple and efficient command-line interface for [DeepL Translator API](https://www.deepl.com/api).

## Features

- 🌍 Translate text between 29+ languages
- 📋 Clipboard support (copy & paste)
- 📄 File input/output
- 🔧 Unix pipe support
- ⚡ Fast and lightweight
- 🔐 Secure API key management
- 📊 Usage statistics with quota warnings
- 🎯 Smart error handling and validation
- 🔄 Auto-detection of source language

## Installation

### From PyPI

```bash
pip install deepl-cli

# With clipboard support
pip install deepl-cli[clipboard]
```

### From Source

```bash
git clone https://github.com/${GITHUB_USERNAME}/deepl-cli.git
cd deepl-cli
pip install -e .
```

## Setup

1. Get your DeepL API key from [DeepL Pro](https://www.deepl.com/pro-api)

2. Create a configuration file (recommended):
```bash
mkdir -p ~/.token/deepl-cli
echo "YOUR_API_KEY" > ~/.token/deepl-cli/api_key
chmod 600 ~/.token/deepl-cli/api_key
```

Alternatively, set the environment variable:
```bash
export DEEPL_API_KEY="YOUR_API_KEY"
```

## Usage

### Basic Translation

```bash
# Translate text to Japanese
deepl-cli JA "Hello, world!"

# Translate from file
deepl-cli EN-US input.txt

# Translate from pipe
echo "Bonjour" | deepl-cli EN

# Save to file
deepl-cli JA input.txt -o output.txt
```

### Clipboard Operations

```bash
# Translate clipboard content (requires pyperclip)
deepl-cli JA --clipboard

# Result is automatically copied back to clipboard
```

### Advanced Options

```bash
# Specify source language
deepl-cli JA -s EN "Hello"

# List supported languages
deepl-cli --list-languages

# Check API usage with quota warnings
deepl-cli --usage

# Verbose mode with detailed logging
deepl-cli JA "Hello" -v
```

### Supported Languages

DeepL CLI supports all DeepL languages:

- **BG** (Bulgarian), **CS** (Czech), **DA** (Danish)
- **DE** (German), **EL** (Greek)
- **EN-GB** (English UK), **EN-US** (English US), **EN** (English)
- **ES** (Spanish), **ET** (Estonian), **FI** (Finnish)
- **FR** (French), **HU** (Hungarian), **IT** (Italian)
- **JA** (Japanese), **LT** (Lithuanian), **LV** (Latvian)
- **NL** (Dutch), **PL** (Polish)
- **PT-PT** (Portuguese), **PT-BR** (Portuguese Brazilian), **PT** (Portuguese)
- **RO** (Romanian), **RU** (Russian), **SK** (Slovak)
- **SL** (Slovenian), **SV** (Swedish), **ZH** (Chinese)

Use `deepl-cli --list-languages` for the complete list.

## Examples

### Shell Script Integration

```bash
#!/bin/bash
# Translate all .txt files in a directory
for file in *.txt; do
    echo "Translating $file..."
    deepl-cli JA "$file" -o "ja_${file}"
done
```

### Batch Translation with Progress

```bash
#!/bin/bash
# Translate multiple files with progress indication
files=(*.txt)
total=${#files[@]}

for i in "${!files[@]}"; do
    file="${files[$i]}"
    echo "[$((i+1))/$total] Translating $file..."
    deepl-cli JA "$file" -o "translated_${file}"
    
    # Check quota after each translation
    if ! deepl-cli --usage | grep -q "Warning"; then
        echo "✓ Translation completed"
    else
        echo "⚠️ Warning: API quota is getting high"
    fi
done
```

### Python Integration

```python
from deepl_cli import DeepLTranslator

# Initialize translator
translator = DeepLTranslator()

# Translate text
result = translator.translate("Hello, world!", "JA")
print(result)  # こんにちは、世界！

# Check usage
usage = translator.get_usage()
print(f"Used: {usage['character_count']:,} / {usage['character_limit']:,}")
print(f"Usage: {usage['usage_percentage']:.1f}%")

# Validate language support
if translator.is_language_supported("JA"):
    print("Japanese is supported!")
```

## Configuration Files

The CLI looks for API keys in the following locations (in order of priority):

1. **Command line argument**: `--api-key YOUR_KEY`
2. **Environment variable**: `DEEPL_API_KEY`
3. **Primary config file**: `~/.token/deepl-cli/api_key` ⭐ **Recommended**
4. **Legacy config files** (for backward compatibility):
   - `~/.config/deepl-cli/api_key`
   - `~/.config/.deepl_apikey`
   - `~/.deepl_apikey`

### Secure Configuration

For security, set appropriate file permissions:

```bash
# Create secure config directory
mkdir -p ~/.token/deepl-cli
chmod 700 ~/.token/deepl-cli

# Create API key file with restricted permissions
echo "YOUR_API_KEY" > ~/.token/deepl-cli/api_key
chmod 600 ~/.token/deepl-cli/api_key
```

## Error Handling

The CLI provides helpful error messages and suggestions:

```bash
# Invalid language code
$ deepl-cli INVALID "Hello"
Error: Unsupported target language: INVALID
Available languages: BG, CS, DA, DE, EL... (use --list-languages for full list)

# Quota exceeded
$ deepl-cli JA "Hello"
Error: DeepL API quota exceeded. Please check your usage limits.

# Empty clipboard
$ deepl-cli JA --clipboard
Error: Clipboard is empty. Please copy some text to translate and try again.
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/${GITHUB_USERNAME}/deepl-cli.git
cd deepl-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific test file
pytest tests/test_translator.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with black
black src tests

# Lint with flake8
flake8 src tests

# Type checking with mypy
mypy src

# Run all pre-commit hooks
pre-commit run --all-files
```

### Building and Publishing

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (requires authentication)
twine upload dist/*
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest`)
5. Format your code (`black src tests`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Troubleshooting

### Common Issues

**Q: "Clipboard support not available" error**
```bash
# Install clipboard support
pip install deepl-cli[clipboard]
```

**Q: "API key not found" error**
```bash
# Check if config file exists and has content
cat ~/.token/deepl-cli/api_key

# Or set environment variable
export DEEPL_API_KEY="your_api_key_here"
```

**Q: Permission denied errors**
```bash
# Fix file permissions
chmod 600 ~/.token/deepl-cli/api_key
chmod 700 ~/.token/deepl-cli
```

**Q: Character encoding issues**
```bash
# Ensure input files are UTF-8 encoded
file -i your_file.txt
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt
```

### Getting Help

- Check the [Issues](https://github.com/${GITHUB_USERNAME}/deepl-cli/issues) page
- Review [DeepL API documentation](https://www.deepl.com/docs-api)
- Use `deepl-cli --help` for quick reference

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DeepL](https://www.deepl.com) for providing the excellent translation API
- [pyperclip](https://github.com/asweigart/pyperclip) for clipboard functionality
- All contributors who help improve this tool

## Changelog

### v0.1.0
- Initial release with core translation functionality
- Clipboard support
- File input/output
- Configuration management
- Comprehensive error handling
- Usage monitoring with quota warnings

---

**Note**: This is an unofficial client for the DeepL API. It is not affiliated with DeepL SE.

## Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/${GITHUB_USERNAME}/deepl-cli/issues).

⭐ If you find this tool useful, please consider giving it a star on GitHub!