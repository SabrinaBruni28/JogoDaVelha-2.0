import random

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

    def gerar_posicao(self):
        for x in range(3):
            for y in range(3):
                if not self.posicao_marcada(x, y):
                    return (x, y)
        return None, None

    def gerar_posicao_inteligente(self):
        chance_erro = 0.3  # 30% de chance de ignorar a jogada ideal

        # 1. Tenta ganhar
        if random.random() > chance_erro:
            pos = self.encontrar_posicao_vitoria(self.current_player())
            if pos:
                return pos

        # 2. Bloquear o adversário
        if random.random() > chance_erro:
            adversario = 1 if self.current_player() == 2 else 2
            pos = self.encontrar_posicao_vitoria(adversario)
            if pos:
                return pos

        # 3. Centro
        if not self.posicao_marcada(1, 1):
            if random.random() > chance_erro:
                return (1, 1)

        # 4. Cantos
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        cantos_livres = [c for c in cantos if not self.posicao_marcada(*c)]
        if cantos_livres:
            if random.random() > chance_erro:
                return random.choice(cantos_livres)

        # 5. Qualquer posição livre (aleatória)
        posicoes_livres = [(x, y) for x in range(3) for y in range(3) if not self.posicao_marcada(x, y)]
        if posicoes_livres:
            return random.choice(posicoes_livres)

        return None, None  # tabuleiro cheio
                
    def encontrar_posicao_vitoria(self, jogador):
        for x in range(3):
            for y in range(3):
                if not self.posicao_marcada(x, y):
                    self.jogo[x][y] = jogador  # tenta marcar
                    if self.confere_vencedor() == jogador:
                        self.jogo[x][y] = 0  # desfaz a marcação
                        return (x, y)
                    self.jogo[x][y] = 0  # desfaz a marcação
        return None

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

                


   
