import random
from world_02 import World


RENDER = 100
trials = 10
results = []
for trial in range(trials):
    WINDOW_TITLE = 'RANDOM TRIAL {} of {}'.format(trial + 1, trials)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    i = 0
    while not w.done():
        move = random.uniform(-1, 1)
        w.episode(move)
        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
if results:
    print('\t{} average RANDOM TRIAL performance ({} failures)'.format(
        int(round(sum(results) / len(results))),
        trials - len(results)))
else:
    print('\t... RANDOM TRIAL literally can\'t even')

results = []
for trial in range(trials):
    WINDOW_TITLE = 'STRAIGHTLINE TRIAL {} of {}'.format(trial + 1, trials)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    i = 0
    while not w.done():
        w.episode(0)
        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
if results:
    print('\t{} average STRAIGHTLINE TRIAL performance ({} failures)'.format(
        int(round(sum(results) / len(results))),
        trials - len(results)))
else:
    print('\t... STRAIGHTLINE TRIAL literally can\'t even')
