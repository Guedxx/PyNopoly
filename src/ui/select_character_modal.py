import os
from src.ui.character_card import CharacterCard
from src.ui.modal_interface import Modal
import pygame, sys

class SelectCharacterModal(Modal):
    def __init__(self, x, y, modal_image, screen, clock, background_surface):
        super().__init__(x, y, modal_image, screen, clock, background_surface)
        self.character_cards = {}
        self.create_character_cards()
        self.selected_character = None
    
    def create_character_cards(self):
        assets_dir = os.path.join("assets", "select-character")

        # Map full character names to asset filenames
        character_asset_map = {
            "hellokitty": "kitty",
            "keroppi": "keropi",
            "kuromi": "kuromi",
            "mymelody": "melody",
            "pompompurin": "pompom",
            "cinnamoroll": "cinnamon"
        }

        characters_data = [
            ("hellokitty", 425, 264),
            ("kuromi", 561, 264),
            ("cinnamoroll", 697, 264),
            ("mymelody", 425, 413),
            ("pompompurin", 561, 413),
            ("keroppi", 697, 413),
        ]

        for name, x, y in characters_data:
            asset_name = character_asset_map.get(name)
            if asset_name:
                normal_img = pygame.image.load(
                    os.path.join(assets_dir, f"{asset_name}.png")
                ).convert_alpha()

                # Use the same image for hover as there are no separate hover assets
                hover_img = normal_img 

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

        active_cards = {name: card for name, card in self.character_cards.items() if name in available_characters}

        while showing:
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
            
            self.screen.blit(self.background_surface, (0, 0))
            self.screen.blit(self.modal_image, self.modal_rect)

            for char_name, card in self.character_cards.items():
                is_active = char_name in active_cards
                card.update_hover(mouse_pos if is_active else (-1, -1))
                card.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.selected_character