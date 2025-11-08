import os
import sys
import pygame
from pygame import *
from pygame._sdl2.video import Texture

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.engine.Jogador import Jogador
from src.ui.animation import AnimacaoMovimento

class Game:
    def __init__(self, selected_character, renderer):
        # Core components
        self.renderer = renderer
        self.clock = pygame.time.Clock()

        # Constants
        self.height = 720
        self.width = 1280
        self.font = pygame.font.Font(None, 36)
        
        # Assets
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.background = pygame.image.load(os.path.join(assets_dir, 'tabuleiro.png'))
        self.tabuleiro_img = pygame.image.load(os.path.join(assets_dir, 'tabuleirobase.png'))
        self.icon_jogadores = {
            0: pygame.image.load(os.path.join(assets_dir, 'icone-gato-azul.png')),
            1: pygame.image.load(os.path.join(assets_dir, 'icone-gato-rosa.png')),
            2: pygame.image.load(os.path.join(assets_dir, 'icone-gato-roxo.png')),
            3: pygame.image.load(os.path.join(assets_dir, 'icone-gato-verde.png'))
        }

        # Game state
        self.running = True
        self.valor_dado1 = 0
        self.valor_dado2 = 0
        
        # Players
        pecas = {0: "azul", 1: "verde", 2: "rosa", 3: "roxo"}
        
        # Player 1 is the human-selected character
        player1 = Jogador(pecas[0], selected_character) 
        
        self.jogadores = [player1]
        # Add other default players
        for i in range(1, 4):
            self.jogadores.append(Jogador(pecas[i], f"Jogador {i+1}"))

        self.current_player_idx = 0

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

    def get_draw_pos(self, jogador_idx: int, pos_interpolada=None):
        jogador = self.jogadores[jogador_idx]
        
        if pos_interpolada:
            base = pos_interpolada
        else:
            base = self.casas_x_y.get(jogador.posicao, self.casas_x_y[0])
        
        offset = (jogador_idx * 18, 0)
        return (base[0] + offset[0], base[1] + offset[1])

    def run(self):
        while self.running:
            self.clock.tick(60)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if not self.animacao.ativa and not self.animacao.tem_passos_pendentes():
                            jogador_atual = self.jogadores[self.current_player_idx]
                            dados = jogador_atual.dados.lancar()
                            valor_total = sum(dados)
                            self.valor_dado1, self.valor_dado2 = dados[0], dados[1]
                            
                            print(f"\n=== Turno do Jogador {self.current_player_idx} ({jogador_atual.peca}) ===")
                            print(f"Dados: {dados} = {valor_total}")
                            print(f"Posição inicial: {jogador_atual.posicao}")
                            
                            self.animacao.iniciar(self.current_player_idx, jogador_atual, valor_total)
            
            # Animation management
            if not self.animacao.ativa and self.animacao.tem_passos_pendentes():
                self.animacao.proximo_passo(self.jogadores[self.animacao.jogador_idx])
            
            if not self.animacao.ativa and not self.animacao.tem_passos_pendentes() and self.animacao.jogador_idx is not None:
                jogador_atual = self.jogadores[self.current_player_idx]
                print(f"Posição final: {jogador_atual.posicao}")
                print(f"Casa: {self.casas_x_y.get(jogador_atual.posicao, 'desconhecida')}")
                
                self.current_player_idx = (self.current_player_idx + 1) % len(self.jogadores)
                self.animacao.finalizar()
                print(f"\n>>> Próximo turno: Jogador {self.current_player_idx} ({self.jogadores[self.current_player_idx].peca})")
            
            pos_interpolada = None
            if self.animacao.ativa:
                pos_interpolada = self.animacao.atualizar(self.jogadores[self.animacao.jogador_idx])
            
            # Rendering
            frame_surface = self.background.copy()
            frame_surface.blit(self.tabuleiro_img, (328, 0))
            
            for i, jogador in enumerate(self.jogadores):
                draw_pos = self.get_draw_pos(i, pos_interpolada if self.animacao.ativa and i == self.animacao.jogador_idx else None)
                frame_surface.blit(self.icon_jogadores[i], draw_pos)
            
            texto_dado1 = self.font.render(str(self.valor_dado1), True, (255, 255, 255))
            texto_dado2 = self.font.render(str(self.valor_dado2), True, (255, 255, 255))
            
            frame_surface.blit(texto_dado1, (1190, 540))
            frame_surface.blit(texto_dado2, (1230, 540))

            # Convert to texture and render
            game_texture = Texture.from_surface(self.renderer, frame_surface)
            self.renderer.clear()
            self.renderer.blit(game_texture)
            self.renderer.present()