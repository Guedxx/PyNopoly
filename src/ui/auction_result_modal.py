import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class AuctionResultModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, imovel, vencedor, lance):
        
        super().__init__(x, y, modal_image, screen, clock)
        
        self.imovel = imovel
        self.vencedor = vencedor
        self.lance = lance

        # Fonts
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        fonte = os.path.join(assets_dir, 'fonte')
        fonte_path = os.path.join(fonte, 'LilitaOne-Regular.ttf')

        self.font = pygame.font.Font(fonte_path, 22)
        self.title_font = pygame.font.Font(fonte_path, 22)
        self.price_font = pygame.font.Font(fonte_path, 22)

        # Buttons
        ok_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-ok.png')).convert_alpha()
        self.new_auction_image = pygame.image.load(os.path.join(assets_dir, 'leilao_vencedor.png')).convert_alpha()
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

        # Title
        title_surf = self.title_font.render("Leilão", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 50))
        self.screen.blit(title_surf, title_rect)

        if self.vencedor:
            # Winner text
            vencedor_text = f"{self.vencedor.nome}"
            vencedor_surf = self.font.render(vencedor_text, True, (255, 255, 255))
            vencedor_rect = vencedor_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 100))
            self.screen.blit(vencedor_surf, vencedor_rect)

            # Property name
            imovel_text = f"{self.imovel.nome}"
            imovel_surf = self.font.render(imovel_text, True, (255, 255, 255))
            imovel_rect = imovel_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 140))
            self.screen.blit(imovel_surf, imovel_rect)

            # Price
            lance_text = f"{self.lance}"
            lance_surf = self.price_font.render(lance_text, True, (255, 255, 255))
            lance_rect = lance_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 190))
            self.screen.blit(lance_surf, lance_rect)
        else:
            # No winner text
            no_winner_text = "Leilão terminou sem vencedor."
            no_winner_surf = self.font.render(no_winner_text, True, (255, 255, 255))
            no_winner_rect = no_winner_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 120))
            self.screen.blit(no_winner_surf, no_winner_rect)


        # Buttons
        btn_y = self.modal_rect.y + 250
        self.ok_button = Button(self.modal_rect.centerx - ok_button_img.get_width() // 2, btn_y, ok_button_img, self.close)
        
        self.buttons = [self.ok_button]
        self.should_close = False

    def close(self):
        self.should_close = True

    def show(self):
        self.should_close = False
        background_capture = self.screen.copy()

        while not self.should_close:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                for button in self.buttons:
                    button.handle_event(event)
            
            # Drawing
            self.screen.blit(background_capture, (0, 0))
            self.screen.blit(self.new_auction_image, (self.carta_x, self.carta_y))

            if self.vencedor:
                # Winner text
                vencedor_text = f"{self.vencedor.nome}"
                vencedor_surf = self.font.render(vencedor_text, True, (255, 255, 255))
                vencedor_rect = vencedor_surf.get_rect(center=(self.modal_rect.centerx+50, self.modal_rect.y + 80))
                self.screen.blit(vencedor_surf, vencedor_rect)

                # Property name
                imovel_text = f"{self.imovel.nome}"
                imovel_surf = self.font.render(imovel_text, True, (255, 255, 255))
                imovel_rect = imovel_surf.get_rect(center=(self.modal_rect.centerx+20, self.modal_rect.y + 175))
                self.screen.blit(imovel_surf, imovel_rect)

                # Price
                lance_text = f"{self.lance}"
                lance_surf = self.price_font.render(lance_text, True, (255, 255, 255))
                lance_rect = lance_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 128))
                self.screen.blit(lance_surf, lance_rect)
            else:
                # No winner text
                no_winner_text = "Leilão terminou sem vencedor."
                no_winner_surf = self.font.render(no_winner_text, True, (255, 255, 255))
                no_winner_rect = no_winner_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 120))
                self.screen.blit(no_winner_surf, no_winner_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
