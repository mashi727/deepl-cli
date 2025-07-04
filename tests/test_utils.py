"""Tests for utility functions"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import time

from deepl_cli.utils import (
    BatchTranslator,
    TextProcessor,
    SubtitleTranslator,
    format_file_size,
    estimate_translation_time
)


class TestBatchTranslator:
    """Test cases for BatchTranslator"""

    def test_translate_files_success(self, tmp_path):
        """Test successful batch translation"""
        # Create mock translator
        mock_translator = Mock()
        mock_translator.translate.return_value = "Translated text"

        # Create test files
        file1 = tmp_path / "test1.txt"
        file1.write_text("Hello world")
        file2 = tmp_path / "test2.txt"
        file2.write_text("Test content")

        # Create batch translator
        batch = BatchTranslator(mock_translator)

        # Translate files
        results = batch.translate_files(
            [file1, file2],
            "JA",
            output_dir=tmp_path / "output",
            max_workers=1,
            delay_between=0.1
        )

        # Check results
        assert results['statistics']['total_files'] == 2
        assert results['statistics']['successful'] == 2
        assert results['statistics']['failed'] == 0
        assert results['statistics']['total_characters'] == len("Hello world") + len("Test content")

        # Check output files exist
        output_dir = tmp_path / "output"
        assert (output_dir / "test1_ja.txt").exists()
        assert (output_dir / "test2_ja.txt").exists()

    def test_translate_segments(self):
        """Test text segmentation for large texts"""
        mock_translator = Mock()
        mock_translator.translate.side_effect = lambda text, *args: f"[{text}]"

        batch = BatchTranslator(mock_translator)

        # Test text that needs segmentation
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        result = batch.translate_segments(text, "JA", segment_size=15)

        # Should preserve paragraph structure
        assert "\n\n" in result
        assert mock_translator.translate.call_count > 1


class TestTextProcessor:
    """Test cases for TextProcessor"""

    def test_preserve_placeholders(self):
        """Test placeholder preservation"""
        text = "Hello {name}, welcome to {place}!"
        processed, placeholders = TextProcessor.preserve_placeholders(text)

        assert "__PLACEHOLDER_0__" in processed
        assert "__PLACEHOLDER_1__" in processed
        assert placeholders["__PLACEHOLDER_0__"] == "{name}"
        assert placeholders["__PLACEHOLDER_1__"] == "{place}"

        # Test restoration
        restored = TextProcessor.restore_placeholders(processed, placeholders)
        assert restored == text

    def test_extract_code_blocks(self):
        """Test code block extraction"""
        text = "Here is code: `inline` and ```\nblock\ncode\n```"
        processed, blocks = TextProcessor.extract_code_blocks(text)

        assert "__CODE_BLOCK_0__" in processed
        assert "__CODE_BLOCK_1__" in processed
        assert len(blocks) == 2

        # Test restoration
        restored = TextProcessor.restore_code_blocks(processed, blocks)
        assert restored == text


class TestSubtitleTranslator:
    """Test cases for SubtitleTranslator"""

    def test_translate_srt(self):
        """Test SRT subtitle translation"""
        mock_translator = Mock()
        mock_translator.translate.side_effect = lambda text, *args: f"[{text}]"

        srt_content = """1
00:00:00,000 --> 00:00:02,000
Hello world

2
00:00:02,000 --> 00:00:04,000
Test subtitle
"""

        subtitle_translator = SubtitleTranslator(mock_translator)
        result = subtitle_translator.translate_srt(srt_content, "JA")

        assert "[Hello world]" in result
        assert "[Test subtitle]" in result
        assert "00:00:00,000 --> 00:00:02,000" in result
        assert "00:00:02,000 --> 00:00:04,000" in result


class TestHelperFunctions:
    """Test cases for helper functions"""

    def test_format_file_size(self):
        """Test file size formatting"""
        assert format_file_size(500) == "500.0 B"
        assert format_file_size(1500) == "1.5 KB"
        assert format_file_size(1500000) == "1.4 MB"
        assert format_file_size(1500000000) == "1.4 GB"

    def test_estimate_translation_time(self):
        """Test translation time estimation"""
        assert estimate_translation_time(500) == "0 seconds"
        assert estimate_translation_time(60000) == "1.0 minutes"
        assert estimate_translation_time(3600000) == "1.0 hours"
