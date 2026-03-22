"""Zoho Sheet API client."""

import json
from typing import Any, Dict, List, Optional

import requests
from rich.console import Console

from zoho_sheet_cli.config import Config

console = Console()


class ZohoSheetError(Exception):
    """Base exception for Zoho Sheet API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ZohoSheetClient:
    """Client for interacting with Zoho Sheet API v2."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the client.
        
        Args:
            config: Configuration instance
        """
        self.config = config or Config()
        self.session = requests.Session()
        self._refresh_access_token()
    
    def _refresh_access_token(self) -> None:
        """Refresh the access token using refresh token."""
        if not self.config.is_authenticated:
            raise ZohoSheetError(
                "Not authenticated. Please set ZOHO_CLIENT_ID, "
                "ZOHO_CLIENT_SECRET, and ZOHO_REFRESH_TOKEN environment variables "
                "or run 'zsheet auth init'"
            )
        
        url = f"{self.config.auth_base_url}/oauth/v2/token"
        data = {
            "refresh_token": self.config.refresh_token,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "refresh_token",
        }
        
        response = self.session.post(url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data.get("access_token")
        
        # Update session headers
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body data
            files: Files to upload
            
        Returns:
            API response as dictionary
        """
        url = f"{self.config.api_base_url}/{endpoint}"
        
        # Handle different content types
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        
        if files:
            # multipart/form-data for file uploads
            headers.pop("Content-Type", None)
        else:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data if not files else None,
                files=files,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                # Token expired, refresh and retry
                self._refresh_access_token()
                return self._request(method, endpoint, params, data, files)
            
            error_msg = f"API Error: {e}"
            try:
                error_data = response.json()
                error_msg = f"API Error: {error_data.get('message', str(e))}"
            except:
                pass
            raise ZohoSheetError(error_msg, response.status_code)
        except requests.exceptions.RequestException as e:
            raise ZohoSheetError(f"Request failed: {e}")
    
    # ==================== Workbook Operations ====================
    
    def list_workbooks(self) -> List[Dict[str, Any]]:
        """List all workbooks.
        
        Returns:
            List of workbook dictionaries
        """
        response = self._request("GET", "workbooks")
        return response.get("data", {}).get("workbooks", [])
    
    def create_workbook(self, name: str) -> Dict[str, Any]:
        """Create a new workbook.
        
        Args:
            name: Workbook name
            
        Returns:
            Created workbook data
        """
        data = {"workbook_name": name}
        return self._request("POST", "workbooks", data=data)
    
    def get_workbook(self, workbook_id: str) -> Dict[str, Any]:
        """Get workbook details.
        
        Args:
            workbook_id: Workbook ID
            
        Returns:
            Workbook details
        """
        return self._request("GET", f"workbooks/{workbook_id}")
    
    def delete_workbook(self, workbook_id: str) -> Dict[str, Any]:
        """Delete a workbook.
        
        Args:
            workbook_id: Workbook ID
            
        Returns:
            API response
        """
        return self._request("DELETE", f"workbooks/{workbook_id}")
    
    def copy_workbook(self, workbook_id: str, name: str) -> Dict[str, Any]:
        """Copy a workbook.
        
        Args:
            workbook_id: Source workbook ID
            name: New workbook name
            
        Returns:
            Copied workbook data
        """
        data = {"workbook_name": name}
        return self._request("POST", f"workbooks/{workbook_id}/copy", data=data)
    
    def rename_workbook(self, workbook_id: str, name: str) -> Dict[str, Any]:
        """Rename a workbook.
        
        Args:
            workbook_id: Workbook ID
            name: New name
            
        Returns:
            API response
        """
        data = {"workbook_name": name}
        return self._request("PUT", f"workbooks/{workbook_id}", data=data)
    
    # ==================== Worksheet Operations ====================
    
    def list_worksheets(self, workbook_id: str) -> List[Dict[str, Any]]:
        """List all worksheets in a workbook.
        
        Args:
            workbook_id: Workbook ID
            
        Returns:
            List of worksheet dictionaries
        """
        response = self._request("GET", f"workbooks/{workbook_id}/sheets")
        return response.get("data", {}).get("sheets", [])
    
    def add_worksheet(self, workbook_id: str, name: str) -> Dict[str, Any]:
        """Add a new worksheet.
        
        Args:
            workbook_id: Workbook ID
            name: Worksheet name
            
        Returns:
            API response
        """
        data = {"sheet_name": name}
        return self._request("POST", f"workbooks/{workbook_id}/sheets", data=data)
    
    def delete_worksheet(self, workbook_id: str, sheet_name: str) -> Dict[str, Any]:
        """Delete a worksheet.
        
        Args:
            workbook_id: Workbook ID
            sheet_name: Worksheet name
            
        Returns:
            API response
        """
        data = {"sheet_name": sheet_name}
        return self._request("DELETE", f"workbooks/{workbook_id}/sheets", data=data)
    
    def rename_worksheet(
        self, workbook_id: str, old_name: str, new_name: str
    ) -> Dict[str, Any]:
        """Rename a worksheet.
        
        Args:
            workbook_id: Workbook ID
            old_name: Current worksheet name
            new_name: New worksheet name
            
        Returns:
            API response
        """
        data = {
            "sheet_name": old_name,
            "new_sheet_name": new_name,
        }
        return self._request("PUT", f"workbooks/{workbook_id}/sheets", data=data)
    
    # ==================== Cell Operations ====================
    
    def get_cell(
        self, workbook_id: str, sheet_name: str, cell: str
    ) -> Dict[str, Any]:
        """Get cell value.
        
        Args:
            workbook_id: Workbook ID
            sheet_name: Worksheet name
            cell: Cell address (e.g., "A1")
            
        Returns:
            Cell data
        """
        params = {
            "sheet_name": sheet_name,
            "cell": cell,
        }
        return self._request("GET", f"workbooks/{workbook_id}/cells", params=params)
    
    def set_cell(
        self,
        workbook_id: str,
        sheet_name: str,
        cell: str,
        value: str,
    ) -> Dict[str, Any]:
        """Set cell value.
        
        Args:
            workbook_id: Workbook ID
            sheet_name: Worksheet name
            cell: Cell address (e.g., "A1")
            value: Cell value
            
        Returns:
            API response
        """
        data = {
            "sheet_name": sheet_name,
            "cell": cell,
            "data": value,
        }
        return self._request("PUT", f"workbooks/{workbook_id}/cells", data=data)
    
    def get_range(
        self, workbook_id: str, sheet_name: str, range_addr: str
    ) -> Dict[str, Any]:
        """Get range values.
        
        Args:
            workbook_id: Workbook ID
            sheet_name: Worksheet name
            range_addr: Range address (e.g., "A1:D10")
            
        Returns:
            Range data
        """
        params = {
            "sheet_name": sheet_name,
            "range": range_addr,
        }
        return self._request("GET", f"workbooks/{workbook_id}/range", params=params)
    
    def set_range(
        self,
        workbook_id: str,
        sheet_name: str,
        range_addr: str,
        values: List[List[str]],
    ) -> Dict[str, Any]:
        """Set range values.
        
        Args:
            workbook_id: Workbook ID
            sheet_name: Worksheet name
            range_addr: Range address (e.g., "A1:D10")
            values: 2D list of values
            
        Returns:
            API response
        """
        data = {
            "sheet_name": sheet_name,
            "range": range_addr,
            "data": json.dumps(values),
        }
        return self._request("PUT", f"workbooks/{workbook_id}/range", data=data)
    
    # ==================== File Operations ====================
    
    def export_workbook(
        self, workbook_id: str, format_type: str = "xlsx"
    ) -> bytes:
        """Export workbook to file.
        
        Args:
            workbook_id: Workbook ID
            format_type: Export format (xlsx, xls, csv, pdf, ods)
            
        Returns:
            File content as bytes
        """
        url = f"{self.config.api_base_url}/workbooks/{workbook_id}/export"
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        params = {"format": format_type}
        
        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.content
    
    def import_file(
        self,
        file_path: str,
        workbook_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Import a file as a new workbook.
        
        Args:
            file_path: Path to the file to import
            workbook_name: Optional name for the new workbook
            
        Returns:
            Created workbook data
        """
        import os
        
        filename = os.path.basename(file_path)
        name = workbook_name or os.path.splitext(filename)[0]
        
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            data = {"workbook_name": name}
            
            url = f"{self.config.api_base_url}/workbooks/import"
            headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
            
            response = self.session.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            return response.json()
