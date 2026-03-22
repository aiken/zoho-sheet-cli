"""Tests for API client."""

import json
from unittest.mock import Mock, patch

import pytest
import responses

from zoho_sheet_cli.client import ZohoSheetClient, ZohoSheetError
from zoho_sheet_cli.config import Config


class TestZohoSheetClient:
    """Test cases for ZohoSheetClient."""
    
    @responses.activate
    def test_client_initialization(self, tmp_path):
        """Test client initialization with token refresh."""
        # Mock token refresh endpoint
        responses.add(
            responses.POST,
            "https://accounts.zoho.com/oauth/v2/token",
            json={"access_token": "test_access_token"},
            status=200,
        )
        
        config = Config(config_path=str(tmp_path / "config.env"))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_refresh"
        config.region = "us"
        
        client = ZohoSheetClient(config)
        
        assert client.access_token == "test_access_token"
        assert "Authorization" in client.session.headers
    
    @responses.activate
    def test_list_workbooks(self, tmp_path):
        """Test listing workbooks."""
        # Mock token refresh
        responses.add(
            responses.POST,
            "https://accounts.zoho.com/oauth/v2/token",
            json={"access_token": "test_access_token"},
            status=200,
        )
        
        # Mock API endpoint
        mock_data = {
            "data": {
                "workbooks": [
                    {"resource_id": "wb1", "workbook_name": "Test 1"},
                    {"resource_id": "wb2", "workbook_name": "Test 2"},
                ]
            }
        }
        responses.add(
            responses.GET,
            "https://sheet.zoho.com/api/v2/workbooks",
            json=mock_data,
            status=200,
        )
        
        config = Config(config_path=str(tmp_path / "config.env"))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_refresh"
        
        client = ZohoSheetClient(config)
        workbooks = client.list_workbooks()
        
        assert len(workbooks) == 2
        assert workbooks[0]["workbook_name"] == "Test 1"
    
    @responses.activate
    def test_create_workbook(self, tmp_path):
        """Test creating a workbook."""
        # Mock token refresh
        responses.add(
            responses.POST,
            "https://accounts.zoho.com/oauth/v2/token",
            json={"access_token": "test_access_token"},
            status=200,
        )
        
        # Mock API endpoint
        mock_data = {
            "data": {
                "workbook_id": "new_wb_123",
                "workbook_name": "New Workbook",
            }
        }
        responses.add(
            responses.POST,
            "https://sheet.zoho.com/api/v2/workbooks",
            json=mock_data,
            status=200,
        )
        
        config = Config(config_path=str(tmp_path / "config.env"))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_refresh"
        
        client = ZohoSheetClient(config)
        result = client.create_workbook("New Workbook")
        
        assert result["data"]["workbook_id"] == "new_wb_123"
    
    @responses.activate
    def test_get_cell(self, tmp_path):
        """Test getting cell value."""
        # Mock token refresh
        responses.add(
            responses.POST,
            "https://accounts.zoho.com/oauth/v2/token",
            json={"access_token": "test_access_token"},
            status=200,
        )
        
        # Mock API endpoint
        mock_data = {
            "data": {
                "cell": "A1",
                "value": "Hello",
                "data_type": "string",
            }
        }
        responses.add(
            responses.GET,
            "https://sheet.zoho.com/api/v2/workbooks/wb123/cells",
            json=mock_data,
            status=200,
        )
        
        config = Config(config_path=str(tmp_path / "config.env"))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_refresh"
        
        client = ZohoSheetClient(config)
        result = client.get_cell("wb123", "Sheet1", "A1")
        
        assert result["data"]["value"] == "Hello"
    
    @responses.activate
    def test_set_cell(self, tmp_path):
        """Test setting cell value."""
        # Mock token refresh
        responses.add(
            responses.POST,
            "https://accounts.zoho.com/oauth/v2/token",
            json={"access_token": "test_access_token"},
            status=200,
        )
        
        # Mock API endpoint
        mock_data = {"message": "Success"}
        responses.add(
            responses.PUT,
            "https://sheet.zoho.com/api/v2/workbooks/wb123/cells",
            json=mock_data,
            status=200,
        )
        
        config = Config(config_path=str(tmp_path / "config.env"))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_refresh"
        
        client = ZohoSheetClient(config)
        result = client.set_cell("wb123", "Sheet1", "A1", "Test Value")
        
        assert result["message"] == "Success"
    
    def test_unauthenticated_error(self, tmp_path):
        """Test error when not authenticated."""
        config = Config(config_path=str(tmp_path / "config.env"))
        # Leave credentials empty
        
        with pytest.raises(ZohoSheetError) as exc_info:
            ZohoSheetClient(config)
        
        assert "Not authenticated" in str(exc_info.value)
    
    @responses.activate
    def test_api_error(self, tmp_path):
        """Test handling API errors."""
        # Mock token refresh
        responses.add(
            responses.POST,
            "https://accounts.zoho.com/oauth/v2/token",
            json={"access_token": "test_access_token"},
            status=200,
        )
        
        # Mock API error
        responses.add(
            responses.GET,
            "https://sheet.zoho.com/api/v2/workbooks",
            json={"message": "Invalid workbook ID"},
            status=400,
        )
        
        config = Config(config_path=str(tmp_path / "config.env"))
        config.client_id = "test_id"
        config.client_secret = "test_secret"
        config.refresh_token = "test_refresh"
        
        client = ZohoSheetClient(config)
        
        with pytest.raises(ZohoSheetError):
            client.list_workbooks()
