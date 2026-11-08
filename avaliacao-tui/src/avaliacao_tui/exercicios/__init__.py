"""Registro dos 10 exercícios da Avaliação Parte 2 (em C).

Layout no disco:
    exercicios/
        fontes/exNN_*.c    # fontes dos programas
        bin/exNN_*.exe     # binários compilados (gerados em runtime)

Cada Exercicio traz, além dos metadados técnicos:
    - resumo:        uma frase em linguagem simples sobre o que o programa faz
    - como_operar:   passo a passo claro para o usuário operar
    - placeholder:   dica curta exibida no campo de input da TUI
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

EXERCICIOS_DIR = Path(__file__).parent
FONTES_DIR = EXERCICIOS_DIR / "fontes"
BIN_DIR = EXERCICIOS_DIR / "bin"


@dataclass(frozen=True)
class Exercicio:
    num: str          # "01" .. "10"
    nome: str         # título curto
    desc: str         # descrição técnica do enunciado
    topicos: str      # conteúdos (for, if/else, etc.)
    fonte: str        # nome do arquivo .c (dentro de fontes/)
    executavel: str   # nome do .exe gerado (dentro de bin/)
    resumo: str       # resumo de uma linha em linguagem simples
    como_operar: str  # instruções passo a passo para o usuário
    placeholder: str  # dica curta exibida no campo de input


EXERCICIOS: tuple[Exercicio, ...] = (
    Exercicio(
        "01", "Pares e Ímpares",
        "Ler 10 números inteiros; contar pares e ímpares.",
        "for, if/else, %",
        "ex01_pares_impares.c", "ex01_pares_impares.exe",
        resumo="Digite 10 números inteiros; o programa diz se cada um é par ou ímpar e conta o total.",
        como_operar=(
            "1. Digite 10 números inteiros, um por vez (Enter entre cada).\n"
            "2. Após cada número, o programa responde: «N é PAR» ou «N é ÍMPAR».\n"
            "3. Ao digitar o 10º, ele mostra o total de pares e de ímpares."
        ),
        placeholder="Digite um número inteiro e pressione Enter…",
    ),
    Exercicio(
        "02", "Maior e Menor",
        "Ler 8 inteiros e determinar o maior e o menor informados.",
        "for, if/else, comparadores",
        "ex02_maior_menor.c", "ex02_maior_menor.exe",
        resumo="Digite 8 números inteiros; o programa descobre qual é o maior e qual é o menor.",
        como_operar=(
            "1. Digite 8 números inteiros, um por vez (Enter entre cada).\n"
            "2. Após o 8º número, o programa mostra o maior e o menor de todos."
        ),
        placeholder="Digite um número inteiro e pressione Enter…",
    ),
    Exercicio(
        "03", "Média de Alunos",
        "Notas de 10 alunos (2 por aluno); classificar e contar.",
        "for, if/else, contadores",
        "ex03_media_alunos.c", "ex03_media_alunos.exe",
        resumo="Cadastre 10 alunos com 2 notas cada; o programa calcula a média e diz se cada um foi Aprovado, Recuperação ou Reprovado.",
        como_operar=(
            "1. Para cada um dos 10 alunos, digite a Nota 1 e a Nota 2 (Enter entre cada).\n"
            "2. O programa calcula a média e mostra a situação:\n"
            "     • Aprovado    (média ≥ 7)\n"
            "     • Recuperação (5 ≤ média < 7)\n"
            "     • Reprovado   (média < 5)\n"
            "3. No final, mostra o total de aprovados, em recuperação e reprovados."
        ),
        placeholder="Nota 1 do aluno (Enter) → Nota 2 (Enter)…",
    ),
    Exercicio(
        "04", "Tabuada",
        "Solicitar inteiro entre 1 e 10 e mostrar a tabuada; repetir até entrada válida.",
        "do/while, if/else, for",
        "ex04_tabuada.c", "ex04_tabuada.exe",
        resumo="Escolha um número de 1 a 10 e o programa mostra a tabuada completa (de 1×n até 10×n).",
        como_operar=(
            "1. Digite um número inteiro entre 1 e 10.\n"
            "2. Se digitar fora do intervalo, o programa pede novamente.\n"
            "3. Quando aceitar, ele imprime a tabuada de n×1 até n×10."
        ),
        placeholder="Digite um número de 1 a 10…",
    ),
    Exercicio(
        "05", "Soma de Positivos",
        "Ler inteiros até digitar 0; somar positivos e contar positivos/negativos.",
        "while, if/else, acumuladores",
        "ex05_soma_positivos.c", "ex05_soma_positivos.exe",
        resumo="Digite números à vontade; quando digitar 0, o programa mostra a soma dos positivos e a contagem de positivos e negativos.",
        como_operar=(
            "1. Digite números inteiros, um por vez.\n"
            "2. Quando quiser parar, digite 0.\n"
            "3. O programa mostra a soma dos positivos, a quantidade de positivos e a de negativos."
        ),
        placeholder="Digite um inteiro (0 para parar)…",
    ),
    Exercicio(
        "06", "Caixa Eletrônico",
        "Saque com notas de 100, 50, 20 e 10; perguntar se deseja nova operação.",
        "while, if/else, /, %",
        "ex06_caixa_eletronico.c", "ex06_caixa_eletronico.exe",
        resumo="Simula um caixa eletrônico: digite o valor do saque e o programa entrega as notas (R$100, R$50, R$20 e R$10).",
        como_operar=(
            "1. Digite o valor do saque (deve ser múltiplo de 10 e positivo).\n"
            "2. O programa mostra quantas notas de R$100, R$50, R$20 e R$10 entrega.\n"
            "3. Pergunta se quer fazer outra operação — responda s ou n."
        ),
        placeholder="Valor do saque (múltiplo de R$10)…",
    ),
    Exercicio(
        "07", "Menu de Operações",
        "Somar / Subtrair / Multiplicar / Dividir / Sair; tratar divisão por zero.",
        "do/while, switch, if/else",
        "ex07_menu_operacoes.c", "ex07_menu_operacoes.exe",
        resumo="Calculadora com menu: somar, subtrair, multiplicar, dividir ou sair.",
        como_operar=(
            "1. Escolha a operação:\n"
            "     1 - Somar      2 - Subtrair\n"
            "     3 - Multiplicar   4 - Dividir\n"
            "     5 - Sair\n"
            "2. Digite os dois números (Enter entre cada).\n"
            "3. O programa mostra o resultado. Divisão por zero é protegida.\n"
            "4. O menu reaparece até você escolher 5."
        ),
        placeholder="1-Somar  2-Sub  3-Mul  4-Div  5-Sair…",
    ),
    Exercicio(
        "08", "Número Primo",
        "Ler inteiro positivo e informar se é primo.",
        "for, if, %, contador",
        "ex08_primo.c", "ex08_primo.exe",
        resumo="Digite um número inteiro positivo; o programa diz se ele é primo.",
        como_operar=(
            "1. Digite um número inteiro positivo.\n"
            "2. O programa conta quantos divisores o número tem.\n"
            "3. Se tiver exatamente 2 divisores (1 e ele mesmo), é primo."
        ),
        placeholder="Digite um número inteiro positivo…",
    ),
    Exercicio(
        "09", "Estatística da Turma",
        "Idade e nota de 15 estudantes; médias, aprovados, recuperação, reprovados e maior nota.",
        "for, if/else, acumuladores",
        "ex09_estatistica.c", "ex09_estatistica.exe",
        resumo="Cadastre 15 alunos (idade + nota) e o programa calcula várias estatísticas da turma.",
        como_operar=(
            "1. Para cada um dos 15 estudantes, digite idade e nota (Enter entre cada).\n"
            "2. Ao final, o programa mostra:\n"
            "     • Média das idades e das notas\n"
            "     • Aprovados (≥7), em recuperação (5–6,9), reprovados (<5)\n"
            "     • Maior nota da turma"
        ),
        placeholder="Idade (Enter) → Nota (Enter)…",
    ),
    Exercicio(
        "10", "Senha com Tentativas",
        "Senha 2026, 3 tentativas; bloquear após exceder.",
        "while, contador, if/else",
        "ex10_senha.c", "ex10_senha.exe",
        resumo="Tente adivinhar a senha numérica em até 3 tentativas. A senha correta é 2026.",
        como_operar=(
            "1. Digite a senha numérica.\n"
            "2. Você tem 3 tentativas. A senha correta é 2026.\n"
            "3. Se acertar, vê «Acesso permitido!».\n"
            "4. Se errar as 3 vezes, o acesso é bloqueado."
        ),
        placeholder="Digite a senha numérica…",
    ),
)


def script_path(num: str) -> Path:
    """Caminho absoluto do arquivo-fonte .c (em fontes/)."""
    for ex in EXERCICIOS:
        if ex.num == num:
            return FONTES_DIR / ex.fonte
    raise KeyError(f"Exercício {num!r} não encontrado")


def exe_path(num: str) -> Path:
    """Caminho absoluto do .exe compilado (em bin/)."""
    for ex in EXERCICIOS:
        if ex.num == num:
            return BIN_DIR / ex.executavel
    raise KeyError(f"Exercício {num!r} não encontrado")
