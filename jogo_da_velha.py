

class JogoDaVelha:
    def __init__(self):
        self.player_1 = 1
        self.player_2 = 2
        self.jogador_atual = 0
        self.jogo = [[0 for _ in range(3)] for _ in range(3)]

    def init_player(self, who):
        self.jogador_atual = who

    def reiniciar_jogo(self):
        # Resetar matriz do jogo
        self.jogo = [[0 for _ in range(3)] for _ in range(3)]
        self.jogador_atual = self.player_1

    def change_player(self):
        self.jogador_atual = self.player_1 if self.jogador_atual == self.player_2 else self.player_2

    def posicao_marcada(self, x, y):
        return self.jogo[x][y] != 0
    
    def marcar_matriz(self, x, y):
        self.jogo[x][y] = self.jogador_atual

    def current_player(self):
        return self.jogador_atual
    
    def confere_vencedor(self):
        # Verificar linhas
        for linha in self.jogo:
            if linha[0] != 0 and linha[0] == linha[1] == linha[2]:
                return linha[0]  # Retorna o jogador vencedor

        # Verificar colunas
        for col in range(3):
            if self.jogo[0][col] != 0 and self.jogo[0][col] == self.jogo[1][col] == self.jogo[2][col]:
                return self.jogo[0][col]

        # Verificar diagonal principal
        if self.jogo[0][0] != 0 and self.jogo[0][0] == self.jogo[1][1] == self.jogo[2][2]:
            return self.jogo[0][0]

        # Verificar diagonal secundária
        if self.jogo[0][2] != 0 and self.jogo[0][2] == self.jogo[1][1] == self.jogo[2][0]:
            return self.jogo[0][2]

        # Verifica empate (tabuleiro cheio e ninguém ganhou)
        if all(cell != 0 for row in self.jogo for cell in row):
            return -1  # Empate

        return 0  # Ninguém ganhou ainda

                


   
