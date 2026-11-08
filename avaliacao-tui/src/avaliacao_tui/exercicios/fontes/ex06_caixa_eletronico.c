/* Exercício 06 — Caixa Eletrônico (notas 100, 50, 20, 10).
 * Conteúdos: while, if/else, divisão inteira e módulo. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int valor, restante, qtd;
    char opc;

    while (1) {
        printf("\nValor do saque (R$): ");
        if (scanf("%d", &valor) != 1) return 1;

        if (valor <= 0) {
            printf("Valor deve ser positivo.\n");
        } else if (valor % 10 != 0) {
            printf("Valor indisponível (múltiplos de R$10 apenas).\n");
        } else {
            restante = valor;
            printf("Notas entregues:\n");
            int notas[] = {100, 50, 20, 10};
            for (int i = 0; i < 4; i++) {
                qtd = restante / notas[i];
                if (qtd > 0) {
                    printf("  %d x R$ %d\n", qtd, notas[i]);
                    restante = restante % notas[i];
                }
            }
            if (restante != 0) {
                printf("  (não foi possível compor R$ %d)\n", restante);
            }
        }

        printf("\nDeseja realizar outra operação? (s/n): ");
        scanf(" %c", &opc);
        if (opc != 's' && opc != 'S') {
            printf("Saindo do caixa. Até logo!\n");
            break;
        }
    }
    return 0;
}
