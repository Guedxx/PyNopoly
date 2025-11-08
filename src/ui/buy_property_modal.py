import pygame
import sys
import os
from .modal_interface import Modal
from .button import Button

class BuyPropertyModal(Modal):
    def __init__(self, x, y, screen, clock, imovel):
        
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        modal_image = pygame.image.load(os.path.join(assets_dir, 'alert-comprar-propriedade.png')).convert_alpha()
        
        super().__init__(x, y, modal_image, screen, clock)
        
        self.imovel = imovel
        self.decision = None # True for buy, False for not buy

        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.price_font = pygame.font.Font(None, 48)

        # Buttons
        sim_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-sim.png')).convert_alpha()
        nao_button_img = pygame.image.load(os.path.join(assets_dir, 'botao-nao.png')).convert_alpha()

        btn_y = self.modal_rect.y + 220
        self.sim_button = Button(self.modal_rect.x + 70, btn_y, sim_button_img, lambda: self.set_decision(True))
        self.nao_button = Button(self.modal_rect.x + 250, btn_y, nao_button_img, lambda: self.set_decision(False))
        
        self.buttons = [self.sim_button, self.nao_button]

    def set_decision(self, decision):
        self.decision = decision

    def show(self):
        showing = True
        self.decision = None # Reset before showing
        
        # Render text surfaces once
        title_surf = self.title_font.render(self.imovel.nome, True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 130))
        
        price_text = f"$ {self.imovel.preco}"
        price_surf = self.price_font.render(price_text, True, (0, 0, 0))
        price_rect = price_surf.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y + 180))

        while showing:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                for button in self.buttons:
                    if button.handle_event(event):
                        showing = False
                        break
                if not showing:
                    break
            
            # Drawing
            self.screen.blit(self.modal_image, self.modal_rect)
            self.screen.blit(title_surf, title_rect)
            self.screen.blit(price_surf, price_rect)

            for button in self.buttons:
                button.update_hover(mouse_pos)
                button.draw_to_surface(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
            
        return self.decision
