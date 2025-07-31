"""Tests for CLI functionality with improved stdin support"""

import pytest
import sys
import io
from unittest.mock import Mock, patch, mock_open
from deepl_cli.cli import main, read_input, write_output, CLIError, validate_arguments


class TestCLI:
    """Test cases for CLI functionality"""
    
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', '--list-languages'])
    def test_list_languages_command(self, capsys):
        """Test --list-languages command"""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Supported language codes:" in captured.out
        assert "JA" in captured.out
        assert "Total:" in captured.out
        assert "deepl-cli <TARGET_LANG> --stdin" in captured.out
    
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', '--version'])
    def test_version_command(self, capsys):
        """Test --version command"""
        with pytest.raises(SystemExit):
            main()
        
        captured = capsys.readouterr()
        assert "0.2.0" in captured.out
    
    def test_validate_arguments_missing_target_lang(self):
        """Test argument validation with missing target language"""
        args = Mock()
        args.list_languages = False
        args.usage = False
        args.target_lang = None
        
        with pytest.raises(CLIError) as exc_info:
            validate_arguments(args)
        
        assert "Target language is required" in str(exc_info.value)
    
    def test_validate_arguments_invalid_target_lang(self):
        """Test argument validation with invalid target language"""
        args = Mock()
        args.list_languages = False
        args.usage = False
        args.target_lang = "INVALID"
        args.source_lang = None
        args.clipboard = False
        args.stdin = False
        args.input_text = None
        
        with pytest.raises(CLIError) as exc_info:
            validate_arguments(args)
        
        assert "Unsupported target language" in str(exc_info.value)
    
    def test_validate_arguments_conflicting_options(self):
        """Test argument validation with conflicting options"""
        args = Mock()
        args.list_languages = False
        args.usage = False
        args.target_lang = "JA"
        args.source_lang = None
        args.clipboard = True
        args.stdin = True
        args.input_text = None
        
        with pytest.raises(CLIError) as exc_info:
            validate_arguments(args)
        
        assert "Cannot use --clipboard with --stdin" in str(exc_info.value)
    
    def test_validate_arguments_clipboard_with_dash(self):
        """Test argument validation with clipboard and dash"""
        args = Mock()
        args.list_languages = False
        args.usage = False
        args.target_lang = "JA"
        args.source_lang = None
        args.clipboard = True
        args.stdin = False
        args.input_text = "-"
        
        with pytest.raises(CLIError) as exc_info:
            validate_arguments(args)
        
        assert "Cannot use --clipboard with --stdin or '-'" in str(exc_info.value)
    
    def test_validate_arguments_valid(self):
        """Test argument validation with valid arguments"""
        args = Mock()
        args.list_languages = False
        args.usage = False
        args.target_lang = "ja"  # lowercase should be normalized
        args.source_lang = "en"  # lowercase should be normalized
        args.clipboard = False
        args.stdin = False
        args.input_text = None
        
        validate_arguments(args)
        
        assert args.target_lang == "JA"
        assert args.source_lang == "EN"
    
    def test_read_input_from_file(self):
        """Test reading input from file"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = "test.txt"
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.read_text', return_value="Hello, world!"), \
             patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            result = read_input(args)
        
        assert result == "Hello, world!"
    
    def test_read_input_direct_text(self):
        """Test reading direct text input"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = "Hello, world!"
        
        with patch('pathlib.Path.exists', return_value=False), \
             patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            result = read_input(args)
        
        assert result == "Hello, world!"
    
    def test_read_input_file_not_found(self):
        """Test reading input from non-existent file that's not direct text"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = "nonexistent.txt"
        
        with patch('pathlib.Path.exists', return_value=False), \
             patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            # This should treat it as direct text, not file
            result = read_input(args)
            assert result == "nonexistent.txt"
    
    def test_read_input_empty_file(self):
        """Test reading input from empty file"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = "empty.txt"
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.read_text', return_value="   \n  "), \
             patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            with pytest.raises(CLIError) as exc_info:
                read_input(args)
        
        assert "Input file is empty" in str(exc_info.value)
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_read_input_from_stdin_explicit(self, mock_stdin):
        """Test reading input from stdin with --stdin flag"""
        args = Mock()
        args.clipboard = False
        args.stdin = True
        args.input_text = None
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "Hello from stdin"
        
        result = read_input(args)
        assert result == "Hello from stdin"
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_read_input_from_stdin_dash(self, mock_stdin):
        """Test reading input from stdin with - argument"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = "-"
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "Hello from stdin dash"
        
        result = read_input(args)
        assert result == "Hello from stdin dash"
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_read_input_from_stdin_auto_detect(self, mock_stdin):
        """Test auto-detecting stdin input (pipe)"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = None
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "Hello from piped stdin"
        
        result = read_input(args)
        assert result == "Hello from piped stdin"
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_read_input_from_stdin_empty(self, mock_stdin):
        """Test reading empty input from stdin"""
        args = Mock()
        args.clipboard = False
        args.stdin = True
        args.input_text = None
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = ""
        
        with pytest.raises(CLIError) as exc_info:
            read_input(args)
        
        assert "No input received from stdin" in str(exc_info.value)
    
    @patch('deepl_cli.clipboard.ClipboardManager.is_available')
    @patch('deepl_cli.clipboard.ClipboardManager.read')
    def test_read_input_from_clipboard(self, mock_read, mock_available):
        """Test reading input from clipboard"""
        args = Mock()
        args.clipboard = True
        args.stdin = False
        args.input_text = None
        
        mock_available.return_value = True
        mock_read.return_value = "Hello from clipboard"
        
        result = read_input(args)
        assert result == "Hello from clipboard"
    
    def test_read_input_no_input(self):
        """Test reading input when no input is provided"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = None
        
        with patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            with pytest.raises(CLIError) as exc_info:
                read_input(args)
        
        assert "No input provided" in str(exc_info.value)
        assert "deepl-cli JA --stdin" in str(exc_info.value)
        assert "deepl-cli JA -" in str(exc_info.value)
    
    def test_write_output_to_stdout(self, capsys):
        """Test writing output to stdout"""
        args = Mock()
        args.clipboard = False
        args.output = None
        
        write_output("Test output", args)
        
        captured = capsys.readouterr()
        assert captured.out.strip() == "Test output"
    
    def test_write_output_to_file(self):
        """Test writing output to file"""
        args = Mock()
        args.clipboard = False
        args.output = "output.txt"
        
        with patch('pathlib.Path.write_text') as mock_write, \
             patch('pathlib.Path.parent') as mock_parent:
            mock_parent.mkdir = Mock()
            write_output("Test output", args)
            mock_write.assert_called_once_with("Test output", encoding='utf-8')
    
    @patch('deepl_cli.clipboard.ClipboardManager.is_available')
    @patch('deepl_cli.clipboard.ClipboardManager.write')
    def test_write_output_to_clipboard(self, mock_write, mock_available, capsys):
        """Test writing output to clipboard"""
        args = Mock()
        args.clipboard = True
        args.output = None
        
        mock_available.return_value = True
        
        write_output("Test output", args)
        
        mock_write.assert_called_once_with("Test output")
        captured = capsys.readouterr()
        assert "copied to clipboard" in captured.err


# Integration tests
class TestIntegration:
    """Integration tests"""
    
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', '--help'])
    def test_help_command(self):
        """Test help command shows usage information"""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
    
    @patch('deepl_cli.cli.DeepLTranslator')
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', 'JA', 'Hello'])
    def test_simple_translation(self, mock_translator_class):
        """Test simple translation workflow"""
        mock_translator = Mock()
        mock_translator.translate.return_value = "こんにちは"
        mock_translator_class.return_value = mock_translator
        
        with patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            exit_code = main()
        
        assert exit_code == 0
        mock_translator.translate.assert_called_once_with("Hello", "JA", None)
    
    @patch('deepl_cli.cli.DeepLTranslator')
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', 'JA', '--stdin'])
    @patch('deepl_cli.cli.sys.stdin')
    def test_stdin_translation(self, mock_stdin, mock_translator_class):
        """Test translation from stdin"""
        mock_translator = Mock()
        mock_translator.translate.return_value = "こんにちは"
        mock_translator_class.return_value = mock_translator
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "Hello from stdin"
        
        exit_code = main()
        
        assert exit_code == 0
        mock_translator.translate.assert_called_once_with("Hello from stdin", "JA", None)
    
    @patch('deepl_cli.cli.DeepLTranslator')
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', 'JA', '-'])
    @patch('deepl_cli.cli.sys.stdin')
    def test_dash_translation(self, mock_stdin, mock_translator_class):
        """Test translation with dash argument"""
        mock_translator = Mock()
        mock_translator.translate.return_value = "こんにちは"
        mock_translator_class.return_value = mock_translator
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "Hello from dash"
        
        exit_code = main()
        
        assert exit_code == 0
        mock_translator.translate.assert_called_once_with("Hello from dash", "JA", None)


class TestStdinBehavior:
    """Test different stdin behaviors"""
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_stdin_priority_explicit_flag(self, mock_stdin):
        """Test that explicit --stdin flag takes priority"""
        args = Mock()
        args.clipboard = False
        args.stdin = True
        args.input_text = "some_text"  # This should be ignored when --stdin is used
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "stdin content"
        
        result = read_input(args)
        assert result == "stdin content"
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_stdin_priority_dash(self, mock_stdin):
        """Test that dash (-) takes priority over text content"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = "-"
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "dash stdin content"
        
        result = read_input(args)
        assert result == "dash stdin content"
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_stdin_auto_detect_with_content(self, mock_stdin):
        """Test auto-detection of stdin when content is available"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = None
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "auto detected content"
        
        result = read_input(args)
        assert result == "auto detected content"
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_stdin_auto_detect_empty_falls_back(self, mock_stdin):
        """Test that empty auto-detected stdin falls back to error"""
        args = Mock()
        args.clipboard = False
        args.stdin = False
        args.input_text = None
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = ""  # Empty content
        
        with pytest.raises(CLIError) as exc_info:
            read_input(args)
        
        assert "No input provided" in str(exc_info.value)