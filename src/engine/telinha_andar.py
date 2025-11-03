import os
import sys
import pygame
from pygame import *
from src.engine.Jogador import Jogador

# Base do projeto (raiz do repositório)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

pygame.init()

# Base do projeto e diretório de artes
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ARTS_DIR = os.path.join(BASE_DIR, 'assets')

# Fonte para renderizar números
font = pygame.font.Font(None, 36)  # Tamanho 72 para os números dos dados

# Variáveis para armazenar os valores dos dados
valor_dado1 = 0
valor_dado2 = 0

height = 720
width = 1280

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyNopoly")

# Baixando o fundo do tabuleiro e os ícones dos jogadores
background = pygame.image.load(os.path.join(ARTS_DIR, 'tabuleiro.png')).convert_alpha()
icon_jogadores = {
    0: pygame.image.load(os.path.join(ARTS_DIR, 'icone-gato-azul.png')).convert_alpha(),
    1: pygame.image.load(os.path.join(ARTS_DIR, 'icone-gato-rosa.png')).convert_alpha(),
    2: pygame.image.load(os.path.join(ARTS_DIR, 'icone-gato-roxo.png')).convert_alpha(),
    3: pygame.image.load(os.path.join(ARTS_DIR, 'icone-gato-verde.png')).convert_alpha()
}

clock = pygame.time.Clock()
running = True



# Criando jogadores
pecas = {0: "azul", 1: "verde", 2: "rosa", 3: "roxo"}
# Jogador espera (peca, nome). Usamos um nome simples baseado no índice.
jogadores = [Jogador(pecas[i], f"Jogador {i+1}") for i in range(len(pecas))]

# Mapeando posições das casas do tabuleiro para coordenadas x,y na tela 
# Expandido para 40 casas (tabuleiro completo do Monopoly)
casas_x_y = {
    0: (350, 310), 1: (390, 350), 2: (420, 380), 3: (445, 405), 
    4: (465, 430), 5: (490, 450), 6: (520, 480), 7: (540, 500), 
    8: (560, 520), 9: (590, 550), 10: (630, 590), 11: (658,542),
    12: (695, 520), 13: (719,500), 14: (748,478), 15:(777,446),
    16: (795, 422), 17: (817, 402), 18: (848,376), 19: (873,346), 
    20: (913,316), 21: (873,279), 22: (852,254), 23: (823,225), 
    24: (800,200), 25: (766,178), 26: (745,156), 27: (725,128),
    28: (698,102), 29:(670,76), 30: (633,40), 31: (591,74),
    32: (571,96), 33:(544,125), 34:(524,147), 35: (496,172),
    36: (475,194), 37:(446,218), 38:(418,248), 39:(398,272)

}

NUM_CASAS = len(casas_x_y)

# Controle de turno
current_player = 0

# Controle de animação
class AnimacaoMovimento:
    def __init__(self):
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
            proxima_casa = (posicao_inicial + i) % NUM_CASAS
            self.passos_restantes.append(proxima_casa)
        
        print(f"Animação iniciada: Jogador {jogador_idx} vai da casa {posicao_inicial} para {self.passos_restantes[-1]}")
    
    def proximo_passo(self, jogador):
        """Inicia a animação do próximo passo"""
        if not self.passos_restantes:
            return False
        
        self.casa_destino_atual = self.passos_restantes.pop(0)
        casa_origem = jogador.posicao
        
        self.pos_inicio = casas_x_y.get(casa_origem, casas_x_y[0])
        self.pos_fim = casas_x_y.get(self.casa_destino_atual, casas_x_y[0])
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

animacao = AnimacaoMovimento()

def get_draw_pos(jogador_idx: int, pos_interpolada=None):
    """
    Calcula a posição de desenho do jogador na tela.
    Se pos_interpolada for fornecida, usa ela; caso contrário, usa a posição atual do jogador.
    """
    jogador = jogadores[jogador_idx]
    
    if pos_interpolada:
        base = pos_interpolada
    else:
        base = casas_x_y.get(jogador.posicao, casas_x_y[0])
    
    # Offset para que múltiplos jogadores não fiquem sobrepostos
    offset = (jogador_idx * 18, 0)
    return (base[0] + offset[0], base[1] + offset[1])

# Loop principal
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Só permite rolar dados se não há animação em andamento
                if not animacao.ativa and not animacao.tem_passos_pendentes():
                    jogador_atual = jogadores[current_player]
                    
                    # Usa o objeto Dados do jogador para lançar os dados
                    dados = jogador_atual.dados.lancar()
                    valor_total = sum(dados)
                    
                    # Atualiza os valores dos dados para renderização
                    valor_dado1, valor_dado2 = dados[0], dados[1]
                    
                    print(f"\n=== Turno do Jogador {current_player} ({jogador_atual.peca}) ===")
                    print(f"Dados: {dados} = {valor_total}")
                    print(f"Posição inicial: {jogador_atual.posicao}")
                    
                    # Inicia a animação de movimento
                    animacao.iniciar(current_player, jogador_atual, valor_total)
    
    # Gerencia a animação
    if not animacao.ativa and animacao.tem_passos_pendentes():
        # Inicia o próximo passo da animação
        animacao.proximo_passo(jogadores[animacao.jogador_idx])
    
    # Se não há mais passos e a animação terminou, avança o turno
    if not animacao.ativa and not animacao.tem_passos_pendentes() and animacao.jogador_idx is not None:
        jogador_atual = jogadores[current_player]
        print(f"Posição final: {jogador_atual.posicao}")
        print(f"Casa: {casas_x_y.get(jogador_atual.posicao, 'desconhecida')}")
        
        # Aqui você pode adicionar lógica para processar a casa onde o jogador parou
        # Por exemplo: verificar se é propriedade, pagar aluguel, etc.
        
        # Avança o turno
        current_player = (current_player + 1) % len(jogadores)
        animacao.finalizar()
        print(f"\n>>> Próximo turno: Jogador {current_player} ({jogadores[current_player].peca})")
    
    # Atualiza a posição interpolada se há animação ativa
    pos_interpolada = None
    if animacao.ativa:
        pos_interpolada = animacao.atualizar(jogadores[animacao.jogador_idx])
    
    # Renderização
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # Desenha todos os jogadores
    for i, jogador in enumerate(jogadores):
        if animacao.ativa and i == animacao.jogador_idx:
            # Jogador em movimento: usa posição interpolada
            draw_pos = get_draw_pos(i, pos_interpolada)
        else:
            # Jogador parado: usa posição atual
            draw_pos = get_draw_pos(i)
        
        screen.blit(icon_jogadores[i], draw_pos)
    
    # Renderiza os números dos dados
    texto_dado1 = font.render(str(valor_dado1), True, (255, 255, 255))
    texto_dado2 = font.render(str(valor_dado2), True, (255, 255, 255))
    
    # Posiciona os números dos dados na tela
    screen.blit(texto_dado1, (1190, 540))  # Dado 1 à esquerda
    screen.blit(texto_dado2, (1230, 540))  # Dado 2 à direita

    pygame.display.flip()
pygame.quit()