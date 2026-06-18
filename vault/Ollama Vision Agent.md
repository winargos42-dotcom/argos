# Ollama Vision Agent

## Identity
- **Name**: Ollama Vision
- **Type**: Vision / Image Analysis Entity
- **Model**: llava:7b (pulling to PC)
- **Status**: 🔄 Pulling (llava:7b → 192.168.1.66)
- **Host**: http://192.168.1.66:11434

## Capabilities
- Screenshot analysis
- Image description and OCR
- Visual question answering
- Camera/webcam input processing

## Configuration
```env
OLLAMA_HOST=http://192.168.1.66:11434
OLLAMA_VISION_MODEL=llava:7b
```

## Integration
- `ArgosVision` → `OllamaVisionBridge`
- Commands: "что на экране?", "опиши фото", "смотри камеру"

---
#autogpt #vision #ollama #agent
