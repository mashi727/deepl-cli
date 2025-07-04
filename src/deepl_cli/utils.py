"""Utility functions for DeepL CLI"""

import re
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from .translator import DeepLTranslator


logger = logging.getLogger(__name__)


class BatchTranslator:
    """
    Batch translation utilities for processing multiple files or text segments
    """

    def __init__(self, translator: DeepLTranslator):
        """
        Initialize batch translator

        Args:
            translator: DeepL translator instance
        """
        self.translator = translator
        self._stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_characters': 0,
            'start_time': None,
            'end_time': None
        }

    def translate_files(
        self,
        input_files: List[Path],
        target_lang: str,
        output_dir: Optional[Path] = None,
        source_lang: Optional[str] = None,
        max_workers: int = 3,
        delay_between: float = 0.5
    ) -> Dict[str, any]:
        """
        Translate multiple files in batch

        Args:
            input_files: List of input file paths
            target_lang: Target language code
            output_dir: Output directory (default: same as input)
            source_lang: Source language code (auto-detect if None)
            max_workers: Maximum concurrent translations
            delay_between: Delay between translations (seconds)

        Returns:
            Dictionary with translation statistics and results
        """
        self._stats['total_files'] = len(input_files)
        self._stats['start_time'] = time.time()

        results = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    self._translate_single_file,
                    file_path,
                    target_lang,
                    output_dir,
                    source_lang
                ): file_path
                for file_path in input_files
            }

            for i, future in enumerate(as_completed(future_to_file)):
                file_path = future_to_file[future]

                try:
                    output_path, char_count = future.result()
                    results[str(file_path)] = {
                        'status': 'success',
                        'output': str(output_path),
                        'characters': char_count
                    }
                    self._stats['successful'] += 1
                    self._stats['total_characters'] += char_count
                    logger.info(f"Translated: {file_path} -> {output_path}")

                except Exception as e:
                    results[str(file_path)] = {
                        'status': 'failed',
                        'error': str(e)
                    }
                    self._stats['failed'] += 1
                    logger.error(f"Failed to translate {file_path}: {e}")

                # Add delay between translations (except for the last one)
                if i < len(input_files) - 1:
                    time.sleep(delay_between)

        self._stats['end_time'] = time.time()

        return {
            'statistics': self._stats.copy(),
            'results': results,
            'duration': self._stats['end_time'] - self._stats['start_time']
        }

    def _translate_single_file(
        self,
        input_path: Path,
        target_lang: str,
        output_dir: Optional[Path],
        source_lang: Optional[str]
    ) -> Tuple[Path, int]:
        """
        Translate a single file

        Args:
            input_path: Input file path
            target_lang: Target language code
            output_dir: Output directory
            source_lang: Source language code

        Returns:
            Tuple of (output_path, character_count)
        """
        # Read input file
        text = input_path.read_text(encoding='utf-8')

        if not text.strip():
            raise ValueError(f"File is empty: {input_path}")

        # Translate
        translated = self.translator.translate(text, target_lang, source_lang)

        # Determine output path
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{input_path.stem}_{target_lang.lower()}{input_path.suffix}"
        else:
            output_path = input_path.parent / f"{input_path.stem}_{target_lang.lower()}{input_path.suffix}"

        # Write output
        output_path.write_text(translated, encoding='utf-8')

        return output_path, len(text)

    def translate_segments(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        segment_size: int = 5000,
        preserve_formatting: bool = True
    ) -> str:
        """
        Translate text in segments to handle large texts

        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code
            segment_size: Maximum characters per segment
            preserve_formatting: Try to preserve paragraph formatting

        Returns:
            Translated text
        """
        if len(text) <= segment_size:
            return self.translator.translate(text, target_lang, source_lang)

        segments = self._split_text(text, segment_size, preserve_formatting)
        translated_segments = []

        for i, segment in enumerate(segments):
            logger.debug(f"Translating segment {i+1}/{len(segments)} ({len(segment)} chars)")
            translated = self.translator.translate(segment, target_lang, source_lang)
            translated_segments.append(translated)

            # Small delay between segments
            if i < len(segments) - 1:
                time.sleep(0.2)

        # Join with appropriate separator
        if preserve_formatting and '\n\n' in text:
            return '\n\n'.join(translated_segments)
        else:
            return ' '.join(translated_segments)

    def _split_text(
        self,
        text: str,
        max_size: int,
        preserve_formatting: bool
    ) -> List[str]:
        """
        Split text into segments

        Args:
            text: Text to split
            max_size: Maximum size per segment
            preserve_formatting: Try to preserve paragraph boundaries

        Returns:
            List of text segments
        """
        if not preserve_formatting:
            # Simple character-based splitting
            return [text[i:i+max_size] for i in range(0, len(text), max_size)]

        # Try to split on paragraph boundaries
        paragraphs = text.split('\n\n')
        segments = []
        current_segment = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para) + 2  # +2 for \n\n

            if current_size + para_size > max_size and current_segment:
                # Start new segment
                segments.append('\n\n'.join(current_segment))
                current_segment = [para]
                current_size = para_size
            else:
                current_segment.append(para)
                current_size += para_size

        if current_segment:
            segments.append('\n\n'.join(current_segment))

        return segments


class TextProcessor:
    """
    Text processing utilities for pre/post translation
    """

    @staticmethod
    def preserve_placeholders(
        text: str,
        placeholder_pattern: str = r'\{[^}]+\}'
    ) -> Tuple[str, Dict[str, str]]:
        """
        Replace placeholders with tokens to preserve them during translation

        Args:
            text: Input text
            placeholder_pattern: Regex pattern for placeholders

        Returns:
            Tuple of (processed_text, placeholder_map)
        """
        placeholders = {}
        counter = 0

        def replace_placeholder(match):
            nonlocal counter
            placeholder = match.group(0)
            token = f"__PLACEHOLDER_{counter}__"
            placeholders[token] = placeholder
            counter += 1
            return token

        processed = re.sub(placeholder_pattern, replace_placeholder, text)
        return processed, placeholders

    @staticmethod
    def restore_placeholders(
        text: str,
        placeholder_map: Dict[str, str]
    ) -> str:
        """
        Restore placeholders after translation

        Args:
            text: Translated text with tokens
            placeholder_map: Mapping of tokens to original placeholders

        Returns:
            Text with restored placeholders
        """
        for token, placeholder in placeholder_map.items():
            text = text.replace(token, placeholder)
        return text

    @staticmethod
    def extract_code_blocks(
        text: str
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Extract code blocks to prevent translation

        Args:
            text: Input text

        Returns:
            Tuple of (text_without_code, list_of_code_blocks)
        """
        code_blocks = []
        counter = 0

        # Match both inline code and code blocks
        pattern = r'```[\s\S]*?```|`[^`]+`'

        def replace_code(match):
            nonlocal counter
            code = match.group(0)
            token = f"__CODE_BLOCK_{counter}__"
            code_blocks.append((token, code))
            counter += 1
            return token

        processed = re.sub(pattern, replace_code, text)
        return processed, code_blocks

    @staticmethod
    def restore_code_blocks(
        text: str,
        code_blocks: List[Tuple[str, str]]
    ) -> str:
        """
        Restore code blocks after translation

        Args:
            text: Translated text
            code_blocks: List of (token, code) tuples

        Returns:
            Text with restored code blocks
        """
        for token, code in code_blocks:
            text = text.replace(token, code)
        return text


class SubtitleTranslator:
    """
    Subtitle file translation utilities (SRT format)
    """

    def __init__(self, translator: DeepLTranslator):
        """
        Initialize subtitle translator

        Args:
            translator: DeepL translator instance
        """
        self.translator = translator
        self.srt_pattern = re.compile(
            r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)',
            re.DOTALL
        )

    def translate_srt(
        self,
        srt_content: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> str:
        """
        Translate SRT subtitle file content

        Args:
            srt_content: SRT file content
            target_lang: Target language code
            source_lang: Source language code

        Returns:
            Translated SRT content
        """
        subtitles = list(self.srt_pattern.finditer(srt_content))
        translated_parts = []

        for i, match in enumerate(subtitles):
            number = match.group(1)
            timing = match.group(2)
            text = match.group(3).strip()

            if text:
                # Translate the subtitle text
                logger.debug(f"Translating subtitle {number}/{len(subtitles)}")
                translated_text = self.translator.translate(text, target_lang, source_lang)
            else:
                translated_text = ""

            # Reconstruct subtitle entry
            translated_parts.append(f"{number}\n{timing}\n{translated_text}")

            # Small delay between translations
            if i < len(subtitles) - 1:
                time.sleep(0.1)

        return '\n\n'.join(translated_parts) + '\n'


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def estimate_translation_time(
    character_count: int,
    chars_per_second: float = 1000.0
) -> str:
    """
    Estimate translation time based on character count

    Args:
        character_count: Number of characters to translate
        chars_per_second: Estimated translation speed

    Returns:
        Human-readable time estimate
    """
    seconds = character_count / chars_per_second

    if seconds < 60:
        return f"{seconds:.0f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
