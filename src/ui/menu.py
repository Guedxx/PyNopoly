import pygame
import sys
import os

from .button import Button
from .credits_modal import CreditsModal
from .select_character_modal import SelectCharacterModal
from .player_count_modal import PlayerCountModal
from .game import Game


class Menu:
    def __init__(self):
        pygame.init()

        # Screen setup
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("PyNopoly")

        # Assets
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        self.menu_surface = pygame.image.load(os.path.join(assets_dir, "menu.png")).convert()
        self.menu_surface = pygame.transform.scale(self.menu_surface, (1280, 720))
        
        start_button_image = pygame.image.load(os.path.join(assets_dir, "botao-jogar.png")).convert_alpha()
        credits_button_image = pygame.image.load(os.path.join(assets_dir, "botao-creditos.png")).convert_alpha()
        exit_button_image = pygame.image.load(os.path.join(assets_dir, "botao-sair.png")).convert_alpha()
        
        credits_image = pygame.image.load(os.path.join(assets_dir, "modal-creditos.png")).convert_alpha()
        select_character_image = pygame.image.load(os.path.join(assets_dir, "modal-selecao-personagem.png")).convert_alpha()
        
        self.title = pygame.image.load(os.path.join(assets_dir, "titulo.png")).convert_alpha()

        # Clock
        self.clock = pygame.time.Clock()

        # Modals
        self.credits_modal = CreditsModal(240, 86, 
                                     credits_image, 
                                     self.screen,
                                     self.clock)
        self.select_character_modal = SelectCharacterModal(240, 120,
                                                      select_character_image,
                                                      self.screen,
                                                      self.clock)
        # Using credits modal background as a generic one for player count
        modal_w = select_character_image.get_width()
        modal_h = select_character_image.get_height()
        modal_x = (self.screen.get_width() - modal_w) // 2
        modal_y = (self.screen.get_height() - modal_h) // 2
        self.player_count_modal = PlayerCountModal(modal_x, modal_y,
                                                   select_character_image.copy(),
                                                   self.screen,
                                                   self.clock)

        # Buttons
        self.start_button = Button(200, 380, start_button_image, self.start_game_flow)
        self.credits_button = Button(200, 470, credits_button_image, self.credits_modal.show)
        self.exit_button = Button(200, 560, exit_button_image, self.exit_game)
    
    def start_game_flow(self):
        selected_char = self.select_character_modal.show()
        if selected_char:
            player_count = self.player_count_modal.show()
            if player_count:
                player_names = [selected_char]
                player_names.extend([f"Jogador {i+2}" for i in range(player_count - 1)])
                
                game = Game(player_names, self.screen)
                game.run()
    
    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()

                # Handle button events
                self.start_button.handle_event(event)
                self.credits_button.handle_event(event)
                self.exit_button.handle_event(event)

            # Update button hover states
            self.start_button.update_hover(mouse_pos)
            self.credits_button.update_hover(mouse_pos)
            self.exit_button.update_hover(mouse_pos)

            # Drawing
            self.screen.blit(self.menu_surface, (0, 0))

            title_rect = self.title.get_rect(center=(1280 // 2, 100))
            self.screen.blit(self.title, title_rect)

            self.start_button.draw_to_surface(self.screen)
            self.credits_button.draw_to_surface(self.screen)
            self.exit_button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)