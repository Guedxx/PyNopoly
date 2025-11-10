import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class BuildHouseModal(Modal):
    def __init__(self, screen, clock, imovel):
        
        # --- Image Loading ---
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        
        # Choose image based on whether there are houses
        if imovel.casas > 0:
            image_name = 'card-info-propriedade-com-construcao-rosa.png'
        else:
            image_name = 'card-info-propriedade-default-rosa.png'
            
        modal_image_path = os.path.join(assets_dir, 'property info', image_name)
        modal_image = pygame.image.load(modal_image_path).convert_alpha()

        x = (screen.get_width() - modal_image.get_width()) // 2
        y = (screen.get_height() - modal_image.get_height()) // 2

        super().__init__(x, y, modal_image, screen, clock)
        
        self.imovel = imovel
        self.decision = None

        # --- Font ---
        fonte_path = os.path.join(assets_dir, 'fonte', 'LilitaOne-Regular.ttf')
        self.font = pygame.font.Font(fonte_path, 20)
        self.title_font = pygame.font.Font(fonte_path, 24)

        # --- House/Hotel Icons ---
        self.house_icon = pygame.image.load(os.path.join(assets_dir, 'icone-casa.png')).convert_alpha()
        self.hotel_icon = pygame.image.load(os.path.join(assets_dir, 'icone-hotel.png')).convert_alpha()

        # --- Buttons ---
        comprar_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-comprar.png')).convert_alpha()
        cancelar_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-nao.png')).convert_alpha()

        btn_y = self.modal_rect.y + self.modal_rect.height - 80
        self.comprar_button = Button(self.modal_rect.centerx - comprar_button_img.get_width() - 10, btn_y, comprar_button_img, lambda: self.set_decision(True))
        self.cancelar_button = Button(self.modal_rect.centerx + 10, btn_y, cancelar_button_img, lambda: self.set_decision(False))
        
        self.buttons = [self.comprar_button, self.cancelar_button]
        self.should_close = False

    def set_decision(self, decision):
        self.decision = decision
        self.should_close = True

    def show(self):
        self.should_close = False
        self.decision = None
        background_capture = self.screen.copy()

        while not self.should_close:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                for button in self.buttons:
                    button.handle_event(event)
            
            # Drawing
            self.screen.blit(background_capture, (0, 0))
            self.screen.blit(self.modal_image, self.modal_rect)

            # Title (Property Name)
            title_surf = self.title_font.render(self.imovel.nome, True, (0,0,0))
            title_rect = title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 40))
            self.screen.blit(title_surf, title_rect)

            # Cost to build
            cost_text = f"Custo para construir: ${self.imovel.preco_casa}"
            cost_surf = self.font.render(cost_text, True, (0,0,0))
            cost_rect = cost_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 200))
            self.screen.blit(cost_surf, cost_rect)

            # Current houses
            house_area_y = self.modal_rect.y + 80
            icon_width = self.house_icon.get_width()
            start_x = self.modal_rect.centerx - (self.imovel.casas * icon_width) / 2

            if self.imovel.casas < 5:
                for i in range(self.imovel.casas):
                    self.screen.blit(self.house_icon, (start_x + i * icon_width, house_area_y))
            elif self.imovel.casas == 5:
                self.screen.blit(self.hotel_icon, (self.modal_rect.centerx - self.hotel_icon.get_width() // 2, house_area_y))

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.decision
