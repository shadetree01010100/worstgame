import math
import random
from world_02 import World


RENDER = 10
World.EPISODE_LIMIT = 5000

agents = 100
creatures = {}
results = []

for a in range(agents):
    WINDOW_TITLE = 'agent {}'.format(a)
    w = World(WINDOW_TITLE, RENDER=RENDER)

    i = 0
    dist = w.player.closest_food()
    move = random.uniform(-1, 1)
    delta = 0

    # neuralnet params
    bias = True
    input_nodes = 2
    hidden_neurons = 3
    output_neurons = 1

    weights_0 = []
    weights_1 = []

    for r in range(hidden_neurons):
        weights_0.append([random.gauss(0, 1) for _ in range(input_nodes + bias)])
    for r in range(output_neurons):
        weights_1.append([random.gauss(0, 1) for _ in range(hidden_neurons + bias)])

    creatures[a] = {'weights_0': weights_0, 'weights_1': weights_1}

    done = w.done()
    while not done:
        w.episode(move)

        last_dist = dist
        dist = w.player.closest_food()
        delta = dist - last_dist

        input_layer = [delta, move]
        if bias:
            input_layer.append(1)
        hidden_layer = [math.tanh(sum([i * w for i, w in zip(input_layer, weights_0[r])])) for r in range(hidden_neurons)]
        if bias:
            hidden_layer.append(1)
        output_layer = [math.tanh(sum([h * w for h, w in zip(hidden_layer, weights_1[r])])) for r in range(output_neurons)]

        move = output_layer[0]

        i += 1
        done = w.done()
    if i == w.EPISODE_LIMIT:
        creatures[a]['performance'] = -len(w.foods)
    elif done != -1:
        creatures[a]['performance'] = i
    else:
        creatures[a]['performance'] = 0
    success = [creatures[c]['performance'] for c in creatures if creatures[c]['performance'] > 0]
    if len(success) > 0:
        best = min([creatures[c]['performance'] for c in creatures if creatures[c]['performance'] > 0])
    else:
        try:
            best = max([creatures[c]['performance'] for c in creatures if (w.START_FOODS * -1) < creatures[c]['performance'] < 0])
        except ValueError:
            best = None
print('best: {}'.format(best))
if best:
    print([creatures[c] for c in creatures if creatures[c]['performance'] == best])
