import os
import sys
import pygame
from pygame import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.engine.Jogador import Jogador
from src.ui.animation import AnimacaoMovimento
from src.engine.Partida import Partida
from src.engine.Fabricas import TabuleiroPadraoFactory

class Game:
    def __init__(self, selected_characters, screen):
        # Core components
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Constants
        self.height = 720
        self.width = 1280
        self.font = pygame.font.Font(None, 36)
        
        # Assets
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.background = pygame.image.load(os.path.join(assets_dir, 'gamebg.png')).convert()
        self.tabuleiro_img = pygame.image.load(os.path.join(assets_dir, 'tabuleirobase.png')).convert_alpha()
        
        self.icon_jogadores = {
            "azul": pygame.image.load(os.path.join(assets_dir, 'icone-gato-azul.png')).convert_alpha(),
            "rosa": pygame.image.load(os.path.join(assets_dir, 'icone-gato-rosa.png')).convert_alpha(),
            "roxo": pygame.image.load(os.path.join(assets_dir, 'icone-gato-roxo.png')).convert_alpha(),
            "verde": pygame.image.load(os.path.join(assets_dir, 'icone-gato-verde.png')).convert_alpha(),
            "amarelo": pygame.image.load(os.path.join(assets_dir, 'icone-gato.png')).convert_alpha(), # Placeholder
            "ciano": pygame.image.load(os.path.join(assets_dir, 'icove-gato-azul.png')).convert_alpha(), # Placeholder
        }

        # Game state
        self.running = True
        self.valor_dado1 = 0
        self.valor_dado2 = 0
        
        # Engine Setup
        player_names = selected_characters
        factory = TabuleiroPadraoFactory()
        self.partida = Partida(player_names, factory)
        self.partida.iniciar_jogo()
        self.jogadores = self.partida.jogadores

        # Load player cards
        self.player_cards = {}
        for jogador in self.jogadores:
            try:
                path = os.path.join(assets_dir, f'card-jogador-{jogador.peca}.png')
                self.player_cards[jogador.peca] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                print(f"Aviso: Imagem do card do jogador '{jogador.peca}' não encontrada.")

        # Board positions
        self.casas_x_y = {
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
        self.num_casas = len(self.casas_x_y)

        # Animation
        self.animacao = AnimacaoMovimento(self.casas_x_y, self.num_casas)

    def get_draw_pos(self, jogador: Jogador, pos_interpolada=None):
        if pos_interpolada:
            base = pos_interpolada
        else:
            base = self.casas_x_y.get(jogador.posicao, self.casas_x_y[0])
        
        try:
            jogador_idx = self.jogadores.index(jogador)
            offset = (jogador_idx * 18, 0)
            return (base[0] + offset[0], base[1] + offset[1])
        except ValueError:
            return base

    def run(self):
        while self.running:
            self.clock.tick(60)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if not self.animacao.ativa and not self.animacao.tem_passos_pendentes():
                            resultado_turno = self.partida.jogar_rodada()
                            
                            if resultado_turno:
                                jogador_da_vez = resultado_turno["jogador"]
                                dados = resultado_turno["dados"]
                                
                                #print(f"\n=== Turno do Jogador: {jogador_da_vez.nome} ===")
                                
                                if resultado_turno["acao"] == "moveu":
                                    self.valor_dado1, self.valor_dado2 = dados[0], dados[1]
                                    path = resultado_turno["path"]
                                    pos_anterior = resultado_turno["posicao_anterior"]
                                    
                                    try:
                                        jogador_idx = self.jogadores.index(jogador_da_vez)
                                        self.animacao.iniciar(jogador_idx, path, pos_anterior)
                                        # Inicia o primeiro passo da animação imediatamente para evitar o "teleporte"
                                        if self.animacao.tem_passos_pendentes():
                                            self.animacao.proximo_passo()
                                    except ValueError:
                                        pass # Player not found, should not happen
                                
                                elif resultado_turno["acao"] == "foi_preso_por_doubles":
                                    try:
                                        jogador_idx = self.jogadores.index(jogador_da_vez)
                                        # Posição anterior é a mesma que a atual antes de ir para a cadeia
                                        pos_anterior = jogador_da_vez.posicao 
                                        self.animacao.iniciar(jogador_idx, resultado_turno["path"], pos_anterior)
                                        if self.animacao.tem_passos_pendentes():
                                            self.animacao.proximo_passo()
                                    except ValueError:
                                        pass
            
            # Animation management
            if not self.animacao.ativa and self.animacao.tem_passos_pendentes():
                self.animacao.proximo_passo()
            
            if not self.animacao.ativa and not self.animacao.tem_passos_pendentes() and self.animacao.jogador_idx is not None:
                self.animacao.finalizar()
            
            pos_interpolada = None
            if self.animacao.ativa:
                jogador_animado = self.jogadores[self.animacao.jogador_idx]
                pos_interpolada = self.animacao.atualizar(jogador_animado)
            
            # Rendering
            self.screen.blit(self.background, (0, 0))
            
            # Draw Player Cards
            card_positions = [
                (0, 0), # Top-Left
                (self.width, 0), # Top-Right
                (0, self.height), # Bottom-Left
                (self.width, self.height) # Bottom-Right
            ]

            for i, jogador in enumerate(self.jogadores):
                if i < 4:
                    card_surface = self.player_cards.get(jogador.peca)
                    if card_surface:
                        # Position and draw the card
                        pos = card_positions[i]
                        rect = card_surface.get_rect()
                        if pos[0] > 0: rect.right = pos[0]
                        else: rect.left = pos[0]
                        if pos[1] > 0: rect.bottom = pos[1]
                        else: rect.top = pos[1]
                        self.screen.blit(card_surface, rect)

                        # Render and draw the player's money
                        money_text = f"{jogador.dinheiro}"
                        money_surface = self.font.render(money_text, True, (255, 255, 255))
                        # Position text relative to the card's top-left corner
                        text_pos = (rect.left + 150, rect.top + 30)
                        self.screen.blit(money_surface, text_pos)

            self.screen.blit(self.tabuleiro_img, (328, 0))
            
            for i, jogador in enumerate(self.jogadores):
                is_animating = self.animacao.ativa and i == self.animacao.jogador_idx
                current_pos = pos_interpolada if is_animating else None
                
                draw_pos = self.get_draw_pos(jogador, current_pos)
                self.screen.blit(self.icon_jogadores[jogador.peca], draw_pos)
            
            texto_dado1 = self.font.render(str(self.valor_dado1), True, (255, 255, 255))
            texto_dado2 = self.font.render(str(self.valor_dado2), True, (255, 255, 255))
            
            self.screen.blit(texto_dado1, (1190, 540))
            self.screen.blit(texto_dado2, (1230, 540))

            pygame.display.flip()