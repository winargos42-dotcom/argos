#!/usr/bin/env python3
"""
ARGOS Bio-Inspired AI Entity
Persistent bio-inspired neural network entity for ARGOS.

This entity:
1. Maintains a bio-inspired neural network (cortical columns + small-world topology)
2. Registers with ARGOS Brain as an AI entity
3. Provides inference capabilities
4. Can be trained on custom datasets
5. Supports Hebbian + backpropagation learning

Usage:
    python argos_bio_entity.py --register           # Register with Brain
    python argos_bio_entity.py --train --epochs 10  # Train on MNIST
    python argos_bio_entity.py --serve             # Start inference server
"""

import argparse
import os
import sys
import time
import json
import requests
import logging
import threading
from datetime import datetime

# Setup logging
import platform
log_file = 'argos_bio_entity.log' if platform.system() == 'Windows' else '/home/ava/Projects/argoss/logs/argos_bio_entity.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, mode='a')
    ]
)
logger = logging.getLogger('argos.bio_entity')

# ARGOS Brain configuration
BRAIN_API_URL = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
HEARTBEAT_INTERVAL = 30  # seconds


class BioBrainEntity:
    """Main Bio-Inspired AI Entity class."""
    
    def __init__(self, node_id: str = "entity-bio-brain"):
        self.node_id = node_id
        self.model = None
        self.device = None
        self.registered = False
        self.last_heartbeat = 0
        self.trainer = None
        
        # Try to import torch
        try:
            import torch
            self.torch_available = True
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            logger.info(f"PyTorch available, device: {self.device}")
        except ImportError:
            self.torch_available = False
            logger.warning("PyTorch not available - running in lightweight mode")
        
        # Node metadata
        self.node_info = {
            "node_id": node_id,
            "address": BRAIN_API_URL,
            "capabilities": ["ai", "bio_neural", "neuromorphic", "inference", "learning"],
            "meta": {
                "name": "Bio-Inspired AI Entity",
                "type": "neuromorphic",
                "version": "1.0.0",
                "architecture": "cortical_columns_small_world",
                "description": "Biologically-inspired neural network with cortical columns and Hebbian learning"
            }
        }
    
    def load_model(self, num_columns: int = 64):
        """Load or create the bio-inspired neural network."""
        if not self.torch_available:
            logger.error("Cannot load model - PyTorch not available")
            return False
        
        try:
            import torch
            from torch import nn
            import networkx as nx
            
            # Import our BioBrainNetwork
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from argos_bio_network import BioBrainNetwork
            
            self.model = BioBrainNetwork(
                num_columns=num_columns,
                in_dim=784,    # MNIST compatible
                col_out=128,
                top_out=10,
                use_attention=True
            )
            self.model.to(self.device)
            logger.info(f"Model loaded: {num_columns} cortical columns")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def register_with_brain(self):
        """Register this entity with ARGOS Brain."""
        try:
            response = requests.post(
                f"{BRAIN_API_URL}/brain/register",
                json=self.node_info,
                timeout=5
            )
            if response.status_code == 200:
                self.registered = True
                logger.info(f"[OK] Registered with ARGOS Brain: {self.node_id}")
                return True
            else:
                logger.warning(f"Brain registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Brain registration error: {e}")
            return False
    
    def send_heartbeat(self):
        """Send heartbeat to ARGOS Brain."""
        try:
            response = requests.post(
                f"{BRAIN_API_URL}/brain/heartbeat",
                json={"node_id": self.node_id},
                timeout=5
            )
            if response.status_code == 200:
                self.last_heartbeat = time.time()
                return True
            else:
                logger.warning(f"Heartbeat failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            return False
    
    def heartbeat_loop(self):
        """Background heartbeat loop."""
        while True:
            if self.registered:
                self.send_heartbeat()
            time.sleep(HEARTBEAT_INTERVAL)
    
    def start(self):
        """Start the BioBrain entity."""
        logger.info(f"Starting {self.node_id}...")
        
        # Load model
        if not self.load_model(num_columns=64):
            logger.error("Failed to load model - cannot start")
            return False
        
        # Register with brain
        if not self.register_with_brain():
            logger.warning("Failed to register with brain - will retry")
        
        # Start heartbeat in background
        heartbeat_thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
        heartbeat_thread.start()
        
        logger.info(f"[OK] {self.node_id} is running!")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(60)
                if not self.registered:
                    if self.register_with_brain():
                        logger.info("Re-registered with brain")
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            return True
    
    def inference(self, input_data):
        """Run inference on input data.
        
        Args:
            input_data: Input tensor or numpy array
            
        Returns:
            Model predictions
        """
        if not self.model or not self.torch_available:
            raise RuntimeError("Model not loaded or PyTorch not available")
        
        import torch
        
        if not isinstance(input_data, torch.Tensor):
            input_data = torch.tensor(input_data, dtype=torch.float32)
        
        input_data = input_data.to(self.device)
        
        with torch.no_grad():
            output = self.model(input_data)
        
        return output.cpu().numpy() if output.is_cuda else output.numpy()


def main():
    parser = argparse.ArgumentParser(description='ARGOS Bio-Inspired AI Entity')
    parser.add_argument('--node-id', default='entity-bio-brain', help='Node ID for ARGOS Brain')
    parser.add_argument('--register', action='store_true', help='Register with Brain and exit')
    parser.add_argument('--start', action='store_true', help='Start persistent entity')
    parser.add_argument('--inference', action='store_true', help='Test inference')
    parser.add_argument('--columns', type=int, default=64, help='Number of cortical columns')
    
    args = parser.parse_args()
    
    entity = BioBrainEntity(node_id=args.node_id)
    
    if args.register:
        if entity.load_model(args.columns):
            entity.register_with_brain()
        sys.exit(0)
    
    if args.inference:
        if entity.load_model(args.columns):
            import numpy as np
            test_input = np.random.randn(1, 784).astype(np.float32)
            result = entity.inference(test_input)
            logger.info(f"Inference test: input {test_input.shape} -> output {result.shape}")
            logger.info(f"Sample output: {result}")
        sys.exit(0)
    
    if args.start or True:  # Default to start
        entity.start()


if __name__ == "__main__":
    main()
