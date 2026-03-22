"""Tests for CLI commands."""

from click.testing import CliRunner
import pytest

from zoho_sheet_cli.cli import cli


class TestCLI:
    """Test cases for CLI."""
    
    def test_cli_help(self):
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        
        assert result.exit_code == 0
        assert "Zoho Sheet CLI" in result.output
        assert "auth" in result.output
        assert "workbook" in result.output
        assert "worksheet" in result.output
        assert "cell" in result.output
        assert "file" in result.output
    
    def test_cli_version(self):
        """Test CLI version flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        
        assert result.exit_code == 0
        assert "zsheet" in result.output
        assert "0.1.0" in result.output
    
    def test_auth_help(self):
        """Test auth command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["auth", "--help"])
        
        assert result.exit_code == 0
        assert "init" in result.output
        assert "status" in result.output
    
    def test_workbook_help(self):
        """Test workbook command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["workbook", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.output
        assert "create" in result.output
    
    def test_worksheet_help(self):
        """Test worksheet command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["worksheet", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.output
        assert "add" in result.output
    
    def test_cell_help(self):
        """Test cell command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["cell", "--help"])
        
        assert result.exit_code == 0
        assert "get" in result.output
        assert "set" in result.output
    
    def test_file_help(self):
        """Test file command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["file", "--help"])
        
        assert result.exit_code == 0
        assert "export" in result.output
        assert "import" in result.output
