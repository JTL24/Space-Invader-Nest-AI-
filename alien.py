import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, number, x, y):
        super().__init__()
        filePath = 'Graphics/Enemy' + number + '.png'
        self.image = pygame.image.load(filePath).convert_alpha()
        self.rect = self.image.get_rect(topleft= (x,y))
        self.value = 0
        if number == '1': self.value = 300
        elif number == '2': self.value = 200
        else: self.value = 100


    def update(self, direction):
        self.rect.x += direction

class UFO(pygame.sprite.Sprite):
    def __init__(self, startSide, screenWidth):
        super().__init__()
        self.image = pygame.image.load('Graphics/ufo.png').convert_alpha()

        if startSide == 'right':
            x = screenWidth + 50
            self.speed = -3        
        else:
            x = -50
            self.speed = 3
        
        self.rect = self.image.get_rect(topleft = (x, 40))
    
    def update(self):
        self.rect.x += self.speed
