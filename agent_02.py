import random
from world_02 import World


RENDER = 1
trials = 1
results = []
for trial in range(trials):
    WINDOW_TITLE = 'trial {} of {}'.format(trial + 1, trials)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    move = random.choice([-1, 1])
    last_dist = w.player.closest_food()
    w.episode(move)
    dist = w.player.closest_food()
    i = 1
    while not w.done():
        if dist > last_dist:
            move *= -1
        last_dist = dist
        w.episode(move)
        dist = w.player.closest_food()
        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
if results:
    average = int(round(sum(results) / len(results)))
    print('\t{} average performance, excluding {} failures'.format(
        average,
        trials - len(results)))
else:
    print('\t... literally can\'t even ({} trials)'.format(trials))
