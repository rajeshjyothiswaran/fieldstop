#!/usr/bin/env bash
# Fieldstop deploy — syncs the version across the app + service worker,
# snapshots a copy into releases/, then commits and pushes to GitHub Pages.
#
#   ./deploy.sh            → deploy at the current version
#   ./deploy.sh 1.1.0      → set a new version, then deploy
#
set -euo pipefail
cd "$(dirname "$0")"

read_html_version() { grep -oE 'fieldstop-version" content="[0-9]+\.[0-9]+\.[0-9]+"' fieldstop.html | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'; }
read_sw_version()   { grep -oE "VERSION = '[0-9]+\.[0-9]+\.[0-9]+'" fieldstop-sw.js | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'; }

CURRENT="$(read_html_version)"
VERSION="${1:-$CURRENT}"

# sed -i syntax differs on macOS (BSD) vs Linux (GNU)
if sed --version >/dev/null 2>&1; then SEDI=(sed -i); else SEDI=(sed -i ''); fi

# Write the version into both files (single source of truth = the html meta)
"${SEDI[@]}" -E "s/(fieldstop-version\" content=\")[0-9.]+(\")/\1${VERSION}\2/" fieldstop.html
"${SEDI[@]}" -E "s/(VERSION = ')[0-9.]+(')/\1${VERSION}\2/" fieldstop-sw.js

# Parity gate — refuse to deploy if the two ever disagree
HV="$(read_html_version)"; SV="$(read_sw_version)"
if [ "$HV" != "$SV" ]; then
  echo "✗ Version parity failed: fieldstop.html=$HV  fieldstop-sw.js=$SV"; exit 1
fi
echo "✓ Version $VERSION  (app + service worker in parity)"

# Snapshot the deployable site into releases/ (local archive, gitignored)
DEST="releases/v$VERSION"
rm -rf "$DEST"; mkdir -p "$DEST"
rsync -a --exclude 'releases' --exclude '.git' --exclude 'build' --exclude 'deploy.sh' ./ "$DEST"/ >/dev/null
echo "✓ Snapshot copied to $DEST/"

# Commit + push
git add -A
if git diff --cached --quiet; then
  echo "• Nothing changed to commit — pushing anyway in case of unpushed commits."
else
  git commit -m "Deploy Fieldstop v$VERSION"
fi
git push
echo "✓ Pushed. Live at https://fieldstop.app/  (GitHub Pages rebuilds in ~1 min)"
echo "  On your phone, open the app twice so the service worker swaps to v$VERSION."
