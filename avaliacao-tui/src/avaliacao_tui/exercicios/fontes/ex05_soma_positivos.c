/* Exercício 05 — Soma dos números positivos (até digitar 0).
 * Conteúdos: while, if/else, acumuladores e contadores. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int n;
    int soma = 0, positivos = 0, negativos = 0;

    while (1) {
        printf("Digite um inteiro (0 para parar): ");
        if (scanf("%d", &n) != 1) return 1;
        if (n == 0) break;
        if (n > 0) {
            soma += n;
            positivos++;
        } else {
            negativos++;
        }
    }

    printf("\nSoma dos positivos:  %d\n", soma);
    printf("Qtd. positivos:     %d\n", positivos);
    printf("Qtd. negativos:     %d\n", negativos);
    return 0;
}
