/* Exercício 02 — Maior e Menor Número.
 * Lê 8 inteiros; mostra maior e menor.
 * Conteúdos: for, if/else, comparadores. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int n, maior, menor;

    printf("Digite o 1º número inteiro: ");
    if (scanf("%d", &n) != 1) return 1;
    maior = menor = n;

    for (int i = 2; i <= 8; i++) {
        printf("Digite o %dº número inteiro: ", i);
        if (scanf("%d", &n) != 1) return 1;
        if (n > maior) maior = n;
        if (n < menor) menor = n;
    }

    printf("\nMaior número informado: %d\n", maior);
    printf("Menor número informado: %d\n", menor);
    return 0;
}
