"""Inspect recorded neural experiments; this module does not run checkpoints."""

import hashlib
import json
from pathlib import Path
import re


DATA = Path(__file__).resolve().parent / "data" / "verification"


def _file(name):
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+\.(json|txt)", name):
        raise ValueError("Недоступный файл эксперимента")
    root = Path(DATA).resolve()
    path = (root / name).resolve()
    if path.parent != root or not path.is_file():
        raise ValueError("Файл отсутствует или находится вне verification")
    return path


def _manifest():
    manifest = json.loads(_file("manifest.json").read_text(encoding="utf-8"))
    if (manifest.get("schema_version") != 1 or
            manifest.get("evidence_kind") != "recorded_experiment_results" or
            not re.fullmatch(r"[0-9a-f]{40}", manifest.get("source_revision", "")) or
            not isinstance(manifest.get("artifacts"), dict)):
        raise ValueError("Несовместимый verification manifest")
    return manifest


def _verified(name):
    manifest = _manifest()
    if not isinstance(name, str) or name == "manifest.json" or name not in manifest["artifacts"]:
        raise ValueError("Недоступный файл эксперимента")
    path = _file(name)
    contents = path.read_bytes()
    entry = manifest["artifacts"][name]
    if hashlib.sha256(contents).hexdigest() != entry["sha256"]:
        raise ValueError(f"Не совпадает SHA256: {name}")
    return path, contents, manifest, entry


def list_experiments():
    names = sorted(_manifest()["artifacts"])
    for name in names:
        _verified(name)
    return names


def load_experiment(name):
    _, contents, manifest, entry = _verified(name)
    text = contents.decode("utf-8")
    if name.endswith(".json"):
        data = json.loads(text)
    else:
        data = []
        for line in text.splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                data.append(row)
    return {"name": name, "data": data, "raw_text": text,
            "source_revision": manifest["source_revision"],
            "sha256": entry["sha256"],
            "source_url": (f"{manifest['source_repo']}/blob/{manifest['source_revision']}/"
                           f"{entry['source_path']}"),
            "evidence_kind": "recorded_experiment_results",
            "checkpoint_validation": "not_performed"}


def raw_path(name):
    path, _, _, _ = _verified(name)
    return str(path)


def _accuracies(data):
    if not isinstance(data, dict):
        return None, None
    if "mean_test_acc" in data:
        return data["mean_test_acc"], "Reported mean test accuracy"
    results = data.get("results", {})
    for metric in ("acc", "test_acc"):
        values = {name: row[metric] for name, row in results.items()
                  if isinstance(row, dict) and metric in row}
        if values:
            return values, "Recorded accuracy" if metric == "acc" else "Recorded test accuracy"
    return None, None


def plot_experiment(name):
    from matplotlib.figure import Figure

    data = load_experiment(name)["data"]
    values, metric = _accuracies(data)
    figure = Figure(figsize=(9, 4.6), layout="constrained")
    ax = figure.subplots()
    if values:
        ax.bar(list(values), list(values.values()), color="#427cac")
        ax.set_ylim(0, 1)
        ax.set_ylabel(metric)
        ax.tick_params(axis="x", labelrotation=30)
        chance = data.get("chance", data.get("info", {}).get("chance"))
        if chance is not None:
            ax.axhline(chance, color="#a64f37", linestyle="--", label="Recorded chance baseline")
            ax.legend()
    elif isinstance(data, list) and any("modules" in row for row in data):
        for row in data:
            if "modules" in row:
                ax.plot(list(row["modules"]),
                        [module["period_s"] for module in row["modules"].values()],
                        marker="o", label=f"repeat {row['repeat']}")
        ax.set_ylabel("Recorded period, seconds")
        ax.legend()
    elif isinstance(data, list) and any("variant" in row for row in data):
        trials = [row for row in data if "variant" in row]
        for variant in dict.fromkeys(row["variant"] for row in trials):
            rows = [row for row in trials if row["variant"] == variant]
            ax.plot([row["scenario"] for row in rows],
                    [row["final_dist"] for row in rows], marker="o", label=variant)
        ax.set_xlabel("Recorded scenario")
        ax.set_ylabel("Final distance to goal, metres")
        ax.legend()
    elif isinstance(data, dict) and "angles" in data and "pops" in data:
        for population, sides in data["pops"].items():
            for side, activity in sides.items():
                ax.plot(data["angles"], activity, label=f"{population}/{side}")
        ax.set_xlabel("Angle, degrees")
        ax.set_ylabel("Recorded population activity")
        ax.legend(ncol=2)
    else:
        return None
    ax.set_title(name.removesuffix(".json").removesuffix(".txt") + " — recorded results")
    ax.grid(axis="y", alpha=0.2)
    return figure


def render_summary(name):
    record = load_experiment(name)
    data = record["data"]
    lines = [f"### {name}", "",
             "**Режим: анализ записанных результатов.** Тяжёлый эксперимент здесь не повторяется.",
             "SHA256 подтверждает целостность файла; checkpoint не проверен и не запускается.",
             "Git revision закрепляет файлы результатов, а не доказывает версию исходного вычислительного тракта.",
             f"Источник: [Git {record['source_revision']}]({record['source_url']})",
             f"SHA256: `{record['sha256']}`", ""]
    if isinstance(data, dict):
        info = data.get("info", {})
        for key in ("task", "weights", "neurons", "n_train", "n_test", "frames", "ticks"):
            value = info.get(key, data.get(key))
            if value is not None:
                lines.append(f"- {key}: {value}")
        for key in ("dataset", "source", "seed", "n_seeds", "caveat"):
            if key in data:
                lines.append(f"- {key}: {data[key]}")
        accuracies, metric = _accuracies(data)
        if accuracies:
            lines += ["", f"| Вариант | {metric} |", "|---|---:|"]
            lines += [f"| {variant} | {value} |" for variant, value in accuracies.items()]
        for key in ("fly_minus_twin", "fly_minus_best_baseline", "total_sec"):
            if key in data:
                lines.append(f"- {key}: {data[key]}")
        if "fly_minus_twin" in data and data["fly_minus_twin"] < 0:
            lines.append("В этой записи fly слабее twin; преимущество анатомического ядра не показано.")
    elif isinstance(data, list):
        trials = [row for row in data if "variant" in row]
        if trials:
            lines += ["| Scenario | Variant | Goal reached | Final distance, m |",
                      "|---|---|---|---:|"]
            lines += [f"| {row['scenario']} | {row['variant']} | {row['goal_reached']} | {row['final_dist']} |"
                      for row in trials]
        elif any("modules" in row for row in data):
            lines.append("B09 shadow: записана активность шести модулей рядом с походкой. "
                         "Это не доказательство управления телом этими модулями.")
            for row in data:
                if "repeat" in row:
                    lines.append(f"- repeat {row['repeat']}: body_x_m={row['body_x_m']}, "
                                 f"cpu_ms_per_tick_6modules={row['cpu_ms_per_tick_6modules']}")
    lines += ["", "Полная структура и исходный файл доступны ниже; отсутствующие измерения не восстановлены."]
    return "\n".join(lines)
