from world_02 import World


RENDER = 100
trials = 10
results = []
for trial in range(trials):
    WINDOW_TITLE = 'trial {} of {}'.format(trial + 1, trials)
    w = World(WINDOW_TITLE, RENDER=RENDER)
    i = 0
    dist = last_dist = w.player.closest_food()
    while not w.done():
        if dist > last_dist:
            move = 1
        else:
            move = 0
        last_dist = dist
        w.episode(move)
        dist = w.player.closest_food()
        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
if results:
    print('\t{} average performance, excluding {} failures'.format(
        int(round(sum(results) / len(results))),
        trials - len(results)))
else:
    print('\t... literally can\'t even ({} trials)'.format(trials))
