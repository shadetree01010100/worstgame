from world_02 import World


World.RENDER = 100
trials = 100
results = []
for trial in range(trials):
    w = World('trial {}'.format(trial + 1))
    i = 0
    move = 0
    dist = w.episode(move)
    i += 1
    last_dist = dist
    dist = w.episode(move)
    i += 1
    while dist:
        if dist > last_dist:
            move = 1
        else:
            move = 0
        last_dist = dist
        dist = w.episode(move)
        i += 1
    if i < w.EPISODE_LIMIT - 1:
        results.append(i)
print('\t{} average performance, excluding {} failures'.format(
    int(round(sum(results) / len(results))),
    trials - len(results)))
