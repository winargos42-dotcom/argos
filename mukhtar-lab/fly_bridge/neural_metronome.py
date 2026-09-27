"""neural_metronome.py — мост MaleCNS CPG → контроллер Б (M6 v1).

Принцип (по спека Севы): нейронный модуль задаёт только КАДЕНС (темп
шага), математический CPG Б сохраняет фазовые смещения трипода и всю
кинематику; safety остаётся у Б. R1 (удар лапы в swing) даёт короткий
импульс +2.0 в I2 метронома на 1 нейро-тик — по PRC это сдвигает фазу
следующего burst'а (фазовый сброс шага).

Параметры моста:
  - dt_neural: длительность нейро-тика в секундах. Модуль даёт ~16-20
    тиков на цикл; целевой шаг ~0.8 с → dt_neural ≈ 0.04-0.05 с.
  - drive: ток в DNg100 (команда скорости от навигации), тот же sweep
    0.4-1.6, что в M1.
  - omega_gait = 2*pi / (period_neural * dt_neural) — частота походки.
Выходные сигналы для Б: cadence_hz, phase (0..2pi по burst-таймеру),
pulse_ok (подтверждение инъекции).
"""
import math

import torch

BETA = 0.9
THR = 1.0
ERF_K = math.sqrt(math.pi) / 2.0
NAMES = ['DgR', 'E1', 'E2', 'I1', 'I2']
IDX = {n: i for i, n in enumerate(NAMES)}

BASE_EDGES = {
    ('DgR', 'E1'): 1.55, ('DgR', 'E2'): 0.01, ('DgR', 'I2'): 0.07,
    ('E1', 'E2'): 4.65, ('E2', 'E1'): 0.11, ('E1', 'DgR'): 0.01,
    ('E2', 'I1'): 0.38, ('E1', 'I1'): 0.06,
    ('E1', 'I2'): 0.84, ('E2', 'I2'): 2.15,
    ('I1', 'E1'): -5.26, ('I1', 'E2'): -1.21, ('I1', 'I2'): -0.02,
    ('I2', 'E1'): -3.28, ('I2', 'E2'): -0.56,
}

# TRAINED T1-L (из /tmp/cpg_arc_edges.json, точные значения после обучения)
TRAINED_EDGES = {
    ('DgR', 'E1'): 2.640017032623291, ('DgR', 'E2'): 0.019999999552965164,
    ('DgR', 'I2'): 0.04612334445118904,
    ('E1', 'E2'): 4.650899410247803, ('E2', 'E1'): 0.10757360607385635,
    ('E1', 'DgR'): 0.010295931249856949, ('I2', 'DgR'): -0.009999999776482582,
    ('E2', 'I1'): 0.3809918463230133, ('E1', 'I1'): 0.06114206835627556,
    ('E1', 'I2'): 0.8407794833183289, ('E2', 'I2'): 2.150804042816162,
    ('I1', 'E1'): -5.259999752044678, ('I1', 'E2'): -1.209999918937683,
    ('I1', 'I2'): -0.019999999552965164,
    ('I2', 'E1'): -3.2799999713897705, ('I2', 'E2'): -0.5600000023841858,
}


class NeuralMetronome:
    def __init__(self, dt_neural=0.05, edges=None):
        self.dt_neural = dt_neural
        self.edges = edges or BASE_EDGES
        W = torch.zeros(5, 5)
        for (pre, post), w in self.edges.items():
            W[IDX[post], IDX[pre]] = w
        self.W = W
        self.mem = torch.zeros(5)
        self.spk = torch.zeros(5)
        self._pulse = 0.0
        self._last_onset = -1.0
        self._t = 0
        self._period_ema = 18.0  # тиков
        self._e_hist = []
        self._above = False
        self.prc_pending = None
        self.prc_log = []   # записи: {phi, pred_dphi, meas_dphi, at_tick}

    def _spike(self, pre, thr):
        return (pre >= thr).to(pre.dtype)

    def _soft_clamp(self, x, bound=30.0):
        # ровно как в lif.py: bound*erf(x*sqrt(pi)/2/bound)
        return bound * torch.erf(x * (ERF_K / bound))

    def tick(self, drive):
        """Один нейро-тик. drive — ток в DgR. Возвращает (spikes, burst_onset_now)."""
        cur = torch.zeros(5)
        cur[IDX['DgR']] = drive
        cur[IDX['I2']] += self._pulse
        self._pulse = 0.0  # импульс ровно один тик
        recurrent = self.W @ self.spk  # W[post,pre]: I[post] = sum_pre W*spk[pre]
        pre = BETA * self.mem + cur + recurrent
        s = self._spike(pre, THR)
        self.mem = self._soft_clamp(pre - s * THR)
        self.spk = s
        self._t += 1
        # onset-детектор ровно как в cpg_module_test: boxcar(3) по E1+E2,
        # порог 0.6, гистерезис 0.2
        e_sum = float(s[IDX['E1']] + s[IDX['E2']])
        self._e_hist.append(e_sum)
        burst_onset = False
        if len(self._e_hist) > 3:
            self._e_hist.pop(0)
        if len(self._e_hist) == 3:
            sm = sum(self._e_hist) / 3.0
            if not self._above and sm >= 0.6:
                burst_onset = True
                self._above = True
                if self._last_onset > 0:
                    per = self._t - self._last_onset
                    self._period_ema = 0.9 * self._period_ema + 0.1 * per
                self._last_onset = self._t
                # завершаем pending PRC-замер, если был пульс
                if self.prc_pending is not None and self._t > 3:
                    phi = self.prc_pending['phi']
                    pred_t = self.prc_pending['pred_tick']
                    meas = (2.0 * math.pi * (self._t - pred_t)
                            / max(self._period_ema, 1e-3)) if pred_t else None
                    self.prc_log.append({
                        'phi': round(phi, 3),
                        'pred_dphi': round(self.predicted_prc_shift(phi), 3),
                        'meas_dphi': round(meas, 3) if meas is not None
                        else None,
                        'at_tick': self._t,
                    })
                    self.prc_pending = None
            elif sm < 0.2:
                self._above = False
        return s, burst_onset

    def period_ticks(self):
        """EMA текущего периода в тиках."""
        return self._period_ema

    def is_valid(self, max_gap_mult=5.0):
        """Валиден ли ритм: после последнего burst'а не должно пройти
        больше max_gap_mult периодов (иначе модуль молчит/насытился)."""
        if self._last_onset < 0:
            return False
        gap = self._t - self._last_onset
        return gap <= max_gap_mult * self._period_ema

    def cadence_hz(self):
        return 1.0 / (self._period_ema * self.dt_neural)

    # ------------------------------------------------------------------
    # PRC: измерение фазового сдвига при пульсе + предсказание из таблицы M2
    # ------------------------------------------------------------------
    _PRC_I2_PTS = [(0.0, -1.75), (0.7, 0.35), (3.5, 0.35), (4.2, 1.05),
                   (4.9, 1.05), (5.2, 1.75), (5.6, 1.75), (6.28, 2.09)]

    @classmethod
    def predicted_prc_shift(cls, phi):
        """Интерполяция измеренной PRC M2 (I2 pulse, рад -> сдвиг рад)."""
        pts = cls._PRC_I2_PTS
        if phi <= pts[0][0]:
            return pts[0][1]
        if phi >= pts[-1][0]:
            return pts[-1][1]
        for (p1, d1), (p2, d2) in zip(pts, pts[1:]):
            if p1 <= phi <= p2:
                return d1 + (d2 - d1) * (phi - p1) / (p2 - p1)
        return 0.0

    def pulse_i2(self, amp=2.0):
        """Импульс в I2 на один следующий тик (R1 phase-reset, M6.3).
        Логируем фазу пульса и предсказанный момент следующего onset'а."""
        self._pulse += amp
        self.prc_pending = {
            'phi': self.phase(),
            'pred_tick': (self._last_onset + self._period_ema
                          if self._last_onset > 0 else None),
        }

    def phase(self):
        """Фаза 0..2pi от последнего burst-начала."""
        if self._last_onset < 0:
            return 0.0
        return (2 * math.pi * (self._t - self._last_onset)
                / self._period_ema) % (2 * math.pi)

    def drive(self, current):
        return self.tick(current)


if __name__ == '__main__':
    # Смоук-тест: каденс растёт с драйвом, пульс в I2 сдвигает фазу
    for d in (0.4, 0.8, 1.2):
        m = NeuralMetronome()
        for _ in range(400):
            m.tick(d)
        print(f'BASE drive={d}: period={m._period_ema:.1f} ticks, '
              f'cadence={m.cadence_hz():.3f} Hz, valid={m.is_valid()}',
              flush=True)
    # TRAINED T1-L — P_REF кандидат на drive 0.8
    for d in (0.4, 0.8, 1.2, 1.6):
        m = NeuralMetronome(edges=TRAINED_EDGES)
        for _ in range(400):
            m.tick(d)
        print(f'TRAINED drive={d}: period={m._period_ema:.1f} ticks, '
              f'cadence={m.cadence_hz():.3f} Hz, valid={m.is_valid()}',
              flush=True)
    # PRC-смоук: пульс в I2 на известной фазе
    m = NeuralMetronome()
    for _ in range(300):
        m.tick(0.8)
    phase_before = m.phase()
    m.pulse_i2(2.0)
    m.tick(0.8)
    print(f'pulse smoke: phase before={phase_before:.2f}, '
          f'after 1 tick={m.phase():.2f}', flush=True)
    print('METRONOME_SMOKE_DONE')
