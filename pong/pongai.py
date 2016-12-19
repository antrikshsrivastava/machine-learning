""" 2-input XOR example """
from __future__ import print_function
import pong_auto1

import os

from neat import nn, population, statistics

generation = 0
max_bounces = 15

def eval_fitness(genomes):
    global generation
    for i, g in enumerate(genomes):
        net = nn.create_feed_forward_phenotype(g)
        stupidai = lambda y1, y2: net.serial_activate([y1, y2])
        pong_auto1.play(stupidai, max_bounces, generation, i)
        #try:
        g.fitness = pong_auto1.total_bounces_nn / float(max_bounces)
        #except:
        #    g.fitness = 0.5
        pong_auto1.bounce1 = 0
        print("Genome: " + str(i))
        print("Fitness: " + str(g.fitness))
        print("Generation:" + str(generation))
    generation += 1


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'xor2_config')
pop = population.Population(config_path)
pop.run(eval_fitness, 30)

# Log statistics.
statistics.save_stats(pop.statistics)
statistics.save_species_count(pop.statistics)
statistics.save_species_fitness(pop.statistics)

print('Number of evaluations: {0}'.format(pop.total_evaluations))

# Show output of the most fit genome against training data.
winner = pop.statistics.best_genome()
print('\nBest genome:\n{!s}'.format(winner))
winner_net = nn.create_feed_forward_phenotype(winner)
best_ai = lambda y1, y2: winner_net.serial_activate([y1, y2])
pong_auto1.play(best_ai, 30, -1, -1)
print("Fitness: " + str(pong_auto1.total_bounces_nn / float(max_bounces)))
