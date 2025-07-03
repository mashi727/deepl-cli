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
