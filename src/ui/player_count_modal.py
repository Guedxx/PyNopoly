import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

def create_text_button(text, width, height, font):
    """Helper function to create a button surface with text."""
    button_surface = pygame.Surface((width, height))
    button_surface.fill((255, 170, 216))  # A simple rose color
    pygame.draw.rect(button_surface, (255, 255, 255), button_surface.get_rect(), 2) # White border

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(width // 2, height // 2))
    button_surface.blit(text_surf, text_rect)
    return button_surface

class PlayerCountModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, background_surface):
        
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.new_background_image = pygame.image.load(os.path.join(assets_dir, 'number_players.png')).convert_alpha()
        self.new_background_image = pygame.transform.scale(
            self.new_background_image, screen.get_size()
        )

        super().__init__(x, y, modal_image, screen, clock, background_surface)
        self.player_count = None
        
        font = pygame.font.Font(None, 48)
        title_font = pygame.font.Font(None, 36)
        
        # Create buttons
        btn_w, btn_h = 80, 60
        btn_y = self.modal_rect.centery
        
        btn_2_surf = create_text_button("2", btn_w, btn_h, font)
        btn_3_surf = create_text_button("3", btn_w, btn_h, font)
        btn_4_surf = create_text_button("4", btn_w, btn_h, font)

        self.button_2 = Button(self.modal_rect.centerx - 150, btn_y, btn_2_surf, lambda: self.set_count(2))
        self.button_3 = Button(self.modal_rect.centerx - (btn_w // 2), btn_y, btn_3_surf, lambda: self.set_count(3))
        self.button_4 = Button(self.modal_rect.centerx + 150 - btn_w, btn_y, btn_4_surf, lambda: self.set_count(4))
        
        self.buttons = [self.button_2, self.button_3, self.button_4]

    def set_count(self, count):
        self.player_count = count

    def show(self):
        showing = True
        self.player_count = None # Reset before showing
        while showing:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False
                
                for button in self.buttons:
                    if button.handle_event(event):
                        showing = False
                        break
                if not showing:
                    break
            
            # Drawing
            self.screen.blit(self.new_background_image, (0, 0))
            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.player_count
