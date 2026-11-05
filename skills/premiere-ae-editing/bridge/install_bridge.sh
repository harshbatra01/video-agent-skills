#!/bin/zsh
# Installs the Edit Bridge: a hidden Premiere Pro panel (CEP extension) that runs ExtendScript sent by
# scripts/premiere/pp.py. It listens on 127.0.0.1 only (port 47915 in Premiere 2026, 47916 in Premiere 2025), needs a
# secret token from ~/.editbridge_token on every request, and refuses requests that carry a browser Origin header.
#
# What this script changes on the Mac (ask the user before running it):
#   1. copies com.local.editbridge into ~/Library/Application Support/Adobe/CEP/extensions/
#   2. writes a new random token to ~/.editbridge_token (chmod 600) if that file does not exist yet
#   3. sets PlayerDebugMode = 1 for CSXS 10, 11 and 12, the Adobe preference that lets unsigned panels load.
#      Premiere 2025 and 2026 use CSXS 12; 10 and 11 only matter for older Adobe apps. The setting lets ANY unsigned
#      panel in the extensions folder load in those apps, not only this one.
# Premiere only discovers panels when it launches, so restart Premiere afterwards (after the user has saved their work).
#
# Undo by hand (ask the user first):
#   rm -rf ~/Library/Application\ Support/Adobe/CEP/extensions/com.local.editbridge
#   rm ~/.editbridge_token
#   defaults delete com.adobe.CSXS.12 PlayerDebugMode   (same for .10 and .11; keep it if other unsigned panels need it)
#
# usage: zsh install_bridge.sh            (asks before changing anything)
#        zsh install_bridge.sh --yes      (no question)
set -e
HERE="${0:A:h}"
NAME="com.local.editbridge"
DEST="$HOME/Library/Application Support/Adobe/CEP/extensions"
TOKEN="$HOME/.editbridge_token"

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This installer is for macOS. On Windows the extensions folder is %APPDATA%\\Adobe\\CEP\\extensions and"
  echo "PlayerDebugMode lives in the registry under HKEY_CURRENT_USER\\Software\\Adobe\\CSXS.<n>."
  exit 1
fi

if [[ "$1" != "--yes" ]]; then
  echo "This will copy the Edit Bridge panel into $DEST,"
  echo "create $TOKEN if it is missing, and set Adobe's PlayerDebugMode for CSXS 10-12."
  read "ok?Continue? [y/N] "
  [[ "$ok" == [yY]* ]] || { echo "Nothing changed."; exit 0; }
fi

mkdir -p "$DEST"
rm -rf "$DEST/$NAME"
cp -R "$HERE/$NAME" "$DEST/"
echo "copied the panel to $DEST/$NAME"

if [[ ! -s "$TOKEN" ]]; then
  ( umask 077; LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 40 > "$TOKEN" )
  chmod 600 "$TOKEN"
  echo "wrote a new token to $TOKEN (keep it private; never print it)"
else
  echo "kept the existing token in $TOKEN"
fi

for n in 10 11 12; do
  defaults write "com.adobe.CSXS.$n" PlayerDebugMode 1
done
echo "PlayerDebugMode = 1 for CSXS 10, 11, 12"

# another bridge panel on the same ports (an older copy under another name) would clash: warn, change nothing
for d in "$DEST"/*(N/); do
  if [[ "${d:t}" == "$NAME" ]]; then continue; fi
  if [[ -f "$d/main.js" ]] && grep -q "47915" "$d/main.js"; then
    echo "NOTE: ${d:t} also listens on port 47915/47916. Two bridges cannot run at once: remove one."
  fi
done

echo ""
echo "Done. Quit and reopen Premiere Pro (2025 or 2026), then test with:"
echo "  ~/.venvs/premiere-ae/bin/python <skill>/scripts/premiere/pp.py --v 2026 --status"
