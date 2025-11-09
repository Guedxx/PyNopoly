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
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 42)
        self.price_font = pygame.font.Font(None, 52)

        # Buttons
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        ok_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-ok.png')).convert_alpha()

        # Title
        title_surf = self.title_font.render("Leilão", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 50))
        self.screen.blit(title_surf, title_rect)

        if self.vencedor:
            # Winner text
            vencedor_text = f"{self.vencedor.nome} venceu o leilão e adquiriu"
            vencedor_surf = self.font.render(vencedor_text, True, (255, 255, 255))
            vencedor_rect = vencedor_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 100))
            self.screen.blit(vencedor_surf, vencedor_rect)

            # Property name
            imovel_text = f"{self.imovel.nome}"
            imovel_surf = self.font.render(imovel_text, True, (255, 255, 255))
            imovel_rect = imovel_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 140))
            self.screen.blit(imovel_surf, imovel_rect)

            # Price
            lance_text = f"por $ {self.lance}"
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
            self.screen.blit(self.modal_image, self.modal_rect)

            if self.vencedor:
                # Winner text
                vencedor_text = f"{self.vencedor.nome} venceu o leilão e adquiriu"
                vencedor_surf = self.font.render(vencedor_text, True, (255, 255, 255))
                vencedor_rect = vencedor_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 100))
                self.screen.blit(vencedor_surf, vencedor_rect)

                # Property name
                imovel_text = f"{self.imovel.nome}"
                imovel_surf = self.font.render(imovel_text, True, (255, 255, 255))
                imovel_rect = imovel_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 140))
                self.screen.blit(imovel_surf, imovel_rect)

                # Price
                lance_text = f"por $ {self.lance}"
                lance_surf = self.price_font.render(lance_text, True, (255, 255, 255))
                lance_rect = lance_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 190))
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
