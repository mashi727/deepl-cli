"""DeepL API translator implementation"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Union

import deepl


logger = logging.getLogger(__name__)


class DeepLTranslator:
    """
    DeepL API wrapper for translation operations
    
    This class provides a high-level interface to the DeepL translation API,
    handling authentication, translation requests, and usage monitoring.
    """
    
    # Supported language codes
    _SUPPORTED_LANGUAGES = [
        "BG", "CS", "DA", "DE", "EL", "EN", "EN-GB", "EN-US",
        "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO",
        "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR", "PT-PT",
        "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"
    ]
    
    # Configuration file paths (in order of priority)
    _CONFIG_PATHS = [
        Path.home() / ".token" / "deepl-cli" / "api_key",
        Path.home() / ".config" / "deepl-cli" / "api_key",
        Path.home() / ".config" / ".deepl_apikey",
        Path.home() / ".deepl_apikey",
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the DeepL translator
        
        Args:
            api_key: DeepL API key. If not provided, will attempt to load from
                    environment variable or configuration files.
                    
        Raises:
            ValueError: If no valid API key is found or if authentication fails
        """
        self.api_key = api_key or self._load_api_key()
        self._translator = self._init_translator()
    
    def _load_api_key(self) -> str:
        """
        Load API key from configuration files
        
        Returns:
            API key string
            
        Raises:
            ValueError: If no valid API key is found
        """
        # Try each config path in order
        for config_path in self._CONFIG_PATHS:
            if config_path.exists() and config_path.is_file():
                try:
                    api_key = config_path.read_text(encoding='utf-8').strip()
                    if api_key:
                        logger.debug(f"Loaded API key from {config_path}")
                        return api_key
                except Exception as e:
                    logger.warning(f"Failed to read {config_path}: {e}")
        
        # If no config file found, provide helpful error message
        config_locations = "\n  ".join(str(p) for p in self._CONFIG_PATHS[:2])
        raise ValueError(
            f"API key not found. Please provide one of:\n"
            f"1. Pass api_key parameter\n"
            f"2. Set DEEPL_API_KEY environment variable\n"
            f"3. Create config file at:\n  {config_locations}\n"
            f"Get your API key from: https://www.deepl.com/pro-api"
        )
    
    def _init_translator(self) -> deepl.Translator:
        """
        Initialize the DeepL translator client
        
        Returns:
            Configured DeepL translator instance
            
        Raises:
            ValueError: If API key is invalid or authentication fails
        """
        try:
            translator = deepl.Translator(self.api_key)
            # Verify API key by checking usage
            translator.get_usage()
            logger.info("DeepL translator initialized successfully")
            return translator
        except deepl.AuthorizationException:
            raise ValueError(
                "Invalid DeepL API key. Please check your API key at:\n"
                "https://www.deepl.com/account/summary"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize DeepL translator: {e}")
    
    @classmethod
    def list_languages(cls) -> List[str]:
        """
        Get list of supported language codes
        
        Returns:
            List of supported language codes
        """
        return cls._SUPPORTED_LANGUAGES.copy()
    
    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        """
        Check if a language code is supported
        
        Args:
            language: Language code to check
            
        Returns:
            True if language is supported, False otherwise
        """
        if not language:
            return False
        return language.upper() in cls._SUPPORTED_LANGUAGES
    
    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'JA', 'EN-US')
            source_lang: Source language code (auto-detect if None)
            
        Returns:
            Translated text
            
        Raises:
            ValueError: If translation fails or languages are unsupported
        """
        # Handle empty input
        if not text or not text.strip():
            return ""
        
        # Validate languages
        target_lang = target_lang.upper()
        if not self.is_language_supported(target_lang):
            raise ValueError(
                f"Unsupported target language: {target_lang}\n"
                f"Supported languages: {', '.join(self._SUPPORTED_LANGUAGES[:10])}..."
            )
        
        if source_lang:
            source_lang = source_lang.upper()
            if not self.is_language_supported(source_lang):
                raise ValueError(f"Unsupported source language: {source_lang}")
        
        try:
            logger.debug(
                f"Translating {len(text)} characters to {target_lang}"
                f"{f' from {source_lang}' if source_lang else ''}"
            )
            
            result = self._translator.translate_text(
                text,
                target_lang=target_lang,
                source_lang=source_lang
            )
            
            logger.info(
                f"Translation completed: {result.detected_source_lang or source_lang} → {target_lang}"
            )
            
            return result.text
            
        except deepl.QuotaExceededException:
            raise ValueError(
                "DeepL API quota exceeded. Please check your usage limits:\n"
                "https://www.deepl.com/account/usage"
            )
        except deepl.DeepLException as e:
            raise ValueError(f"Translation failed: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error during translation: {e}")
    
    def get_usage(self) -> Dict[str, Union[int, float]]:
        """
        Get API usage information
        
        Returns:
            Dictionary with usage information:
            - character_count: Characters used
            - character_limit: Total character limit
            - usage_percentage: Percentage of quota used
            
        Raises:
            ValueError: If usage information cannot be retrieved
        """
        try:
            usage = self._translator.get_usage()
            
            if usage.character is None:
                raise ValueError("Character usage information not available")
            
            character_count = usage.character.count
            character_limit = usage.character.limit
            
            # Calculate percentage with proper handling of edge cases
            if character_limit == 0:
                usage_percentage = 100.0
            else:
                usage_percentage = (character_count / character_limit) * 100
            
            return {
                'character_count': character_count,
                'character_limit': character_limit,
                'usage_percentage': round(usage_percentage, 2)
            }
            
        except Exception as e:
            raise ValueError(f"Failed to retrieve usage information: {e}")
    
    def __repr__(self) -> str:
        """String representation of the translator"""
        return f"DeepLTranslator(api_key={'***' if self.api_key else 'None'})"
