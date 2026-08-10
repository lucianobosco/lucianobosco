#!/usr/bin/env bash
# Choose which design is live on the profile.
#
#   ./switch.sh                 list the designs
#   ./switch.sh terminal        make designs/terminal the live one
#
# It copies that design's SVG to the repo root and rewrites README.md, so the profile
# always renders one design while every design stays in the repo.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

if [ $# -eq 0 ]; then
  echo "Designs available:"
  for d in designs/*/; do
    name=$(basename "$d")
    [ -f "$d/terminal.svg" ] || continue
    live=""
    cmp -s "$d/terminal.svg" terminal.svg 2>/dev/null && live="   <- live"
    size=$(du -h "$d/terminal.svg" | cut -f1)
    echo "  $name  ($size)$live"
  done
  echo
  echo "Concepts not built yet: designs/concepts/*.md"
  exit 0
fi

DESIGN="$1"
[ -f "designs/$DESIGN/terminal.svg" ] || { echo "No such design: designs/$DESIGN"; exit 1; }

cp "designs/$DESIGN/terminal.svg" terminal.svg
sed -i "s|<!-- design: .* -->|<!-- design: $DESIGN -->|" README.md
echo "Live design is now '$DESIGN'. Commit terminal.svg and README.md to publish it."
