"""cpg_base_vs_trained.py — порёберное BASE vs TRAINED для CPG-подграфа.
Источник trained: exports/malecns_vision_v4_step14580_frozen_day30.feather
(точные дробные веса + weight_original + sign_original + sign_matches_nt).
Источник BASE: /root/output/male_cns_spikewhale.pt (row=post, col=pre).
CPG-клетки: DNg100 L/R + 6 leg-модулей E1/E2/I1/I2 (26 клеток).
Артефакты:
  /tmp/cpg_base_vs_trained_edges.csv  — порёберно (pre, post, base_w,
      trained_w, delta, base_sign, trained_sign, sign_flip, base_abs, trained_abs)
  /tmp/cpg_arc_edges.json             — trained-веса для dynamics-теста
  печать: статистика по подграфу + сводка по дугам мотива.
"""
import csv
import json

import pyarrow.feather as pf
import torch

# --- BASE ---
pt = torch.load('/root/output/male_cns_spikewhale.pt', map_location='cpu', weights_only=False)
crow, col, wb, ids = pt['crow'], pt['col'], pt['weights'], pt['body_ids']
id2i = {int(b): i for i, b in enumerate(ids.tolist())}
row_of_edge = torch.repeat_interleave(torch.arange(ids.numel()), crow[1:] - crow[:-1])
pre_body = ids[col.long()].tolist()
post_body = ids[row_of_edge].tolist()
wb_list = wb.tolist()
base_by_edge = {}
for i in range(len(pre_body)):
    base_by_edge[(int(pre_body[i]), int(post_body[i]))] = float(wb_list[i])

CPG = [10045, 10056,
       800173, 800009, 800003, 800288, 818556, 800114,
       800863, 801728, 801149, 903216, 802025, 801429,
       801884, 903139, 801257, 803183, 904079, 801916,
       800374, 800233, 800494, 800411, 800103, 800119]
cpg_set = set(CPG)

# --- TRAINED ---
t = pf.read_table('/root/malecns/exports/malecns_vision_v4_step14580_frozen_day30.feather')
print('TRAINED feather cols:', t.column_names, 'rows:', t.num_rows)
df = t.to_pandas()
pre_t = df['body_pre'].to_numpy()
post_t = df['body_post'].to_numpy()
w_t = df['weight'].to_numpy()  # точные дробные (synapse-scale веса или счётчики?)
print('trained weight sample range:', w_t.min(), w_t.max(), 'mean', round(float(w_t.mean()), 4))
frac = (w_t - w_t.round()).__abs__() > 1e-6
print('trained weights fractional rate:', round(float(frac.mean()), 4))
# в каком масштабе? проверим известное ребро DgR->E1_T1L
known = (pre_t == 10056) & (post_t == 800173)
if known.any():
    print('feather known edge DgR->E1_T1L:', float(w_t[known][0]),
          'BASE:', base_by_edge.get((10056, 800173)))
# масштаб: если weight ~= count*0.01 или count
col_w = 'weight'
w_orig = None
if 'weight_original' in t.column_names:
    w_orig = df['weight_original'].to_numpy()
    print('has weight_original; sample:', w_orig[known].tolist() if known.any() else None)

# subgraph rows
sub = df[(df['body_pre'].isin(cpg_set)) & (df['body_post'].isin(cpg_set))]
print('CPG-subgraph rows in trained export:', len(sub))

# порёберный CSV
rows = []
trained_by_edge = {}
for _, r in sub.iterrows():
    pre, post = int(r['body_pre']), int(r['body_post'])
    tw = float(r['weight'])
    trained_by_edge[(pre, post)] = tw
all_edges = sorted(set(base_by_edge) | set(trained_by_edge))
for (pre, post) in all_edges:
    bw = base_by_edge.get((pre, post))
    tw = trained_by_edge.get((pre, post))
    if bw is not None and tw is not None:
        delta = tw - bw
        flip = (bw * tw < 0)
    elif bw is not None:
        delta, flip = -bw, False  # исчезло в trained
    else:
        delta, flip = tw, False  # новое в trained (не должно быть)
    rows.append([pre, post, bw, tw, delta, flip])

with open('/tmp/cpg_base_vs_trained_edges.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['body_pre', 'body_post', 'base_w', 'trained_w', 'delta_w', 'sign_flip'])
    for r in rows:
        wr.writerow(r)

n_kept = sum(1 for r in rows if r[2] is not None and r[3] is not None)
n_lost = sum(1 for r in rows if r[2] is not None and r[3] is None)
n_added = sum(1 for r in rows if r[2] is None and r[3] is not None)
n_flip = sum(1 for r in rows if r[5])
print(f'STATS: total={len(rows)} kept={n_kept} lost={n_lost} added={n_added} sign_flips={n_flip}')
kept = [r for r in rows if r[2] is not None and r[3] is not None]
if kept:
    dw = [abs(r[4]) for r in kept]
    print(f'delta: mean_abs={sum(dw)/len(dw):.4f} max_abs={max(dw):.4f}')
    rel = [abs(r[4]) / max(abs(r[2]), 1e-9) for r in kept]
    print(f'rel_change mean={sum(rel)/len(rel):.3f}')

# JSON для dynamics-теста: только рёбра модуля T1-L
T1L = {'DgR': 10056, 'E1': 800173, 'E2': 800863, 'I1': 801884, 'I2': 800374}
names = {v: k for k, v in T1L.items()}
arc = {}
for (pre, post), tw in trained_by_edge.items():
    if pre in names and post in names:
        arc[f'{names[pre]}->{names[post]}'] = tw
json.dump(arc, open('/tmp/cpg_arc_edges.json', 'w'), ensure_ascii=False, indent=1)
print('T1-L trained edges:', json.dumps(arc, ensure_ascii=False))

# сводка по ключевым дугам мотива (все модули, имена через bodyId-таблицу)
CELLNAME = {
    10045: 'DgL', 10056: 'DgR',
    800173: 'E1_T1L', 800009: 'E1_T2L', 800003: 'E1_T3L',
    800288: 'E1_T1R', 818556: 'E1_T2R', 800114: 'E1_T3R',
    800863: 'E2_T1L', 801728: 'E2_T2L', 801149: 'E2_T3L',
    903216: 'E2_T1R', 802025: 'E2_T2R', 801429: 'E2_T3R',
    801884: 'I1_T1L', 903139: 'I1_T2L', 801257: 'I1_T3L',
    803183: 'I1_T1R', 904079: 'I1_T2R', 801916: 'I1_T3R',
    800374: 'I2_T1L', 800233: 'I2_T2L', 800494: 'I2_T3L',
    800411: 'I2_T1R', 800103: 'I2_T2R', 800119: 'I2_T3R',
}
print('--- MOTIF ARCS: trained vs base (все модули) ---')
arcs = [('E1', 'E2'), ('E2', 'E1'), ('E2', 'I1'), ('E1', 'I1'),
        ('I1', 'E1'), ('I1', 'E2'), ('I2', 'E1'), ('I2', 'E2'),
        ('E1', 'I2'), ('E2', 'I2')]
for (ga, gb) in arcs:
    line = []
    for (pre, post), tw in sorted(trained_by_edge.items()):
        pn = CELLNAME.get(pre, '')
        qn = CELLNAME.get(post, '')
        if pn.startswith(ga + '_') and qn.startswith(gb + '_'):
            bw = base_by_edge.get((pre, post))
            if bw is None:
                bw = 0.0
            line.append(f'{pn}->{qn} base={bw:+.2f} trained={tw:+.3f}')
    print(f'{ga}->{gb}: ' + (' | '.join(line) if line else '(нет рёбер)'))
print('CPG_CSV_DONE')
