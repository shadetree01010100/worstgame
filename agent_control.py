import random
from world_02 import World


RENDER = 1
trials = 1
results = []
for trial in range(trials):
    WINDOW_TITLE = 'trial {} of {}'.format(trial + 1, trials)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    i = 1
    while not w.done():
        move = random.choice([-1, 0, 1])
        w.episode(move)
        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
if results:
    print('\t{} average performance, excluding {} failures'.format(
        int(round(sum(results) / len(results))),
        trials - len(results)))
else:
    print('\t... literally can\'t even ({} trials)'.format(trials))
