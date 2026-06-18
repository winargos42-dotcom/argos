#!/usr/bin/env python3
"""
ARGOS Cubbit Workspace Integration Module

Cubbit provides cloud storage with versioning, encryption, and collaboration features.
This module integrates Cubbit workspace as cloud storage for ARGOS.

Workspace ID: be544a2c-4f35-466e-a4be-b05b53ab7bda
Console: https://console.trial.cubbit.eu/workspace/projects/

Features:
- Upload/download files to Cubbit buckets
- List workspace projects and buckets
- Versioning support
- Metadata management
- Integration with ARGOS Brain
"""

import os
import sys
import json
import time
import requests
import logging
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('argos.cubbit')


class CubbitConfig:
    """Configuration for Cubbit API."""
    
    def __init__(self):
        self.workspace_id = "be544a2c-4f35-466e-a4be-b05b53ab7bda"
        self.base_url = "https://api.cubbit.eu/api/v2/"
        self.console_url = "https://console.trial.cubbit.eu/workspace/projects/"
        self.api_key = os.getenv("CUBBIT_API_KEY")
        self.timeout = 30
        self.retry_count = 3
        
        # Local cache
        self.cache_dir = Path.home() / ".argos_cubbit_cache"
        self.cache_dir.mkdir(exist_ok=True)


class CubbitClient:
    """Client for Cubbit API."""
    
    def __init__(self, config: Optional[CubbitConfig] = None):
        self.config = config or CubbitConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ARGOS-Cubbit-Client/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        if self.config.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.config.api_key}"
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Make API request with retries."""
        url = f"{self.config.base_url}{endpoint}"
        
        for attempt in range(self.config.retry_count):
            try:
                response = self.session.request(
                    method, url, timeout=self.config.timeout, **kwargs
                )
                
                if response.status_code == 200:
                    return response.json() if response.content else {}
                elif response.status_code == 404:
                    logger.warning(f"Cubbit API endpoint not found: {endpoint}")
                    return None
                elif response.status_code == 401:
                    logger.error(f"Cubbit authentication failed: {endpoint}")
                    return None
                elif response.status_code >= 500:
                    logger.warning(f"Cubbit server error ({response.status_code}): {endpoint}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.warning(f"Cubbit API error ({response.status_code}): {endpoint}")
                    return None
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Cubbit request timeout (attempt {attempt + 1}): {endpoint}")
                time.sleep(2 ** attempt)
                continue
            except requests.exceptions.RequestException as e:
                logger.error(f"Cubbit request failed: {endpoint} - {e}")
                return None
        
        return None
    
    def get_workspace_info(self) -> Optional[Dict]:
        """Get workspace information."""
        return self._request("GET", f"workspaces/{self.config.workspace_id}")
    
    def list_projects(self) -> Optional[List[Dict]]:
        """List all projects in workspace."""
        result = self._request("GET", f"workspaces/{self.config.workspace_id}/projects")
        if result:
            return result.get("projects", result.get("items", []))
        return None
    
    def list_buckets(self, project_id: str) -> Optional[List[Dict]]:
        """List all buckets in a project."""
        result = self._request("GET", f"projects/{project_id}/buckets")
        if result:
            return result.get("buckets", result.get("items", []))
        return None
    
    def list_files(self, bucket_id: str, path: str = "") -> Optional[List[Dict]]:
        """List files in a bucket."""
        endpoint = f"buckets/{bucket_id}/files"
        if path:
            endpoint += f"?path={path}"
        result = self._request("GET", endpoint)
        if result:
            return result.get("files", result.get("items", []))
        return None
    
    def upload_file(self, bucket_id: str, local_path: str, remote_path: str = None) -> Optional[Dict]:
        """Upload file to Cubbit bucket."""
        local_path = Path(local_path)
        if not local_path.exists():
            logger.error(f"Local file not found: {local_path}")
            return None
        
        remote_path = remote_path or local_path.name
        
        # Check if file already exists and has same hash
        existing = self.get_file_info(bucket_id, remote_path)
        if existing:
            local_hash = self._calculate_hash(local_path)
            if local_hash == existing.get("hash", ""):
                logger.info(f"File already exists with same hash: {remote_path}")
                return existing
        
        # For now, use simple file read - will need multipart upload for large files
        with open(local_path, 'rb') as f:
            file_content = f.read()
        
        files = {
            'file': (remote_path, file_content)
        }
        
        result = self._request(
            "POST", 
            f"buckets/{bucket_id}/upload",
            files=files
        )
        return result
    
    def download_file(self, bucket_id: str, remote_path: str, local_path: str) -> bool:
        """Download file from Cubbit bucket."""
        result = self._request("GET", f"buckets/{bucket_id}/download?path={remote_path}")
        if result and "url" in result:
            # Follow the download URL
            download_url = result["url"]
            response = self.session.get(download_url, timeout=self.config.timeout)
            if response.status_code == 200:
                Path(local_path).write_bytes(response.content)
                return True
        return False
    
    def get_file_info(self, bucket_id: str, remote_path: str) -> Optional[Dict]:
        """Get file metadata."""
        result = self._request("GET", f"buckets/{bucket_id}/files/{remote_path}")
        return result
    
    def delete_file(self, bucket_id: str, remote_path: str) -> bool:
        """Delete file from bucket."""
        result = self._request("DELETE", f"buckets/{bucket_id}/files/{remote_path}")
        return result is not None
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def create_backup(self, source_dir: str, bucket_id: str, prefix: str = "backup") -> Dict[str, Any]:
        """Create backup of directory to Cubbit bucket."""
        source_dir = Path(source_dir)
        results = {"success": [], "failed": []}
        
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                relative = file_path.relative_to(source_dir)
                remote_path = f"{prefix}/{relative.as_posix()}"
                
                result = self.upload_file(str(file_path), bucket_id, remote_path)
                if result:
                    results["success"].append(str(relative))
                else:
                    results["failed"].append(str(relative))
        
        return results


class CubbitARGOSIntegration:
    """Integration of Cubbit with ARGOS Brain."""
    
    def __init__(self, cubbit_client: CubbitClient):
        self.client = cubbit_client
        self.brain_api_url = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
        self.node_id = "entity-cubbit-storage"
    
    def register_with_brain(self) -> bool:
        """Register Cubbit integration as ARGOS node."""
        node_data = {
            "node_id": self.node_id,
            "address": self.brain_api_url,
            "capabilities": ["storage", "cloud", "backup", "cubbit"],
            "meta": {
                "name": "Cubbit Cloud Storage",
                "type": "storage",
                "workspace_id": self.client.config.workspace_id,
                "console": self.client.config.console_url,
                "description": "Cubbit workspace cloud storage integration"
            }
        }
        
        try:
            response = requests.post(
                f"{self.brain_api_url}/brain/register",
                json=node_data,
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Registered Cubbit node: {self.node_id}")
                return True
            else:
                logger.warning(f"Failed to register Cubbit node: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error registering Cubbit node: {e}")
            return False
    
    def send_heartbeat(self) -> bool:
        """Send heartbeat to ARGOS Brain."""
        try:
            response = requests.post(
                f"{self.brain_api_url}/brain/heartbeat",
                json={"node_id": self.node_id},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            return False
    
    def backup_argos_vault(self, vault_path: str = "/home/ava/Projects/argoss/vault") -> Dict[str, Any]:
        """Backup ARGOS Obsidian vault to Cubbit."""
        # For now, just get workspace info and projects
        workspace = self.client.get_workspace_info()
        projects = self.client.list_projects()
        
        result = {
            "workspace": workspace,
            "projects": projects,
            "status": "partial",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Cubbit workspace info retrieved: {workspace is not None}")
        logger.info(f"Cubbit projects found: {len(projects) if projects else 0}")
        
        return result
    
    def sync_configs(self, configs_dir: str = "/home/ava/Projects/argoss/configs") -> Dict[str, Any]:
        """Sync ARGOS configs with Cubbit storage."""
        configs_dir = Path(configs_dir)
        if not configs_dir.exists():
            return {"error": "Configs directory not found"}
        
        # This will be implemented when API is accessible
        return {
            "status": "pending",
            "files": list(configs_dir.rglob("*")),
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main function for testing Cubbit integration."""
    logger.info("Testing Cubbit integration...")
    
    # Initialize client
    config = CubbitConfig()
    client = CubbitClient(config)
    
    # Test workspace info
    logger.info(f"Testing workspace: {config.workspace_id}")
    workspace = client.get_workspace_info()
    
    if workspace:
        logger.info(f"Workspace info: {json.dumps(workspace, indent=2)}")
    else:
        logger.warning("Could not retrieve workspace info - API may require authentication")
    
    # Test projects
    projects = client.list_projects()
    if projects:
        logger.info(f"Found {len(projects)} projects:")
        for p in projects:
            logger.info(f"  - {p.get('name', p.get('id', 'Unknown'))}")
    else:
        logger.warning("Could not list projects - API may require authentication or workspace ID")
    
    # Test ARGOS integration
    integration = CubbitARGOSIntegration(client)
    if integration.register_with_brain():
        logger.info("Cubbit registered with ARGOS Brain")
    
    # Backup test
    logger.info("Testing backup functionality...")
    backup_result = integration.backup_argos_vault()
    logger.info(f"Backup result: {json.dumps(backup_result, indent=2)}")
    
    logger.info("Cubbit integration test complete")


if __name__ == "__main__":
    main()
