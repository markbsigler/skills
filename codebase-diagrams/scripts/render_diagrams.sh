#!/usr/bin/env bash
# render_diagrams.sh — Batch render .mmd files to .png using mmdc (Mermaid CLI)
# Usage: bash render_diagrams.sh [diagram_directory]
# Default directory: docs/diagrams/

set -euo pipefail

DIAGRAM_DIR="${1:-docs/diagrams}"
WIDTH="${RENDER_WIDTH:-3200}"
HEIGHT="${RENDER_HEIGHT:-2400}"
SCALE="${RENDER_SCALE:-2}"
BG="${RENDER_BG:-white}"

# Auto-install mmdc if not available
if ! command -v mmdc &>/dev/null; then
  echo "mmdc not found. Installing @mermaid-js/mermaid-cli..."
  if command -v npm &>/dev/null; then
    npm install -g @mermaid-js/mermaid-cli
  else
    echo "ERROR: npm not found. Install Node.js first, or install mmdc manually:"
    echo "  npm install -g @mermaid-js/mermaid-cli"
    exit 1
  fi
fi

# Validate directory
if [ ! -d "$DIAGRAM_DIR" ]; then
  echo "ERROR: Directory not found: $DIAGRAM_DIR"
  exit 1
fi

# Count .mmd files
MMD_COUNT=$(find "$DIAGRAM_DIR" -maxdepth 1 -name "*.mmd" | wc -l | tr -d ' ')
if [ "$MMD_COUNT" -eq 0 ]; then
  echo "No .mmd files found in $DIAGRAM_DIR"
  exit 0
fi

echo "Rendering $MMD_COUNT diagrams from $DIAGRAM_DIR"
echo "Settings: ${WIDTH}x${HEIGHT} scale=${SCALE} bg=${BG}"
echo "---"

SUCCESS=0
FAILED=0

for f in "$DIAGRAM_DIR"/*.mmd; do
  BASENAME=$(basename "$f" .mmd)
  OUTPUT="$DIAGRAM_DIR/${BASENAME}.png"
  echo -n "  $BASENAME.mmd → .png ... "
  if mmdc -i "$f" -o "$OUTPUT" --width "$WIDTH" --height "$HEIGHT" --backgroundColor "$BG" --scale "$SCALE" 2>/dev/null; then
    SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
    echo "OK ($SIZE)"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "FAILED"
    FAILED=$((FAILED + 1))
  fi
done

echo "---"
echo "Done: $SUCCESS succeeded, $FAILED failed"
