/* Exercício 01 — Números Pares e Ímpares.
 * Lê 10 inteiros; informa par/ímpar e conta.
 * Conteúdos: for, if/else, operador %. */

#include <stdio.h>

int main(void) {
    /* stdout em modo pipe (Windows) é block-buffered por padrão;
       isso prende os prompts até o programa terminar. _IONBF = sem buffer. */
    setvbuf(stdout, NULL, _IONBF, 0);

    int pares = 0, impares = 0, n;

    for (int i = 1; i <= 10; i++) {
        printf("Digite o %dº número inteiro: ", i);
        if (scanf("%d", &n) != 1) return 1;
        if (n % 2 == 0) {
            printf("%d é PAR.\n", n);
            pares++;
        } else {
            printf("%d é ÍMPAR.\n", n);
            impares++;
        }
    }

    printf("\nQuantidade de números pares: %d\n", pares);
    printf("Quantidade de números ímpares: %d\n", impares);
    return 0;
}
