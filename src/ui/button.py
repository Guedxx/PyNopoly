import pygame
import os

class Button:
    def __init__(self, x, y, image, callback=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        self.is_hovered = False
        
        # Load sound
        sound_path = os.path.join('sounds', 'button.wav')
        self.click_sound = pygame.mixer.Sound(sound_path)

        hover_sound_path = os.path.join('sounds', 'hover.wav')
        if os.path.exists(hover_sound_path):
            self.hover_sound = pygame.mixer.Sound(hover_sound_path)
        else:
            self.hover_sound = None

    def handle_event(self, event):
        """Handle mouse click events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.click_sound.play() # Play sound on click
                if self.callback:
                    self.callback()
                return True
        return False

    def update_hover(self, mouse_pos):
        """Update hover state for visual feedback"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and not was_hovered and self.hover_sound:
            self.hover_sound.play()

    def draw_to_surface(self, surface):
        """Draw button to a pygame surface"""
        surface.blit(self.image, self.rect)
        if self.is_hovered:
            darken_surface = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
            darken_surface.fill((0, 0, 0, 50))  # Black with 50 alpha

            # Create a temporary surface to apply the darkening within the button's shape
            temp_surface = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
            temp_surface.blit(self.image, (0, 0)) # Blit the button image onto a transparent surface
            temp_surface.blit(darken_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT) # Apply darkening

            surface.blit(temp_surface, self.rect.topleft)