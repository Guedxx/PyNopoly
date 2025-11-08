import pygame

class Modal:
    def __init__(self, x, y, modal_image, screen, clock):
        self.modal_image = modal_image
        self.modal_rect = modal_image.get_rect(topleft=(x, y))  
        self.screen = screen
        self.clock = clock
    
    def show(self):
        raise NotImplementedError("Subclasses devem implementar o método show()")