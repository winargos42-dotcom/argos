"""cpg_base_vs_trained2.py — финальный CSV BASE vs TRAINED для CPG-подграфа.

Критические проверки:
 1. trained feather: weight — счётчик (unsigned, Dale-совместимый) или signed?
    Проверка по известному ребру DgR(10056)->E1_T1L(800173), base count 155.
 2. Восстановление знака: signed_trained_w = sign(nt_pre) * count * 0.01,
    где sign(nt_pre) из identity артефакта (ACh/DA/oct/5HT/unclear=+,
    GABA/Glu/hist=-).
CSV: pre_body, pre_type, post_body, post_type, base_count, trained_count,
     base_signed_w, trained_signed_w, ratio_trained_base, delta_abs,
     edge_present_base, edge_present_trained
JSON для dynamics: /tmp/cpg_arc_edges.json (T1-L модуль, signed trained).
"""
import csv
import json

import pyarrow.feather as pf
import torch

FEATHER = '/root/malecns/exports/malecns_vision_v4_step14580_frozen_day30.real.feather'
SCALE = 0.01

# --- BASE ---
pt = torch.load('/root/output/male_cns_spikewhale.pt', map_location='cpu', weights_only=False)
crow, col, wb, ids, ident = (pt['crow'], pt['col'], pt['weights'],
                             pt['body_ids'], pt['identity'])
n = ids.numel()
id2i = {int(b): i for i, b in enumerate(ids.tolist())}
row_of_edge = torch.repeat_interleave(torch.arange(n), crow[1:] - crow[:-1])
pre_body = ids[col.long()].tolist()
post_body = ids[row_of_edge].tolist()
cpg_set = {10045, 10056,
           800173, 800009, 800003, 800288, 818556, 800114,
           800863, 801728, 801149, 903216, 802025, 801429,
           801884, 903139, 801257, 803183, 904079, 801916,
           800374, 800233, 800494, 800411, 800103, 800119}
wb_list = wb.tolist()
base_by_edge = {}
for i in range(len(pre_body)):
    p, q = int(pre_body[i]), int(post_body[i])
    if p in cpg_set and q in cpg_set:
        base_by_edge[(p, q)] = float(wb_list[i])

# --- transmitter sign по identity ---
NT = pt['config']['nt_names']
NT_SIGN = {'acetylcholine': 1, 'dopamine': 1, 'octopamine': 1,
           'serotonin': 1, 'unclear': 1,
           'gaba': -1, 'glutamate': -1, 'histamine': -1}
nt_of_body = {}
for b, i in id2i.items():
    nt_of_body[b] = NT[int(ident[i].argmax())]
print('NT order:', NT)

# --- CPG клетки ---
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
cpg_set = set(CELLNAME)

# --- TRAINED ---
t = pf.read_table(FEATHER)
print('TRAINED feather cols:', t.column_names, 'rows:', t.num_rows)
df = t.to_pandas()
print('weight dtype:', df['weight'].dtype)
wmin, wmax = float(df['weight'].min()), float(df['weight'].max())
print('weight range:', wmin, wmax, 'mean:', round(float(df['weight'].mean()), 4))
frac = (df['weight'].to_numpy() - df['weight'].to_numpy().round()).__abs__() > 1e-6
print('fractional rate:', round(float(frac.mean()), 5))
# Проверка 1: известное ребро
known = (df['body_pre'] == 10056) & (df['body_post'] == 800173)
if known.any():
    print('CHECK1 known edge DgR->E1_T1L trained weight:',
          float(df.loc[known, 'weight'].iloc[0]),
          '(base count=155, base w=+1.55)')
neg_rate = float((df['weight'] < 0).mean())
print('negative weight rate in feather:', round(neg_rate, 5),
      '(если ~0 — weight это unsigned count)')

sub = df[(df['body_pre'].isin(cpg_set)) & (df['body_post'].isin(cpg_set))]
trained_by_edge = {}
for _, r in sub.iterrows():
    trained_by_edge[(int(r['body_pre']), int(r['body_post']))] = float(r['weight'])

# --- CSV ---
rows = []
all_edges = sorted(set(base_by_edge) | set(trained_by_edge))
for (pre, post) in all_edges:
    pn = CELLNAME[pre]
    qn = CELLNAME[post]
    b = base_by_edge.get((pre, post))
    t = trained_by_edge.get((pre, post))
    base_count = None if b is None else abs(b) / SCALE
    trained_count = None if t is None else t  # unsigned count по CHECK1
    base_signed = b
    sign_pre = NT_SIGN[nt_of_body[pre]]
    trained_signed = None if t is None else sign_pre * t * SCALE
    if base_signed is not None and trained_signed is not None:
        ratio = trained_signed / base_signed if base_signed != 0 else float('nan')
        delta_abs = abs(trained_signed - base_signed)
    else:
        ratio = float('nan')
        delta_abs = None
    rows.append([
        pre, pn, post, qn,
        base_count, trained_count,
        base_signed, trained_signed,
        round(ratio, 4) if ratio == ratio else None,
        round(delta_abs, 4) if delta_abs is not None else None,
        1 if b is not None else 0,
        1 if t is not None else 0,
    ])

with open('/tmp/cpg_base_vs_trained_edges.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['pre_body', 'pre_type', 'post_body', 'post_type',
                 'base_count', 'trained_count', 'base_signed_w',
                 'trained_signed_w', 'ratio_trained_base', 'delta_abs',
                 'edge_present_base', 'edge_present_trained'])
    wr.writerows(rows)

n_kept = sum(1 for r in rows if r[4] is not None and r[5] is not None)
n_lost = sum(1 for r in rows if r[4] is not None and r[5] is None)
n_added = sum(1 for r in rows if r[4] is None and r[5] is not None)
n_zeroed = sum(1 for r in rows if r[5] == 0)
print(f'STATS total={len(rows)} kept={n_kept} lost={n_lost} added={n_added} zeroed={n_zeroed}')
kept = [r for r in rows if r[4] is not None and r[5] is not None]
if kept:
    rel = [abs(r[8]) for r in kept if r[8] is not None and r[8] == r[8]]
    print(f'kept edges ratio_trained_base: mean={sum(rel)/len(rel):.3f} '
          f'min={min(rel):.3f} max={max(rel):.3f}')

# --- JSON для dynamics (T1-L) ---
T1L = {'DgR': 10056, 'E1': 800173, 'E2': 800863, 'I1': 801884, 'I2': 800374}
names = {v: k for k, v in T1L.items()}
arc = {}
for (pre, post), t in trained_by_edge.items():
    if pre in names and post in names:
        sign_pre = NT_SIGN[nt_of_body[pre]]
        arc[f'{names[pre]}->{names[post]}'] = sign_pre * t * SCALE
json.dump(arc, open('/tmp/cpg_arc_edges.json', 'w'), ensure_ascii=False, indent=1)
print('T1-L trained signed edges:', json.dumps(arc, ensure_ascii=False))

# --- агрегаты мотива ---
print('--- MOTIF ARCS: BASE vs TRAINED (все модули) ---')
for (ga, gb) in [('E1', 'E2'), ('E2', 'E1'), ('E2', 'I1'), ('E1', 'I1'),
                 ('I1', 'E1'), ('I1', 'E2'), ('I2', 'E1'), ('I2', 'E2'),
                 ('E1', 'I2'), ('E2', 'I2'), ('Dg', 'E1')]:
    line = []
    for r in rows:
        if r[1].startswith(ga + '_') and r[3].startswith(gb + '_'):
            line.append(f'{r[1]}->{r[3]} base={r[6]:+.2f} trained={r[7]:+.3f}'
                        if r[7] is not None else
                        f'{r[1]}->{r[3]} base={r[6]:+.2f} trained=GONE')
    print(f'{ga}->{gb}: ' + (' | '.join(line) if line else '(нет рёбер)'))
print('CPG_CSV_DONE')
