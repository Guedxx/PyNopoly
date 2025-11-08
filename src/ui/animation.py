import pygame

class AnimacaoMovimento:
    def __init__(self, casas_x_y, num_casas):
        self.casas_x_y = casas_x_y
        self.num_casas = num_casas
        self.ativa = False
        self.jogador_idx = None
        self.passos_restantes = []
        self.pos_inicio = (0, 0)
        self.pos_fim = (0, 0)
        self.tempo_inicio = 0
        self.casa_origem_anim = 0
        self.casa_destino_atual = 0
        self.duracao_passo = 180  # ms por casa
    
    def iniciar(self, jogador_idx, path, pos_inicial):
        """Inicia a animação de movimento para um jogador usando um caminho e uma posição inicial."""
        self.jogador_idx = jogador_idx
        self.passos_restantes = path
        self.casa_origem_anim = pos_inicial
        
        if self.passos_restantes:
            print(f"Animação iniciada: Jogador {jogador_idx} da casa {pos_inicial} seguirá o caminho: {path}")
    
    def proximo_passo(self):
        """Inicia a animação do próximo passo"""
        if not self.passos_restantes:
            self.ativa = False
            return False
        
        self.casa_destino_atual = self.passos_restantes.pop(0)
        
        self.pos_inicio = self.casas_x_y.get(self.casa_origem_anim, self.casas_x_y[0])
        self.pos_fim = self.casas_x_y.get(self.casa_destino_atual, self.casas_x_y[0])
        self.tempo_inicio = pygame.time.get_ticks()
        self.ativa = True
        
        # A origem da proxima animação será o destino da atual
        self.casa_origem_anim = self.casa_destino_atual
        
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
            # A posição canônica do jogador só é atualizada aqui, ao final de cada passo.
            # Isso previne a dessincronização entre a UI e o estado do motor.
            jogador.posicao = self.casa_destino_atual
            self.ativa = False
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