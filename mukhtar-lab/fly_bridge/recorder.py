"""recorder.py — запись наблюдений и команд учителя в датасет для адаптеров мухи.

Разделение данных — ПО ЦЕЛЫМ ПРОХОДАМ (сценариям), не по перемешанным кадрам:
  сценарии 0..N_train-1  -> train
  сценарии N_train..N-1  -> held-out (другие старты/цели/препятствия)

Сценарий: старт (x0,y0,yaw0), цель (gx,gy), набор препятствий [(x,y,r)].
Каждый кадр: obs = [dx_goal, dy_goal (в системе тела), sin(yaw_err), cos(yaw_err),
                    tilt_roll, tilt_pitch, 6 контактов, d_obstacle (норм), sin(a_obst), cos(a_obst),
                    prev_speed, prev_turn, prev_step_h]  (17 чисел)
              cmd = [speed, turn, step_h]

Обязательные требования: учитель правит теми же командами; кадры пишутся
в порядке шагов симуляции; сценарии хранятся отдельными последовательностями.
"""
import json
import math
import random

OBS_DIM = 18


def make_scenarios(n, seed=42):
    """Генерирует сценарии: разные старты, цели, расстановки препятствий."""
    rng = random.Random(seed)
    scenarios = []
    for i in range(n):
        x0, y0 = rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)
        yaw0 = rng.uniform(-0.5, 0.5)
        gx = 2.0 + rng.uniform(0.0, 0.4)
        gy = rng.uniform(-0.8, 0.8)
        obstacles = []
        for _ in range(rng.randint(1, 3)):
            ox = 0.7 + rng.uniform(0.0, 1.2)
            oy = rng.uniform(-0.9, 0.9)
            obstacles.append([round(ox, 3), round(oy, 3), 0.12])
        scenarios.append({
            'start': [round(x0, 3), round(y0, 3), round(yaw0, 3)],
            'goal': [round(gx, 3), round(gy, 3)],
            'obstacles': obstacles,
        })
    return scenarios


def obs_vector(body_pos, body_yaw, goal, obstacles, tilt, contacts, prev_cmd,
               max_d=2.0):
    x, y = body_pos[0], body_pos[1]
    gx, gy = goal
    yaw = body_yaw
    dx, dy = gx - x, gy - y
    # в системе тела
    cos_y, sin_y = math.cos(yaw), math.sin(yaw)
    dx_b = dx * cos_y + dy * sin_y
    dy_b = -dx * sin_y + dy * cos_y
    dist = math.hypot(dx, dy) + 1e-6
    yaw_err = math.atan2(dy, dx) - yaw
    # ближайшее препятствие (любое направление — признак видимости)
    d_o, a_o = max_d, 0.0
    for (ox, oy, r) in obstacles:
        d = math.hypot(ox - x, oy - y) - r
        if d < d_o:
            d_o = d
            a_o = (math.atan2(oy - y, ox - x) - yaw + math.pi) % (2 * math.pi) - math.pi
    obs = [
        round(dx_b / 2.0, 4), round(dy_b / 2.0, 4),
        round(math.sin(yaw_err), 4), round(math.cos(yaw_err), 4),
        round(tilt[0], 4), round(tilt[1], 4),
    ] + [1.0 if c else 0.0 for c in contacts] + [
        round(min(d_o, max_d) / max_d, 4),
        round(math.sin(a_o), 4), round(math.cos(a_o), 4),
        round(prev_cmd[0], 4), round(prev_cmd[1], 4), round(prev_cmd[2], 4),
    ]
    assert len(obs) == OBS_DIM, len(obs)
    return obs


def save_dataset(scenarios, sequences, path):
    """sequences: list of list of {'obs': [...], 'cmd': [...]} в порядке шагов."""
    with open(path, 'w', encoding='utf-8') as f:
        for sc, seq in zip(scenarios, sequences):
            f.write(json.dumps({'scenario': sc, 'frames': seq},
                               ensure_ascii=False) + '\n')


def load_dataset(path):
    runs = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                runs.append(json.loads(line))
    return runs


if __name__ == '__main__':
    sc = make_scenarios(3)
    for s in sc:
        print(json.dumps(s, ensure_ascii=False))
    # смоук: кадр из состояния
    o = obs_vector((0, 0, 0.15), 0.1, (2, 0), [(1.0, 0.3, 0.12)],
                   (0.02, -0.01), [1, 1, 1, 0, 1, 1], (0.7, 0.1, 0.6))
    print('obs', o, 'dim', len(o))
