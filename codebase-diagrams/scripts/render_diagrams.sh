#!/usr/bin/env bash
# render_diagrams.sh — Batch render .mmd files to .png using the Mermaid CLI (mmdc)
set -euo pipefail

# Pinned so renders stay reproducible when mmdc is not installed and npx fetches it.
MERMAID_CLI_VERSION="11.12.0"

usage() {
  cat <<EOF
Usage: render_diagrams.sh [-h|--help] [diagram_directory]

Render every .mmd file in diagram_directory (default: docs/diagrams) to a .png
next to it. Uses mmdc if installed, otherwise runs @mermaid-js/mermaid-cli@${MERMAID_CLI_VERSION}
through npx (no global install).

Environment overrides: RENDER_WIDTH (3200), RENDER_HEIGHT (2400), RENDER_SCALE (2),
RENDER_BG (white).

Exit codes:
  0  all diagrams rendered
  1  one or more diagrams failed to render (the mmdc error is printed)
  2  bad usage, missing directory, no .mmd files, or neither mmdc nor npx available
EOF
}

case "${1:-}" in
  -h | --help)
    usage
    exit 0
    ;;
esac

DIAGRAM_DIR="${1:-docs/diagrams}"
WIDTH="${RENDER_WIDTH:-3200}"
HEIGHT="${RENDER_HEIGHT:-2400}"
SCALE="${RENDER_SCALE:-2}"
BG="${RENDER_BG:-white}"

if command -v mmdc &>/dev/null; then
  MMDC=(mmdc)
elif command -v npx &>/dev/null; then
  MMDC=(npx --yes "@mermaid-js/mermaid-cli@${MERMAID_CLI_VERSION}")
else
  echo "error: need mmdc or Node.js (npx). Install Node.js 18+, or run: npm install -g @mermaid-js/mermaid-cli" >&2
  exit 2
fi

if [ ! -d "$DIAGRAM_DIR" ]; then
  echo "error: directory not found: $DIAGRAM_DIR" >&2
  exit 2
fi

shopt -s nullglob
FILES=("$DIAGRAM_DIR"/*.mmd)
if [ "${#FILES[@]}" -eq 0 ]; then
  echo "error: no .mmd files found in $DIAGRAM_DIR" >&2
  exit 2
fi

echo "Rendering ${#FILES[@]} diagrams from $DIAGRAM_DIR (${WIDTH}x${HEIGHT}, scale ${SCALE}, bg ${BG})"

SUCCESS=0
FAILED=0

for f in "${FILES[@]}"; do
  BASENAME=$(basename "$f" .mmd)
  OUTPUT="$DIAGRAM_DIR/${BASENAME}.png"
  if ERR=$("${MMDC[@]}" -i "$f" -o "$OUTPUT" --width "$WIDTH" --height "$HEIGHT" \
    --backgroundColor "$BG" --scale "$SCALE" 2>&1); then
    echo "  ok      ${BASENAME}.mmd"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "  FAILED  ${BASENAME}.mmd" >&2
    echo "$ERR" | head -n 8 | sed 's/^/          /' >&2
    FAILED=$((FAILED + 1))
  fi
done

echo "Done: $SUCCESS succeeded, $FAILED failed"
[ "$FAILED" -eq 0 ]
