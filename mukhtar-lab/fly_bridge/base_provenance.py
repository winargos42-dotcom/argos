"""base_provenance.py — 4 проверки происхождения /root/output/male_cns_spikewhale.pt:
1. формула W = sign(nt)*count*0.01 (доля рёбер с целыми счётчиками)
2. Dale-нарушения при предполагаемой конвенции + гистограмма знаков по nt
3. sha256 + статистика файла
4. (база для) порёберное сравнение: инстанс-матрица CPG (26 клеток)
"""
import hashlib
import json

import torch

PATH = '/root/output/male_cns_spikewhale.pt'
pt = torch.load(PATH, map_location='cpu', weights_only=False)
crow, col, w, ident, ids = pt['crow'], pt['col'], pt['weights'], pt['identity'], pt['body_ids']
n = ids.numel()
E = w.numel()
NT = pt['config']['nt_names']
print('NEURONS', n, 'EDGES', E)
print('SHA256', hashlib.sha256(open(PATH, 'rb').read()).hexdigest())
print('W range', float(w.min()), float(w.max()), 'mean', round(float(w.mean()), 5))

# --- Check 3: формула. w = count*0.01 => |w|/0.01 целое ---
sc = float(pt['config']['synapse_scale'])
counts = (w.abs() / sc)
exact = ((counts - counts.round()).abs() < 1e-3)
print('FORMULA exact-multiples rate:', round(float(exact.float().mean()), 6))
frac_hist = {
    'zero': float((w == 0).float().mean()),
    'frac_small': float(((w != 0) & ~exact).float().mean()),
}

# --- Check 2: Dale-нарушения ---
# Предполагаемая конвенция: ACh+, GABA-, Glu-, hist-, DA-, oct+, 5HT-, unclear+
NT_SIGN = torch.tensor([1, -1, -1, -1, -1, 1, -1, 1], dtype=torch.float32)
pre_nt = ident.argmax(1)
rowlen = crow[1:] - crow[:-1]
pre_of_edge = torch.repeat_interleave(torch.arange(n), rowlen)
sign_pre = NT_SIGN[pre_nt[pre_of_edge]]
viol = (torch.sign(w) != sign_pre) & (w != 0)
print('DALE violations (assumed conv):', int(viol.sum()), 'of', E,
      round(float(viol.float().mean()), 6))
print('PER_NT sign histogram (pos/neg/zero, viol rate):')
for i, nm in enumerate(NT):
    em = pre_nt[pre_of_edge] == i
    if int(em.sum()) == 0:
        continue
    pos = int(((w > 0) & em).sum())
    neg = int(((w < 0) & em).sum())
    zro = int(((w == 0) & em).sum())
    v = int((viol & em).sum())
    print(f'  {nm:12s} edges={int(em.sum()):9d} pos={pos:9d} neg={neg:9d} zero={zro:8d} viol_rate={v/em.sum():.4f}')

# --- Check 4 prep: инстанс-матрица CPG ---
cells = {
    'DgL': 10045, 'DgR': 10056,
    'E1_T1L': 800173, 'E1_T2L': 800009, 'E1_T3L': 800003,
    'E1_T1R': 800288, 'E1_T2R': 818556, 'E1_T3R': 800114,
    'E2_T1L': 800863, 'E2_T2L': 801728, 'E2_T3L': 801149,
    'E2_T1R': 903216, 'E2_T2R': 802025, 'E2_T3R': 801429,
    'I1_T1L': 801884, 'I1_T2L': 903139, 'I1_T3L': 801257,
    'I1_T1R': 803183, 'I1_T2R': 904079, 'I1_T3R': 801916,
    'I2_T1L': 800374, 'I2_T2L': 800233, 'I2_T3L': 800494,
    'I2_T1R': 800411, 'I2_T2R': 800103, 'I2_T3R': 800119,
}
id2i = {int(b): i for i, b in enumerate(ids.tolist())}
rev_idx = {id2i[v]: k for k, v in cells.items()}
pairs = []
for a, v in cells.items():
    ia = id2i[v]
    for j in range(int(crow[ia]), int(crow[ia + 1])):
        b = int(col[j])
        if b in rev_idx:
            pairs.append([a, rev_idx[b], round(float(w[j]), 4)])
print('INSTANCE_MATRIX', json.dumps(pairs, ensure_ascii=False))
print('N_PAIRS', len(pairs))

# --- Check 5: знак был per-cell или per-edge? ---
# Доля клеток, у которых исходящие рёбра однородны по знаку (>=95% одного знака)
uniform = 0
mixed = 0
total_cells = 0
for i in range(n):
    a, b = int(crow[i]), int(crow[i + 1])
    deg = b - a
    if deg < 5:
        continue
    total_cells += 1
    seg = w[a:b]
    frac_pos = float((seg > 0).float().mean())
    if frac_pos > 0.95 or frac_pos < 0.05:
        uniform += 1
    else:
        mixed += 1
print('SIGN_PER_CELL: uniform(>=95%) =', uniform, 'mixed =', mixed,
      'of', total_cells, 'cells with deg>=5')
