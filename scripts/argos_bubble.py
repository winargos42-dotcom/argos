#!/usr/bin/env python3
"""
ARGOS Bubble.io Integration Module

Bubble.io is a no-code platform for building web applications.
This module integrates Bubble.io projects with ARGOS for:
- Webhook notifications
- API access to Bubble.io data
- Project monitoring
- Automated workflows

URL: https://bubble.io/home/projects

Features:
- List Bubble.io projects
- Trigger Bubble.io workflows via API
- Receive webhooks from Bubble.io
- Monitor project status
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
from http.server import HTTPServer, BaseHTTPRequestHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('argos.bubble')


class BubbleConfig:
    """Configuration for Bubble.io API."""
    
    def __init__(self):
        self.base_url = "https://api.bubble.io/api/1.1/"
        self.bubble_url = "https://bubble.io/home/projects"
        self.api_key = os.getenv("BUBBLE_API_KEY")
        self.timeout = 30
        self.retry_count = 3


class BubbleClient:
    """Client for Bubble.io API."""
    
    def __init__(self, config: Optional[BubbleConfig] = None):
        self.config = config or BubbleConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ARGOS-Bubble-Client/1.0",
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
                elif response.status_code == 401:
                    logger.error(f"Bubble authentication failed: {endpoint}")
                    return None
                elif response.status_code == 404:
                    logger.warning(f"Bubble endpoint not found: {endpoint}")
                    return None
                elif response.status_code >= 500:
                    logger.warning(f"Bubble server error ({response.status_code}): {endpoint}")
                    time.sleep(2 ** attempt)
                    continue
                else:
                    logger.warning(f"Bubble API error ({response.status_code}): {endpoint}")
                    return None
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Bubble request timeout (attempt {attempt + 1}): {endpoint}")
                time.sleep(2 ** attempt)
                continue
            except requests.exceptions.RequestException as e:
                logger.error(f"Bubble request failed: {endpoint} - {e}")
                return None
        
        return None
    
    def list_applications(self) -> Optional[List[Dict]]:
        """List all Bubble.io applications/projects."""
        result = self._request("GET", "app")
        if result:
            return result.get("response", result)
        return None
    
    def get_application(self, app_id: str) -> Optional[Dict]:
        """Get details of a specific application."""
        result = self._request("GET", f"app/{app_id}")
        return result
    
    def list_workflows(self, app_id: str) -> Optional[List[Dict]]:
        """List workflows in an application."""
        result = self._request("GET", f"app/{app_id}/workflows")
        if result:
            return result.get("response", result)
        return None
    
    def run_workflow(self, app_id: str, workflow_name: str, data: Dict = None) -> Optional[Dict]:
        """Run a Bubble.io workflow via API."""
        payload = {
            "name": workflow_name,
            "data": data or {}
        }
        result = self._request("POST", f"app/{app_id}/run_workflow", json=payload)
        return result
    
    def list_data_types(self, app_id: str) -> Optional[List[Dict]]:
        """List data types in an application."""
        result = self._request("GET", f"app/{app_id}/data_types")
        if result:
            return result.get("response", result)
        return None
    
    def list_things(self, app_id: str, type_name: str, limit: int = 100) -> Optional[List[Dict]]:
        """List things of a specific data type."""
        result = self._request("GET", f"app/{app_id}/data/{type_name}?limit={limit}")
        if result:
            return result.get("response", result)
        return None
    
    def create_thing(self, app_id: str, type_name: str, data: Dict) -> Optional[Dict]:
        """Create a new thing in Bubble.io."""
        result = self._request("POST", f"app/{app_id}/data/{type_name}", json=data)
        return result
    
    def update_thing(self, app_id: str, type_name: str, thing_id: str, data: Dict) -> Optional[Dict]:
        """Update a thing in Bubble.io."""
        result = self._request("PUT", f"app/{app_id}/data/{type_name}/{thing_id}", json=data)
        return result
    
    def delete_thing(self, app_id: str, type_name: str, thing_id: str) -> bool:
        """Delete a thing from Bubble.io."""
        result = self._request("DELETE", f"app/{app_id}/data/{type_name}/{thing_id}")
        return result is not None
    
    def get_webhook_url(self, app_id: str, workflow_name: str) -> str:
        """Generate webhook URL for a workflow."""
        return f"https://{app_id}.bubbleapps.io/version-test/api/1.1/w/{workflow_name}"


class BubbleWebhookHandler(BaseHTTPRequestHandler):
    """HTTP handler for receiving Bubble.io webhooks."""
    
    def do_POST(self):
        """Handle POST webhook from Bubble.io."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            logger.info(f"Received Bubble webhook: {json.dumps(data, indent=2)}")
            
            # Process webhook
            self._process_webhook(data)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "received"}).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
    
    def _process_webhook(self, data: Dict):
        """Process incoming webhook data."""
        # Extract useful information
        app_id = data.get("app_id")
        workflow_name = data.get("workflow_name")
        event_data = data.get("data", {})
        
        logger.info(f"Webhook from app: {app_id}, workflow: {workflow_name}")
        logger.info(f"Event data: {json.dumps(event_data, indent=2)}")
        
        # Here you can add custom logic to handle specific webhooks
        # For example, notify ARGOS Brain about the event
        if workflow_name == "new_user_signup":
            self._handle_new_user(event_data)
        elif workflow_name == "data_updated":
            self._handle_data_update(event_data)
    
    def _handle_new_user(self, data: Dict):
        """Handle new user signup event."""
        logger.info(f"New user signup: {data.get('email')}")
        # Notify ARGOS Brain
        self._notify_argos_brain("bubble_new_user", data)
    
    def _handle_data_update(self, data: Dict):
        """Handle data update event."""
        logger.info(f"Data updated: {data.get('type')}")
        # Notify ARGOS Brain
        self._notify_argos_brain("bubble_data_update", data)
    
    def _notify_argos_brain(self, event_type: str, data: Dict):
        """Send notification to ARGOS Brain about Bubble event."""
        brain_url = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
        try:
            requests.post(
                f"{brain_url}/brain/event",
                json={
                    "source": "bubble.io",
                    "type": event_type,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=5
            )
        except Exception as e:
            logger.error(f"Failed to notify ARGOS Brain: {e}")
    
    def log_message(self, format, *args):
        """Override to prevent default logging."""
        logger.debug(format % args)


class BubbleARGOSIntegration:
    """Integration of Bubble.io with ARGOS Brain."""
    
    def __init__(self, bubble_client: BubbleClient):
        self.client = bubble_client
        self.brain_api_url = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
        self.node_id = "entity-bubble-io"
    
    def register_with_brain(self) -> bool:
        """Register Bubble.io integration as ARGOS node."""
        node_data = {
            "node_id": self.node_id,
            "address": self.brain_api_url,
            "capabilities": ["webhooks", "api", "bubble", "web"],
            "meta": {
                "name": "Bubble.io Integration",
                "type": "web",
                "platform": "Bubble.io",
                "description": "Bubble.io no-code web application platform integration"
            }
        }
        
        try:
            response = requests.post(
                f"{self.brain_api_url}/brain/register",
                json=node_data,
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Registered Bubble.io node: {self.node_id}")
                return True
            else:
                logger.warning(f"Failed to register Bubble.io node: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error registering Bubble.io node: {e}")
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
    
    def start_webhook_server(self, port: int = 8080):
        """Start webhook server to receive Bubble.io events."""
        server_address = ('', port)
        httpd = HTTPServer(server_address, BubbleWebhookHandler)
        logger.info(f"Starting Bubble webhook server on port {port}")
        httpd.serve_forever()
    
    def monitor_applications(self, interval: int = 300) -> None:
        """Monitor Bubble.io applications periodically."""
        logger.info(f"Starting Bubble application monitor (interval: {interval}s)")
        
        while True:
            try:
                apps = self.client.list_applications()
                if apps:
                    logger.info(f"Found {len(apps)} Bubble.io applications")
                    for app in apps:
                        logger.info(f"  - {app.get('name', app.get('id', 'Unknown'))}")
                else:
                    logger.warning("No applications found - check API authentication")
            except Exception as e:
                logger.error(f"Error monitoring applications: {e}")
            
            time.sleep(interval)


def main():
    """Main function for testing Bubble.io integration."""
    logger.info("Testing Bubble.io integration...")
    
    # Initialize client
    config = BubbleConfig()
    client = BubbleClient(config)
    
    # Test applications
    logger.info("Fetching Bubble.io applications...")
    apps = client.list_applications()
    
    if apps:
        logger.info(f"Found {len(apps)} applications:")
        for app in apps:
            logger.info(f"  - {app.get('name', app.get('id', 'Unknown'))}")
    else:
        logger.warning("Could not list applications - API may require authentication")
    
    # Test ARGOS integration
    integration = BubbleARGOSIntegration(client)
    if integration.register_with_brain():
        logger.info("Bubble.io registered with ARGOS Brain")
    
    logger.info("Bubble.io integration test complete")


if __name__ == "__main__":
    main()
