/* Exercício 04 — Tabuada com validação de entrada.
 * Lê inteiro entre 1 e 10; repete até entrada válida.
 * Conteúdos: do/while, if/else, for. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int n;

    do {
        printf("Digite um número inteiro entre 1 e 10: ");
        if (scanf("%d", &n) != 1) return 1;
        if (n < 1 || n > 10) {
            printf("Valor fora do intervalo. Tente novamente.\n");
        }
    } while (n < 1 || n > 10);

    printf("\nTabuada de %d:\n", n);
    for (int i = 1; i <= 10; i++) {
        printf("%d x %2d = %3d\n", n, i, n * i);
    }
    return 0;
}
