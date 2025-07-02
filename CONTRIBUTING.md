# Contributing to DeepL CLI

Thank you for your interest in contributing to DeepL CLI! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/${GITHUB_USERNAME}/deepl-cli/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)

### Suggesting Features

1. Check existing issues and pull requests
2. Open a new issue with the "enhancement" label
3. Describe the feature and its use case

### Submitting Code

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Format code: `black src tests`
7. Commit with descriptive message
8. Push and create a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/deepl-cli.git
cd deepl-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

### Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update type hints

## Pull Request Process

1. Update documentation
2. Add tests
3. Ensure CI passes
4. Request review
5. Address feedback
6. Merge after approval

Thank you for contributing!
