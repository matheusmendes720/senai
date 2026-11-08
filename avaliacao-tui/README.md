# Avaliação TUI — Parte 2 (Implantação de Sistemas)

Painel TUI interativo (Python + Textual) que compila e executa os **10
exercícios em C** da Avaliação Parte 2 da disciplina *Implantação de Sistemas*
(SENAI). O professor roda um comando, escolhe o programa no menu, digita
entradas, vê o resultado, navega para o próximo — tudo com mouse ou teclado.

```
┌─ Avaliação Parte 2 ───────────────────────────────────────┐
│ EXERCÍCIOS                │ Exercício 08 — Número Primo   │
│ ▸ [01] Pares e Ímpares    │                                │
│   [02] Maior e Menor      │ Ler inteiro positivo e         │
│   [03] Média de Alunos    │ informar se é primo.           │
│   [04] Tabuada            │                                │
│   [05] Soma de Positivos  │ Conteúdos: for, if, %, contador│
│   [06] Caixa Eletrônico   │                                │
│   [07] Menu de Operações  │ ▶ Rodando ex08_primo.exe       │
│   [08] Número Primo       │   Digite um número positivo:   │
│   [09] Estatística        │                                │
│   [10] Senha              │ Entrada para o programa…       │
│                           ├───────────────────────────────│
│ compilador: gcc (MSYS2)   │  Sair  Rodar  ▶  ◀  Parar      │
└───────────────────────────────────────────────────────────┘
```

## Como rodar (3 jeitos, todos com 1 comando)

```bash
# 1. Windows — duplo-clique em start.bat, OU:
start.bat

# 2. Git Bash / WSL / Linux / Mac:
./start.sh

# 3. Se tiver uv instalado (qualquer plataforma):
uvx .
```

`start.bat` / `start.sh` detectam `uv`, baixam o `textual` sob demanda
(via `uv run --with textual`) e abrem a TUI. **Não precisa instalar nada
manualmente**, só Python + uv (ou só Python — nesse caso usam `pip --user`).

## Pré-requisitos

| O quê | Por quê | Como instalar |
|---|---|---|
| Python 3.10+ | rodar a TUI | já vem no Windows/Mac; `apt install python3` no Linux |
| uv (opcional) | one-liner sem venv | `pip install uv` ou `winget install astral-sh.uv` |
| Compilador C | compilar os 10 `.c` | veja abaixo |

**Sem compilador C?** A TUI detecta automaticamente `gcc`, `tcc`, `cc` ou
`clang` no `PATH`. Se nenhum estiver instalado:

```bash
# opção leve (~5 MB, compila tudo que precisamos):
scoop install tcc        # Git Bash / Windows
brew install tinycc      # Mac
apt install tcc          # Linux
```

A TUI compila cada `.c` na primeira execução (depois fica em cache em
`src/avaliacao_tui/exercicios/bin/`). Compilação incremental: se o `.c` não
mudou, o `.exe` é reusado.

## Atalhos da TUI

| Tecla | Ação |
|---|---|
| `↑` / `↓` | Navega entre os exercícios |
| `1`–`9` | Pula direto para o exercício 01–09 |
| `0` | Pula para o exercício 10 |
| `Enter` / `r` | Compila (se preciso) e executa o selecionado |
| `n` | Próximo exercício (roda automaticamente) |
| `p` | Exercício anterior (roda automaticamente) |
| `Esc` | Interrompe o programa em execução |
| `q` / `Ctrl+C` | Sai da TUI |
| Click do mouse | Seleciona item da lista |

A área de output mostra a saída do programa em tempo real. O campo de input
na parte inferior envia dados ao `stdin` (digite e pressione `Enter`).

## Como substituir uma solução

Cada exercício vive em
`src/avaliacao_tui/exercicios/fontes/exNN_nome.c`. Para usar sua própria
implementação, sobrescreva o arquivo mantendo o nome. A TUI recompila
automaticamente no próximo `r` (ou delete o `.exe` em `bin/` para forçar).

```c
/* ex01_pares_impares.c */
#include <stdio.h>

int main(void) {
    int pares = 0, impares = 0, n;
    for (int i = 1; i <= 10; i++) {
        printf("Digite o %dº número: ", i);
        if (scanf("%d", &n) != 1) return 1;
        if (n % 2 == 0) pares++; else impares++;
    }
    printf("\nPares: %d | Ímpares: %d\n", pares, impares);
    return 0;
}
```

## Compilação manual (opcional)

Se preferir compilar todos de uma vez antes de abrir a TUI:

```bash
# Linux / Mac / Git Bash (com gcc ou tcc no PATH)
make

# Ou direto:
for f in src/avaliacao_tui/exercicios/fontes/ex*.c; do
    cc "$f" -o "${f%.c}.exe"
done
```

## Estrutura

```
avaliacao-tui/
├── pyproject.toml               # projeto uv, dep: textual
├── README.md
├── Makefile                     # (opcional) compila todos os .c
├── start.bat / start.sh         # one-liner p/ Windows / Unix
├── enunciado/                   # cópia do .docx do enunciado
└── src/avaliacao_tui/
    ├── tui.py                   # app Textual (Python)
    └── exercicios/
        ├── fontes/ex*.c         # os 10 programas (C)
        └── bin/                 # .exe compilados (gerados em runtime)
```

## Lista dos exercícios

1. **Pares e Ímpares** — `for`, `if/else`, `%`
2. **Maior e Menor** — `for`, `if/else`, comparadores
3. **Média de Alunos** — `for`, `if/else`, contadores
4. **Tabuada** — `do/while`, `if/else`, `for`
5. **Soma de Positivos** — `while`, `if/else`, acumuladores
6. **Caixa Eletrônico** — `while`, `if/else`, `/`, `%`
7. **Menu de Operações** — `do/while`, `switch`, `if/else`
8. **Número Primo** — `for`, `if`, `%`, contador
9. **Estatística da Turma** — `for`, `if/else`, acumuladores
10. **Senha com Tentativas** — `while`, contador, `if/else`