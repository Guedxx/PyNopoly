import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class BuyPropertyModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, imovel):
        
        super().__init__(x, y, modal_image, screen, clock)
        
        self.imovel = imovel
        self.decision = None # True for buy, False for not buy

        # Fonts
        self.title_font = pygame.font.Font(None, 42)
        self.price_font = pygame.font.Font(None, 52)

        # Buttons
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        sim_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-sim.png')).convert_alpha()
        nao_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-nao.png')).convert_alpha()

        # Adjust positions for the larger, scaled modal
        # Title (Property Name)
        self.title_surf = self.title_font.render(self.imovel.nome, True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 70))
        
        # Price
        price_text = f"{self.imovel.preco}"
        self.price_surf = self.price_font.render(price_text, True, (255, 255, 255))
        self.price_rect = self.price_surf.get_rect(center=(self.modal_rect.centerx + 37, self.modal_rect.y + 153))

        # Buttons
        btn_y = self.modal_rect.y + 230
        button_spacing = 30
        total_buttons_width = sim_button_img.get_width() + nao_button_img.get_width() + button_spacing
        start_x = self.modal_rect.centerx - (total_buttons_width // 2)

        self.sim_button = Button(start_x, btn_y, sim_button_img, lambda: self.set_decision(True))
        self.nao_button = Button(start_x + sim_button_img.get_width() + button_spacing, btn_y, nao_button_img, lambda: self.set_decision(False))
        
        self.buttons = [self.sim_button, self.nao_button]

    def set_decision(self, decision):
        self.decision = decision

    def show(self):
        showing = True
        self.decision = None

        # Capture the current screen state to use as the background
        background_capture = self.screen.copy()

        while showing:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                for button in self.buttons:
                    if button.handle_event(event):
                        showing = False
                        break
                if not showing:
                    break
            
            # Drawing
            self.screen.blit(background_capture, (0, 0)) # Redraw the background
            self.screen.blit(self.modal_image, self.modal_rect)
            self.screen.blit(self.title_surf, self.title_rect)
            self.screen.blit(self.price_surf, self.price_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.decision