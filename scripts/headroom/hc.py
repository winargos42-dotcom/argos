#!/usr/bin/env python3
"""hc — Headroom Compress CLI. Читает stdin, сжимает, печатает в stdout.
Использование: <большая команда> | python scripts/headroom/hc.py
Экономит токены: большие JSON/логи/списки сжимаются на 90%+.
Ошибки и короткие выводы (< лимита) проходят без потерь (passthrough)."""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from argos_compressor import ArgosCompressor

def main():
    data = sys.stdin.read()
    if not data.strip():
        return
    r = ArgosCompressor().compress(data)
    if r.strategy == "passthrough":
        # короткий вывод — печатаем как есть, без шума
        sys.stdout.write(r.text)
    else:
        sys.stdout.write(
            f"[hc: {r.strategy}, {r.original_chars}→{r.compressed_chars} ch, "
            f"-{r.savings_pct:.0f}%]\n{r.text}\n"
        )

if __name__ == "__main__":
    main()
