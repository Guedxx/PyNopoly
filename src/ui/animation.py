import pygame

class AnimacaoMovimento:
    def __init__(self, casas_x_y, num_casas):
        self.casas_x_y = casas_x_y
        self.num_casas = num_casas
        self.ativa = False
        self.jogador_idx = None
        self.passos_restantes = []  # Lista de índices de casas a animar
        self.pos_inicio = (0, 0)
        self.pos_fim = (0, 0)
        self.tempo_inicio = 0
        self.casa_destino_atual = 0
        self.duracao_passo = 180  # ms por casa
    
    def iniciar(self, jogador_idx, jogador, valor_dados):
        """Inicia a animação de movimento para um jogador"""
        self.jogador_idx = jogador_idx
        self.passos_restantes = []
        
        # Calcula todas as casas intermediárias do movimento
        posicao_inicial = jogador.posicao
        for i in range(1, valor_dados + 1):
            proxima_casa = (posicao_inicial + i) % self.num_casas
            self.passos_restantes.append(proxima_casa)
        
        print(f"Animação iniciada: Jogador {jogador_idx} vai da casa {posicao_inicial} para {self.passos_restantes[-1]}")
    
    def proximo_passo(self, jogador):
        """Inicia a animação do próximo passo"""
        if not self.passos_restantes:
            return False
        
        self.casa_destino_atual = self.passos_restantes.pop(0)
        casa_origem = jogador.posicao
        
        self.pos_inicio = self.casas_x_y.get(casa_origem, self.casas_x_y[0])
        self.pos_fim = self.casas_x_y.get(self.casa_destino_atual, self.casas_x_y[0])
        self.tempo_inicio = pygame.time.get_ticks()
        self.ativa = True
        
        return True
    
    def atualizar(self, jogador):
        """Atualiza a animação atual e retorna a posição interpolada"""
        if not self.ativa:
            return None
        
        tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio
        t = min(1.0, tempo_decorrido / self.duracao_passo)
        
        # Interpolação linear
        x = self.pos_inicio[0] + (self.pos_fim[0] - self.pos_inicio[0]) * t
        y = self.pos_inicio[1] + (self.pos_fim[1] - self.pos_inicio[1]) * t
        
        # Se completou o passo
        if t >= 1.0:
            jogador.posicao = self.casa_destino_atual
            self.ativa = False
            print(f"Jogador {self.jogador_idx} chegou na casa {self.casa_destino_atual}")
            return None
        
        return (int(x), int(y))
    
    def tem_passos_pendentes(self):
        """Verifica se ainda há passos para animar"""
        return len(self.passos_restantes) > 0
    
    def finalizar(self):
        """Finaliza a animação"""
        self.ativa = False
        self.jogador_idx = None
        self.passos_restantes = []
