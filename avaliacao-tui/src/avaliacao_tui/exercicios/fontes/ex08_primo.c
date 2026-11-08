/* Exercício 08 — Número Primo.
 * Conteúdos: for, if, %, contador. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int n, divisores = 0;

    printf("Digite um número inteiro positivo: ");
    if (scanf("%d", &n) != 1) return 1;

    if (n <= 1) {
        printf("%d não é primo.\n", n);
        return 0;
    }

    for (int i = 1; i <= n; i++) {
        if (n % i == 0) divisores++;
    }

    if (divisores == 2) {
        printf("%d é primo.\n", n);
    } else {
        printf("%d não é primo (tem %d divisores).\n", n, divisores);
    }
    return 0;
}
