"""Configuration management for DeepL CLI"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import os


logger = logging.getLogger(__name__)


@dataclass
class TranslationConfig:
    """Translation configuration settings"""

    # API settings
    api_key: Optional[str] = None
    api_endpoint: Optional[str] = None

    # Translation defaults
    default_target_lang: Optional[str] = None
    default_source_lang: Optional[str] = None
    preserve_formatting: bool = True

    # Batch translation settings
    batch_max_workers: int = 3
    batch_delay_seconds: float = 0.5
    segment_size: int = 5000

    # File handling
    output_suffix_format: str = "_{lang}"
    create_backup: bool = False

    # Display settings
    show_progress: bool = True
    verbose: bool = False

    # Advanced settings
    retry_attempts: int = 3
    retry_delay: float = 1.0
    timeout_seconds: int = 30


class ConfigManager:
    """
    Manage DeepL CLI configuration
    """

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".config" / "deepl-cli" / "config.json",
        Path.home() / ".deepl-cli" / "config.json",
    ]

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager

        Args:
            config_path: Custom configuration file path
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()

    def _find_config_file(self) -> Optional[Path]:
        """
        Find existing configuration file

        Returns:
            Path to configuration file or None
        """
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                logger.debug(f"Found config file: {path}")
                return path
        return None

    def _load_config(self) -> TranslationConfig:
        """
        Load configuration from file

        Returns:
            TranslationConfig instance
        """
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Load API key from environment if not in config
                if not data.get('api_key'):
                    data['api_key'] = os.environ.get('DEEPL_API_KEY')

                config = TranslationConfig(**data)
                logger.info(f"Loaded configuration from {self.config_path}")
                return config

            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")

        # Return default config with env API key if available
        return TranslationConfig(api_key=os.environ.get('DEEPL_API_KEY'))

    def save_config(self, config_path: Optional[Path] = None) -> None:
        """
        Save configuration to file

        Args:
            config_path: Path to save configuration
        """
        path = config_path or self.config_path

        if not path:
            path = self.DEFAULT_CONFIG_PATHS[0]

        # Create directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert config to dict, excluding sensitive data for saving
        config_dict = asdict(self.config)

        # Don't save API key to file for security
        if 'api_key' in config_dict:
            config_dict['api_key'] = None

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2)

        # Set appropriate permissions (readable/writable by user only)
        path.chmod(0o600)

        logger.info(f"Saved configuration to {path}")

    def update(self, **kwargs) -> None:
        """
        Update configuration values

        Args:
            **kwargs: Configuration values to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                logger.debug(f"Updated config: {key} = {value}")
            else:
                logger.warning(f"Unknown configuration key: {key}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return getattr(self.config, key, default)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary

        Returns:
            Configuration as dictionary
        """
        return asdict(self.config)

    @classmethod
    def create_default_config(cls, path: Optional[Path] = None) -> None:
        """
        Create default configuration file

        Args:
            path: Path for configuration file
        """
        if not path:
            path = cls.DEFAULT_CONFIG_PATHS[0]

        path.parent.mkdir(parents=True, exist_ok=True)

        default_config = TranslationConfig()
        config_dict = asdict(default_config)

        # Add comments as a special field
        config_dict['_comments'] = {
            'api_key': 'Set via DEEPL_API_KEY environment variable or config file',
            'default_target_lang': 'Default target language code (e.g., JA, EN-US)',
            'batch_max_workers': 'Maximum concurrent translations for batch mode',
            'segment_size': 'Maximum characters per segment for large texts'
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2)

        path.chmod(0o600)
        print(f"Created default configuration at: {path}")


class LanguagePreferences:
    """
    Manage language preferences and shortcuts
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize language preferences

        Args:
            config_path: Path to preferences file
        """
        self.config_path = config_path or (
            Path.home() / ".config" / "deepl-cli" / "languages.json"
        )
        self.preferences = self._load_preferences()

    def _load_preferences(self) -> Dict[str, Any]:
        """
        Load language preferences

        Returns:
            Dictionary of preferences
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load language preferences: {e}")

        # Default preferences
        return {
            'shortcuts': {
                'en': 'EN-US',
                'pt': 'PT-PT',
                'english': 'EN-US',
                'japanese': 'JA',
                'german': 'DE',
                'french': 'FR',
                'spanish': 'ES',
                'chinese': 'ZH'
            },
            'recent': [],
            'favorites': []
        }

    def save_preferences(self) -> None:
        """Save language preferences to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.preferences, f, indent=2)

    def resolve_language_code(self, code: str) -> str:
        """
        Resolve language shortcut to full code

        Args:
            code: Language code or shortcut

        Returns:
            Full language code
        """
        code_lower = code.lower()

        # Check shortcuts
        if code_lower in self.preferences['shortcuts']:
            return self.preferences['shortcuts'][code_lower]

        # Return uppercase version
        return code.upper()

    def add_shortcut(self, shortcut: str, language_code: str) -> None:
        """
        Add language shortcut

        Args:
            shortcut: Shortcut name
            language_code: Full language code
        """
        self.preferences['shortcuts'][shortcut.lower()] = language_code.upper()
        self.save_preferences()

    def add_to_recent(self, language_code: str, max_recent: int = 10) -> None:
        """
        Add language to recent list

        Args:
            language_code: Language code
            max_recent: Maximum number of recent items
        """
        recent = self.preferences['recent']

        # Remove if already exists
        if language_code in recent:
            recent.remove(language_code)

        # Add to beginning
        recent.insert(0, language_code)

        # Trim to max size
        self.preferences['recent'] = recent[:max_recent]
        self.save_preferences()

    def get_recent(self) -> List[str]:
        """Get list of recently used languages"""
        return self.preferences['recent'].copy()

    def toggle_favorite(self, language_code: str) -> bool:
        """
        Toggle language as favorite

        Args:
            language_code: Language code

        Returns:
            True if added to favorites, False if removed
        """
        favorites = self.preferences['favorites']

        if language_code in favorites:
            favorites.remove(language_code)
            added = False
        else:
            favorites.append(language_code)
            added = True

        self.save_preferences()
        return added
