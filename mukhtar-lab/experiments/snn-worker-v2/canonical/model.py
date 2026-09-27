"""Sparse anatomical adaptation of SpikeWhale's recurrent LIF core."""
import torch
import math
from torch import nn
from upstream.lif import spike, soft_clamp


class ConnectomeSNN(nn.Module):
    def __init__(self, artifact):
        super().__init__()
        self.config = artifact['config']
        for name in ('body_ids', 'crow', 'col', 'weights', 'identity'):
            self.register_buffer(name, artifact[name])
        k = self.identity.shape[1]
        self.thr_gain = nn.Parameter(torch.zeros(k))
        self.beta_gain = nn.Parameter(torch.zeros(k))
        self.in_gain = nn.Parameter(torch.zeros(k))
        self.lora = None

    def add_lora(self, rank=2048, alpha=None):
        """Freeze the base and add an unmasked low-rank recurrent correction."""
        if self.lora is not None:
            raise ValueError('LoRA already installed')
        if not isinstance(rank, int) or not 1 <= rank <= self.n:
            raise ValueError('rank must be an integer between 1 and neuron count')
        alpha = float(rank if alpha is None else alpha)
        if not math.isfinite(alpha) or alpha <= 0:
            raise ValueError('alpha must be finite and positive')
        self.requires_grad_(False)
        self.lora = RecurrentLoRA(self.n, rank, alpha).to(self.weights.device)
        return self

    def save_adapter(self, path):
        if self.lora is None:
            raise ValueError('No adapter installed')
        torch.save(dict(format='male-cns-spikewhale-lora-v1',
                        body_ids=self.body_ids.detach().cpu(),
                        rank=self.lora.rank, alpha=self.lora.alpha,
                        state={k: v.detach().cpu() for k,v in self.lora.state_dict().items()}), path)

    def load_adapter(self, path):
        data = torch.load(path, map_location='cpu', weights_only=True)
        if data['format'] != 'male-cns-spikewhale-lora-v1' or not torch.equal(data['body_ids'], self.body_ids.cpu()):
            raise ValueError('Adapter format or neuron ordering does not match')
        self.add_lora(data['rank'], data['alpha'])
        self.lora.load_state_dict(data['state'])
        return self

    @property
    def n(self):
        return self.body_ids.numel()

    def modulation(self):
        # SpikeWhale bridge equations; measured NT identity replaces human genes.
        p = self.identity
        threshold = (self.config['threshold'] * torch.exp(p @ self.thr_gain)).clamp(.25, 3.)
        b = torch.tensor(self.config['beta'], device=p.device)
        beta = torch.sigmoid(torch.logit(b) + p @ self.beta_gain).clamp(.5, .97)
        gain = torch.exp(p @ self.in_gain).clamp(.3, 3.)
        return beta, threshold, gain

    def initial_state(self, batch=1):
        z = self.weights.new_zeros(batch, self.n)
        return {'mem': z, 'spk': z.clone()}

    def step(self, current, state):
        if current.shape != state['mem'].shape or current.shape[-1] != self.n:
            raise ValueError('current and state must have shape [batch, neurons]')
        if getattr(self,'_csr',None) is None or self._csr.device!=self.weights.device:
            self._csr=torch.sparse_csr_tensor(self.crow,self.col,self.weights,
                                              size=(self.n,self.n),device=self.weights.device)
        # Frozen anatomy: no grad through the CSR multiply (saves a ~1 GiB workspace).
        # LoRA still receives gradients through spikes and the low-rank path.
        recurrent=torch.sparse.mm(self._csr,state['spk'].detach().T).T
        if self.lora is not None:
            recurrent=recurrent+self.lora(state['spk'])
        beta, threshold, gain = self.modulation()
        pre = beta * state['mem'] + gain * current + recurrent
        spikes = spike(pre, threshold)
        state = {'mem': soft_clamp(pre - spikes * threshold, 30.), 'spk': spikes}
        return {'spikes': spikes, 'features': torch.tanh(pre)}, state

    @classmethod
    def load(cls, path, device='cpu'):
        return cls(torch.load(path, map_location='cpu', weights_only=True)).to(device)


class RecurrentLoRA(nn.Module):
    def __init__(self, neurons, rank, alpha):
        super().__init__()
        self.rank, self.alpha = rank, alpha
        self.down = nn.Linear(neurons, rank, bias=False)
        self.up = nn.Linear(rank, neurons, bias=False)
        nn.init.zeros_(self.up.weight)

    def forward(self, spikes):
        dtype=self.down.weight.dtype
        out=self.up(self.down(spikes.to(device=self.down.weight.device,dtype=dtype)))*(self.alpha/self.rank)
        return out.to(device=spikes.device,dtype=spikes.dtype)
