import pygame 
from game import Game


width, height = 600,600 
window = pygame.display.set_mode((width, height))
pygame.init()
game = Game(width, height)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break 

    game.loop()
    game.draw()
    pygame.display.update() 


# def eval_genomes(genomes, config):
#     # create this function
#     pass

# def run_neat(config):
#     # Create the population, which is the top-level object for a NEAT run.
#     # p = neat.Checkpointer.restore_checpoint('name of checkpoint you want to use')
#     p = neat.Population(config)

#     # Add a stdout reporter to show progress in the terminal.
#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)
#     p.add_reporter(neat.Checkpointer(1))

#     winner = p.run(eval_genomes, 50)
