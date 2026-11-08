/* Exercício 10 — Sistema de senha com 3 tentativas.
 * Conteúdos: while, contador, if/else. */

#include <stdio.h>
#include <string.h>

#define SENHA "2026"
#define MAX_TENTATIVAS 3

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);  /* desabilita buffer do stdout (pipe no Windows) */
    char senha[64];
    int acesso = 0;

    for (int t = 1; t <= MAX_TENTATIVAS; t++) {
        printf("Tentativa %d/%d — Digite a senha: ", t, MAX_TENTATIVAS);
        if (scanf("%63s", senha) != 1) return 1;
        if (strcmp(senha, SENHA) == 0) {
            printf("Acesso permitido!\n");
            acesso = 1;
            break;
        }
        printf("Senha incorreta.\n");
    }

    if (!acesso) {
        printf("Acesso bloqueado. Excedeu o número de tentativas.\n");
    }
    return 0;
}
