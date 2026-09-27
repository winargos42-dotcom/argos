"""snn_rank_worker.py — персистентный SNN-инференс на ноде (MaleCNS).

Мост ARC: читает построчно JSON-запросы из stdin, отвечает JSON
построчно в stdout (flush). Чекпойнт грузится ОДИН раз при старте.

Запрос:  {"vecs": [[f1..f160], ...]}   (строки = кандидаты; дубликаты
                                        считаются один раз)
Ответ:   {"readout": [[..64], ...]}
"ping" -> {"pong": 1}

Ядро: male_cns_spikewhale.pt (167565 нейронов, 25.6M синапсов).
v0.1: входной пул = 160 клеток с наибольшим in-degree, инжект
внешнего тока tanh(f)*0.3; подграф = входы + 2 синаптических слоя
(каждый слой cap 15000 клеток по входящему |w|); readout = средние
спайк-рейты последних 15 из 40 тиков по топ-64 клеткам подграфа
(по входящему |w|), z-score -> tanh -> 64d.
LIF: beta=0.9, thr=1.0, synapse_scale=0.01 (config чекпойнта).
"""
import json
import sys
import time

import numpy as np
import torch

CKPT = '/root/output/male_cns_spikewhale.pt'
N_IN = 160
N_OUT = 64
CAP_LAYER = 15000
TICKS = 40
READOUT_LAST = 15
INJ_SCALE = 1.0
BETA = 0.9
THR = 1.0
SYN_SCALE = 0.05  # подграф слабее полной сети (30k из 167k клеток)


def log(msg):
    print(json.dumps({'log': msg}), file=sys.stderr, flush=True)


def layer_from(pre_ids, crow, col, w_np, cap):
    """Клетки-пост заданного пула пре: cap лучших по входящему |w|."""
    posts = []
    ws = []
    for p in pre_ids:
        s, e = int(crow[p]), int(crow[p + 1])
        posts.append(col[s:e])
        ws.append(np.abs(w_np[s:e]))
    if not posts:
        return np.array([], dtype=np.int64)
    posts = np.concatenate(posts)
    ws = np.concatenate(ws)
    tot = np.bincount(posts, weights=ws, minlength=crow.shape[0] - 1)
    idx = np.argsort(-tot)
    idx = idx[tot[idx] > 0][:cap]
    return idx.astype(np.int64)


def load_graph():
    t0 = time.time()
    pt = torch.load(CKPT, map_location='cpu', weights_only=False)
    crow = pt['crow'].numpy()
    col = pt['col'].numpy()
    w = pt['weights'].numpy()
    n = crow.shape[0] - 1
    del pt
    log(f'checkpoint loaded {time.time() - t0:.1f}s')
    in_deg = crow[1:] - crow[:-1]
    in_pool = np.argsort(-in_deg)[:N_IN].astype(np.int64)
    l1 = layer_from(in_pool, crow, col, w, CAP_LAYER)
    log(f'layer1: {len(l1)} cells {time.time() - t0:.1f}s')
    l2 = layer_from(l1, crow, col, w, CAP_LAYER)
    log(f'layer2: {len(l2)} cells {time.time() - t0:.1f}s')
    sub = np.concatenate([in_pool, l1, l2])
    sub_sorted = np.sort(sub)
    sub_lookup = np.zeros(n, dtype=np.int64)
    sub_lookup[sub_sorted] = np.arange(sub_sorted.shape[0])
    # рёбра подграфа (post, pre локальные)
    rows, cols, ws = [], [], []
    for p in sub_sorted:
        s, e = int(crow[p]), int(crow[p + 1])
        if s == e:
            continue
        c = col[s:e]
        idx = np.searchsorted(sub_sorted, c)
        idx_c = np.clip(idx, 0, len(sub_sorted) - 1)
        valid = (idx < len(sub_sorted)) & (sub_sorted[idx_c] == c)
        k = np.flatnonzero(valid)
        if k.shape[0]:
            rows.append(np.full(k.shape[0], sub_lookup[p]))
            cols.append(idx[k])
            ws.append(w[s:e][k])
    rows = np.concatenate(rows).astype(np.int64)
    cols = np.concatenate(cols).astype(np.int64)
    ws = np.concatenate(ws).astype(np.float32)
    M = len(sub_sorted)
    order = np.argsort(rows, kind='stable')
    rows = rows[order]
    cols = cols[order]
    ws = ws[order]
    crow_sub = np.zeros(M + 1, dtype=np.int64)
    np.add.at(crow_sub, rows + 1, 1)
    crow_sub = np.cumsum(crow_sub)
    tot = np.bincount(rows, weights=np.abs(ws), minlength=M)
    readout = np.argsort(-tot)[:N_OUT].astype(np.int64)
    in_local = sub_lookup[in_pool]
    log(f'graph ready: M={M} edges={len(ws)} readout={len(readout)} '
        f'total {time.time() - t0:.1f}s')
    return M, crow_sub, torch.from_numpy(cols), torch.from_numpy(ws), \
        torch.from_numpy(in_local), torch.from_numpy(readout), M


def run(vecs):
    M, crow, col, w, in_local, readout, n_ro = G
    # /64: цвета/counts (0..255) не насыщают tanh, мелкие фичи проходят
    f = torch.tanh(torch.tensor(vecs, dtype=torch.float32) / 64.0)
    inj = torch.zeros(M)
    inj.scatter_(0, in_local, f * INJ_SCALE)
    v = torch.zeros(M)
    rate_sum = torch.zeros(M)
    for t in range(TICKS):
        s = (v >= THR).float()
        v = v * BETA + inj
        v = v - s  # subtractive reset (LIF)
        x = w * s[col]
        syn = torch.zeros(M)
        syn.scatter_add_(0, col, x)
        v = v + syn * SYN_SCALE
        v = torch.where(torch.abs(v) > 30.0, torch.sign(v) * 30.0, v)
        if t >= TICKS - READOUT_LAST:
            rate_sum += s
    rates = rate_sum / READOUT_LAST
    # без z-score: масштаб несёт информацию о силе входа (сеть в этом
    # режиме почти линейна, нормировка паттерна убивает различия)
    out = torch.tanh(rates[readout])
    in_rate = float(rates[in_local].mean())
    ro_rate = float(rates[readout].mean())
    return out, in_rate, ro_rate, rates[readout].tolist()


def main():
    global G
    G = load_graph()
    cache = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == 'ping':
            print(json.dumps({'pong': 1}), flush=True)
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            print(json.dumps({'error': f'bad json: {e}'}), flush=True)
            continue
        vecs = req.get('vecs', [])
        out = []
        diag = []
        t0 = time.time()
        for v in vecs:
            key = tuple(round(float(x), 6) for x in v[:160])
            if key not in cache:
                cache[key] = run(key)
            r = cache[key]
            if req.get('diag'):
                diag.append({'in_rate': r[1], 'ro_rate': r[2],
                             'ro': r[3]})
            out.append(r[0].tolist())
        log(f'batch {len(vecs)} in {time.time() - t0:.2f}s')
        resp = {'readout': out}
        if req.get('diag'):
            resp['diag'] = diag
        print(json.dumps(resp), flush=True)


if __name__ == '__main__':
    main()
