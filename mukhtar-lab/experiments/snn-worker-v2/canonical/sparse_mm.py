"""CSR recurrence with gradients only on existing edges (nnz), not dense N×N."""
import torch


class SparseRecurrent(torch.autograd.Function):
    @staticmethod
    def forward(ctx, values, crow, col, spikes):
        n = crow.numel() - 1
        csr = torch.sparse_csr_tensor(crow, col, values, size=(n, n))
        ctx.save_for_backward(values, crow, col, spikes)
        ctx.n = n
        return torch.sparse.mm(csr, spikes.T).T

    @staticmethod
    def backward(ctx, grad_out):
        values, crow, col, spikes = ctx.saved_tensors
        n = ctx.n
        counts = crow[1:] - crow[:-1]
        rows = torch.repeat_interleave(torch.arange(n, device=crow.device), counts)
        # dW_ij = sum_b gout[b,i] * spk[b,j]
        grad_values = (grad_out.index_select(1, rows) * spikes.index_select(1, col)).sum(0)
        # d_spk[b,j] = sum_i W_ij * gout[b,i]
        contrib = grad_out.index_select(1, rows) * values
        grad_spikes = torch.zeros_like(spikes)
        grad_spikes.scatter_add_(1, col.unsqueeze(0).expand_as(contrib), contrib)
        return grad_values, None, None, grad_spikes
