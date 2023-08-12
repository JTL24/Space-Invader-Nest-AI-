import pygame

class Pixel(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill((40,165,112))
        self.rect = self.image.get_rect(topleft = (x,y))

shape = ['  xx   ', 
        '  xxxx  ',
        ' xxxxxx ',
        'xxxxxxxx',
        'xxxxxxxx',
        'xxxxxxxx',
        'xxx  xxx',
        'xxx  xxx',
        'xxx  xxx']