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


        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        fonte = os.path.join(assets_dir, 'fonte')
        fonte_path = os.path.join(fonte, 'LilitaOne-Regular.ttf')

        # Fonts
        self.title_font = pygame.font.Font(fonte_path, 24)
        self.price_font = pygame.font.Font(fonte_path, 24)

        # Buttons
        sim_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-sim.png')).convert_alpha()
        nao_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-nao.png')).convert_alpha()
        self.new_property_image = pygame.image.load(os.path.join(assets_dir, 'buy_property.png')).convert_alpha()
        CARD_SCALE = 1  # Escala da carta

        # Redimensiona a carta
        orig_w, orig_h = self.new_property_image.get_size()
        new_w = int(orig_w * CARD_SCALE)
        new_h = int(orig_h * CARD_SCALE)
        if new_w <= 0: new_w = 1
        if new_h <= 0: new_h = 1
        self.new_property_image = pygame.transform.smoothscale(self.new_property_image, (new_w, new_h))
        
        # Centraliza na tela
        screen_w, screen_h = screen.get_size()
        self.carta_x = (screen_w - new_w) // 2
        self.carta_y = (screen_h - new_h) // 2

        # Adjust positions for the larger, scaled modal
        # Title (Property Name)
        self.title_surf = self.title_font.render(self.imovel.nome, True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 55))
        
        # Price
        price_text = f"{self.imovel.preco}"
        self.price_surf = self.price_font.render(price_text, True, (255, 255, 255))
        self.price_rect = self.price_surf.get_rect(center=(self.modal_rect.centerx + 17, self.modal_rect.y + 123))

        # Buttons
        btn_y = self.modal_rect.y + 200
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
            self.screen.blit(self.new_property_image, (self.carta_x, self.carta_y)) # Draw the property image
            self.screen.blit(self.title_surf, self.title_rect)
            self.screen.blit(self.price_surf, self.price_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.decision