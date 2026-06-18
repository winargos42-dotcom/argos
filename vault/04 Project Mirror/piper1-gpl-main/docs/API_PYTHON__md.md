---
argos_import: project_file
source_path: piper1-gpl-main/docs/API_PYTHON.md
source_abs: F:\debug\argoss\piper1-gpl-main\docs\API_PYTHON.md
source_ext: .md
source_sha256: 734acd1cbcbb971c03746d818e91baef1d0a540fee2c462d1be3a50ef4ed8bde
text_sha256: 734acd1cbcbb971c03746d818e91baef1d0a540fee2c462d1be3a50ef4ed8bde
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:26
---

# API_PYTHON.md

- Source: `piper1-gpl-main/docs/API_PYTHON.md`
- Extract: `text`
- SHA256: `734acd1cbcbb971c03746d818e91baef1d0a540fee2c462d1be3a50ef4ed8bde`

## Content

# 🐍 Python API

Install with:

``` sh
pip install piper-tts
```

Download a voice, for example:

``` sh
python3 -m piper.download_voices en_US-lessac-medium
```

Use `PiperVoice.synthesize_wav`:

``` python
import wave
from piper import PiperVoice

voice = PiperVoice.load("/path/to/en_US-lessac-medium.onnx")
with wave.open("test.wav", "wb") as wav_file:
    voice.synthesize_wav("Welcome to the world of speech synthesis!", wav_file)
```

Adjust synthesis:

``` python
syn_config = SynthesisConfig(
    volume=0.5,  # half as loud
    length_scale=2.0,  # twice as slow
    noise_scale=1.0,  # more audio variation
    noise_w_scale=1.0,  # more speaking variation
    normalize_audio=False, # use raw audio from voice
)

voice.synthesize_wav(..., syn_config=syn_config)
```

To use CUDA for GPU acceleration:

``` python
voice = PiperVoice.load(..., use_cuda=True)
```

This requires the `onnxruntime-gpu` package to be installed.

For streaming, use `PiperVoice.synthesize`:

``` python
for chunk in voice.synthesize("..."):
    set_audio_format(chunk.sample_rate, chunk.sample_width, chunk.sample_channels)
    write_raw_data(chunk.audio_int16_bytes)
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
