import copy
import math
import random
import statistics

import matplotlib.pyplot as plt

import genemixer
from world_03 import World


plt.ion()

World.EPISODE_LIMIT = 5000
max_generations = 100
generation_size = 100
# neuralnet params
bias = True
input_nodes = 2
hidden_neurons = 3
output_neurons = 1

def feed_forward(input_layer, weights_0, weights_1):
    if bias:
        input_layer.append(1)
    hidden_layer = [math.tanh(sum([i * w for i, w in zip(input_layer, weights_0[r])])) for r in range(hidden_neurons)]
    if bias:
        hidden_layer.append(1)
    output_layer = [math.tanh(sum([h * w for h, w in zip(hidden_layer, weights_1[r])])) for r in range(output_neurons)]
    return output_layer

def run(w, weights_0, weights_1):
    dist = w.player.closest_food()
    move = random.uniform(-1, 1)
    delta = 0
    done = w.done()
    while not done:
        w.episode(move)
        last_dist = dist
        dist = w.player.closest_food()
        delta = dist - last_dist
        move = feed_forward([delta, move], weights_0, weights_1)[0]
        done = w.done()
    return done

def random_generation():
    generation = {}
    for agent in range(generation_size):
        weights_0 = []
        weights_1 = []
        for r in range(hidden_neurons):
            weights_0.append([random.gauss(0, math.pi) for _ in range(input_nodes + bias)])
        for r in range(output_neurons):
            weights_1.append([random.gauss(0, math.pi) for _ in range(hidden_neurons + bias)])
        generation[agent] = {'weights_0': weights_0, 'weights_1': weights_1, 'age': 0}
    return generation

def sigmoid(x):
    # roughly 3 to 97%
    k = 7 / generation_size
    x0 = (generation_size - 1) / 2
    return 1 / (1 + math.e ** -(k * (x - x0)))

winners = []
bests = []
worsts = []
averages = []
generation = random_generation()
for gen in range(max_generations):
    world = World(RENDER=False)
    for agent in range(generation_size):
        w = copy.deepcopy(world)
        weights_0 = generation[agent]['weights_0']
        weights_1 = generation[agent]['weights_1']
        generation[agent]['fitness'] = run(w, weights_0, weights_1)
    best = max([generation[agent]['fitness'] for agent in generation])
    worst = min([generation[agent]['fitness'] for agent in generation])
    average = round(sum([generation[agent]['fitness'] for agent in generation]) / generation_size, 1)
    bests.append(best)
    worsts.append(worst)
    averages.append(average)
    median = round(statistics.median([generation[agent]['fitness'] for agent in generation]), 1)
    print('\tGENERATION ', gen)
    print('\tbest:    ', best)
    print('\tworst:   ', worst)
    print('\tmedian:  ', median)
    print('\taverage: ', average)
    plt.plot(bests)
    plt.plot(worsts)
    plt.plot(averages)
    plt.show()
    plt.pause(0.01)
    # more than one agent may have highest fitness
    winners.append(random.choice([generation[agent] for agent in generation if generation[agent]['fitness'] == best]))
    sorted_generation = sorted(generation, key=lambda k: generation[k]['fitness'])
    # the weak die off, uniform distribution
    survivors = [s for i, s in enumerate(sorted_generation) if sigmoid(i) > random.random()]
    need = generation_size - len(survivors)
    print('\t... culled {}'.format(need))
    # todo: weight survivors by fitness maybe?
    new_generation = {}
    for i, survivor in enumerate(survivors):
        new_generation[i] = generation[survivor]
        new_generation[i]['age'] += 1
    for _ in range(need):
        i += 1
        offspring = {'weights_0': [], 'weights_1': [], 'age': 0}
        donor_a = generation[random.choice(survivors)]
        donor_b = generation[random.choice([s for s in survivors if s != donor_a])]
        for a, b in zip(donor_a['weights_0'], donor_b['weights_0']):
            foo = []
            for r in range(len(a)):
                foo.append(genemixer.mix_genes(a[r], b[r]))
            offspring['weights_0'].append(foo)
        for a, b in zip(donor_a['weights_1'], donor_b['weights_1']):
            bar = []
            for r in range(len(a)):
                bar.append(genemixer.mix_genes(a[r], b[r]))
            offspring['weights_1'].append(bar)
        new_generation[i] = offspring
    generation = new_generation

input('\tpress [ENTER] to load view best of each generation')
for i, winner in enumerate(winners):
    w = World(WINDOW_TITLE='WINNER #{}'.format(i), RENDER=True)
    run(w, winner['weights_0'], winner['weights_1'])
