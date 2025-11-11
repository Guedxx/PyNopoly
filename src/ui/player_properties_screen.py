import pygame
import sys
import os
from collections import defaultdict
from .button import Button
from ..engine.Imovel import Imovel
from .property_management_modal import PropertyManagementModal

class PlayerPropertiesScreen:
    def __init__(self, screen, clock, jogador, partida):
        self.screen = screen
        self.clock = clock
        self.jogador = jogador
        self.partida = partida
        self.running = True

        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        fonte_path = os.path.join(assets_dir, 'fonte', 'LilitaOne-Regular.ttf')
        self.title_font = pygame.font.Font(fonte_path, 36)
        self.color_font = pygame.font.Font(fonte_path, 36)
        self.prop_font = pygame.font.Font(fonte_path, 28)

        self.background = pygame.Surface(screen.get_size()).convert()
        self.background.fill((35, 108, 178)) # Dark blue background

        header_image_path = os.path.join(assets_dir, 'header.png')
        self.header_image = pygame.image.load(header_image_path).convert_alpha()
        CARD_SCALE = 1.4  # Escala da carta

        # Redimensiona a carta
        orig_w, orig_h = self.header_image.get_size()
        new_w = int(orig_w * CARD_SCALE)
        new_h = int(orig_h )
        if new_w <= 0: new_w = 1
        if new_h <= 0: new_h = 1
        self.header_image = pygame.transform.smoothscale(self.header_image, (new_w, new_h))
        
        # Centraliza na tela
        screen_w, screen_h = screen.get_size()
        self.carta_x = (screen_w - new_w) // 2
        self.carta_y = 10
        
        # House/Hotel Icons
        self.house_icon = pygame.image.load(os.path.join(assets_dir, 'icone-casa.png')).convert_alpha()
        self.hotel_icon = pygame.image.load(os.path.join(assets_dir, 'icone-hotel.png')).convert_alpha()

        # Back button
        back_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-voltar-azul.png')).convert_alpha()
        self.back_button = Button(50, self.screen.get_height() - back_button_img.get_height() - 50, back_button_img, self.close)
        
        self.properties_by_color = defaultdict(list)
        for prop in self.jogador.propriedades:
            if isinstance(prop, Imovel):
                self.properties_by_color[prop.cor].append(prop)
        
        self.property_buttons = self._create_property_buttons()

    def _create_property_buttons(self):
        buttons = []
        y_offset = 120
        x_offset = 100
        column_width = 500
        for i, (color, props) in enumerate(self.properties_by_color.items()):
            if y_offset > self.screen.get_height() - 200:
                y_offset = 120
                x_offset += column_width
            
            y_offset += 50

            for prop in props:
                color = (106, 190, 247) if prop.hipotecado else (255, 255, 255)
                prop_surf = self.prop_font.render(prop.nome, True, color)
                prop_rect = prop_surf.get_rect(topleft=(x_offset + 50, y_offset))
                prop_button = Button(prop_rect.x, prop_rect.y, prop_surf, lambda p=prop: self.handle_property_click(p))
                buttons.append(prop_button)
                y_offset += 40
            
            y_offset += 20
        return buttons

    def close(self):
        self.running = False

    def handle_property_click(self, prop):
        modal = PropertyManagementModal(self.screen, self.clock, prop, self.jogador, self.partida)
        modal.show()
        self.property_buttons = self._create_property_buttons()

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
                for btn in self.property_buttons:
                    btn.handle_event(event)

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.header_image, (self.carta_x, self.carta_y))

            # Title
            title_text = f"Dados propriedades {self.jogador.nome}"
            title_surf = self.title_font.render(title_text, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 60))
            self.screen.blit(title_surf, title_rect)

            # Display properties
            y_offset = 120
            x_offset = 100
            column_width = 500
            button_idx = 0
            for i, (color, props) in enumerate(self.properties_by_color.items()):
                if y_offset > self.screen.get_height() - 200:
                    y_offset = 120
                    x_offset += column_width

                color_surf = self.color_font.render(color, True, (245, 241, 159))
                self.screen.blit(color_surf, (x_offset, y_offset))
                y_offset += 50

                for prop in props:
                    if button_idx < len(self.property_buttons):
                        button = self.property_buttons[button_idx]
                        button.update_hover(mouse_pos)
                        button.draw_to_surface(self.screen)
                        button_idx += 1

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
