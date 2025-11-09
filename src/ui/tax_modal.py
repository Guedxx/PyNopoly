import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class TaxModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, imposto):
        
        super().__init__(x, y, modal_image, screen, clock)
        
        self.imposto = imposto
        self.decision = None

        # Fonts (no longer used for rendering text, but kept for consistency if needed later)
        self.title_font = pygame.font.Font(None, 42)
        self.price_font = pygame.font.Font(None, 52)

        # Button
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        ok_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-ok.png')).convert_alpha()
        self.new_taxmodal_image = pygame.image.load(os.path.join(assets_dir, 'tax_modal.png')).convert_alpha()

        # Redimensiona a carta
        orig_w, orig_h = self.new_taxmodal_image.get_size()
        new_w = int(orig_w)
        new_h = int(orig_h)
        if new_w <= 0: new_w = 1
        if new_h <= 0: new_h = 1
        self.new_taxmodal_image = pygame.transform.smoothscale(self.new_taxmodal_image, (new_w, new_h))
        
        # Centraliza na tela
        screen_w, screen_h = screen.get_size()
        self.carta_x = (screen_w - new_w) // 2
        self.carta_y = (screen_h - new_h) // 2


        # OK Button
        btn_y = self.modal_rect.y + 200
        btn_x = self.modal_rect.centerx - (ok_button_img.get_width() // 2)
        self.ok_button = Button(btn_x, btn_y, ok_button_img, lambda: self.set_decision(True))
        
        self.buttons = [self.ok_button]

    def set_decision(self, decision):
        self.decision = decision

    def show(self):
        showing = True
        self.decision = None

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
            
            self.screen.blit(background_capture, (0, 0))
            self.screen.blit(self.new_taxmodal_image, (self.carta_x, self.carta_y))
            # Removed text blitting as image contains text

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.decision
