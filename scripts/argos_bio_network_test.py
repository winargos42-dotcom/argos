#!/usr/bin/env python3
"""
ARGOS Bio-Inspired Network - Quick Test
Fast test without downloading MNIST - uses random data for validation.
"""

import torch
from torch import nn
import torch.nn.functional as F
import networkx as nx
import math
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("argos.bio_test")

# Import the full network
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from argos_bio_network import BioBrainNetwork, BioBrainTrainer


def test_network():
    """Quick test with random data."""
    logger.info("Testing BioBrainNetwork with random data...")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")
    
    # Create small network for quick test
    model = BioBrainNetwork(
        num_columns=8,  # Small number for quick test
        in_dim=100,    # Small input dimension
        col_out=32,    # Small output per column
        top_out=5,     # 5 classes
        graph_k=4,
        message_iters=2,
        use_attention=True
    )
    
    logger.info(f"Model created: {model.num_columns} columns")
    
    # Test forward pass
    x = torch.randn(4, 100)  # batch of 4, 100 features
    y = torch.randint(0, 5, (4,))  # 4 random labels
    
    model.to(device)
    x, y = x.to(device), y.to(device)
    
    # Forward pass
    logits = model(x)
    logger.info(f"Forward pass OK: input {x.shape} -> output {logits.shape}")
    
    # Test training step
    loss = model.training_step((x, y))
    logger.info(f"Training step OK: loss = {loss.item():.4f}")
    
    # Test multiple steps
    for i in range(5):
        x = torch.randn(8, 100).to(device)
        y = torch.randint(0, 5, (8,)).to(device)
        loss = model.training_step((x, y))
        if i % 1 == 0:
            logger.info(f"Step {i+1}: loss = {loss.item():.4f}")
    
    logger.info("✅ BioBrainNetwork basic tests PASSED!")
    
    # Register with ARGOS Brain
    trainer = BioBrainTrainer(model, device)
    trainer.register_with_brain("entity-bio-brain-test-v1")
    
    logger.info("✅ Registered with ARGOS Brain!")
    
    return True


if __name__ == "__main__":
    test_network()
