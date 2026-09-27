"""Drop-in faster SparseRecurrent. Same math as sparse_mm.py.

Backward changes:
  * topology-derived index tensors (row ids, W^T CSR, edge permutation) are
    built once and cached instead of repeat_interleave'd every call;
  * grad_spikes = W^T @ grad_out via cuSPARSE instead of a [B, nnz] gather +
    atomic scatter_add;
  * grad_values only touches edges whose presynaptic cell actually fired
    (rate ~0.2% -> ~0.2% of the 25.6M edges) instead of two [B, nnz] temps.
"""
import torch

_cache = {}


def _topology(crow, col):
    key = (crow.data_ptr(), col.data_ptr(), crow.device)
    t = _cache.get(key)
    if t is not None:
        return t
    n = crow.numel() - 1
    counts = crow[1:] - crow[:-1]
    rows = torch.repeat_interleave(torch.arange(n, device=crow.device), counts)
    # Sort edges by presynaptic cell -> CSR of W^T (== CSC of W).
    perm = torch.argsort(col * n + rows)  # stable order within each column
    t_col = rows[perm]  # postsynaptic ids, grouped by presynaptic cell
    t_counts = torch.bincount(col, minlength=n)
    t_crow = torch.zeros(n + 1, dtype=crow.dtype, device=crow.device)
    t_crow[1:] = torch.cumsum(t_counts, 0)
    t = dict(n=n, perm=perm, t_col=t_col, t_crow=t_crow, t_counts=t_counts)
    _cache[key] = t
    return t


class SparseRecurrent(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values, crow, col, spikes):
        n = crow.numel() - 1
        csr = torch.sparse_csr_tensor(crow, col, values, size=(n, n))
        ctx.save_for_backward(values, crow, col, spikes)
        return torch.sparse.mm(csr, spikes.T).T

    @staticmethod
    def backward(ctx, grad_out):
        values, crow, col, spikes = ctx.saved_tensors
        t = _topology(crow, col)
        n, perm = t['n'], t['perm']
        grad_values = grad_spikes = None
        if ctx.needs_input_grad[3]:
            wt = torch.sparse_csr_tensor(t['t_crow'], t['t_col'], values[perm], size=(n, n))
            grad_spikes = torch.sparse.mm(wt, grad_out.T.contiguous()).T
        if ctx.needs_input_grad[0]:
            grad_values = torch.zeros_like(values)
            active = (spikes != 0).any(0).nonzero().squeeze(1)  # presynaptic cells that fired
            if active.numel():
                cnt = t['t_counts'][active]
                start = t['t_crow'][active]
                # edge slots (in W^T order) belonging to active presynaptic cells
                owner = torch.repeat_interleave(torch.arange(active.numel(), device=cnt.device), cnt)
                offs = torch.arange(owner.numel(), device=cnt.device) - torch.repeat_interleave(
                    torch.cumsum(cnt, 0) - cnt, cnt)
                slot = start[owner] + offs
                post = t['t_col'][slot]
                pre = active[owner]
                g = (grad_out.index_select(1, post) * spikes.index_select(1, pre)).sum(0)
                grad_values[perm[slot]] = g
        return grad_values, None, None, grad_spikes
