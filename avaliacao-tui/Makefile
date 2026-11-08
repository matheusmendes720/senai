# Makefile — compila todos os .c (opcional; a TUI compila sob demanda)

CC      ?= gcc
BIN     := src/avaliacao_tui/exercicios/bin
SRCS    := $(wildcard src/avaliacao_tui/exercicios/fontes/ex*.c)
EXES    := $(patsubst fontes/%.c,$(BIN)/%.exe,$(SRCS))

.PHONY: all clean run tui

all: $(EXES)

$(BIN):
	@mkdir -p $@

$(BIN)/%.exe: src/avaliacao_tui/exercicios/fontes/%.c | $(BIN)
	@echo "  CC    $<"
	@$(CC) $< -o $@

run: all
	uv run --with textual python -m avaliacao_tui.tui

tui:
	uv run --with textual python -m avaliacao_tui.tui

clean:
	rm -rf $(BIN)
