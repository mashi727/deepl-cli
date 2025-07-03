"""Tests for CLI functionality"""

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
    
    @patch('deepl_cli.cli.sys.argv', ['deepl-cli', '--version'])
    def test_version_command(self, capsys):
        """Test --version command"""
        with pytest.raises(SystemExit):
            main()
        
        captured = capsys.readouterr()
        assert "0.1.0" in captured.out
    
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
        
        with pytest.raises(CLIError) as exc_info:
            validate_arguments(args)
        
        assert "Unsupported target language" in str(exc_info.value)
    
    def test_validate_arguments_valid(self):
        """Test argument validation with valid arguments"""
        args = Mock()
        args.list_languages = False
        args.usage = False
        args.target_lang = "ja"  # lowercase should be normalized
        args.source_lang = "en"  # lowercase should be normalized
        
        validate_arguments(args)
        
        assert args.target_lang == "JA"
        assert args.source_lang == "EN"
    
    def test_read_input_from_file(self):
        """Test reading input from file"""
        args = Mock()
        args.clipboard = False
        args.input_file = "test.txt"
        
        with patch('builtins.open', mock_open(read_data="Hello, world!")):
            with patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
                result = read_input(args)
        
        assert result == "Hello, world!"
    
    def test_read_input_file_not_found(self):
        """Test reading input from non-existent file"""
        args = Mock()
        args.clipboard = False
        args.input_file = "nonexistent.txt"
        
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
                with pytest.raises(CLIError) as exc_info:
                    read_input(args)
        
        assert "Input file not found" in str(exc_info.value)
    
    def test_read_input_empty_file(self):
        """Test reading input from empty file"""
        args = Mock()
        args.clipboard = False
        args.input_file = "empty.txt"
        
        with patch('builtins.open', mock_open(read_data="   \n  ")):
            with patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
                with pytest.raises(CLIError) as exc_info:
                    read_input(args)
        
        assert "Input file is empty" in str(exc_info.value)
    
    @patch('deepl_cli.cli.sys.stdin')
    def test_read_input_from_stdin(self, mock_stdin):
        """Test reading input from stdin"""
        args = Mock()
        args.clipboard = False
        args.input_file = None
        
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = "Hello from stdin"
        
        result = read_input(args)
        assert result == "Hello from stdin"
    
    @patch('deepl_cli.clipboard.ClipboardManager.is_available')
    @patch('deepl_cli.clipboard.ClipboardManager.read')
    def test_read_input_from_clipboard(self, mock_read, mock_available):
        """Test reading input from clipboard"""
        args = Mock()
        args.clipboard = True
        args.input_file = None
        
        mock_available.return_value = True
        mock_read.return_value = "Hello from clipboard"
        
        result = read_input(args)
        assert result == "Hello from clipboard"
    
    def test_read_input_no_input(self):
        """Test reading input when no input is provided"""
        args = Mock()
        args.clipboard = False
        args.input_file = None
        
        with patch('deepl_cli.cli.sys.stdin.isatty', return_value=True):
            with pytest.raises(CLIError) as exc_info:
                read_input(args)
        
        assert "No input provided" in str(exc_info.value)
    
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
        
        with patch('builtins.open', mock_open()) as mock_file:
            write_output("Test output", args)
        
        mock_file.assert_called_once_with("output.txt", 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with("Test output")
    
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
        assert "copied to clipboard" in captured.out


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
            with patch('builtins.open', mock_open(read_data="Hello")):
                exit_code = main()
        
        assert exit_code == 0
        mock_translator.translate.assert_called_once_with("Hello", "JA", None)