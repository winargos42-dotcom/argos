#!/usr/bin/env python3
"""
ARGOS Bio-Inspired Neural Network Training
Based on the Telegram article: biologically-inspired neural network with cortical columns

This script trains the BioBrainNetwork on MNIST dataset as described in the article.
Results should reach ~98.73% accuracy on test set after 10 epochs.
"""

import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import logging
import argparse
import os
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("argos.bio_training")

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from argos_bio_network import BioBrainNetwork, BioBrainTrainer


def main():
    parser = argparse.ArgumentParser(description='Train Bio-Inspired Neural Network for ARGOS')
    parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=128, help='Batch size for training')
    parser.add_argument('--columns', type=int, default=64, help='Number of cortical columns')
    parser.add_argument('--col-out', type=int, default=128, help='Output dimension per column')
    parser.add_argument('--learning-rate', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--graph-k', type=int, default=8, help='Small-World graph neighbors')
    parser.add_argument('--graph-p', type=float, default=0.15, help='Small-World rewiring probability')
    parser.add_argument('--message-iters', type=int, default=4, help='Message passing iterations')
    parser.add_argument('--use-attention', action='store_true', default=True, help='Enable attention mechanism')
    parser.add_argument('--save-path', type=str, default='brain_bio.pth', help='Path to save trained model')
    parser.add_argument('--data-dir', type=str, default='./data', help='Directory for MNIST data')
    parser.add_argument('--register-brain', action='store_true', help='Register with ARGOS Brain after training')
    parser.add_argument('--node-id', type=str, default='entity-bio-brain-v2', help='Node ID for ARGOS Brain registration')
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("ARGOS Bio-Inspired Neural Network Training")
    logger.info("="*60)
    
    # Setup hyperparameters
    hyperparams = {
        "num_columns": args.columns,
        "in_dim": 784,  # MNIST 28x28
        "col_out": args.col_out,
        "top_out": 10,  # 10 digits
        "graph_k": args.graph_k,
        "graph_p": args.graph_p,
        "message_iters": args.message_iters,
        "plasticity_lr": 5e-5,
        "use_attention": args.use_attention,
        "e_i_ratio": 0.8,
        "dropout": 0.1
    }
    
    logger.info(f"Hyperparameters: {hyperparams}")
    
    # MNIST setup
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.view(-1))
    ])
    
    logger.info(f"Loading MNIST dataset from {args.data_dir}...")
    train_set = datasets.MNIST(root=args.data_dir, train=True, download=True, transform=transform)
    test_set = datasets.MNIST(root=args.data_dir, train=False, download=True, transform=transform)
    
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False)
    
    logger.info(f"Train samples: {len(train_set)}, Test samples: {len(test_set)}")
    
    # Create model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")
    
    model = BioBrainNetwork(**hyperparams)
    model.to(device)
    
    # Create trainer
    trainer = BioBrainTrainer(model, device)
    trainer.setup_optimizer(learning_rate=args.learning_rate, weight_decay=1e-5)
    
    # Train
    logger.info(f"Starting training for {args.epochs} epochs...")
    logger.info("="*60)
    
    history = trainer.train(train_loader, test_loader, epochs=args.epochs)
    
    # Save model
    if args.save_path:
        trainer.save_model(args.save_path)
        logger.info(f"Model saved to {args.save_path}")
    
    # Register with ARGOS Brain
    if args.register_brain:
        logger.info(f"Registering with ARGOS Brain as {args.node_id}...")
        trainer.register_with_brain(args.node_id)
    
    logger.info("="*60)
    logger.info(f"Training complete!")
    logger.info(f"Best test accuracy: {trainer.best_accuracy*100:.2f}%")
    logger.info(f"Final train loss: {history['train_loss'][-1]:.4f}")
    logger.info(f"Final test accuracy: {history['test_accuracy'][-1]*100:.2f}%")
    logger.info("="*60)


if __name__ == "__main__":
    main()
