import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.image.load('Graphics/Player.png').convert_alpha()
        # self.scaledImage = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(midbottom = pos)
        self.ready = True 
        self.laserTime = 0
        self.laserCooldown = 600
        
        self.lasers = pygame.sprite.Group()
        self.laserSound = pygame.mixer.Sound('Audio/Laser.wav')
        self.laserSound.set_volume(0.5)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right <= 600:
            self.rect.x += 5
        if keys[pygame.K_LEFT] and self.rect.left >= 0: 
            self.rect.x -= 5
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laserTime = pygame.time.get_ticks()
            self.laserSound.play()
    
    def move_left(self):
        self.rect.x -= 5
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += 5
        if self.rect.right > 600:
            self.rect.right = 600
    
    def reload(self):
        # Timer for the reload 
        if not self.ready:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserTime >= self.laserCooldown: 
                self.ready = True 
    
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def update(self):
        self.get_input()
        self.reload()
        self.lasers.update()
        