import neat
import pygame
import random
import os
from game import Game, CRT

class SpaceInvadersAI:
    def __init__(self, genome, config):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)

    def make_decision(self, player_x, closest_alien_y, score):
        # Use the neural network to make decisions based on inputs
        output = self.net.activate((player_x, closest_alien_y, score))
        
        move_left = output[0] > 0.5
        move_right = output[1] > 0.5
        shoot_laser = output[2] > 0.5
        
        return move_left, move_right, shoot_laser

def run_game_with_ai(genome, config):
    # Initialize the game and the AI
    pygame.init()
    game = Game(600, 600)
    ai = SpaceInvadersAI(genome, config)
    
    while not game.game_is_over():
        game.run()
        player_x = game.player.sprite.rect.x
        closest_alien_y = game.get_closest_alien_y_position()
        score = game.score

        move_left, move_right, shoot_laser = ai.make_decision(player_x, closest_alien_y, score)
        
        # Perform actions based on AI's decisions
        if move_left:
            game.player.sprite.move_left()
        elif move_right:
            game.player.sprite.move_right()
        
        if shoot_laser:
            game.player.sprite.shoot_laser()
        
        game.run()
    
    return game.score

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = run_game_with_ai(genome, config)

def main():
    # Load NEAT configuration
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create a population
    p = neat.Population(config)

    # Add reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT algorithm
    winner = p.run(eval_genomes, 50)

    # You can save the winner, display final stats, or do other tasks here

if __name__ == '__main__':
    main()
