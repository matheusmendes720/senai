@echo off
REM start.bat — Avaliacao TUI (Windows)
REM Tenta uv primeiro (rapido), depois pip --user como fallback.

cd /d "%~dp0"

where uv >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [start] usando uv...
    uv run --with textual python -m avaliacao_tui.tui
    exit /b %ERRORLEVEL%
)

echo [start] uv nao encontrado; usando pip --user...
python -m pip install --user --quiet textual 2>nul
if errorlevel 1 (
    echo [start] pip falhou; tentando criar venv local...
    if not exist .venv (
        python -m venv .venv
    )
    .venv\Scripts\python -m pip install --quiet textual
    .venv\Scripts\python -m avaliacao_tui.tui
) else (
    python -m avaliacao_tui.tui
)
