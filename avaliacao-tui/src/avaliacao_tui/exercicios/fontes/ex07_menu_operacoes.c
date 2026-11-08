/* Exercício 07 — Menu de Operações Matemáticas.
 * Conteúdos: do/while, switch, if/else. */

#include <stdio.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    int opc;
    float a, b;

    do {
        printf("\n--- Menu ---\n");
        printf("1 - Somar\n");
        printf("2 - Subtrair\n");
        printf("3 - Multiplicar\n");
        printf("4 - Dividir\n");
        printf("5 - Sair\n");
        printf("Escolha uma opção: ");
        if (scanf("%d", &opc) != 1) return 1;

        if (opc == 5) {
            printf("Saindo.\n");
            break;
        }
        if (opc < 1 || opc > 4) {
            printf("Opção inválida.\n");
            continue;
        }

        printf("Primeiro número: ");
        if (scanf("%f", &a) != 1) return 1;
        printf("Segundo número:  ");
        if (scanf("%f", &b) != 1) return 1;

        switch (opc) {
            case 1:
                printf("Resultado: %.2f + %.2f = %.2f\n", a, b, a + b);
                break;
            case 2:
                printf("Resultado: %.2f - %.2f = %.2f\n", a, b, a - b);
                break;
            case 3:
                printf("Resultado: %.2f * %.2f = %.2f\n", a, b, a * b);
                break;
            case 4:
                if (b == 0.0f) {
                    printf("Erro: divisão por zero.\n");
                } else {
                    printf("Resultado: %.2f / %.2f = %.2f\n", a, b, a / b);
                }
                break;
        }
    } while (opc != 5);

    return 0;
}
