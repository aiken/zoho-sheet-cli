"""Tests for configuration module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from zoho_sheet_cli.config import Config, get_config


class TestConfig:
    """Test cases for Config class."""
    
    def test_config_default_values(self, tmp_path):
        """Test config loads with default values."""
        config = Config(config_path=str(tmp_path / "config.env"))
        
        assert config.region == "us"
        assert config.client_id == ""
        assert config.client_secret == ""
        assert config.refresh_token == ""
        assert not config.is_authenticated
    
    def test_config_api_urls(self, tmp_path):
        """Test API URL generation for different regions."""
        config = Config(config_path=str(tmp_path / "config.env"))
        
        # Test US (default)
        assert config.api_base_url == "https://sheet.zoho.com/api/v2"
        assert config.auth_base_url == "https://accounts.zoho.com"
        
        # Test EU
        config.region = "eu"
        assert config.api_base_url == "https://sheet.zoho.eu/api/v2"
        assert config.auth_base_url == "https://accounts.zoho.eu"
        
        # Test IN
        config.region = "in"
        assert config.api_base_url == "https://sheet.zoho.in/api/v2"
        assert config.auth_base_url == "https://accounts.zoho.in"
    
    def test_config_is_authenticated(self, tmp_path):
        """Test is_authenticated property."""
        config = Config(config_path=str(tmp_path / "config.env"))
        
        # Not authenticated initially
        assert not config.is_authenticated
        
        # Set credentials
        config.client_id = "test_client_id"
        config.client_secret = "test_client_secret"
        config.refresh_token = "test_refresh_token"
        
        assert config.is_authenticated
    
    def test_config_save_and_load(self, tmp_path):
        """Test saving and loading configuration."""
        config_path = tmp_path / "config.env"
        
        # Create and save config
        config = Config(config_path=str(config_path))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_token"
        config.region = "eu"
        config.save()
        
        # Load config
        config2 = Config(config_path=str(config_path))
        
        assert config2.client_id == "test_id"
        assert config2.client_secret == "test_secret"
        assert config2.refresh_token == "test_token"
        assert config2.region == "eu"
    
    @patch.dict(os.environ, {
        "ZOHO_CLIENT_ID": "env_client_id",
        "ZOHO_CLIENT_SECRET": "env_client_secret",
        "ZOHO_REFRESH_TOKEN": "env_refresh_token",
        "ZOHO_REGION": "in",
    })
    def test_config_from_environment(self, tmp_path):
        """Test loading config from environment variables."""
        config = Config(config_path=str(tmp_path / "nonexistent.env"))
        
        assert config.client_id == "env_client_id"
        assert config.client_secret == "env_client_secret"
        assert config.refresh_token == "env_refresh_token"
        assert config.region == "in"


class TestGetConfig:
    """Test cases for get_config function."""
    
    def test_get_config_singleton(self, tmp_path):
        """Test get_config returns singleton instance."""
        config_path = str(tmp_path / "config.env")
        
        config1 = get_config(config_path)
        config2 = get_config()
        
        assert config1 is config2
