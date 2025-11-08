import os
from src.ui.button import Button
from src.ui.modal_interface import Modal
import pygame, sys

class CreditsModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock):
        super().__init__(x, y, modal_image, screen, clock)
        back_button_image = pygame.image.load(os.path.join("assets", "botao-voltar-roxo.png")).convert_alpha()
        self.back_button = Button(807, 564, back_button_image) 
    
    def show(self):
        showing = True
        while showing:
            # Capture the screen state before drawing the modal
            background_surface = self.screen.copy()

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.back_button.handle_event(event):
                    showing = False 
            
            self.back_button.update_hover(mouse_pos)

            # Draw the modal components
            self.screen.blit(background_surface, (0, 0)) # Redraw the background
            self.screen.blit(self.modal_image, self.modal_rect)
            self.back_button.draw_to_surface(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)