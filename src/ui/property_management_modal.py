import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class PropertyManagementModal(Modal):
    def __init__(self, screen, clock, imovel, jogador, partida):
        self.imovel = imovel
        self.jogador = jogador
        self.partida = partida

        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        
        modal_image_path = os.path.join(assets_dir, 'modal-creditos.png')
        modal_image = pygame.image.load(modal_image_path).convert_alpha()
        
        x = (screen.get_width() - modal_image.get_width()) // 2
        y = (screen.get_height() - modal_image.get_height()) // 2

        super().__init__(x, y, modal_image, screen, clock)

        fonte_path = os.path.join(assets_dir, 'fonte', 'LilitaOne-Regular.ttf')
        self.title_font = pygame.font.Font(fonte_path, 36)
        self.info_font = pygame.font.Font(fonte_path, 28)

        self.buttons = []
        self.should_close = False
        self._create_buttons()

    def _create_buttons(self):
        self.buttons.clear()
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        
        btn_y = self.modal_rect.y + 200

        if self.imovel.casas > 0:
            sell_house_img = pygame.image.load(os.path.join(assets_dir, 'botao-vender.png')).convert_alpha()
            sell_button = Button(self.modal_rect.centerx - sell_house_img.get_width() // 2, btn_y, sell_house_img, self.sell_house)
            self.buttons.append(sell_button)
            btn_y += 70
        
        if self.imovel.casas == 0:
            if not self.imovel.hipotecado:
                mortgage_img = pygame.image.load(os.path.join(assets_dir, 'botao-vender.png')).convert_alpha()
                mortgage_button = Button(self.modal_rect.centerx - mortgage_img.get_width() // 2, btn_y, mortgage_img, self.mortgage_property)
                self.buttons.append(mortgage_button)
                btn_y += 70
            else:
                unmortgage_img = pygame.image.load(os.path.join(assets_dir, 'botao-comprar.png')).convert_alpha()
                unmortgage_button = Button(self.modal_rect.centerx - unmortgage_img.get_width() // 2, btn_y, unmortgage_img, self.unmortgage_property)
                self.buttons.append(unmortgage_button)
                btn_y += 70

        close_img = pygame.image.load(os.path.join(assets_dir, 'botao-fechar.png')).convert_alpha()
        close_button = Button(self.modal_rect.centerx - close_img.get_width() // 2, self.modal_rect.y + self.modal_rect.height - 100, close_img, self.close)
        self.buttons.append(close_button)

    def sell_house(self):
        self.jogador.vender_casa(self.imovel, self.partida.banco)
        self._create_buttons()

    def mortgage_property(self):
        self.partida.banco.hipotecar_imovel(self.imovel, self.jogador)
        self.should_close = True

    def unmortgage_property(self):
        custo_resgate = int(self.imovel.hipoteca * 1.1)
        if self.jogador.dinheiro >= custo_resgate:
            self.partida.banco.resgatar_hipoteca(self.imovel, self.jogador)
            self.should_close = True
        else:
            print("Not enough money to unmortgage")

    def close(self):
        self.should_close = True

    def show(self):
        self.should_close = False
        background_capture = self.screen.copy()

        while not self.should_close:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                for button in self.buttons:
                    button.handle_event(event)
            
            self.screen.blit(background_capture, (0, 0))
            self.screen.blit(self.modal_image, self.modal_rect)

            title_surf = self.title_font.render(self.imovel.nome, True, (0,0,0))
            title_rect = title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 50))
            self.screen.blit(title_surf, title_rect)

            casas_text = f"Casas: {self.imovel.casas}"
            casas_surf = self.info_font.render(casas_text, True, (0,0,0))
            casas_rect = casas_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 120))
            self.screen.blit(casas_surf, casas_rect)

            if self.imovel.hipotecado:
                hipotecado_text = "Hipotecado"
                hipotecado_surf = self.info_font.render(hipotecado_text, True, (255,0,0))
                hipotecado_rect = hipotecado_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 160))
                self.screen.blit(hipotecado_surf, hipotecado_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
