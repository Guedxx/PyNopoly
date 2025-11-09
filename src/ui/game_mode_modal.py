import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class GameModeModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, background_surface):
        
        super().__init__(x, y, modal_image, screen, clock, background_surface)
        
        self.selected_mode = None

        # Buttons
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'modo-jogo')
        pvp_button_img = pygame.image.load(os.path.join(assets_dir, 'button-pvp.png')).convert_alpha()
        ias_button_img = pygame.image.load(os.path.join(assets_dir, 'button-ias.png')).convert_alpha()

        # Position buttons
        btn_y = self.modal_rect.y + 150
        button_spacing = 40
        total_buttons_width = pvp_button_img.get_width() + ias_button_img.get_width() + button_spacing
        start_x = self.modal_rect.centerx - (total_buttons_width // 2)

        self.pvp_button = Button(start_x, btn_y, pvp_button_img, lambda: self.set_mode("pvp"))
        # The AI button does nothing for now
        self.ias_button = Button(start_x + pvp_button_img.get_width() + button_spacing, btn_y, ias_button_img, lambda: None)
        
        self.buttons = [self.pvp_button, self.ias_button]

    def set_mode(self, mode):
        self.selected_mode = mode

    def show(self):
        showing = True
        self.selected_mode = None

        while showing:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False
                
                if self.pvp_button.handle_event(event):
                    showing = False
                
                self.ias_button.handle_event(event)

                if not showing:
                    break
            
            self.screen.blit(self.background_surface, (0, 0))
            self.screen.blit(self.modal_image, self.modal_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.selected_mode
