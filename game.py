import neat
import pygame, sys
from laser import Laser
from player import Player
from alien import Alien, UFO
from sys import exit 
from random import randint, choice
import os 
import cover 

class Game: 
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Setting up Player
        playerSprite = Player((self.screen_width/2,self.screen_height))
        self.player = pygame.sprite.GroupSingle(playerSprite)
        self.clock = pygame.time.Clock()
        
        # Setting up Health and Score
        self.lives = 3
        self.live_surf = pygame.image.load('Graphics/heart.png').convert_alpha()
        self.liveStartXPos = self.screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('Font/PixelArt.TTF')

        # Setting up Cover
        self.shape = cover.shape
        self.pixelSize = 6
        self.pixels = pygame.sprite.Group()
        
        #Setting up Alien
        self.aliens = pygame.sprite.Group()
        self.create_alien(rows = 6, cols = 8)
        self.alienMovement = 1
        self.alienLasers = pygame.sprite.Group()

        # Setting up UFO
        self.UFO = pygame.sprite.GroupSingle()
        self.UFOSpawnTime = randint(400,800)

        #Creating multiple objects 
        self.create_cover(70, 425)
        self.create_cover(280, 425)
        self.create_cover(490, 425)

        # Music
        music = pygame.mixer.Sound('Audio/backgroundMusic.mp3')
        music.set_volume(0.2)
        music.play(loops = -1)
        self.laserSound = pygame.mixer.Sound('Audio/Laser.wav')
        self.laserSound.set_volume(0.5)
        self.alienKilled = pygame.mixer.Sound('Audio/invaderkilled.wav')
        self.alienKilled.set_volume(0.3)
        self.gameOver = pygame.mixer.Sound('Audio/GameOver.wav')
        self.gameOver.set_volume(0.5)

        # Intro Screen
        self.gameState = 'intro'
        self.introTime = 5000
        self.clock.tick(60)

        
    def intro_screen(self):
        if self.introTime > 0:
            # Render and display the intro screen elements (text, images, etc.)
            introText = self.font.render("Welcome to Space Invaders", True, 'White')
            scaledText = pygame.transform.scale(introText, (introText.get_width() * 20 // introText.get_height(), 20))
            introRect = scaledText.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            self.screen.blit(scaledText, introRect)
            
            # Decrease the intro time
            self.introTime -= self.clock.get_time()
            self.player.sprite.lasers.empty()
        else:
            self.gameState = 'playing' 


    def create_alien(self, rows, cols, xDistance = 60, yDistance= 44, xOffset = 75, yOffset = 100):
        for rIndex, row in enumerate(range(rows)):
            for cIndex, col in enumerate(range(cols)):
                x = cIndex * xDistance + xOffset
                y = rIndex * yDistance + yOffset
                if rIndex == 0: alien_sprite = Alien('1', x, y)
                elif 1 <= rIndex < 3: alien_sprite = Alien('2', x, y)
                else: alien_sprite = Alien('3', x, y)
                self.aliens.add(alien_sprite)

    def create_cover(self, xStart, yStart):
        for rIndex, row in enumerate(self.shape):
            for cIndex, col in enumerate(row):
                if col == 'x':
                    x = xStart + cIndex * self.pixelSize 
                    y = yStart + rIndex * self.pixelSize
                    pixel = cover.Pixel(self.pixelSize, x, y)
                    self.pixels.add(pixel)

    def alien_checker(self):
        allAliens = self.aliens.sprites()
        for alien in allAliens:
            if alien.rect.right >= 600:
                self.alienMovement = -1
                self.alien_down(2)
            elif alien.rect.left <= 0:
                self.alienMovement = 1
                self.alien_down(2)
    
    def alien_down(self, distance):
        if self.aliens.sprites():
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_fire(self):
        if self.gameState == 'playing':  # Only fire lasers during gameplay
            if self.aliens.sprites():
                randomAlien = choice(self.aliens.sprites())
                laserSprite = Laser(randomAlien.rect.center, 5, self.screen_height)
                self.alienLasers.add(laserSprite)

    def collision_checks(self):

        # player lasers 
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers: 
                
                # collisions 
                if pygame.sprite.spritecollide(laser,self.pixels, True):
                    laser.kill()
                    
                
                aliensHit = pygame.sprite.spritecollide(laser,self.aliens, True)
                if aliensHit:
                    for alien in aliensHit:
                        self.score += alien.value
                    laser.kill()
                    self.alienKilled.play()


                if pygame.sprite.spritecollide(laser,self.UFO, True):
                    self.score += 500
                    laser.kill()

        # alien lasers
        if self.alienLasers:
            for laser in self.alienLasers:
                # collisons 
                if pygame.sprite.spritecollide(laser,self.pixels, True):
                    laser.kill()
                
                if pygame.sprite.spritecollide(laser,self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.gameOver.play()
                        pygame.quit()
                        sys.exit()
        
        #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.pixels, True)
            
                if pygame.sprite.spritecollide(alien, self.player, True):
                    pygame.quit()
                    sys.exit()

    def get_closest_alien_y_position(self):
        player_y = self.player.sprite.rect.y
        closest_alien = min(self.aliens.sprites(), key=lambda alien: abs(alien.rect.y - player_y))
        closest_alien_y = closest_alien.rect.y
        return closest_alien_y


    def player_lives(self):
        for live in range(self.lives - 1):
            x = self.liveStartXPos + (live * (self.live_surf.get_size()[0] + 10) )
            self.screen.blit(self.live_surf,(x,8))

    def display_score(self):
        scoreSurf = self.font.render(f'SCORE: {self.score}', False, 'white')
        scaledText = pygame.transform.scale(scoreSurf, (scoreSurf.get_width() * 30 // scoreSurf.get_height(), 30))
        scoreRect = scaledText.get_rect(topleft = (10,20))
        self.screen.blit(scaledText,scoreRect)
        

    def UFO_spawn_timer(self):
        self.UFOSpawnTime -= 1
        if self.UFOSpawnTime <= 0:
            self.UFO.add(UFO(choice(['right','left']), self.screen_width))
            self.UFOSpawnTime = randint(400,800)

    def victory_screen(self):
        if not self.aliens.sprites():
            victorySurf = self.font.render('Victory!!',False, 'white')
            scaledText = pygame.transform.scale(victorySurf, (victorySurf.get_width() * 40 // victorySurf.get_height(), 40))
            victoryRect = scaledText.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
            self.screen.blit(scaledText, victoryRect)
   
    def game_is_over(self):
        if self.lives <= 0: 
            print("here")
            return True
        if self.score >= 8000: 
            print("here")
            return True
        else:
            return False # Game over when the player's lives reach zero or score is >= 8000


    #Draw and Update all Sprite Groups 
    def run(self):
        if self.gameState == 'intro':
            self.intro_screen()
        elif self.gameState == 'playing':
            self.player.update()
            self.aliens.update(self.alienMovement)
            self.alienLasers.update()
            self.UFO_spawn_timer()
            self.UFO.update()
            self.collision_checks()
            self.alien_checker()
            
            
            self.player.sprite.lasers.draw(self.screen)
            self.player.draw(self.screen)

            self.pixels.draw(self.screen)
            self.aliens.draw(self.screen)
            self.alienLasers.draw(self.screen)
            self.UFO.draw(self.screen)
            self.player_lives()
            self.display_score()
            self.victory_screen()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('Graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (600, 600))

    def create_crt_lines(self):
        lineHeight =3
        lineAmount = int(600 / 600)
        for line in range(lineAmount):
            y = line * lineHeight
            pygame.draw.line(self.tv, 'black', (0,y), (600, y),1)
        
    def draw(self):
        self.tv.set_alpha(randint(75, 90))   
        self.create_crt_lines()
        screen.blit(self.tv, (0,0))



if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    pixelFont = pygame.font.Font('Font/PixelArt.TTF')
    game = Game(600,600)
    CRT = CRT()
    alienLaser = pygame.USEREVENT + 1
    pygame.time.set_timer(alienLaser, 650)

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == alienLaser:
                game.alien_fire()
        screen.fill((30,30,30))
        game.run()
        CRT.draw()
        pygame.display.flip()
        clock.tick(60)