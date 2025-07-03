"""Tests for DeepL translator"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

from deepl_cli.translator import DeepLTranslator
import deepl


class TestDeepLTranslator:
    """Test cases for DeepLTranslator class"""
    
    def test_supported_languages(self):
        """Test that supported languages are properly defined"""
        languages = DeepLTranslator.list_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "JA" in languages
        assert "EN-US" in languages
        assert "DE" in languages
        assert "ZH" in languages
    
    def test_is_language_supported(self):
        """Test language support validation"""
        assert DeepLTranslator.is_language_supported("JA")
        assert DeepLTranslator.is_language_supported("EN-US")
        assert DeepLTranslator.is_language_supported("ja")  # Case insensitive
        assert not DeepLTranslator.is_language_supported("INVALID")
        assert not DeepLTranslator.is_language_supported("")
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_init_with_api_key(self, mock_deepl):
        """Test initialization with provided API key"""
        mock_translator = Mock()
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator(api_key="test_key")
        
        mock_deepl.assert_called_once_with("test_key")
        mock_translator.get_usage.assert_called_once()
        assert translator.api_key == "test_key"
    
    @patch('deepl_cli.translator.deepl.Translator')
    @patch.object(DeepLTranslator, '_load_api_key')
    def test_init_without_api_key(self, mock_load_api_key, mock_deepl):
        """Test initialization without API key (loads from config)"""
        mock_load_api_key.return_value = "loaded_key"
        mock_translator = Mock()
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator()
        
        mock_load_api_key.assert_called_once()
        mock_deepl.assert_called_once_with("loaded_key")
        assert translator.api_key == "loaded_key"
    
    def test_load_api_key_from_file(self):
        """Test loading API key from configuration file"""
        with patch('pathlib.Path.exists') as mock_exists, \
             patch('pathlib.Path.is_file') as mock_is_file, \
             patch('pathlib.Path.read_text') as mock_read_text:
            
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_read_text.return_value = "test_api_key_123\n"
            
            translator = DeepLTranslator.__new__(DeepLTranslator)  # Don't call __init__
            api_key = translator._load_api_key()
            
            assert api_key == "test_api_key_123"
    
    def test_load_api_key_file_not_found(self):
        """Test API key loading when no config file exists"""
        with patch('pathlib.Path.exists', return_value=False):
            translator = DeepLTranslator.__new__(DeepLTranslator)
            
            with pytest.raises(ValueError) as exc_info:
                translator._load_api_key()
            
            assert "API key not found" in str(exc_info.value)
            assert "DEEPL_API_KEY" in str(exc_info.value)
    
    def test_load_api_key_empty_file(self):
        """Test API key loading when config file is empty"""
        with patch('pathlib.Path.exists') as mock_exists, \
             patch('pathlib.Path.is_file') as mock_is_file, \
             patch('pathlib.Path.read_text') as mock_read_text:
            
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_read_text.return_value = "   \n  "  # Only whitespace
            
            translator = DeepLTranslator.__new__(DeepLTranslator)
            
            with pytest.raises(ValueError):
                translator._load_api_key()
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_init_translator_invalid_key(self, mock_deepl):
        """Test initialization with invalid API key"""
        mock_deepl.side_effect = deepl.AuthorizationException("Invalid API key")
        
        with pytest.raises(ValueError) as exc_info:
            DeepLTranslator(api_key="invalid_key")
        
        assert "Invalid DeepL API key" in str(exc_info.value)
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_translate_empty_text(self, mock_deepl):
        """Test translation of empty text"""
        mock_translator = Mock()
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator(api_key="test_key")
        
        # Test empty string
        result = translator.translate("", "JA")
        assert result == ""
        
        # Test whitespace only
        result = translator.translate("   \n  ", "JA")
        assert result == ""
        
        # translate_text should not be called for empty input
        mock_translator.translate_text.assert_not_called()
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_translate_success(self, mock_deepl):
        """Test successful translation"""
        mock_translator = Mock()
        mock_result = Mock()
        mock_result.text = "こんにちは"
        mock_result.detected_source_lang = "EN"
        mock_translator.translate_text.return_value = mock_result
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator(api_key="test_key")
        result = translator.translate("Hello", "JA", "EN")
        
        assert result == "こんにちは"
        mock_translator.translate_text.assert_called_once_with(
            "Hello",
            target_lang="JA",
            source_lang="EN"
        )
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_translate_unsupported_language(self, mock_deepl):
        """Test translation with unsupported language"""
        mock_deepl.return_value = Mock()
        translator = DeepLTranslator(api_key="test_key")
        
        with pytest.raises(ValueError) as exc_info:
            translator.translate("Hello", "INVALID")
        
        assert "Unsupported target language" in str(exc_info.value)
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_translate_quota_exceeded(self, mock_deepl):
        """Test translation when API quota is exceeded"""
        mock_translator = Mock()
        mock_translator.translate_text.side_effect = deepl.QuotaExceededException("Quota exceeded")
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator(api_key="test_key")
        
        with pytest.raises(ValueError) as exc_info:
            translator.translate("Hello", "JA")
        
        assert "quota exceeded" in str(exc_info.value).lower()
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_get_usage_success(self, mock_deepl):
        """Test successful usage retrieval"""
        mock_translator = Mock()
        mock_usage = Mock()
        mock_usage.character.count = 1000
        mock_usage.character.limit = 500000
        mock_translator.get_usage.return_value = mock_usage
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator(api_key="test_key")
        usage = translator.get_usage()
        
        assert usage['character_count'] == 1000
        assert usage['character_limit'] == 500000
        assert usage['usage_percentage'] == 0.2  # 1000/500000 * 100
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_get_usage_error(self, mock_deepl):
        """Test usage retrieval error"""
        mock_translator = Mock()
        mock_translator.get_usage.side_effect = Exception("API error")
        mock_deepl.return_value = mock_translator
        
        translator = DeepLTranslator(api_key="test_key")
        
        with pytest.raises(ValueError) as exc_info:
            translator.get_usage()
        
        assert "Failed to retrieve usage information" in str(exc_info.value)