import os
from src.ui.character_card import CharacterCard
from src.ui.modal_interface import Modal
import pygame, sys

class SelectCharacterModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock):
        super().__init__(x, y, modal_image, screen, clock)
        self.character_cards = {}
        self.create_character_cards()
        self.selected_character = None
    
    def create_character_cards(self):
        assets_dir = os.path.join("assets", "characters")

        characters = [
            ("hellokitty", 465, 264),
            ("kuromi", 601, 264),
            ("cinnamoroll", 737, 264),
            ("mymelody", 465, 428),
            ("pompompurin", 601, 428),
            ("keroppi", 737, 428),
        ]

        for name, x, y in characters:
            normal_img = pygame.image.load(
                os.path.join(assets_dir, f"card-{name}.png")
            ).convert_alpha()

            hover_img = pygame.image.load(
                os.path.join(assets_dir, f"card-{name}-hover.png")
            ).convert_alpha()

            self.character_cards[name] = CharacterCard(
                x, y,
                normal_img,
                hover_img,
                callback=lambda n=name: self.select_character(n)
            )

    def select_character(self, name):
        self.selected_character = name

    def show(self, available_characters):
        showing = True
        self.selected_character = None

        # Filter cards to only show available characters
        active_cards = {name: card for name, card in self.character_cards.items() if name in available_characters}

        while showing:
            background_surface = self.screen.copy()
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False
                
                for card in active_cards.values():
                    if card.handle_event(event):
                        showing = False
                        break
                if not showing:
                    break
            
            self.screen.blit(background_surface, (0, 0))
            self.screen.blit(self.modal_image, self.modal_rect)

            for char_name, card in self.character_cards.items():
                is_active = char_name in active_cards
                card.update_hover(mouse_pos if is_active else (-1, -1)) # Update hover only if active
                card.draw_to_surface(self.screen) # Let the card draw itself

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.selected_character
