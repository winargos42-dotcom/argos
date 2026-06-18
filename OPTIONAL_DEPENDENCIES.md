# Optional Dependencies for ARGOS

This document lists optional dependencies that can enhance ARGOS functionality but are not required for basic operation.

## Currently Missing Optional Modules

The following optional modules are not currently installed but can be added to enhance specific functionalities:

### 1. ChromaDB
- **Purpose**: Vector database for enhanced memory and similarity search
- **Installation**: `pip install chromadb`
- **Benefits**: Improved memory retrieval, semantic search capabilities

### 2. Sentence Transformers
- **Purpose**: For generating sentence embeddings
- **Installation**: `pip install sentence-transformers`
- **Benefits**: Better semantic understanding, improved similarity comparisons

### 3. Faster Whisper
- **Purpose**: Efficient speech-to-text transcription
- **Installation**: `pip install faster-whisper`
- **Benefits**: Faster and more accurate speech processing

## How These Integrate with ARGOS

ARGOS is designed to handle missing optional dependencies gracefully. When an optional module is not available:
- The system continues to function with reduced capabilities
- Alternative methods or fallbacks are used where possible
- No critical functionality is lost

To check if these modules are available in your installation, you can use:
```python
try:
    import chromadb
    print("ChromaDB: Available")
except ImportError:
    print("ChromaDB: Not installed")

try:
    import sentence_transformers
    print("Sentence Transformers: Available")
except ImportError:
    print("Sentence Transformers: Not installed")

try:
    import faster_whisper
    print("Faster Whisper: Available")
except ImportError:
    print("Faster Whisper: Not installed")
```

## Recommendations

For users who want to enhance their ARGOS experience:
1. Install ChromaDB for improved memory functions
2. Install Sentence Transformers for better semantic processing
3. Install Faster Whisper for improved speech-to-text capabilities

These installations are optional and can be done incrementally based on specific needs.