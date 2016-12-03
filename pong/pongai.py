""" 2-input XOR example """
from __future__ import print_function
import pong_auto1

import os

from neat import nn, population, statistics

# Network inputs and expected outputs.

def eval_fitness_yield(genomes):
    for g in genomes:
        net = nn.create_feed_forward_phenotype(g)
        yield net

def eval_fitness(genomes):
    net_dummy = eval_fitness_yield(genomes)
    for g in genomes:
        net = next(net_dummy)
        sum_square_error = 0.0
        stupidai = lambda y1, y2: 1 if net.serial_activate([y1, y2]) < 0.5 else -1
        score = pong_auto1.play(stupidai)
        g.fitness = pong_auto1.bounce1


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'xor2_config')
pop = population.Population(config_path)
pop.run(eval_fitness, 300)

# Log statistics.
statistics.save_stats(pop.statistics)
statistics.save_species_count(pop.statistics)
statistics.save_species_fitness(pop.statistics)

print('Number of evaluations: {0}'.format(pop.total_evaluations))

# Show output of the most fit genome against training data.
winner = pop.statistics.best_genome()
print('\nBest genome:\n{!s}'.format(winner))
print('\nOutput:')
winner_net = nn.create_feed_forward_phenotype(winner)
for inputs, expected in zip(xor_inputs, xor_outputs):
    output = winner_net.serial_activate(inputs)
    print("expected {0:1.5f} got {1:1.5f}".format(expected, output[0]))