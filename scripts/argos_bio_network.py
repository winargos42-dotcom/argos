#!/usr/bin/env python3
"""
ARGOS Bio-Inspired Neural Network Module
Biologically-inspired neural network based on cortical columns architecture.

Architecture inspired by:
- Cortical columns (80% excitatory, 20% inhibitory neurons)
- Small-World network topology (Watts-Strogatz)
- Hebbian learning for graph connections
- Backpropagation for column weights
- Homeostatic scaling for stability

References:
[1] Hubel & Wiesel - Cortical columns in visual cortex
[2] Watts & Strogatz - Collective dynamics of small-world networks
[3] Hebb - The Organization of Behavior (1949)
[4] Mountcastle - Modular organization of cortical columns
"""

import torch
from torch import nn
import torch.nn.functional as F
import networkx as nx
import math
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("argos.bio_network")


class Column(nn.Module):
    """Cortical Column - Basic processing unit inspired by biological neural columns.
    
    Contains ~80-120 neurons organized vertically through cortex layers.
    Implements Excitation-Inhibition (E-I) balance fundamental for neural processing.
    
    Args:
        in_feat: Input feature dimension
        out_feat: Output feature dimension  
        e_i_ratio: Ratio of excitatory to inhibitory neurons (default: 0.8)
        dropout: Dropout rate for regularization (default: 0.1)
    """
    
    def __init__(self, in_feat: int, out_feat: int, e_i_ratio: float = 0.8, dropout: float = 0.1):
        super().__init__()
        self.fc_exc = nn.Linear(in_feat, out_feat, bias=False)
        self.fc_inh = nn.Linear(in_feat, out_feat, bias=False)
        self.norm = nn.LayerNorm(out_feat)
        self.dropout = nn.Dropout(dropout)
        self.e_i_ratio = e_i_ratio
        
        # Kaiming Normal for excitatory (ReLU), Xavier Uniform for inhibitory (Sigmoid)
        nn.init.kaiming_normal_(self.fc_exc.weight, nonlinearity='relu')
        nn.init.xavier_uniform_(self.fc_inh.weight)
        
        self.use_projection = (in_feat != out_feat)
        if self.use_projection:
            self.projection = nn.Linear(in_feat, out_feat, bias=False)
    
    def forward(self, x):
        """Forward pass through cortical column.
        
        Excitatory path: ReLU activation
        Inhibitory path: Sigmoid activation
        Combined with E-I balance ratio
        """
        exc = F.relu(self.fc_exc(x))
        inh = torch.sigmoid(self.fc_inh(x))
        out = exc * (1.0 - self.e_i_ratio * inh)
        
        if self.use_projection:
            out = out + self.projection(x)
        
        out = self.norm(out)
        out = self.dropout(out)
        return out


class AttentionGate(nn.Module):
    """Attention mechanism for column communication.
    
    Each column decides which neighbors are most relevant and amplifies their signals.
    """
    
    def __init__(self, dim: int):
        super().__init__()
        self.query = nn.Linear(dim, dim, bias=False)
        self.key = nn.Linear(dim, dim, bias=False)
        self.scale = math.sqrt(dim)
    
    def forward(self, center: torch.Tensor, neighbors: torch.Tensor, adj_mask: torch.Tensor):
        """Compute attention weights for neighboring columns.
        
        Args:
            center: Central column representation (batch, dim)
            neighbors: All neighbor representations (batch, num_neighbors, dim)
            adj_mask: Adjacency mask for valid connections
            
        Returns:
            Attention weights for each neighbor
        """
        q = self.query(center).unsqueeze(1)
        k = self.key(neighbors)
        scores = torch.bmm(q, k.transpose(1, 2)) / self.scale
        scores = scores.squeeze(1)
        scores = scores.masked_fill(adj_mask.unsqueeze(0) == 0, -1e9)
        weights = F.softmax(scores, dim=-1)
        return weights


def make_small_world(num_nodes: int, k: int = 4, p: float = 0.1) -> torch.Tensor:
    """Create Small-World graph adjacency matrix.
    
    Watts-Strogatz model: Regular ring with random rewiring.
    Provides high efficiency with low energy consumption (like biological brain).
    
    Args:
        num_nodes: Number of columns/nodes
        k: Number of nearest neighbors to connect
        p: Probability of rewiring each connection
        
    Returns:
        Adjacency matrix (num_nodes, num_nodes)
    """
    G = nx.watts_strogatz_graph(num_nodes, k, p)
    adj = torch.zeros(num_nodes, num_nodes, dtype=torch.float32)
    for i, j in G.edges():
        adj[i, j] = 1.0
        adj[j, i] = 1.0
    return adj


class BioBrainNetwork(nn.Module):
    """Bio-Inspired Neural Network - Main ARGOS Brain Network.
    
    Combines:
    - Cortical columns for feature processing
    - Small-World topology for efficient communication
    - Hebbian learning for graph structure adaptation
    - Backpropagation for supervised learning
    - Homeostatic scaling for stability
    
    This implements a dual learning approach:
    1. Supervised (Backprop): Optimizes column weights and classifier
    2. Unsupervised (Hebbian): Adapts graph connection structure
    
    Args:
        num_columns: Number of cortical columns (default: 64)
        in_dim: Input dimension (784 for MNIST 28x28)
        col_out: Output dimension per column (default: 128)
        top_out: Final output dimension (10 for MNIST digits)
        graph_k: Small-World graph neighbors (default: 8)
        graph_p: Small-World rewiring probability (default: 0.15)
        message_iters: Message passing iterations (default: 4)
        plasticity_lr: Hebbian learning rate (default: 5e-5)
        use_attention: Enable attention mechanism (default: True)
        e_i_ratio: E-I balance ratio (default: 0.8)
        dropout: Dropout rate (default: 0.1)
    """
    
    def __init__(self,
                 num_columns: int = 64,
                 in_dim: int = 784,
                 col_out: int = 128,
                 top_out: int = 10,
                 graph_k: int = 8,
                 graph_p: float = 0.15,
                 message_iters: int = 4,
                 plasticity_lr: float = 5e-5,
                 use_attention: bool = True,
                 e_i_ratio: float = 0.8,
                 dropout: float = 0.1):
        super().__init__()
        
        self.num_columns = num_columns
        self.message_iters = message_iters
        self.plasticity_lr = plasticity_lr
        self.use_attention = use_attention
        
        # Create cortical columns
        self.columns = nn.ModuleList([
            Column(in_dim, col_out, e_i_ratio=e_i_ratio, dropout=dropout) 
            for _ in range(num_columns)
        ])
        
        # Attention gates for each column
        if use_attention:
            self.attention_gates = nn.ModuleList([
                AttentionGate(col_out) for _ in range(num_columns)
            ])
        
        # Small-World graph structure (fixed)
        adj_struct = make_small_world(num_columns, k=graph_k, p=graph_p)
        self.register_buffer('adj_struct', adj_struct)
        
        # Learnable graph weights
        self.adj_weight = nn.Parameter(torch.randn(num_columns, num_columns) * 0.1)
        
        # Homeostatic scaling state
        self.register_buffer('activity_avg', torch.ones(num_columns))
        self.homeostatic_rate = 0.01
        
        # Intermediate processing
        self.intermediate = nn.Sequential(
            nn.Linear(col_out, col_out),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.LayerNorm(col_out)
        )
        
        # Final classifier
        self.top_fc = nn.Linear(col_out, top_out)
        
        logger.info(f"BioBrainNetwork initialized: {num_columns} columns, "
                   f"input={in_dim}, output={col_out}, top={top_out}")
    
    def _homeostatic_scaling(self, activations: torch.Tensor) -> torch.Tensor:
        """Apply homeostatic scaling to prevent activity explosion or decay.
        
        Maintains stable average activity levels across columns.
        """
        current_activity = activations.mean(dim=(0, 2))
        with torch.no_grad():
            self.activity_avg = (1 - self.homeostatic_rate) * self.activity_avg + \
                               self.homeostatic_rate * current_activity
        scale = 1.0 / (self.activity_avg.unsqueeze(0).unsqueeze(2) + 1e-6)
        return activations * scale.detach()
    
    def _column_activations(self, x: torch.Tensor) -> tuple:
        """Compute activations for all columns with message passing.
        
        Args:
            x: Input tensor (batch, input_dim)
            
        Returns:
            Tuple of (pre-activations, post-activations)
        """
        # Initial column processing
        pre = torch.stack([col(x) for col in self.columns], dim=1)
        
        # Get weighted adjacency matrix
        w = torch.sigmoid(self.adj_weight)
        adj = self.adj_struct * w
        
        post = pre.clone()
        decay_factor = 0.9
        
        # Message passing iterations
        for iter_idx in range(self.message_iters):
            if self.use_attention:
                new_post = []
                for col_idx in range(self.num_columns):
                    center = post[:, col_idx, :]
                    adj_mask = adj[col_idx]
                    attn_weights = self.attention_gates[col_idx](
                        center, post, adj_mask
                    )
                    neigh_msg = torch.einsum('bc,bcd->bd', attn_weights, post)
                    new_col = F.relu(post[:, col_idx, :] + 0.2 * neigh_msg)
                    new_post.append(new_col)
                post = torch.stack(new_post, dim=1)
            else:
                neigh_msg = torch.einsum('ij,bjd->bid', adj, post)
                post = F.relu(post + 0.2 * neigh_msg)
            
            # Decay to prevent signal explosion
            post = decay_factor * post + (1 - decay_factor) * pre
        
        post = self._homeostatic_scaling(post)
        return pre, post
    
    def _hebb_update(self, pre_acts: torch.Tensor, post_acts: torch.Tensor):
        """Hebbian learning update for graph connections.
        
        "Neurons that fire together, wire together"
        Unsupervised learning of connection structure.
        """
        pre = F.normalize(pre_acts.mean(dim=(0, 2)), dim=0)
        post = F.normalize(post_acts.mean(dim=(0, 2)), dim=0)
        
        # Hebbian: strengthen connections between co-active columns
        delta_corr = torch.ger(pre, post)
        
        # Anti-Hebbian: weaken self-connections to prevent runaway excitation
        delta_anti = -0.1 * torch.ger(post, post)
        
        delta = delta_corr + delta_anti
        delta = delta * self.adj_struct  # Only update existing connections
        
        with torch.no_grad():
            self.adj_weight += self.plasticity_lr * delta
            self.adj_weight.data = torch.tanh(self.adj_weight.data)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass for inference.
        
        Args:
            x: Input tensor (batch, input_dim)
            
        Returns:
            Output logits (batch, top_out)
        """
        _, post = self._column_activations(x)
        pooled = torch.mean(post, dim=1)
        features = self.intermediate(pooled)
        logits = self.top_fc(features)
        return logits
    
    def training_step(self, batch: tuple) -> torch.Tensor:
        """Training step with both supervised and unsupervised learning.
        
        Args:
            batch: Tuple of (input, labels)
            
        Returns:
            Loss value
        """
        x, y = batch
        pre, post = self._column_activations(x)
        pooled = torch.mean(post, dim=1)
        features = self.intermediate(pooled)
        logits = self.top_fc(features)
        
        # Supervised loss
        loss = F.cross_entropy(logits, y)
        loss.backward()
        
        # Unsupervised Hebbian update
        self._hebb_update(pre.detach(), post.detach())
        
        return loss
    
    def get_graph_visualization(self) -> str:
        """Get visualization of current graph structure.
        
        Returns:
            DOT format graph string
        """
        w = torch.sigmoid(self.adj_weight).detach().cpu().numpy()
        G = nx.Graph()
        for i in range(self.num_columns):
            G.add_node(f"C{i}")
        for i in range(self.num_columns):
            for j in range(i+1, self.num_columns):
                if self.adj_struct[i, j] == 1:
                    weight = w[i, j]
                    if weight > 0.5:
                        G.add_edge(f"C{i}", f"C{j}", weight=f"{weight:.2f}")
        
        import io
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 10))
        nx.draw(G, pos, node_color='lightblue', with_labels=True, 
                font_size=8, edge_color='gray', alpha=0.7)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf


class BioBrainTrainer:
    """Trainer for Bio-Inspired Neural Network.
    
    Handles training loop, evaluation, and model persistence.
    """
    
    def __init__(self, model: BioBrainNetwork, device: str = None):
        self.model = model
        self.device = device or torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.model.to(self.device)
        self.optimizer = None
        self.scheduler = None
        self.best_accuracy = 0.0
        
        # ARGOS Brain integration
        self.brain_api_url = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
    
    def setup_optimizer(self, learning_rate: float = 1e-3, weight_decay: float = 1e-5):
        """Setup optimizer and learning rate scheduler."""
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(), 
            lr=learning_rate, 
            weight_decay=weight_decay
        )
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, 
            T_max=100  # Adjust based on dataset size
        )
    
    def train_epoch(self, train_loader, epoch: int) -> dict:
        """Train for one epoch.
        
        Args:
            train_loader: DataLoader with training data
            epoch: Current epoch number
            
        Returns:
            Statistics dictionary
        """
        self.model.train()
        total_loss = 0.0
        total_samples = 0
        
        for batch_idx, (x, y) in enumerate(train_loader, start=1):
            x, y = x.to(self.device), y.to(self.device)
            self.optimizer.zero_grad()
            loss = self.model.training_step((x, y))
            self.optimizer.step()
            self.scheduler.step()
            
            total_loss += loss.item() * y.size(0)
            total_samples += y.size(0)
            
            if batch_idx % 100 == 0:
                avg_loss = total_loss / total_samples
                logger.info(f"Epoch {epoch:02d} [{batch_idx}/{len(train_loader)}] "
                          f"Loss={avg_loss:.4f} LR={self.scheduler.get_last_lr()[0]:.6f}")
        
        return {
            'loss': total_loss / total_samples,
            'samples': total_samples
        }
    
    def evaluate(self, test_loader) -> dict:
        """Evaluate model on test data.
        
        Args:
            test_loader: DataLoader with test data
            
        Returns:
            Statistics dictionary with accuracy
        """
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for x, y in test_loader:
                x, y = x.to(self.device), y.to(self.device)
                logits = self.model(x)
                preds = logits.argmax(dim=1)
                correct += (preds == y).sum().item()
                total += y.size(0)
        
        accuracy = correct / total
        logger.info(f"Evaluation: {correct}/{total} ({accuracy*100:.2f}%)")
        
        if accuracy > self.best_accuracy:
            self.best_accuracy = accuracy
            logger.info(f"New best accuracy: {accuracy*100:.2f}%")
        
        return {
            'accuracy': accuracy,
            'correct': correct,
            'total': total
        }
    
    def train(self, train_loader, test_loader, epochs: int = 10) -> dict:
        """Complete training loop.
        
        Args:
            train_loader: Training DataLoader
            test_loader: Test DataLoader
            epochs: Number of epochs
            
        Returns:
            Full training history
        """
        history = {
            'train_loss': [],
            'test_accuracy': []
        }
        
        for epoch in range(1, epochs + 1):
            train_stats = self.train_epoch(train_loader, epoch)
            test_stats = self.evaluate(test_loader)
            
            history['train_loss'].append(train_stats['loss'])
            history['test_accuracy'].append(test_stats['accuracy'])
            
            logger.info(f"Epoch {epoch:02d} Summary: "
                       f"Loss={train_stats['loss']:.4f} "
                       f"Acc={test_stats['accuracy']*100:.2f}%")
        
        return history
    
    def save_model(self, path: str):
        """Save model checkpoint.
        
        Args:
            path: Path to save model
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict() if self.optimizer else None,
            'best_accuracy': self.best_accuracy,
            'adj_weight': self.model.adj_weight,
        }, path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load model checkpoint.
        
        Args:
            path: Path to load model from
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        if self.optimizer and checkpoint.get('optimizer_state_dict'):
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.best_accuracy = checkpoint.get('best_accuracy', 0.0)
        logger.info(f"Model loaded from {path}, best accuracy: {self.best_accuracy*100:.2f}%")
    
    def register_with_brain(self, node_id: str = "entity-bio-brain"):
        """Register this network as a node in ARGOS Brain.
        
        Args:
            node_id: Unique identifier for this node
        """
        import requests
        import json
        
        node_data = {
            "node_id": node_id,
            "address": f"{self.brain_api_url}",
            "capabilities": ["ai", "bio_neural", "mnist", "neuromorphic"],
            "meta": {
                "name": "Bio-Inspired Brain Network",
                "type": "neuromorphic",
                "columns": self.model.num_columns,
                "architecture": "cortical_columns_small_world"
            }
        }
        
        try:
            response = requests.post(
                f"{self.brain_api_url}/brain/register",
                json=node_data,
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Registered with ARGOS Brain: {node_id}")
            else:
                logger.warning(f"Brain registration failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Brain registration error: {e}")


if __name__ == "__main__":
    # Quick test on MNIST
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader
    
    logger.info("Testing BioBrainNetwork on MNIST...")
    
    # MNIST setup
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.view(-1))
    ])
    
    train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    test_set = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    
    train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=32, shuffle=False)
    
    # Create model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BioBrainNetwork(
        num_columns=64,
        in_dim=784,
        col_out=128,
        top_out=10,
        use_attention=True
    )
    
    # Create trainer
    trainer = BioBrainTrainer(model, device)
    trainer.setup_optimizer(learning_rate=1e-3, weight_decay=1e-5)
    
    # Train
    logger.info("Starting training...")
    history = trainer.train(train_loader, test_loader, epochs=5)
    
    # Register with ARGOS Brain
    trainer.register_with_brain("entity-bio-brain-v1")
    
    logger.info(f"Training complete. Best accuracy: {trainer.best_accuracy*100:.2f}%")
    logger.info("BioBrainNetwork ready for ARGOS integration!")
