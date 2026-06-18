#!/bin/bash
# Install obsidian-spaced-repetition plugin into ARGOS vault
# Usage: bash argos_install_spaced_repetition.sh

set -euo pipefail

VAULT="/home/ava/Projects/argoss/vault"
PLUGINS="$VAULT/.obsidian/plugins"
PLUGIN_ID="obsidian-spaced-repetition"

echo "=== ARGOS Spaced Repetition Installer ==="

mkdir -p "$PLUGINS/$PLUGIN_ID"

cd /tmp
# Download latest release assets
RELEASE=$(curl -s https://api.github.com/repos/st3v3nmw/$PLUGIN_ID/releases/latest | grep '"tag_name":' | head -n1 | sed 's/.*"v\([^"]*\)".*/\1/')
echo "Latest release: v$RELEASE"

for file in main.js manifest.json styles.css; do
    curl -sL "https://github.com/st3v3nmw/$PLUGIN_ID/releases/download/v$RELEASE/$file" \
        -o "$PLUGINS/$PLUGIN_ID/$file"
    echo "  ↓ $file"
done

echo "✅ Plugin installed to $PLUGINS/$PLUGIN_ID"
echo ""
echo "Next steps in Obsidian:"
echo "  1. Restart Obsidian (Ctrl+R)"
echo "  2. Settings → Community plugins → Enable 'Spaced Repetition'"
echo "  3. Settings → Spaced Repetition → set tag: #flashcards"
echo ""
echo "Quick test: create a note with:"
echo '    2+2 :: 4'
echo '    #flashcards'
