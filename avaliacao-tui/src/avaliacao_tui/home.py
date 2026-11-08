"""Tela inicial (welcome / splash) do avaliacao-tui.

Mostra um ASCII art "SENAI" com gradiente arco-íris + subtítulo.
Qualquer tecla (exceto q) avança para o painel principal.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static


# === ASCII art "PROF. LUCAS" (fonte ansi_shadow via pyfiglet, hardcoded) ===
# Gerado uma vez e embutido — assim o app não precisa de pyfiglet em runtime.
PROF_LUCAS_ART = """\
██████╗ ██████╗  ██████╗ ███████╗    ██╗     ██╗   ██╗ ██████╗ █████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝    ██║     ██║   ██║██╔════╝██╔══██╗██╔════╝
██████╔╝██████╔╝██║   ██║█████╗      ██║     ██║   ██║██║     ███████║███████╗
██╔═══╝ ██╔══██╗██║   ██║██╔══╝      ██║     ██║   ██║██║     ██╔══██║╚════██║
██║     ██║  ██║╚██████╔╝██║  ██╗    ███████╗╚██████╔╝╚██████╗██║  ██║███████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝"""


# Paleta do arco-íris (6 cores — Rich aceita nomes padrão)
RAINBOW = ("red", "yellow", "green", "cyan", "blue", "magenta")


def rainbow_lines(text: str) -> str:
    """Aplica **uma cor por linha**, ciclando o arco-íris.

    Por que por linha e não por caractere? Porque markup por caractere
    (`[red]X[/red][yellow]Y[/yellow]...`) faz o Textual quebrar o
    alinhamento da arte ASCII (cada char vira uma "fatia" e o
    desenho fica ilegível). Pintar a linha inteira mantém o
    alinhamento perfeito.
    """
    out: list[str] = []
    for i, line in enumerate(text.split("\n")):
        color = RAINBOW[i % len(RAINBOW)]
        out.append(f"[{color}]{line}[/{color}]")
    return "\n".join(out)


class HomeScreen(Screen):
    """Tela de boas-vindas. Qualquer tecla → vai para o MainScreen."""

    DEFAULT_CSS = """
    HomeScreen {
        align: center middle;
        background: $surface;
    }

    #home-stack {
        align: center middle;
        width: auto;
        height: auto;
    }

    #ascii-art {
        content-align: center middle;
        width: 80;
        height: auto;
        text-style: bold;
    }

    #subtitle {
        margin-top: 2;
        content-align: center middle;
        width: 100%;
        color: $accent;
        text-style: bold;
    }

    #prompt {
        margin-top: 3;
        content-align: center middle;
        width: 100%;
        color: $secondary;
    }

    #hint {
        margin-top: 1;
        content-align: center middle;
        width: 100%;
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("q", "app.quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="home-stack"):
            # ASCII art "PROF. LUCAS" em arco-íris (1 cor por linha)
            yield Static(rainbow_lines(PROF_LUCAS_ART), id="ascii-art", markup=True)
            yield Static(
                "Avaliação  —  Parte 2  (Implantação de Sistemas)",
                id="subtitle",
            )
            yield Static(
                "[bold]Pressione qualquer tecla para continuar[/bold]",
                id="prompt",
                markup=True,
            )
            yield Static(
                "[dim]q  sair  ·  Enter / Space / Esc  começar[/dim]",
                id="hint",
                markup=True,
            )

    def on_key(self, event) -> None:
        # Qualquer tecla que não seja 'q' (que está em BINDINGS) avança.
        # q já é tratada pela binding acima → sai do app.
        if event.key == "q":
            return
        # Empilha o painel principal por cima. MainScreen.quit() via 'q'
        # encerra o app inteiro (limpa a pilha).
        self.app.push_screen("main")
