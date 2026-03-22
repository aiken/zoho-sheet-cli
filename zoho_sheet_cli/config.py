"""Configuration management for Zoho Sheet CLI."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


# Default config paths
CONFIG_DIR = Path.home() / ".config" / "zsheet"
CONFIG_FILE = CONFIG_DIR / "config.env"


class Config:
    """Configuration manager for Zoho Sheet CLI."""
    
    # Zoho API endpoints by region
    API_ENDPOINTS = {
        "us": "https://sheet.zoho.com/api/v2",
        "eu": "https://sheet.zoho.eu/api/v2",
        "in": "https://sheet.zoho.in/api/v2",
        "cn": "https://sheet.zohoapis.com.cn/api/v2",
        "au": "https://sheet.zoho.com.au/api/v2",
        "jp": "https://sheet.zoho.jp/api/v2",
    }
    
    AUTH_ENDPOINTS = {
        "us": "https://accounts.zoho.com",
        "eu": "https://accounts.zoho.eu",
        "in": "https://accounts.zoho.in",
        "cn": "https://accounts.zoho.com.cn",
        "au": "https://accounts.zoho.com.au",
        "jp": "https://accounts.zoho.jp",
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Optional custom config file path
        """
        self.config_path = Path(config_path) if config_path else CONFIG_FILE
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from environment and config file."""
        # Load from config file if exists
        if self.config_path.exists():
            load_dotenv(self.config_path)
        
        # Load from environment
        self.client_id = os.getenv("ZOHO_CLIENT_ID", "")
        self.client_secret = os.getenv("ZOHO_CLIENT_SECRET", "")
        self.refresh_token = os.getenv("ZOHO_REFRESH_TOKEN", "")
        self.access_token = os.getenv("ZOHO_ACCESS_TOKEN", "")
        self.region = os.getenv("ZOHO_REGION", "us").lower()
    
    @property
    def api_base_url(self) -> str:
        """Get API base URL for the configured region."""
        return self.API_ENDPOINTS.get(self.region, self.API_ENDPOINTS["us"])
    
    @property
    def auth_base_url(self) -> str:
        """Get Auth base URL for the configured region."""
        return self.AUTH_ENDPOINTS.get(self.region, self.AUTH_ENDPOINTS["us"])
    
    @property
    def is_authenticated(self) -> bool:
        """Check if all required credentials are present."""
        return all([
            self.client_id,
            self.client_secret,
            self.refresh_token,
        ])
    
    def save(self) -> None:
        """Save current configuration to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        config_content = f"""# Zoho Sheet CLI Configuration
ZOHO_CLIENT_ID={self.client_id}
ZOHO_CLIENT_SECRET={self.client_secret}
ZOHO_REFRESH_TOKEN={self.refresh_token}
ZOHO_ACCESS_TOKEN={self.access_token}
ZOHO_REGION={self.region}
"""
        self.config_path.write_text(config_content)
    
    def update(self, **kwargs) -> None:
        """Update configuration values.
        
        Args:
            **kwargs: Configuration key-value pairs to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


# Global config instance
_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance.
    
    Args:
        config_path: Optional custom config file path
        
    Returns:
        Config instance
    """
    global _config
    if _config is None or config_path:
        _config = Config(config_path)
    return _config
