from world_02 import World


World.RENDER = 100
trials = 10
results = []
for trial in range(trials):
    w = World('trial {} of {}'.format(trial + 1, trials))
    i = 0
    dist = last_dist = w.start_here
    while dist:
        if dist > last_dist:
            move = 1
        else:
            move = 0
        last_dist = dist
        dist = w.episode(move)
        i += 1
    if i < w.EPISODE_LIMIT:
        results.append(i)
print('\t{} average performance, excluding {} failures'.format(
    int(round(sum(results) / len(results))), trials - len(results)))
