"""TUI interativa — Avaliação Parte 2 (Implantação de Sistemas).

Compila e executa os 10 programas em C da avaliação, com mouse e atalhos de teclado.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    RichLog,
    Static,
)
from textual import events, on

from avaliacao_tui.exercicios import (
    EXERCICIOS, EXERCICIOS_DIR, BIN_DIR, exe_path, script_path,
)
from avaliacao_tui.home import HomeScreen


# ---------- Localizador de compilador C ----------

# Ordem: gcc (PATH) → tcc (PATH) → candidatos comuns do Windows
CANDIDATE_COMPILERS: list[tuple[str, str | None]] = [
    # (label, exe_path) — None = descobrir via PATH
    ("gcc",  None),
    ("tcc",  None),
    ("cc",   None),
    ("clang",None),
    # caminhos fixos comuns do Windows
    ("gcc (MSYS2 UCRT64)",   r"C:\msys64\ucrt64\bin\gcc.exe"),
    ("gcc (MSYS2 MinGW64)",  r"C:\msys64\mingw64\bin\gcc.exe"),
    ("gcc (MSYS2 MinGW32)",  r"C:\msys64\mingw32\bin\gcc.exe"),
    ("gcc (Dev-C++)",        r"C:\Program Files (x86)\Dev-Cpp\MinGW64\bin\gcc.exe"),
    ("gcc (Code::Blocks)",   r"C:\Program Files\CodeBlocks\MinGW\bin\gcc.exe"),
    ("gcc (TDM)",            r"C:\TDM-GCC-64\bin\gcc.exe"),
    ("gcc (MinGW)",          r"C:\MinGW\bin\gcc.exe"),
    ("tcc (scoop)",          r"C:\Users\mathe\scoop\apps\tcc\current\tcc.exe"),
]


def find_compiler() -> Optional[tuple[str, str]]:
    """Retorna (label, caminho) do compilador C encontrado, ou None.

    Ordem de preferência: gcc → tcc → cc → clang → candidatos fixos.
    """
    for label, path in CANDIDATE_COMPILERS:
        if path is None:
            exe = shutil.which(label)
            if exe:
                return (label, exe)
        elif Path(path).is_file():
            return (label, path)
    return None


# ---------- Item da lista ----------

class ExerciseItem(ListItem):
    def __init__(self, num: str, nome: str) -> None:
        super().__init__(Label(f"  [{num}]  {nome}"))
        self.num = num


# ---------- Atalhos do painel ----------

#: Teclas que o painel trata como atalho no modo navegação.
SHORTCUT_KEYS = frozenset("q r n p 0 1 2 3 4 5 6 7 8 9".split())

#: Caracteres correspondentes às teclas de atalho de um só carácter.
SHORTCUT_CHARS = frozenset(key for key in SHORTCUT_KEYS if len(key) == 1)


class StdinInput(Input):
    """Campo de stdin que não engole os atalhos do ecrã.

    O `Input` do Textual captura todas as teclas imprimíveis
    (`event.stop()` em `Input._on_key`) e, por isso, as teclas `r`/`n`/`p`/
    `0-9`/`q` nunca chegavam ao `Screen` — o `Screen` é que tem as `BINDINGS`
    do painel. Com o campo focado, `r` virava texto no campo em vez de
    arrancar o exercício.

    Aqui o campo tem dois modos, alternados com `Tab`:

    - **navegação** (default): as teclas de atalho não são escritas no campo
      e sobem até ao `Screen`, que as executa como atalhos;
    - **escrita**: todas as teclas imprimíveis vão para o `stdin` do programa
      (é o que o exercício 06 — "s/n" — e o 10 — senha — precisam).
    """

    def _painel(self) -> "MainScreen":
        return cast("MainScreen", self.screen)

    def _em_navegacao(self) -> bool:
        return not bool(getattr(self.screen, "typing_mode", False))

    def check_consume_key(self, key: str, character: str | None) -> bool:
        # Em modo navegação o `Screen` precisa destas teclas no seu binding
        # chain: se o `Input` as captura, o `Screen` nunca chega a vê-las.
        if self._em_navegacao() and key in SHORTCUT_KEYS:
            return False
        return super().check_consume_key(key, character)

    async def _on_key(self, event: events.Key) -> None:
        if event.key == "tab":
            # Tab alterna entre navegação e escrita.
            event.prevent_default()
            event.stop()
            self._painel().action_toggle_typing()
            return
        if (
            self._em_navegacao()
            and event.is_printable
            and event.character is not None
            and event.character in SHORTCUT_CHARS
        ):
            # Não escreve no campo: deixa a tecla subir até ao `Screen`.
            event.prevent_default()
            return
        await super()._on_key(event)

    def on_blur(self, event: events.Blur) -> None:
        # O modo escrita só faz sentido com o campo focado — se o foco sai
        # daqui (o programa acabou, o professor trocou de exercício), volta
        # ao modo navegação para as teclas voltarem a ser atalhos.
        painel = self._painel()
        if painel.typing_mode:
            painel.typing_mode = False
            painel._refresh_status()


# ---------- App principal ----------

class MainScreen(Screen):
    """Painel principal: lista de exercícios + descrição + output + input."""

    CSS = """
    Screen { layout: vertical; background: $surface; }

    #main { height: 1fr; }

    #sidebar {
        width: 38%;
        min-width: 28;
        border: round $accent;
        padding: 0 1;
    }
    #sidebar-title {
        height: 1;
        padding: 0 1;
        background: $accent;
        color: $text;
        text-style: bold;
    }

    #content {
        width: 1fr;
        border: round $primary;
        padding: 0 1;
    }
    #description {
        height: auto;
        padding: 1;
        background: $boost;
        margin-bottom: 1;
    }
    #status {
        height: 1;
        padding: 0 1;
        color: $secondary;
    }
    #output {
        height: 1fr;
        min-height: 8;
        border: solid $secondary;
        background: $surface-darken-1;
    }
    #input-row {
        height: 3;
        margin-top: 1;
    }
    #stdin {
        height: 3;
    }

    ListView > ListItem {
        padding: 0 1;
    }
    ListView > ListItem.--highlight {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    """

    BINDINGS = [
        Binding("q", "app.quit", "Sair"),
        Binding("tab", "toggle_typing", "Escrever"),
        Binding("r", "run", "Rodar"),
        Binding("enter", "run", show=False),
        Binding("n", "next_ex", "Próximo ▶"),
        Binding("p", "prev_ex", "◀ Anterior"),
        Binding("escape", "stop_or_back", "Parar"),
        Binding("0", "jump(0)", show=False),
        Binding("1", "jump(1)", show=False),
        Binding("2", "jump(2)", show=False),
        Binding("3", "jump(3)", show=False),
        Binding("4", "jump(4)", show=False),
        Binding("5", "jump(5)", show=False),
        Binding("6", "jump(6)", show=False),
        Binding("7", "jump(7)", show=False),
        Binding("8", "jump(8)", show=False),
        Binding("9", "jump(9)", show=False),
    ]

    current_index: reactive[int] = reactive(0)
    typing_mode: reactive[bool] = reactive(False)
    """False = navegação (as teclas são atalhos); True = escrita (vão para o stdin)."""
    proc: Optional[asyncio.subprocess.Process] = None
    reader_task: Optional[asyncio.Task] = None
    compiler: Optional[tuple[str, str]] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            with Vertical(id="sidebar"):
                yield Static("  EXERCÍCIOS  ", id="sidebar-title")
                yield ListView(
                    *[ExerciseItem(ex.num, ex.nome) for ex in EXERCICIOS],
                    id="list",
                )
            with Vertical(id="content"):
                yield Static("", id="description")
                yield Static("", id="status")
                yield RichLog(id="output", highlight=True, markup=True, wrap=True)
                yield StdinInput(placeholder="Entrada para o programa… (Enter envia)", id="stdin")  # placeholder inicial; é atualizado em _refresh_description
        yield Footer()

    def on_mount(self) -> None:
        try:
            self.compiler = find_compiler()
            self.list_view = self.query_one("#list", ListView)
            self.desc = self.query_one("#description", Static)
            self.status = self.query_one("#status", Static)
            self.output = self.query_one("#output", RichLog)
            self.stdin_widget = self.query_one("#stdin", Input)
            self.list_view.index = 0
            self._refresh_description()
            self._refresh_status()
            self.list_view.focus()
        except Exception as e:
            # Não derruba o app se algo falhar ao montar
            self.log(f"[MainScreen] erro no on_mount: {e}")

    # ---------- helpers de UI ----------

    def _ex_at(self, idx: int):
        return EXERCICIOS[idx % len(EXERCICIOS)]

    def _refresh_description(self) -> None:
        ex = self._ex_at(self.current_index)
        md = (
            f"[bold cyan]Exercício {ex.num}[/bold cyan]  "
            f"[bold]{ex.nome}[/bold]\n\n"
            f"[italic]{ex.resumo}[/italic]\n\n"
            f"[dim]Descrição técnica:[/dim]  {ex.desc}\n\n"
            f"[bold yellow]→ Como operar:[/bold yellow]\n{ex.como_operar}\n\n"
            f"[dim]Conteúdos:[/dim] [italic]{ex.topicos}[/italic]\n"
            f"[dim]Fonte:[/dim] [italic]{ex.fonte}[/italic]\n\n"
            f"[dim]Atalhos:[/dim]  [b]r[/b] Rodar · [b]n[/b] Próximo · [b]p[/b] Anterior · "
            f"[b]0-9[/b] Pular · [b]Esc[/b] Parar · [b]q[/b] Sair"
        )
        self.desc.update(md)
        # Atualiza o placeholder do input pra dica específica do exercício
        self.stdin_widget.placeholder = f"{ex.placeholder}  (Enter envia)"
        # Limpa output antigo se não há processo rodando
        if not (self.proc and self.proc.returncode is None):
            if self.output.lines:
                self.output.clear()
                self.output.write(
                    f"[dim](output limpo — pressione r para rodar "
                    f"o Exercício {ex.num})[/dim]"
                )

    def _refresh_status(self) -> None:
        if self.compiler:
            label, path = self.compiler
            comp = f"[dim]compilador:[/dim] [green]{label}[/green] [dim]({path})[/dim]"
        else:
            comp = (
                "[bold red]Nenhum compilador C encontrado —[/bold red] "
                "instale gcc (MinGW/MSYS2) ou rode "
                "[cyan]scoop install tcc[/cyan]"
            )
        if self.typing_mode:
            modo = (
                "[bold cyan]modo escrita[/bold cyan] [dim]"
                "(Tab → navegação; as teclas vão para o stdin do programa)[/dim]"
            )
        else:
            modo = (
                "[bold cyan]modo navegação[/bold cyan] [dim]"
                "(Tab → escrita; r/n/p/0-9/q são atalhos)[/dim]"
            )
        self.status.update(f"{modo}  ·  {comp}")

    # ---------- actions ----------

    def action_run(self) -> None:
        asyncio.create_task(self._run_selected())

    def action_toggle_typing(self) -> None:
        """Alterna entre o modo navegação (atalhos) e o modo escrita (stdin).

        O modo escrita é o único em que as teclas digitáveis chegam ao
        programa — o exercício 06 pede "s/n" e o 10 pede a senha.
        """
        self.typing_mode = not self.typing_mode
        if self.typing_mode:
            self.stdin_widget.focus()
        else:
            self.list_view.focus()
        self._refresh_status()

    async def action_next_ex(self) -> None:
        await self._stop_proc()
        self.current_index = (self.current_index + 1) % len(EXERCICIOS)
        self.list_view.index = self.current_index
        self._refresh_description()
        await self._run_selected()

    async def action_prev_ex(self) -> None:
        await self._stop_proc()
        self.current_index = (self.current_index - 1) % len(EXERCICIOS)
        self.list_view.index = self.current_index
        self._refresh_description()
        await self._run_selected()

    def action_jump(self, idx: int) -> None:
        # Mapeamento: tecla 1-9 → exercício 01-09 (idx 0-8);
        # tecla 0 → exercício 10 (idx 9).
        # Teclas numéricas só selecionam (não rodam) — Enter/r roda.
        target = 9 if idx == 0 else idx - 1
        if 0 <= target < len(EXERCICIOS):
            self.current_index = target
            self.list_view.index = target
            self._refresh_description()
            self.list_view.focus()

    async def action_stop_or_back(self) -> None:
        if self.proc and self.proc.returncode is None:
            await self._stop_proc()
        else:
            self.list_view.focus()

    # ---------- compilação + execução ----------

    def _env_filho(self) -> dict[str, str]:
        """Ambiente para o compilador e para o programa filho.

        O toolchain do MSYS2/TDM no Windows só funciona com o próprio
        diretório no PATH: as DLLs dele (libgcc, libwinpthread) moram lá.
        Sem isto o gcc morre com "código 1" e stderr vazio.
        """
        env = dict(os.environ)
        if self.compiler:
            compiler_dir = str(Path(self.compiler[1]).parent)
            env["PATH"] = compiler_dir + os.pathsep + env.get("PATH", "")
        env["PYTHONIOENCODING"] = "utf-8"
        return env

    async def _compile(self, ex) -> Optional[Path]:
        src = script_path(ex.num)
        dst = exe_path(ex.num)
        if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime:
            return dst  # já compilado e atualizado
        if not self.compiler:
            self.output.write(
                "[bold red]Nenhum compilador C disponível.[/bold red] "
                "Instale gcc/tcc para compilar."
            )
            return None
        _label, compiler_path = self.compiler
        BIN_DIR.mkdir(parents=True, exist_ok=True)
        self.output.write(
            f"[dim]Compilando {src.name} → {dst.name} ({_label})…[/dim]"
        )
        try:
            proc = await asyncio.create_subprocess_exec(
                compiler_path, str(src), "-o", str(dst),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self._env_filho(),
            )
            _, err = await proc.communicate()
        except FileNotFoundError as e:
            self.output.write(f"[bold red]Falha ao invocar compilador:[/bold red] {e}")
            return None
        except Exception as e:
            self.output.write(f"[bold red]Erro ao compilar:[/bold red] {e}")
            return None
        if proc.returncode != 0:
            err_text = err.decode("utf-8", errors="replace").strip()
            self.output.write(
                f"[bold red]Erro de compilação (código {proc.returncode}):[/bold red]\n{err_text}"
            )
            return None
        self.output.write(f"[green]✓ Compilado em {dst.name}.[/green]")
        return dst

    async def _run_selected(self) -> None:
        if self.proc and self.proc.returncode is None:
            self.output.write("[yellow]Já existe um programa rodando. Pare-o primeiro (Esc).[/yellow]")
            return
        ex = self._ex_at(self.current_index)
        self.output.clear()
        self.output.write(f"[bold green]▶ Exercício {ex.num} — {ex.nome}[/bold green]")

        exe = await self._compile(ex)
        if not exe or not exe.exists():
            return

        try:
            # No Windows, .exe com PIPE funciona. Em Linux/Mac, seria ./.exe_name
            self.proc = await asyncio.create_subprocess_exec(
                str(exe),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(EXERCICIOS_DIR),
                env=self._env_filho(),
            )
        except Exception as e:
            self.output.write(f"[bold red]Falha ao iniciar o .exe:[/bold red] {e}")
            self.proc = None
            return

        self.reader_task = asyncio.create_task(self._read_output())
        self.stdin_widget.focus()

    async def _read_output(self) -> None:
        assert self.proc
        try:
            while True:
                chunk = await self.proc.stdout.read(512)
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="replace")
                # preserva quebras de linha
                for line in text.splitlines(keepends=True):
                    self.output.write(line.rstrip("\n"))
        except Exception as e:
            self.output.write(f"[red]Erro de leitura: {e}[/red]")
        finally:
            rc = -1
            try:
                # Espera limitada: um programa à espera de input no stdin nunca
                # termina sozinho. Sem este limite, o `wait()` ficava pendurado
                # e o `App` não fechava quando o utilizador carregava em "q"
                # com um exercício a correr.
                rc = await asyncio.wait_for(self.proc.wait(), timeout=0.5)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                rc = -1
            except Exception:
                rc = -1
            if rc == -1 and self.proc.returncode is None:
                # O programa ficou à espera de input e o `App` está a fechar:
                # terminá-lo para não deixar um processo órfão pelo caminho.
                try:
                    self.proc.terminate()
                except Exception:
                    pass
            try:
                # Fecha os pipes do filho: sem isto o asyncio reclama
                # "unclosed transport" quando o interpreter termina.
                self.proc._transport.close()
            except Exception:
                pass
            cor = "green" if rc == 0 else "red"
            self.output.write(f"\n[bold {cor}]■ Programa finalizado (código {rc})[/bold {cor}]")
            self.proc = None
            self.reader_task = None
            self.list_view.focus()

    async def _stop_proc(self) -> None:
        if self.proc and self.proc.returncode is None:
            try:
                self.proc.terminate()
                await asyncio.wait_for(self.proc.wait(), timeout=1.5)
            except asyncio.TimeoutError:
                self.proc.kill()
            self.output.write("\n[yellow]■ Processo interrompido[/yellow]")
        if self.reader_task and not self.reader_task.done():
            self.reader_task.cancel()
            try:
                await self.reader_task
            except (asyncio.CancelledError, Exception):
                pass
        self.proc = None
        self.reader_task = None

    # ---------- handlers de eventos ----------

    @on(ListView.Highlighted, "#list")
    def on_highlighted(self, event: ListView.Highlighted) -> None:
        if event.list_view.index is not None:
            self.current_index = event.list_view.index
            self._refresh_description()

    @on(Input.Submitted, "#stdin")
    async def on_stdin_submitted(self, event: Input.Submitted) -> None:
        value = event.value
        self.stdin_widget.value = ""
        # Sem processo rodando: avisa o usuário em vez de engolir o input
        if not (self.proc and self.proc.stdin and self.proc.returncode is None):
            if not self.typing_mode:
                # Enter em modo navegação = rodar o exercício (mesmo que "r").
                await self._run_selected()
                return
            ex = self._ex_at(self.current_index)
            self.output.write(
                f"[bold blue]›[/bold blue] {value}  "
                f"[yellow](nenhum programa rodando — pressione r "
                f"para iniciar o Exercício {ex.num})[/yellow]"
            )
            return
        self.output.write(f"[bold blue]›[/bold blue] {value}")
        try:
            self.proc.stdin.write((value + "\n").encode("utf-8"))
            await self.proc.stdin.drain()
        except Exception as e:
            self.output.write(f"[red]Erro ao enviar entrada: {e}[/red]")


class AvaliacaoTUI(App):
    """App raiz: gerencia as telas (HomeScreen → MainScreen)."""

    SCREENS = {
        "home": HomeScreen,
        "main": MainScreen,
    }

    def get_default_screen(self) -> "HomeScreen":
        """Sobrescreve a tela default da App — splash aparece
        desde o primeiro frame, antes do on_mount."""
        return HomeScreen()

    def on_mount(self) -> None:
        # Nada aqui — a tela inicial já é o HomeScreen via get_default_screen.
        # Quando o usuário apertar uma tecla, o HomeScreen.on_key
        # empilha MainScreen por cima.
        pass


def main() -> None:
    app = AvaliacaoTUI()
    app.run()


if __name__ == "__main__":
    main()
