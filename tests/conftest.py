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
