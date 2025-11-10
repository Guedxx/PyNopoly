import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class AuctionModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, imovel, jogadores, partida):
        
        super().__init__(x, y, modal_image, screen, clock)
        
        self.imovel = imovel
        self.jogadores = jogadores
        self.partida = partida

        # Fonts
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        fonte = os.path.join(assets_dir, 'fonte')
        fonte_path = os.path.join(fonte, 'LilitaOne-Regular.ttf')
        self.font = pygame.font.Font(fonte_path, 22)
        self.title_font = pygame.font.Font(fonte_path, 22)
        self.price_font = pygame.font.Font(fonte_path, 22)

        # Buttons
        lance_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-dar-lance.png')).convert_alpha()
        desistir_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-desistir.png')).convert_alpha()

        self.new_auction_image = pygame.image.load(os.path.join(assets_dir, 'leilao_card.png')).convert_alpha()
        CARD_SCALE = 1  # Escala da carta

        # Redimensiona a carta
        orig_w, orig_h = self.new_auction_image.get_size()
        new_w = int(orig_w * CARD_SCALE)
        new_h = int(orig_h * CARD_SCALE)
        if new_w <= 0: new_w = 1
        if new_h <= 0: new_h = 1
        self.new_auction_image = pygame.transform.smoothscale(self.new_auction_image, (new_w, new_h))
        
        # Centraliza na tela
        screen_w, screen_h = screen.get_size()
        self.carta_x = (screen_w - new_w) // 2
        self.carta_y = (screen_h - new_h) // 2

        # Input box
        self.input_rect = pygame.Rect(self.modal_rect.centerx - 100, self.modal_rect.y + 230, 200, 40)
        self.input_text = ""
        self.input_active = False

        # Buttons
        btn_y = self.modal_rect.y + 280
        self.lance_button = Button(self.modal_rect.centerx - lance_button_img.get_width() - 10, btn_y, lance_button_img, self.dar_lance)
        self.desistir_button = Button(self.modal_rect.centerx + 10, btn_y, desistir_button_img, self.desistir)
        
        self.buttons = [self.lance_button, self.desistir_button]
        self.should_close = False

    def dar_lance(self):
        try:
            valor = int(self.input_text)
            jogador_atual = self.partida.jogadores_leilao[self.partida.leilao_jogador_atual_idx]
            self.partida.dar_lance(jogador_atual, valor)
            self.input_text = ""
            
            if len(self.partida.jogadores_leilao) > 1:
                self.partida.leilao_jogador_atual_idx = (self.partida.leilao_jogador_atual_idx + 1) % len(self.partida.jogadores_leilao)
            else:
                self.should_close = True

        except (ValueError, IndexError):
            print("Invalid bid")

    def desistir(self):
        if not self.partida.jogadores_leilao:
            self.should_close = True
            return

        jogador_atual = self.partida.jogadores_leilao[self.partida.leilao_jogador_atual_idx]
        self.partida.desistir_leilao(jogador_atual)
        
        if len(self.partida.jogadores_leilao) <= 1:
            self.should_close = True
        elif self.partida.leilao_jogador_atual_idx >= len(self.partida.jogadores_leilao):
            self.partida.leilao_jogador_atual_idx = 0


    def show(self):
        self.should_close = False
        background_capture = self.screen.copy()

        while not self.should_close:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(event.pos):
                        self.input_active = not self.input_active
                    else:
                        self.input_active = False

                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.dar_lance()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

                for button in self.buttons:
                    button.handle_event(event)
            
            # Drawing
            self.screen.blit(background_capture, (0, 0))
            self.screen.blit(self.new_auction_image, (self.carta_x, self.carta_y))

            # Title
            title_surf = self.title_font.render(f"{self.imovel.nome}", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.modal_rect.centerx+20, self.modal_rect.y + 51))
            self.screen.blit(title_surf, title_rect)

            # Highest bid
            maior_lance_text = f"{self.partida.maior_lance}"
            maior_lance_surf = self.font.render(maior_lance_text, True, (255, 255, 255))
            maior_lance_rect = maior_lance_surf.get_rect(center=(self.modal_rect.centerx+40, self.modal_rect.y + 98))
            self.screen.blit(maior_lance_surf, maior_lance_rect)

            # Bid author
            if self.partida.jogador_maior_lance:
                autor_text = f"{self.partida.jogador_maior_lance.nome}"
                autor_surf = self.font.render(autor_text, True, (255, 255, 255))
                autor_rect = autor_surf.get_rect(center=(self.modal_rect.centerx+10, self.modal_rect.y + 140))
                self.screen.blit(autor_surf, autor_rect)

            # Current player
            if not self.partida.jogadores_leilao or self.partida.leilao_jogador_atual_idx >= len(self.partida.jogadores_leilao):
                self.should_close = True
                continue
            
            jogador_atual = self.partida.jogadores_leilao[self.partida.leilao_jogador_atual_idx]
            jogador_text = f"{jogador_atual.nome}"
            jogador_surf = self.font.render(jogador_text, True, (255, 255, 255))
            jogador_rect = jogador_surf.get_rect(center=(self.modal_rect.centerx+10, self.modal_rect.y + 190))
            self.screen.blit(jogador_surf, jogador_rect)

            # Input box
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
            input_surf = self.font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(input_surf, (self.input_rect.x + 5, self.input_rect.y + 5))

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        
        return self.partida.jogador_maior_lance, self.partida.maior_lance
