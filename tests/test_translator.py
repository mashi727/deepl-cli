"""Tests for DeepL translator"""

import pytest
from unittest.mock import Mock, patch
from deepl_cli.translator import DeepLTranslator


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
    
    @patch('deepl_cli.translator.deepl.Translator')
    def test_translate_empty_text(self, mock_deepl):
        """Test translation of empty text"""
        translator = DeepLTranslator(api_key="test_key")
        result = translator.translate("", "JA")
        assert result == ""
        mock_deepl.return_value.translate_text.assert_not_called()
    
    def test_invalid_api_key_error(self):
        """Test that invalid API key raises appropriate error"""
        with patch('deepl_cli.translator.deepl.Translator') as mock_deepl:
            mock_deepl.side_effect = Exception("Invalid API key")
            with pytest.raises(ValueError):
                DeepLTranslator(api_key="invalid_key")
