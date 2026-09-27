# ARC state-action head: проверенное исправление, экспериментальная политика

Исправлена архитектура головы: состояние теперь может менять порядок
кандидатов, в том числе порядок кликов одной категории. Это подтверждено
регрессионными тестами и градиентной проверкой. Полезность новой политики
для прохождения игр **не показана**: Search и обученная v2 получили ноль
уровней/побед во всех пяти локальных играх при бюджете400.

Рабочие файлы ARGOS, опубликованный Space, runtime и HF не изменялись.
Все исходники, настоящие данные, checkpoint и измерения находятся здесь.

## Свежая исходная точка

27.09 в20:50–20:56 исходный `/home/argos-data/improve/arc3` уже получил
стабильные action tags и trained checkpoints. Поэтому прежние выводы
«hash(tag) ещё нестабилен» и «trainedhead отсутствует» более не актуальны.
В `reference/` сохранена точная свежая копия и SHA256 manifest.

Реальный `arc3_head_stable_route.npz`, SHA256
`12e2938d381903084b1776a9d59110f38b8fcc2dc2496d3c1e348545af40270c`:
содержит w_emb[64], w_tag[8], b. На двух разных общих embeddings ranking
совпадает; изменение попарных разностей score лишь2.22e-16 (roundoff).

Причина: `_embeds()` копирует один вектор состояния каждому кандидату;
`score_i = embedding @ w_emb + action_tag_i @ w_tag + b`. Общий первый
член сокращается при сравнении. Обучение в свежем `train_imitation.py`
по-прежнему использует dummy_features. Новая ветка `node_scores()` вызывает
head с tag `state`, который строгий action parser не принимает: для оценки
BFS-состояний нужен отдельный обученный контракт, не подмена action head.

## Исправление и API

`action_head.ActionHead` сохраняет методы `scores`, `train_step`, `save`,
`load` и `tag_onehot`. Формулаv2:

```
score(state, candidate) = state @ W_state_action @ action_features
                         + action_features @ action_bias
```

Action features: стабильный one-hot action ID, нормированные x/y и признак
наличия координат. `A6:0,32` и `A6:63,32` сохраняют разные представления.
Optional `legal_mask` исключает нелегальных кандидатов из ranking/softmax;
обучение на нелегальном teacher action отвергается. Проверяются размерности,
конечность входов/весов и диапазон координат0..63.

Checkpoint formatv2 хранит матрицу взаимодействия; старый checkpoint
**явно отвергается**, поскольку в нём отсутствуют требуемые параметры.
Никакие старые веса не выдаются за новые/обученные. Новый checkpoint получен
реальным обучением ниже. API совместим по основным методам, формат весов
намеренно несовместим. Generic head может принимать другие embeddings;
этот конкретный эксперимент использует **native pixel features, не SNN**.

`interaction_ranker.InteractionRanker` возвращает исходные candidate tuples,
сохраняет связанные с ними click data, фильтрует available_actions и применяет
тот же tabu приоритет. Это отдельный явный adapter; не скрытая замена старой
SNN policy или BFS node scoring.

## Настоящие данные и разделение

`teacher-recording/` — проверенная запись исполнения известного LS20 route:
309 действий,310 native frames,7 уровней/WIN, полученная раньше локальным SDK.
Данные здесь не подменяют живое решение. Для обучения берётся кадр **до**
действия, previous frame/action берутся только из прошлого. Loader сверяет
SHA256 артефактов, пары before/after hash, допустимость действия и размерность.

- Train: уровни1–5,184 примера.
- Withheld: уровни6–7,125 примеров. Пересечения raw frame hashes нет.
- Вход1096:8×8 spatial colour occupancy по16 цветам, доля изменённых клеток
  в8×8блоках, предыдущий action one-hot. Ни level ID, ни step ID не подаются.
- 250 epochs full-batch CPU, lr0.1, L2=0.0001, seed7. Гиперпараметры заданы
  до измерения withheld; checkpoint сохранён/захеширован до первой оценки.
- Нормализации, подбора модели или early stopping по withheld нет.

Это withheld **уровни одной известной игры**, не held-out games и не
демонстрация общего ARC solving. Шаги одной траектории коррелированы.

## Измерения

`trained-v2/report.json`, checkpoint `trained-v2/head_v2.npz`:
SHA256 `e3b2f89112d2faa0b8d49c966de975039667bae81f21b1b3b15f509fcce37177`.

| Teacher-action prediction | Train1–5 | Withheld6–7 |
|---|---:|---:|
| v2 |60.33%|50.40%|
| Train-only action-frequency prior |34.24%|32.00%|
| Повтор предыдущего действия* |55.43%|48.80%|
| Train-only Markov(previous→next)* |55.43%|48.80%|

*Последние два контроля добавлены как post-hoc diagnostics без ретрейна или
подбора checkpoint; сохранены в `trained-v2/baseline_diagnostics.json`.
Преимущество над повтором — всего2 действия из125; сильный вывод о качестве
не делается. CPU train занял0.35с на этой системе.

Живой A/B, одинаковые version/seed0/start/candidates/tabu, budget400,
checkpoint во время rollout не обновляется; route при rollout не читается:

| Игра | Search actions | v2 actions | Уровни Search/v2 | Итог |
|---|---:|---:|---:|---|
| LS20 |186|130|0/0|оба GAME_OVER|
| CD82 |100|100|0/0|оба GAME_OVER|
| VC33 |50|50|0/0|оба GAME_OVER|
| SC25 |52|240|0/0|оба GAME_OVER; v2206 unchanged actions|
| FT09 |400|400|0/0|оба NOT_FINISHED;400 unchanged actions|

Все Search counts совпали с независимым fullmatrix root baseline. Более
ранний GAME_OVER LS20 не является улучшением. SC25 показывает регрессию
повторов. Политика училась только directional actions LS20; click actions
в этом checkpoint не обучены, хотя архитектура и adapter сохраняют их.
Нулевые игровые результаты — причина оставить политику экспериментальной,
не включать её по умолчанию в Space.

## Воспроизведение

Python3.12+, `numpy==2.4.6`, `arc-agi==0.9.9`, `arcengine==0.9.3`, pytest.
Внешняя сеть для экспериментов не нужна. Protocol/assets заморожены в
`protocol/`, MIT notices игр сохранены. Новые выходные каталоги обязательны.

```sh
OPENBLAS_NUM_THREADS=1 python -m pytest tests -q
OPENBLAS_NUM_THREADS=1 python train_experiment.py \
  --recording teacher-recording --out new-training
OPENBLAS_NUM_THREADS=1 python evaluate_policies.py \
  --checkpoint new-training/head_v2.npz --out new-evaluation
```

`evaluated-v2/summary.json` и десять подпапок содержат полные action logs,
native frames, локальные scorecards, summaries, runtime и source/artifact
SHA256. Процесс использует явный OFFLINE SDK и запрет socket/DNS. Budget
до400 и проверка60с на игру; launcher окружения может дополнительно задать
общий timeout. Никакого remote SNN worker или API scoring не вызывается.

TDD: на свежем исходном head7FAIL/2PASS; после исправления10PASS. Данные и
trainer/ranker сначала дали4FAIL+4FAIL, actual-game evaluator1FAIL; затем
весь локальный suite **19PASS**. Проверены противоположные действия для
противоположных состояний, клики, legalmask, finite-difference gradient,
roundtrip/version rejection, отсутствие withheld leakage и реальные rollouts.

Следующий качественный шаг требует более разнообразных экспертных данных,
особенно кликов, и проверки кандидатов на FT09: текущий generator даёт
400 неизменивших кадр действий обеим политикам. Улучшение SNN sparse operator
и обучение на настоящих SNN embeddings — отдельная работа, здесь не заявлены.
