import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos,speed,screenHeight):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.screenHeight = screenHeight

        

    def clear(self):
        if self.rect.y <= -25 or self.rect.y >= self.screenHeight + 25:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.clear()