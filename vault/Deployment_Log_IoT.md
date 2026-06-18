# ARGOS Deployment Log: Zigbee & ESP Integration
Date: 2026-05-14
Status: 🏗️ In Progress

## 🎯 Goal
Integrate Zigbee2MQTT on Orange Pi, configure two ESPs via ESPHome, and detect the Windows PC dongle.

## 🛠 Artifacts
| Artifact | Destination | Status | Notes |
|----------|-------------|--------|---------|
| `z2m-config.yaml` | Orange Pi | ⏳ Pending | Configuration for Zigbee2MQTT |
| `esp-bridge.yaml` | ESP8266 | ⏳ Pending | ESPHome config for bridge |
| `esp-display.yaml` | ESP32 | ⏳ Pending | ESPHome config for display |
| `win-dongle-check.ps1` | Windows PC | ⏳ Pending | Detection script |
| `deploy-op.sh` | Orange Pi | ⏳ Pending | Bash script for local execution |

## 📝 Execution Steps
1. [x] Generate Z2M config based on detected USB dongle.
2. [x] Generate ESPHome YAMLs for the 2 nodes.
3. [x] Create a deployment bundle for the user to run on Orange Pi.
4. [x] Provide instructions for Windows dongle detection.
5. [ ] Verify P2P connectivity after deployment.
6. [x] Prepare mini-tron-50 GGUF pipeline.

