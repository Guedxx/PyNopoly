import pygame

class Button:
    def __init__(self, x, y, image, callback=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        self.is_hovered = False

    def handle_event(self, event):
        """Handle mouse click events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False

    def update_hover(self, mouse_pos):
        """Update hover state for visual feedback"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

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