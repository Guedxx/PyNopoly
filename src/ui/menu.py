import pygame
import sys
import os
from pygame._sdl2.video import Window, Renderer, Texture

from .button import Button
from .credits_modal import CreditsModal
from .select_character_modal import SelectCharacterModal


class Menu:
    def __init__(self):
        pygame.init()

        try:
            self.window = Window("PyNopoly", size=(1280, 720))
            self.renderer = Renderer(self.window)
        except Exception as e:
            print(f"Error creating window or renderer: {e}")
            pygame.quit()
            exit()

        # Load menu background
        self.menu_surface = pygame.image.load(os.path.join("assets", "menu.png"))
        self.menu_surface = pygame.transform.scale(self.menu_surface, (1280, 720))

        # Create a working surface for drawing buttons
        self.working_surface = self.menu_surface.copy()

        # Converting surface into texture
        self.menu_texture = Texture.from_surface(self.renderer, self.menu_surface)
        self.clock = pygame.time.Clock()

        # Load button images
        start_button_image = pygame.image.load(os.path.join("assets", "botao-jogar.png"))
        credits_button_image = pygame.image.load(os.path.join("assets", "botao-creditos.png"))
        exit_button_image = pygame.image.load(os.path.join("assets", "botao-sair.png"))

        # Load modal images
        credits_image = pygame.image.load(os.path.join("assets", "modal-creditos.png"))
        select_character_image = pygame.image.load(os.path.join(
            "assets", "modal-selecao-personagem.png"))
        
        # Create modals
        credits_modal = CreditsModal(240, 86, 
                                     self.menu_surface.copy(), 
                                     credits_image, 
                                     self.renderer,
                                     self.clock)
        # Mudar isso pro início do jogo no futuro, por enquanto está aqui só pra testar
        select_character_modal = SelectCharacterModal(240, 120,
                                                      self.menu_surface.copy(),
                                                      select_character_image,
                                                      self.renderer,
                                                      self.clock)

        # Load title
        self.title = pygame.image.load(os.path.join("assets", "titulo.png"))

        # Create buttons at specified position
        self.start_button = Button(200, 380, start_button_image, select_character_modal.show)
        self.credits_button = Button(200, 470, credits_button_image, credits_modal.show)
        self.exit_button = Button(200, 560, exit_button_image, self.exit_game)

    def start_game(self):
        pass  
    
    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle button events
                self.start_button.handle_event(event)
                self.credits_button.handle_event(event)
                self.exit_button.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    pass

            # Update button hover states
            self.start_button.update_hover(mouse_pos)
            self.credits_button.update_hover(mouse_pos)
            self.exit_button.update_hover(mouse_pos)

            # Prepare the surface with menu background
            menu_surface = self.menu_surface.copy()

            title_rect = self.title.get_rect(center=(1280 // 2, 100))
            menu_surface.blit(self.title, title_rect)

            # Draw buttons on the surface
            self.start_button.draw_to_surface(menu_surface)
            self.credits_button.draw_to_surface(menu_surface)
            self.exit_button.draw_to_surface(menu_surface)

            # Convert surface to texture and render
            self.menu_texture = Texture.from_surface(self.renderer, menu_surface)

            self.renderer.clear()
            self.renderer.blit(self.menu_texture)
            self.renderer.present()
            self.clock.tick(60)