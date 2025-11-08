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
    def __init__(self, selected_characters, screen): # Changed to screen
        # Core components
        self.screen = screen # Use the passed screen
        self.clock = pygame.time.Clock()

        # Constants
        self.height = 720
        self.width = 1280
        self.font = pygame.font.Font(None, 36)
        
        # Assets
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.background = pygame.image.load(os.path.join(assets_dir, 'tabuleiro.png')).convert()
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
        # For now, we add default players if less than 2 are selected.
        player_names = selected_characters
        if len(player_names) < 2:
            player_names.extend([f"Jogador {i+2}" for i in range(2 - len(player_names))])

        factory = TabuleiroPadraoFactory()
        self.partida = Partida(player_names, factory)
        self.partida.iniciar_jogo()
        self.jogadores = self.partida.jogadores

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
        
        # Find player index for offset
        try:
            jogador_idx = self.jogadores.index(jogador)
            offset = (jogador_idx * 18, 0)
            return (base[0] + offset[0], base[1] + offset[1])
        except ValueError:
            return base # Should not happen

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
                                
                                print(f"\n=== Turno do Jogador: {jogador_da_vez.nome} ===")
                                
                                if resultado_turno["acao"] == "moveu":
                                    self.valor_dado1, self.valor_dado2 = dados[0], dados[1]
                                    valor_total = sum(dados)
                                    
                                    try:
                                        jogador_idx = self.jogadores.index(jogador_da_vez)
                                        pos_real = jogador_da_vez.posicao
                                        jogador_da_vez.posicao = resultado_turno["posicao_anterior"]
                                        
                                        self.animacao.iniciar(jogador_idx, jogador_da_vez, valor_total)
                                        
                                        # A posição real será restaurada pela própria animação
                                        # jogador_da_vez.posicao = pos_real

                                    except ValueError:
                                        pass # Player not found, should not happen
                                
                                elif resultado_turno["acao"] == "preso":
                                    print(f"{jogador_da_vez.nome} está preso!")
                                
                                elif resultado_turno["acao"] == "foi_preso_por_doubles":
                                    print(f"{jogador_da_vez.nome} foi preso por tirar 3 duplos!")
            
            # Animation management
            if not self.animacao.ativa and self.animacao.tem_passos_pendentes():
                jogador_animado = self.jogadores[self.animacao.jogador_idx]
                self.animacao.proximo_passo(jogador_animado)
            
            if not self.animacao.ativa and not self.animacao.tem_passos_pendentes() and self.animacao.jogador_idx is not None:
                self.animacao.finalizar()
            
            pos_interpolada = None
            if self.animacao.ativa:
                jogador_animado = self.jogadores[self.animacao.jogador_idx]
                pos_interpolada = self.animacao.atualizar(jogador_animado)
            
            # Rendering
            self.screen.blit(self.background, (0, 0))
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
