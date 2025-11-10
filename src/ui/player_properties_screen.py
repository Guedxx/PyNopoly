import pygame
import sys
import os
from collections import defaultdict
from .button import Button
from ..engine.Imovel import Imovel

class PlayerPropertiesScreen:
    def __init__(self, screen, clock, jogador):
        self.screen = screen
        self.clock = clock
        self.jogador = jogador
        self.running = True

        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        fonte_path = os.path.join(assets_dir, 'fonte', 'LilitaOne-Regular.ttf')
        self.title_font = pygame.font.Font(fonte_path, 48)
        self.color_font = pygame.font.Font(fonte_path, 36)
        self.prop_font = pygame.font.Font(fonte_path, 28)

        self.background = pygame.Surface(screen.get_size()).convert()
        self.background.fill((20, 20, 50)) # Dark blue background

        # House/Hotel Icons
        self.house_icon = pygame.image.load(os.path.join(assets_dir, 'icone-casa.png')).convert_alpha()
        self.hotel_icon = pygame.image.load(os.path.join(assets_dir, 'icone-hotel.png')).convert_alpha()

        # Back button
        back_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-voltar-roxo.png')).convert_alpha()
        self.back_button = Button(50, self.screen.get_height() - back_button_img.get_height() - 50, back_button_img, self.close)

    def close(self):
        self.running = False

    def run(self):
        while self.running:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                
                self.back_button.handle_event(event)

            self.screen.blit(self.background, (0, 0))

            # Title
            title_text = f"Dados propriedades {self.jogador.nome}"
            title_surf = self.title_font.render(title_text, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 60))
            self.screen.blit(title_surf, title_rect)

            # Group properties by color
            properties_by_color = defaultdict(list)
            for prop in self.jogador.propriedades:
                if isinstance(prop, Imovel):
                    properties_by_color[prop.cor].append(prop)

            # Display properties
            y_offset = 120
            x_offset = 100
            column_width = 500
            for i, (color, props) in enumerate(properties_by_color.items()):
                if y_offset > self.screen.get_height() - 200:
                    y_offset = 120
                    x_offset += column_width

                color_surf = self.color_font.render(color, True, (255, 255, 0))
                self.screen.blit(color_surf, (x_offset, y_offset))
                y_offset += 50

                for prop in props:
                    prop_surf = self.prop_font.render(prop.nome, True, (255, 255, 255))
                    self.screen.blit(prop_surf, (x_offset + 50, y_offset))

                    # Draw houses
                    if prop.casas > 0:
                        if prop.casas == 5:
                            self.screen.blit(self.hotel_icon, (x_offset + 300, y_offset))
                        else:
                            for i in range(prop.casas):
                                self.screen.blit(self.house_icon, (x_offset + 300 + i * 35, y_offset))
                    
                    y_offset += 40
                
                y_offset += 20 # Extra space between color groups

            self.back_button.update_hover(mouse_pos)
            self.back_button.draw_to_surface(self.screen)

            pygame.display.flip()
