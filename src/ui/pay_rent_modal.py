import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class PayRentModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, imovel):
        
        super().__init__(x, y, modal_image, screen, clock)
        
        self.imovel = imovel

        # Fonts
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 42)
        self.price_font = pygame.font.Font(None, 52)

        # Buttons
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        ok_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-ok.png')).convert_alpha()

        # Title (Property Name)
        self.title_surf = self.title_font.render(self.imovel.nome, True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 70))
        
        # Owner
        owner_text = f"{self.imovel.dono.nome}"
        self.owner_surf = self.font.render(owner_text, True, (255, 255, 255))
        self.owner_rect = self.owner_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 120))

        # Rent
        rent_text = f"pague {self.imovel.calcular_aluguel()}"
        self.rent_surf = self.price_font.render(rent_text, True, (255, 255, 255))
        self.rent_rect = self.rent_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 170))

        # Buttons
        btn_y = self.modal_rect.y + 215
        self.ok_button = Button(self.modal_rect.centerx - ok_button_img.get_width() // 2, btn_y, ok_button_img, self.close)
        
        self.buttons = [self.ok_button]
        self.should_close = False

    def close(self):
        self.should_close = True

    def show(self):
        self.should_close = False

        # Capture the current screen state to use as the background
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
            self.screen.blit(background_capture, (0, 0)) # Redraw the background
            self.screen.blit(self.modal_image, self.modal_rect)
            self.screen.blit(self.title_surf, self.title_rect)
            self.screen.blit(self.owner_surf, self.owner_rect)
            self.screen.blit(self.rent_surf, self.rent_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
