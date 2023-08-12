import os
import neat
import pygame
from game import Game, CRT
from neat.nn import FeedForwardNetwork

# Screen dimensions
screen_width = 600
screen_height = 600

class SpaceInvadersAI:
    def __init__(self, genome, config, alien, player, laser):
        self.genome = genome
        self.network = FeedForwardNetwork.create(genome, config)
        self.game = Game(600,600)
        self.player = self.game.player
        self.alien = self.game.aliens

    def make_decision(self, x_position, aliens_y_position):
        # Use the AI's neural network to decide whether to move left, move right, or shoot the laser
        output = self.network.activate([x_position, aliens_y_position])
        
        # Return the decisions
        return output[0] > 0.5, output[1] > 0.5, output[2] > 0.5

    def run_game_with_ai(self, game, ai):
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            # Get the current X position of the spaceship from the game
            x_position = self.game.player.sprite.rect.x
            aliens_y_position = self.game.get_closest_alien_y_position()  
            
            # Use your AI to make decisions based on the input (x_position, aliens_y_position)
            move_left, move_right, shoot_laser = ai.make_decision(x_position,aliens_y_position)
            
            # Perform the actions based on the AI's decisions
            if move_left:
                self.game.player.sprite.move_left()
            elif move_right:
                self.game.player.sprite.move_right()
            if shoot_laser:
                self.game.player.sprite.shoot_laser()
            
            # Run the game for one frame
            self.game.run()
            self.game.CRT()  # Draw the CRT effect (if you still want it)
            pygame.display.update()

            # Check if the game is over 
            if self.game.game_is_over():  # Assuming you have a function to check if the game is over
                break
        
        # Return the final score achieved by the AI
        return self.game.score

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            # Initialize the game environment and the AI using the current genome
            game = Game(600,600)
            ai = SpaceInvadersAI(genome, config)
            
            # Run the game with the AI and get the final score
            score = self.run_game_with_ai(game, ai)
            
            # Assign the score as the fitness value for the current genome
            genome.fitness = score

    def main():
        # Load NEAT configuration and create NEAT population
        localDir = os.path.dirname(__file__)
        config_path = os.path.join(localDir, "config.txt")
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
        p = neat.Population(config)

        # Add a reporter to track progress (optional but helpful)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(1))

        # Run the NEAT algorithm for a specified number of generations
        winner = p.run(SpaceInvadersAI.eval_genomes(config), 50)

        # Use the best genome to create the final AI for the game
        best_ai = SpaceInvadersAI(winner, config)

        # Run the game with the best AI
        game = Game(600,600)
        final_score = SpaceInvadersAI.run_game_with_ai(game, best_ai)

        # Display the final score or perform other tasks as needed
        print("Final Score:", final_score)

        # Clean up and exit
        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")
    SpaceInvadersAI.main()