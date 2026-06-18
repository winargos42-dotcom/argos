# 2026-05-13 Andrax v5 + AI/ML Arsenal — Full Install

## 📱 Redmi Note 8T (Termux)

### Andrax v5 — Pentest Platform
- **Installer**: `andrax_installer.sh` pushed to `/sdcard/Download/`
- **Source**: https://raw.githubusercontent.com/Kirozaku/Andrax-Termux/refs/heads/main/install-andrax.sh
- **Manual steps on phone**:
  ```bash
  cp /sdcard/Download/andrax_installer.sh ~
  bash ~/andrax_installer.sh
  # Choose option 2 (Download & Install)
  # After: ./andrax.sh
  ```

### AI/ML Python (Termux arm64)
- **Installer**: `ai-termux-install.sh` pushed to `/sdcard/Download/`
- **Limitations**: PyTorch/TensorFlow на Android arm64 ограничены
  - `torch` — возможен через CPU wheel (ограниченная производительность)
  - `tensorflow` — `tflite-runtime` вместо полного TF
  - `xgboost`, `lightgbm` — компилируются из исходников (долго)
- **Core packages** (устанавливаются надёжно):
  - `numpy pandas scipy scikit-learn pillow requests`
  - `transformers langchain llama-index openai anthropic`
  - `spacy nltk`
  - `opencv-python-headless ultralytics`

### ARGOS System Module
- **Path**: `firmwares/redmi-note-8t/argos-system-module/`
- **Status**: ZIP собран, требуется push + reboot
- **Post-install**: `/system/xbin/argos-*` станут доступны

```bash
# PC: install Argos system module
./scripts/install_argos_system.sh
```

---

## 💻 Laptop (Arch Linux)

### Python Environment
- **pyenv**: Python 3.12.9 установлен
- **venv**: `~/.venv-argos-py312` создан
- **Системный Python**: 3.14.4 (слишком свежий для torch/tensorflow)

### Background Install
- **PID**: `108323`
- **Log**: `tail -f /tmp/argos_ai_install_nohup.log`
- **Script**: `scripts/install_all_ai_nohup.sh` (retry logic)

### Установлено
| Пакет | Статус |
|-------|--------|
| numpy | ✅ v2.4.4 |
| pandas | ✅ v3.0.3 |
| scipy | ✅ v1.17.1 |
| scikit-learn | ✅ v1.8.0 |
| pillow | ✅ v12.2.0 |
| requests | ✅ v2.34.0 |
| waydroid | ✅ v1.6.2 |
| lxc | ✅ v1:7.0.0 |
| libgbinder | ✅ v1.1.45 |

### В процессе установки (background)
- `torch torchvision torchaudio` — wheels ~800MB
- `tensorflow keras` — wheels ~500MB
- `xgboost lightgbm catboost` — компиляция/
- `transformers langchain llama-index`
- `openai anthropic`
- `spacy nltk`
- `opencv-python ultralytics`
- `fastapi uvicorn gradio streamlit`
- `chromadb qdrant-client`
- `jupyterlab notebook`

### System packages
- **waydroid** ✅ (LineageOS image downloading)
- **lxc** ✅
- **dnsmasq** ✅ уже был

---

## 📁 Новые скрипты

```
firmwares/redmi-note-8t/scripts/
├── install_ai_pacman.sh              ← Laptop pacman/yay installer
├── install_andrax_ai_termux.sh        ← Phone Andrax + AI installer
├── install_argos_system.sh           ← Phone system-level Argos module
├── install_all_ai_nohup.sh           ← Laptop background pip install
├── redmi8t-tool.sh v2.0             ← ROOT commands (dd_backup, frida, app_dump)
├── mobile_manager.sh v2.0             ← ADB WiFi manager (root_shell, partition_dump)
└── termux-multitool-bootstrap.sh v2.0 ← Full Termux bootstrap

firmwares/redmi-note-8t/argos-system-module/
├── module.prop
├── post-fs-data.sh                    ← USB/CAN permissions
├── service.sh                         ← Auto-start services
└── system/xbin/
    ├── argos-status                   ← System diagnostic
    ├── argos-usb-setup                ← USB permissions fix
    ├── argos-can-up                   ← CAN interface bring-up
    └── argos-bridge                   ← ARGOS bridge launcher
```

---

## 🔧 Команды для проверки

**Phone (ADB WiFi):**
```bash
./mobile_manager.sh status
./mobile_manager.sh shell "su -c 'argos-status'"
./redmi8t-tool.sh root_info
```

**Laptop:**
```bash
tail -f /tmp/argos_ai_install_nohup.log  # watch progress
source ~/.venv-argos-py312/bin/activate
python -c "import numpy, pandas, sklearn; print('OK')"
```

## Связи
- [[Redmi Note 8T Analysis + Multi-Tool]]
- [[Redmi Note 8T Mobile Toolkit]]
- [[USB Arsenal MAX Setup]]
- [[ARGOS]]

[[Backbone Hub]]
