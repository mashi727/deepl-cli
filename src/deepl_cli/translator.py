"""DeepL translator core functionality"""

import os
from pathlib import Path
from typing import Optional, List
import logging

import deepl


class DeepLTranslator:
    """DeepL translation wrapper with configuration management"""
    
    SUPPORTED_LANGUAGES = [
        "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "EN",
        "ES", "ET", "FI", "FR", "HU", "IT", "JA", "LT", "LV",
        "NL", "PL", "PT-PT", "PT-BR", "PT", "RO", "RU", "SK",
        "SL", "SV", "ZH"
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize translator with API key
        
        Args:
            api_key: DeepL API key. If None, will try to load from config file
        """
        self.api_key = api_key or self._load_api_key()
        self.translator = None
        self._init_translator()
    
    def _load_api_key(self) -> str:
        """Load API key from configuration file"""
        config_paths = [
            Path.home() / '.config' / 'deepl-cli' / 'api_key',
            Path.home() / '.config' / '.deepl_apikey',  # Legacy support
            Path.home() / '.deepl_apikey'
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        api_key = f.read().strip()
                        if api_key:
                            logging.debug(f"API key loaded from {path}")
                            return api_key
                except Exception as e:
                    logging.error(f"Error reading {path}: {e}")
        
        raise ValueError(
            "API key not found. Please create one of these files:\n" +
            "\n".join(f"  - {path}" for path in config_paths[:2]) +
            "\nOr set DEEPL_API_KEY environment variable"
        )
    
    def _init_translator(self):
        """Initialize DeepL translator instance"""
        try:
            self.translator = deepl.Translator(self.api_key)
            # Test the API key with usage check
            self.translator.get_usage()
        except deepl.AuthorizationException:
            raise ValueError("Invalid API key")
        except Exception as e:
            raise ValueError(f"Failed to initialize translator: {e}")
    
    def translate(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (optional, auto-detect if None)
            
        Returns:
            Translated text
        """
        if not text.strip():
            return ""
        
        try:
            result = self.translator.translate_text(
                text,
                target_lang=target_lang,
                source_lang=source_lang
            )
            return result.text
        except deepl.QuotaExceededException:
            raise ValueError("DeepL API quota exceeded")
        except Exception as e:
            raise ValueError(f"Translation failed: {e}")
    
    def get_usage(self) -> dict:
        """Get API usage information"""
        usage = self.translator.get_usage()
        return {
            'character_count': usage.character.count,
            'character_limit': usage.character.limit
        }
    
    @classmethod
    def list_languages(cls) -> List[str]:
        """Get list of supported language codes"""
        return cls.SUPPORTED_LANGUAGES
