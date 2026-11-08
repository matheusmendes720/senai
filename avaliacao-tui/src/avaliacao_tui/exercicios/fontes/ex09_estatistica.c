/* Exercício 09 — Estatística de uma turma (15 estudantes).
 * Conteúdos: for, if/else, acumuladores, comparação. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int idade;
    float nota;
    int soma_idades = 0;
    float soma_notas = 0.0f;
    int aprovados = 0, recuperacao = 0, reprovados = 0;
    float maior_nota = -1.0f;

    for (int i = 1; i <= 15; i++) {
        printf("\nEstudante %d:\n", i);
        printf("  Idade: ");
        if (scanf("%d", &idade) != 1) return 1;
        printf("  Nota:  ");
        if (scanf("%f", &nota) != 1) return 1;

        soma_idades += idade;
        soma_notas += nota;
        if (nota > maior_nota) maior_nota = nota;

        if (nota >= 7.0f)      aprovados++;
        else if (nota >= 5.0f) recuperacao++;
        else                   reprovados++;
    }

    printf("\nMédia das idades:      %.2f\n", soma_idades / 15.0f);
    printf("Média das notas:       %.2f\n", soma_notas / 15.0f);
    printf("Aprovados:             %d\n", aprovados);
    printf("Recuperação:           %d\n", recuperacao);
    printf("Reprovados:            %d\n", reprovados);
    printf("Maior nota da turma:   %.2f\n", maior_nota);
    return 0;
}
