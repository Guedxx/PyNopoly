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
from src.ui.pay_rent_modal import PayRentModal
from src.ui.auction_modal import AuctionModal
from src.ui.auction_result_modal import AuctionResultModal
from src.ui.build_house_modal import BuildHouseModal
from src.ui.button import Button
from src.ui.mostrar_cartas import mostrar_carta
from src.ui.player_properties_screen import PlayerPropertiesScreen

class Game:
    def __init__(self, selected_characters, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.height = 720
        self.width = 1280
        self.player_banner_buttons = []

        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        fonte = os.path.join(assets_dir, 'fonte')
        fonte_path = os.path.join(fonte, 'LilitaOne-Regular.ttf')
        self.font = pygame.font.Font(fonte_path, 32)
        
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.background = pygame.image.load(os.path.join(assets_dir, 'gamebg.png')).convert()
        
        # Load, scale, and center the board
        original_board_img = pygame.image.load(os.path.join(assets_dir, 'tab.png')).convert_alpha()
        original_board_size = original_board_img.get_size()
        board_scale = 1.21
        scaled_size = (int(original_board_size[0] * board_scale), int(original_board_size[1] * board_scale))
        self.tabuleiro_img = pygame.transform.smoothscale(original_board_img, scaled_size)
        self.tabuleiro_rect = self.tabuleiro_img.get_rect(center=(self.width // 2, self.height // 2))

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
        character_asset_map = {
            "hellokitty": "kitty", "keroppi": "keropi", "kuromi": "kuromi",
            "mymelody": "melody", "pompompurin": "pompom", "cinnamoroll": "cinnamon"
        }

        board_pieces_dir = os.path.join(assets_dir, 'board_pieces')
        self.character_icons = {}
        for name, asset_name in character_asset_map.items():
            try:
                path = os.path.join(board_pieces_dir, f'piece-{asset_name}.png')
                self.character_icons[name] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                print(f"Aviso: Imagem da peça do personagem '{name}' não encontrada.")
        self.character_icons["default"] = pygame.image.load(os.path.join(assets_dir, 'icone-gato.png')).convert_alpha()

        cards_dir = os.path.join(assets_dir, 'banners')
        self.player_cards = {}
        card_positions = [ (0, 0), (self.width, 0), (0, self.height), (self.width, self.height) ]
        for i, jogador in enumerate(self.jogadores):
            asset_name = character_asset_map.get(jogador.nome)
            if asset_name:
                try:
                    path = os.path.join(cards_dir, f'card-{asset_name}.png')
                    card_surface = pygame.image.load(path).convert_alpha()
                    self.player_cards[jogador.nome] = card_surface
                    
                    if i < 4:
                        pos = card_positions[i]
                        rect = card_surface.get_rect()
                        if pos[0] > 0: rect.right = pos[0]
                        else: rect.left = pos[0]
                        if pos[1] > 0: rect.bottom = pos[1]
                        else: rect.top = pos[1]
                        
                        button = Button(rect.x, rect.y, card_surface, lambda j=jogador: self.show_player_properties(j))
                        self.player_banner_buttons.append(button)

                except pygame.error:
                    print(f"Aviso: Imagem do card do jogador '{jogador.nome}' não encontrada.")
        
        # Pre-load and scale modal images
        unscaled_buy_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-comprar-propriedade.png')).convert_alpha()
        original_width, original_height = unscaled_buy_modal_image.get_size()
        scaled_width, scaled_height = int(original_width * 1.3), int(original_height * 1.3)
        self.buy_property_modal_image = pygame.transform.smoothscale(unscaled_buy_modal_image, (scaled_width, scaled_height))
        self.buy_property_modal_width, self.buy_property_modal_height = self.buy_property_modal_image.get_size()

        unscaled_tax_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-taxa-riqueza.png')).convert_alpha()
        original_tax_width, original_tax_height = unscaled_tax_modal_image.get_size()
        scaled_tax_width, scaled_tax_height = int(original_tax_width * 1.3), int(original_tax_height * 1.3)
        self.tax_modal_image = pygame.transform.smoothscale(unscaled_tax_modal_image, (scaled_tax_width, scaled_tax_height))
        self.tax_modal_width, self.tax_modal_height = self.tax_modal_image.get_size()

        unscaled_pay_rent_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-taxa-propriedade.png')).convert_alpha()
        original_pay_rent_width, original_pay_rent_height = unscaled_pay_rent_modal_image.get_size()
        scaled_pay_rent_width, scaled_pay_rent_height = int(original_pay_rent_width * 1.3), int(original_pay_rent_height * 1.3)
        self.pay_rent_modal_image = pygame.transform.smoothscale(unscaled_pay_rent_modal_image, (scaled_pay_rent_width, scaled_pay_rent_height))
        self.pay_rent_modal_width, self.pay_rent_modal_height = self.pay_rent_modal_image.get_size()

        unscaled_auction_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-leilao.png')).convert_alpha()
        original_auction_width, original_auction_height = unscaled_auction_modal_image.get_size()
        scaled_auction_width, scaled_auction_height = int(original_auction_width * 1.3), int(original_auction_height * 1.3)
        self.auction_modal_image = pygame.transform.smoothscale(unscaled_auction_modal_image, (scaled_auction_width, scaled_auction_height))
        self.auction_modal_width, self.auction_modal_height = self.auction_modal_image.get_size()

        unscaled_auction_result_modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-fim-leilao.png')).convert_alpha()
        original_auction_result_width, original_auction_result_height = unscaled_auction_result_modal_image.get_size()
        scaled_auction_result_width, scaled_auction_result_height = int(original_auction_result_width * 1.3), int(original_auction_result_height * 1.3)
        self.auction_result_modal_image = pygame.transform.smoothscale(unscaled_auction_result_modal_image, (scaled_auction_result_width, scaled_auction_result_height))
        self.auction_result_modal_width, self.auction_result_modal_height = self.auction_result_modal_image.get_size()

        self.dice_display_image = pygame.image.load(os.path.join(assets_dir, 'mostrador-dados.png')).convert_alpha()
        roll_dice_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-rodar-dados.png')).convert_alpha()
        self.roll_dice_button = Button(1090, 530, roll_dice_button_img, self.trigger_roll_dice)

        # Board positions and animation
        self.casas_x_y = {
            0: (370, 595), 1: (426, 616), 2: (474, 616), 3: (522, 617), 4: (570, 617), 5: (618, 618), 6: (666, 618), 7: (714, 619), 8: (762, 619), 9: (810, 620), 
            10: (890, 613), 11: (893, 528), 12: (893, 481), 13: (893, 434), 14: (893, 388), 15: (893, 341), 16: (893, 294), 17: (893, 248), 18: (893, 201), 19: (893, 155), 
            20: (884, 112), 21: (866, 108), 22: (818, 108), 23: (771, 108), 24: (723, 108), 25: (676, 108), 26: (628, 108), 27: (581, 108), 28: (533, 108), 29: (486, 109), 
            30: (385, 103), 31: (390, 145), 32: (390, 193), 33: (390, 242), 34: (390, 291), 35: (390, 340), 36: (390, 388), 37: (390, 437), 38: (390, 486), 39: (390, 535)
        }
        self.num_casas = len(self.casas_x_y)
        self.animacao = AnimacaoMovimento(
            self.casas_x_y, 
            self.num_casas
        )

    def get_draw_pos(self, jogador: Jogador, pos_interpolada=None):
        if pos_interpolada:
            base = pos_interpolada
        else:
            base = self.casas_x_y.get(jogador.posicao, self.casas_x_y[0])
        
        try:
            jogador_idx = self.jogadores.index(jogador)
            if jogador.posicao == 0:
                # Custom offset for start position to spread players out
                offsets = [(-10, -10), (10, -10), (-10, 10), (10, 10)]
                offset = offsets[jogador_idx % len(offsets)]
            else:
                # Original offset for other positions
                offset = (jogador_idx * 18, 0)
            return (base[0] + offset[0], base[1] + offset[1])
        except ValueError:
            return base

    def trigger_roll_dice(self):
        if self.game_state == "AWAITING_ROLL":
            self.game_state = "BUSY"
            result = self.partida.iniciar_turno()
            self.handle_engine_result(result)

    def show_player_properties(self, jogador):
        properties_screen = PlayerPropertiesScreen(self.screen, self.clock, jogador)
        properties_screen.run()



    def run(self):
        while self.running:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.trigger_roll_dice()
                
                for button in self.player_banner_buttons:
                    button.handle_event(event)
                
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
            
            # Draw player banners
            for i, button in enumerate(self.player_banner_buttons):
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)
                
                # Draw money on top of the banner
                jogador = self.jogadores[i]
                money_text = f"{jogador.dinheiro}"
                money_surface = self.font.render(money_text, True, (255, 255, 255))
                text_pos = (button.rect.left + 140, button.rect.top + 30)
                self.screen.blit(money_surface, text_pos)


            self.screen.blit(self.tabuleiro_img, self.tabuleiro_rect)
            
            for i, jogador in enumerate(self.jogadores):
                is_animating = self.animacao.ativa and i == self.animacao.jogador_idx
                current_pos = pos_interpolada if is_animating else None
                draw_pos = self.get_draw_pos(jogador, current_pos)
                
                icon_surface = self.character_icons.get(jogador.nome, self.character_icons["default"])
                self.screen.blit(icon_surface, draw_pos)
            
            self.screen.blit(self.dice_display_image, (1141, 530))
            texto_dado1 = self.font.render(str(self.valor_dado1), True, (255, 255, 255))
            texto_dado2 = self.font.render(str(self.valor_dado2), True, (255, 255, 255))
            self.screen.blit(texto_dado1, (1198, 535))
            self.screen.blit(texto_dado2, (1240, 535))

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
            result = self.partida.resolver_compra(decision)
            if result:
                self.handle_engine_result(result)
            else:
                result = self.partida.finalizar_turno(self.last_roll_was_double)
                self.handle_engine_result(result)

        elif acao == "proposta_construir_casa":
            modal = BuildHouseModal(self.screen, self.clock, result["imovel"])
            decision = modal.show()
            self.partida.resolver_construcao(decision)
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

        elif acao == "pagar_aluguel":
            modal_x = (self.width - self.pay_rent_modal_width) // 2
            modal_y = (self.height - self.pay_rent_modal_height) // 2
            modal = PayRentModal(modal_x, modal_y, self.pay_rent_modal_image, self.screen, self.clock, result["imovel"])
            modal.show()
            # The rent payment is already handled by the engine in Imovel.executar_acao
            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)

        elif acao == "iniciar_leilao":
            modal_x = (self.width - self.auction_modal_width) // 2
            modal_y = (self.height - self.auction_modal_height) // 2
            modal = AuctionModal(modal_x, modal_y, self.auction_modal_image, self.screen, self.clock, result["imovel"], result["jogadores"], self.partida)
            vencedor, lance = modal.show()

            if vencedor:
                result_modal_x = (self.width - self.auction_result_modal_width) // 2
                result_modal_y = (self.height - self.auction_result_modal_height) // 2
                result_modal = AuctionResultModal(result_modal_x, result_modal_y, self.auction_result_modal_image, self.screen, self.clock, result["imovel"], vencedor, lance)
                result_modal.show()
                vencedor.comprar_imovel_leilao(result["imovel"], lance)

            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)

        elif acao == "turno_finalizado":
            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)
        
        elif acao == "carta_tirada":
            jogador_atual = self.partida.jogadores[self.partida.jogador_atual_idx]
            mostrar_carta(result["carta"], self.screen, self.clock, jogador_atual, self.jogadores)
            result = self.partida.finalizar_turno(self.last_roll_was_double)
            self.handle_engine_result(result)

        elif acao == "carta_tirada_e_movido":
            jogador_atual = self.partida.jogadores[self.partida.jogador_atual_idx]
            mostrar_carta(result["carta"], self.screen, self.clock, jogador_atual, self.jogadores)
            try:
                jogador_idx = self.jogadores.index(self.partida.jogadores[self.partida.jogador_atual_idx])
                pos_anterior = result["posicao_inicial_carta"]
                self.animacao.iniciar(jogador_idx, result["path"], pos_anterior)
                if self.animacao.tem_passos_pendentes():
                    self.animacao.proximo_passo()
                self.game_state = "ANIMATING"
            except ValueError:
                self.game_state = "AWAITING_ROLL"
        
        elif acao == "movido_por_carta":
            try:
                jogador_idx = self.jogadores.index(self.partida.jogadores[self.partida.jogador_atual_idx])
                pos_anterior = result["posicao_inicial_carta"]
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
