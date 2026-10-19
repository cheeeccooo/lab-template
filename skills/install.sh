#!/bin/sh
# Collega le skill lab* tra le skill utente di Claude Code (~/.claude/skills).
# Sono collegamenti, non copie: le modifiche fatte qui valgono subito.
set -e
src="$(cd "$(dirname "$0")" && pwd)"
dst="$HOME/.claude/skills"
mkdir -p "$dst"
for d in "$src"/lab*/; do
    name="$(basename "$d")"
    if [ -e "$dst/$name" ] && [ ! -L "$dst/$name" ]; then
        echo "salto $name: in $dst esiste già una cartella vera con questo nome"
        continue
    fi
    ln -sfn "${d%/}" "$dst/$name"
    echo "collegata $name"
done
