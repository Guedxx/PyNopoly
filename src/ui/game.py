import os
import sys
import pygame
from pygame import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.engine.Jogador import Jogador
from src.ui.animation import AnimacaoMovimento
from src.engine.Partida import Partida
from src.engine.Fabricas import TabuleiroPadraoFactory
from src.ui.buy_property_modal import BuyPropertyModal
from src.ui.tax_modal import TaxModal
from src.ui.button import Button

class Game:
    def __init__(self, selected_characters, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.height = 720
        self.width = 1280
        self.font = pygame.font.Font(None, 36)
        
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.background = pygame.image.load(os.path.join(assets_dir, 'gamebg.png')).convert()
        self.tabuleiro_img = pygame.image.load(os.path.join(assets_dir, 'tabuleirobase.png')).convert_alpha()
        
        self.running = True
        self.valor_dado1 = 0
        self.valor_dado2 = 0
        self.game_state = "AWAITING_ROLL"
        self.last_roll_was_double = False
        
        factory = TabuleiroPadraoFactory()
        self.partida = Partida(selected_characters, factory)
        self.partida.iniciar_jogo()
        self.jogadores = self.partida.jogadores

        # --- Asset Loading ---
        # Map full character names to asset filenames
        character_asset_map = {
            "hellokitty": "kitty",
            "keroppi": "keropi",
            "kuromi": "kuromi",
            "mymelody": "melody",
            "pompompurin": "pompom",
            "cinnamoroll": "cinnamon"
        }

        # Load character pawns (board pieces)
        board_pieces_dir = os.path.join(assets_dir, 'board_pieces')
        self.character_icons = {}
        for name, asset_name in character_asset_map.items():
            try:
                path = os.path.join(board_pieces_dir, f'piece-{asset_name}.png')
                self.character_icons[name] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                print(f"Aviso: Imagem da peça do personagem '{name}' não encontrada.")
        self.character_icons["default"] = pygame.image.load(os.path.join(assets_dir, 'icone-gato.png')).convert_alpha()

        # Load player cards (for corners)
        cards_dir = os.path.join(assets_dir, 'cards')
        self.player_cards = {}
        for jogador in self.jogadores:
            asset_name = character_asset_map.get(jogador.nome)
            if asset_name:
                try:
                    path = os.path.join(cards_dir, f'card-{asset_name}.png')
                    self.player_cards[jogador.nome] = pygame.image.load(path).convert_alpha()
                except pygame.error:
                    print(f"Aviso: Imagem do card do jogador '{jogador.nome}' não encontrada.")
        
        # Pre-load and scale modal images
        unscaled_buy_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-comprar-propriedade.png')).convert_alpha()
        original_width = unscaled_buy_modal_image.get_width()
        original_height = unscaled_buy_modal_image.get_height()
        scaled_width = int(original_width * 1.3)
        scaled_height = int(original_height * 1.3)
        self.buy_property_modal_image = pygame.transform.smoothscale(unscaled_buy_modal_image, (scaled_width, scaled_height))
        self.buy_property_modal_width = self.buy_property_modal_image.get_width()
        self.buy_property_modal_height = self.buy_property_modal_image.get_height()

        unscaled_tax_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-taxa-riqueza.png')).convert_alpha()
        original_tax_width = unscaled_tax_modal_image.get_width()
        original_tax_height = unscaled_tax_modal_image.get_height()
        scaled_tax_width = int(original_tax_width * 1.3)
        scaled_tax_height = int(original_tax_height * 1.3)
        self.tax_modal_image = pygame.transform.smoothscale(unscaled_tax_modal_image, (scaled_tax_width, scaled_tax_height))
        self.tax_modal_width = self.tax_modal_image.get_width()
        self.tax_modal_height = self.tax_modal_image.get_height()

        self.dice_display_image = pygame.image.load(os.path.join(assets_dir, 'mostrador-dados.png')).convert_alpha()
        roll_dice_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-rodar-dados.png')).convert_alpha()
        self.roll_dice_button = Button(1090, 530, roll_dice_button_img, self.trigger_roll_dice)

        # Board positions and animation
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

    def trigger_roll_dice(self):
        if self.game_state == "AWAITING_ROLL":
            self.game_state = "BUSY"
            result = self.partida.iniciar_turno()
            self.handle_engine_result(result)

    def run(self):
        while self.running:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.trigger_roll_dice()
                self.roll_dice_button.handle_event(event)

            if self.game_state == "ANIMATING":
                if not self.animacao.ativa and self.animacao.tem_passos_pendentes():
                    self.animacao.proximo_passo()
                elif not self.animacao.ativa and not self.animacao.tem_passos_pendentes():
                    self.game_state = "BUSY"
                    result = self.partida.executar_acao_pos_movimento()
                    self.handle_engine_result(result)
            
            pos_interpolada = None
            if self.animacao.ativa:
                jogador_animado = self.jogadores[self.animacao.jogador_idx]
                pos_interpolada = self.animacao.atualizar(jogador_animado)

            self.screen.blit(self.background, (0, 0))
            
            card_positions = [ (0, 0), (self.width, 0), (0, self.height), (self.width, self.height) ]
            for i, jogador in enumerate(self.jogadores):
                if i < 4:
                    card_surface = self.player_cards.get(jogador.nome)
                    if card_surface:
                        pos = card_positions[i]
                        rect = card_surface.get_rect()
                        if pos[0] > 0: rect.right = pos[0]
                        else: rect.left = pos[0]
                        if pos[1] > 0: rect.bottom = pos[1]
                        else: rect.top = pos[1]
                        self.screen.blit(card_surface, rect)

                        money_text = f"{jogador.dinheiro}"
                        money_surface = self.font.render(money_text, True, (255, 255, 255))
                        text_pos = (rect.left + 150, rect.top + 30)
                        self.screen.blit(money_surface, text_pos)

            self.screen.blit(self.tabuleiro_img, (328, 0))
            
            for i, jogador in enumerate(self.jogadores):
                is_animating = self.animacao.ativa and i == self.animacao.jogador_idx
                current_pos = pos_interpolada if is_animating else None
                draw_pos = self.get_draw_pos(jogador, current_pos)
                
                icon_surface = self.character_icons.get(jogador.nome, self.character_icons["default"])
                self.screen.blit(icon_surface, draw_pos)
            
            self.screen.blit(self.dice_display_image, (1141, 530))
            texto_dado1 = self.font.render(str(self.valor_dado1), True, (255, 255, 255))
            texto_dado2 = self.font.render(str(self.valor_dado2), True, (255, 255, 255))
            self.screen.blit(texto_dado1, (1200, 540))
            self.screen.blit(texto_dado2, (1240, 540))

            self.roll_dice_button.update_hover(mouse_pos)
            self.roll_dice_button.draw_to_surface(self.screen)

            pygame.display.flip()

    def handle_engine_result(self, result):
        if not result:
            return

        acao = result.get("acao")
        
        if acao == "moveu":
            self.valor_dado1, self.valor_dado2 = result["dados"][0], result["dados"][1]
            self.last_roll_was_double = result["is_double"]
            try:
                jogador_idx = self.jogadores.index(result["jogador"])
                self.animacao.iniciar(jogador_idx, result["path"], result["posicao_anterior"])
                if self.animacao.tem_passos_pendentes():
                    self.animacao.proximo_passo()
                self.game_state = "ANIMATING"
            except ValueError:
                self.game_state = "AWAITING_ROLL"

        elif acao == "proposta_compra":
            modal_x = (self.width - self.buy_property_modal_width) // 2
            modal_y = (self.height - self.buy_property_modal_height) // 2
            modal = BuyPropertyModal(modal_x, modal_y, self.buy_property_modal_image, self.screen, self.clock, result["imovel"])
            decision = modal.show()
            self.partida.resolver_compra(decision)
            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)

        elif acao == "pagar_imposto":
            modal_x = (self.width - self.tax_modal_width) // 2
            modal_y = (self.height - self.tax_modal_height) // 2
            modal = TaxModal(modal_x, modal_y, self.tax_modal_image, self.screen, self.clock, result["imposto"])
            modal.show()
            self.partida.resolver_pagamento_imposto()
            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)

        elif acao == "turno_finalizado":
            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)
        
        elif acao == "movido_por_carta":
            try:
                jogador_idx = self.jogadores.index(self.partida.jogadores[self.partida.jogador_atual_idx])
                pos_anterior = self.partida.jogadores[jogador_idx].posicao
                self.animacao.iniciar(jogador_idx, result["path"], pos_anterior)
                if self.animacao.tem_passos_pendentes():
                    self.animacao.proximo_passo()
                self.game_state = "ANIMATING"
            except ValueError:
                self.game_state = "AWAITING_ROLL"

        elif acao in ["preso", "foi_preso_por_doubles", "turno_pronto_para_iniciar"]:
            self.game_state = "AWAITING_ROLL"
        
        elif acao == "fim_de_jogo":
            self.running = False
