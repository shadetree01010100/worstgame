import random
import math
from world_02 import World


RENDER = 1
results = []
World.EPISODE_LIMIT = 10000
agents = 10

creatures = {}
for a in range(agents):
    WINDOW_TITLE = 'agent {}'.format(a)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    i = 0
    dist = w.player.closest_food()
    move = random.uniform(-1, 1)
    delta = 0
    weights_0 = []
    # this model crushed it in 4920, often has interesting behavior
    for r in range(5):
        weights_0.append([random.gauss(0, 1) for _ in range(3)]) # 2 inuts + 1 bias
    weights_1 = [random.gauss(0, 1) for _ in range(6)] # 5 hidden neurons + 1 bias
    creatures[a] = {'weights_0': weights_0, 'weights_1': weights_1}

    while not w.done():
        w.episode(move)

        last_dist = dist
        last_delta = delta

        dist = w.player.closest_food()
        delta = dist - last_dist

        inputs = [delta, move, 1]
        hidden = [math.tanh(sum([i * w for i, w in zip(inputs, weights_0[r])])) for r in range(5)]
        hidden.append(1)
        output = math.tanh(sum([h * w for h, w in zip(hidden, weights_1)]))

        move = output

        i += 1
    if i == w.EPISODE_LIMIT:
        creatures[a]['performance'] = -len(w.foods)
    else:
        creatures[a]['performance'] = i
    success = [creatures[c]['performance'] for c in creatures if creatures[c]['performance'] > 0]
    if len(success) > 0:
        best = min([creatures[c]['performance'] for c in creatures if creatures[c]['performance'] > 0])
    else:
        best = max([creatures[c]['performance'] for c in creatures if creatures[c]['performance'] < 0])
print('best: {}{}'.format(abs(best), ' remain' if best < 0 else ''))
