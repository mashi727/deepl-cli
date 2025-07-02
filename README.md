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
- 📊 Usage statistics

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

2. Create a configuration file:
```bash
mkdir -p ~/.config/deepl-cli
echo "YOUR_API_KEY" > ~/.config/deepl-cli/api_key
chmod 600 ~/.config/deepl-cli/api_key
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

# Check API usage
deepl-cli --usage

# Verbose mode
deepl-cli JA "Hello" -v
```

### Supported Languages

- BG (Bulgarian)
- CS (Czech)
- DA (Danish)
- DE (German)
- EL (Greek)
- EN-GB (English UK)
- EN-US (English US)
- ES (Spanish)
- ET (Estonian)
- FI (Finnish)
- FR (French)
- HU (Hungarian)
- IT (Italian)
- JA (Japanese)
- LT (Lithuanian)
- LV (Latvian)
- NL (Dutch)
- PL (Polish)
- PT-PT (Portuguese)
- PT-BR (Portuguese Brazilian)
- RO (Romanian)
- RU (Russian)
- SK (Slovak)
- SL (Slovenian)
- SV (Swedish)
- ZH (Chinese)

## Examples

### Shell Script Integration

```bash
#!/bin/bash
# Translate all .txt files in a directory
for file in *.txt; do
    deepl-cli JA "$file" -o "translated_${file}"
done
```

### Python Integration

```python
from deepl_cli import DeepLTranslator

translator = DeepLTranslator()
result = translator.translate("Hello, world!", "JA")
print(result)  # こんにちは、世界！
```

## Configuration Files

The CLI looks for API keys in the following locations (in order):

1. Command line argument: `--api-key`
2. Environment variable: `DEEPL_API_KEY`
3. Config file: `~/.config/deepl-cli/api_key`
4. Legacy config: `~/.config/.deepl_apikey`
5. Home directory: `~/.deepl_apikey`

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/${GITHUB_USERNAME}/deepl-cli.git
cd deepl-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black src tests

# Type checking
mypy src
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test
pytest tests/test_translator.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DeepL](https://www.deepl.com) for providing the excellent translation API
- [pyperclip](https://github.com/asweigart/pyperclip) for clipboard functionality

## Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/${GITHUB_USERNAME}/deepl-cli/issues).

---

**Note**: This is an unofficial client for the DeepL API. It is not affiliated with DeepL SE.
