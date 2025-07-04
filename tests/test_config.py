"""Tests for configuration management"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch

from deepl_cli.config import (
    TranslationConfig,
    ConfigManager,
    LanguagePreferences
)


class TestTranslationConfig:
    """Test cases for TranslationConfig"""

    def test_default_values(self):
        """Test default configuration values"""
        config = TranslationConfig()

        assert config.api_key is None
        assert config.preserve_formatting is True
        assert config.batch_max_workers == 3
        assert config.segment_size == 5000


class TestConfigManager:
    """Test cases for ConfigManager"""

    def test_load_config_file_not_found(self):
        """Test loading config when file doesn't exist"""
        with patch('pathlib.Path.exists', return_value=False):
            manager = ConfigManager()
            assert isinstance(manager.config, TranslationConfig)

    def test_save_config(self, tmp_path):
        """Test saving configuration"""
        config_path = tmp_path / "config.json"
        manager = ConfigManager()
        manager.save_config(config_path)

        assert config_path.exists()

        # Check content
        with open(config_path) as f:
            data = json.load(f)

        assert data['api_key'] is None  # Should not save API key
        assert data['batch_max_workers'] == 3

    def test_update_config(self):
        """Test updating configuration values"""
        manager = ConfigManager()
        manager.update(verbose=True, batch_max_workers=5)

        assert manager.config.verbose is True
        assert manager.config.batch_max_workers == 5

    def test_get_config_value(self):
        """Test getting configuration values"""
        manager = ConfigManager()

        assert manager.get('batch_max_workers') == 3
        assert manager.get('nonexistent', 'default') == 'default'


class TestLanguagePreferences:
    """Test cases for LanguagePreferences"""

    def test_default_shortcuts(self, tmp_path):
        """Test default language shortcuts"""
        prefs = LanguagePreferences(tmp_path / "languages.json")

        assert prefs.resolve_language_code('en') == 'EN-US'
        assert prefs.resolve_language_code('japanese') == 'JA'
        assert prefs.resolve_language_code('JA') == 'JA'

    def test_add_shortcut(self, tmp_path):
        """Test adding custom shortcut"""
        prefs_path = tmp_path / "languages.json"
        prefs = LanguagePreferences(prefs_path)

        prefs.add_shortcut('jp', 'JA')

        assert prefs.resolve_language_code('jp') == 'JA'

        # Check persistence
        prefs2 = LanguagePreferences(prefs_path)
        assert prefs2.resolve_language_code('jp') == 'JA'

    def test_recent_languages(self, tmp_path):
        """Test recent languages tracking"""
        prefs = LanguagePreferences(tmp_path / "languages.json")

        prefs.add_to_recent('JA')
        prefs.add_to_recent('DE')
        prefs.add_to_recent('JA')  # Should move to front

        recent = prefs.get_recent()
        assert recent[0] == 'JA'
        assert recent[1] == 'DE'

    def test_favorite_languages(self, tmp_path):
        """Test favorite languages"""
        prefs = LanguagePreferences(tmp_path / "languages.json")

        # Add favorite
        added = prefs.toggle_favorite('JA')
        assert added is True
        assert 'JA' in prefs.preferences['favorites']

        # Remove favorite
        removed = prefs.toggle_favorite('JA')
        assert removed is False
        assert 'JA' not in prefs.preferences['favorites']
