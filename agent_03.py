import random
from world_02 import World


RENDER = 100
trials = 10
results = []

for trial in range(trials):
    WINDOW_TITLE = 'trial {} of {}'.format(trial + 1, trials)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    i = 0
    dist = w.player.closest_food()
    move = random.choice([-1, 1])
    delta = 0
    while not w.done():
        w.episode(move)

        last_dist = dist
        last_delta = delta

        dist = w.player.closest_food()
        delta = dist - last_dist

        if not delta < last_delta:
            move *= -1

        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
if results:
    print('\t{} average performance, excluding {} failures'.format(
        int(round(sum(results) / len(results))),
        trials - len(results)))
else:
    print('\t... literally can\'t even ({} trials)'.format(trials))
