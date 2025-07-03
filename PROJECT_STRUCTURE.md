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
