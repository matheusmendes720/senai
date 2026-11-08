/* Exercício 03 — Média de Alunos.
 * Notas de 10 alunos (2 por aluno); classifica e conta.
 * Conteúdos: for, if/else, contadores. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    float n1, n2, media;
    int aprovados = 0, recuperacao = 0, reprovados = 0;

    for (int i = 1; i <= 10; i++) {
        printf("\nAluno %d:\n", i);
        printf("  Nota 1: ");
        if (scanf("%f", &n1) != 1) return 1;
        printf("  Nota 2: ");
        if (scanf("%f", &n2) != 1) return 1;
        media = (n1 + n2) / 2.0f;

        const char *status;
        if (media >= 7.0f)      { status = "Aprovado";    aprovados++; }
        else if (media >= 5.0f) { status = "Recuperação"; recuperacao++; }
        else                    { status = "Reprovado";   reprovados++; }

        printf("  Média = %.2f  →  %s\n", media, status);
    }

    printf("\nAprovados:    %d\n", aprovados);
    printf("Recuperação:  %d\n", recuperacao);
    printf("Reprovados:   %d\n", reprovados);
    return 0;
}
