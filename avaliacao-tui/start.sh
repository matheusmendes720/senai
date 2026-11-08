#!/usr/bin/env bash
# start.sh — Avaliacao TUI (Git Bash / WSL / Linux / Mac)

set -e
cd "$(dirname "$0")"

if command -v uv >/dev/null 2>&1; then
    echo "[start] usando uv..."
    exec uv run --with textual python -m avaliacao_tui.tui
fi

if command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi

echo "[start] uv nao encontrado; usando pip --user..."
$PY -m pip install --user --quiet textual 2>/dev/null || {
    echo "[start] pip --user falhou; tentando venv local..."
    if [ ! -d .venv ]; then $PY -m venv .venv; fi
    if [ -f .venv/bin/activate ]; then
        # shellcheck disable=SC1091
        . .venv/bin/activate
    fi
    $PY -m pip install --quiet textual
}
exec $PY -m avaliacao_tui.tui
