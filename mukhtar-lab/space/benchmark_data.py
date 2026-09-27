"""Read a complete schema 2 benchmark snapshot and verify its recorded hashes."""

import hashlib
import json
from pathlib import Path


class BenchmarkData:
    def __init__(self, root):
        self.root = Path(root).resolve()
        manifest_bytes = self._path("manifest.json").read_bytes()
        self.manifest = json.loads(manifest_bytes)
        if (self.manifest.get("schema_version") != 2 or
                self.manifest.get("status") != "complete"):
            raise ValueError("Нужен complete manifest schema 2")
        source_files = self.manifest.get("source_files")
        if not isinstance(source_files, dict) or not source_files:
            raise ValueError("Manifest не содержит source_files")
        source_digest = hashlib.sha256(json.dumps(
            source_files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if source_digest != self.manifest.get("source_sha256"):
            raise ValueError("Не совпадает source_sha256 в manifest")
        artifacts = self.manifest.get("artifacts")
        if not isinstance(artifacts, dict) or "summary.json" not in artifacts:
            raise ValueError("Manifest не содержит summary.json")
        self._raw = {"manifest.json": manifest_bytes.decode("utf-8")}
        for name, expected in artifacts.items():
            if name == "manifest.json":
                raise ValueError("Manifest не может включать собственный хэш")
            contents = self._path(name).read_bytes()
            if hashlib.sha256(contents).hexdigest() != expected:
                raise ValueError(f"Не совпадает SHA256: {name}")
            self._raw[name] = contents.decode("utf-8")
        self.summary = json.loads(self._raw["summary.json"])
        if self.summary.get("schema_version") != 2:
            raise ValueError("Нужен summary schema 2")
        results = self.summary.get("results")
        if not isinstance(results, list) or not results:
            raise ValueError("Summary не содержит результатов")
        self._results = {}
        for row in results:
            if row.get("metrics_schema_version") != 2:
                raise ValueError("Нужны метрики schema 2")
            key = (row["bench_id"], row["controller"])
            if key in self._results:
                raise ValueError("Повтор сценария/контроллера в summary")
            if (row["events_file"] not in artifacts or
                    row["model_file"] not in artifacts or
                    row["model_sha256"] != artifacts[row["model_file"]]):
                raise ValueError("Файлы прогона не совпадают с manifest")
            self._results[key] = row

    def _path(self, name):
        if (not isinstance(name, str) or not name or
                Path(name).name != name or "\\" in name or
                Path(name).suffix not in (".json", ".jsonl", ".xml")):
            raise ValueError("Недопустимое имя файла")
        path = (self.root / name).resolve()
        if path.parent != self.root or not path.is_file():
            raise ValueError(f"Файл отсутствует или находится вне schema2: {name}")
        return path

    @property
    def raw_files(self):
        return sorted(self._raw)

    def read_raw(self, name):
        if not isinstance(name, str) or name not in self._raw:
            raise ValueError("Недоступный файл: выберите файл из списка schema 2")
        return self._raw[name]

    def result(self, scenario, controller):
        return self._results.get((scenario, controller))

    def events(self, scenario, controller):
        row = self.result(scenario, controller)
        if row is None:
            return []
        return [json.loads(line) for line in self.read_raw(row["events_file"]).splitlines()
                if line.strip()]
