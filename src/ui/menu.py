import pygame
import sys
import os

from .button import Button
from .credits_modal import CreditsModal
from .select_character_modal import SelectCharacterModal
from .player_count_modal import PlayerCountModal
from .game_mode_modal import GameModeModal
from .game import Game


class Menu:
    def __init__(self):
        pygame.init()

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
        select_character_image = pygame.image.load(os.path.join(assets_dir, "select-character", "modal-select.png")).convert_alpha()
        game_mode_image = pygame.image.load(os.path.join(assets_dir, "modo-jogo", "modal-modo-de-jogo.png")).convert_alpha()
        
        self.title = pygame.image.load(os.path.join(assets_dir, "titulo.png")).convert_alpha()

        self.clock = pygame.time.Clock()

        # Modals
        self.credits_modal = CreditsModal(240, 86, credits_image, self.screen, self.clock, self.menu_surface)
        self.select_character_modal = SelectCharacterModal(240, 120, select_character_image, self.screen, self.clock, self.menu_surface)
        
        player_count_modal_x = (self.screen.get_width() - credits_image.get_width()) // 2
        player_count_modal_y = (self.screen.get_height() - credits_image.get_height()) // 2
        self.player_count_modal = PlayerCountModal(player_count_modal_x, player_count_modal_y, credits_image.copy(), self.screen, self.clock, self.menu_surface)

        game_mode_modal_x = (self.screen.get_width() - game_mode_image.get_width()) // 2
        game_mode_modal_y = (self.screen.get_height() - game_mode_image.get_height()) // 2
        self.game_mode_modal = GameModeModal(game_mode_modal_x, game_mode_modal_y, game_mode_image, self.screen, self.clock, self.menu_surface)

        # Buttons
        self.start_button = Button(200, 380, start_button_image, self.show_game_mode_selection)
        self.credits_button = Button(200, 470, credits_button_image, self.credits_modal.show)
        self.exit_button = Button(200, 560, exit_button_image, self.exit_game)
    
    def show_game_mode_selection(self):
        mode = self.game_mode_modal.show()
        if mode == "pvp":
            self.start_pvp_flow()

    def start_pvp_flow(self):
        player_count = self.player_count_modal.show()
        
        if player_count:
            selected_characters = []
            available_characters = list(self.select_character_modal.character_cards.keys())
            
            for i in range(player_count):
                chosen_char = self.select_character_modal.show(available_characters)
                
                if chosen_char:
                    selected_characters.append(chosen_char)
                    available_characters.remove(chosen_char)
                else:
                    return

            if len(selected_characters) == player_count:
                game = Game(selected_characters, self.screen)
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

                self.start_button.handle_event(event)
                self.credits_button.handle_event(event)
                self.exit_button.handle_event(event)

            self.start_button.update_hover(mouse_pos)
            self.credits_button.update_hover(mouse_pos)
            self.exit_button.update_hover(mouse_pos)

            self.screen.blit(self.menu_surface, (0, 0))
            title_rect = self.title.get_rect(center=(1280 // 2, 100))
            self.screen.blit(self.title, title_rect)

            self.start_button.draw_to_surface(self.screen)
            self.credits_button.draw_to_surface(self.screen)
            self.exit_button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
