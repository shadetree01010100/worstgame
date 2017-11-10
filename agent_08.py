import copy
import math
import random
import statistics
from multiprocessing import Pool
import threading

import dash
import dash_core_components as dcc
import dash_html_components as html

import genemixer
from world_03 import World


World.EPISODE_LIMIT = 5000
max_generations = 100
generation_size = 100
# neuralnet params
bias = True
input_nodes = 2
hidden_neurons = 3
output_neurons = 1

bests = []
worsts = []
means = []
deviations = []
dev_hi = []
dev_lo = []

app = dash.Dash()
app.layout = html.Div([
    html.Button('REFRESH', id='refresh', n_clicks=0),
    dcc.Graph(id='fitness', figure={})])

def feed_forward(input_layer, weights_0, weights_1):
    if bias:
        input_layer.append(1)
    hidden_layer = [math.tanh(sum([i * w for i, w in zip(input_layer, weights_0[r])])) for r in range(hidden_neurons)]
    if bias:
        hidden_layer.append(1)
    output_layer = [math.tanh(sum([h * w for h, w in zip(hidden_layer, weights_1[r])])) for r in range(output_neurons)]
    return output_layer

def run(x):
    w, weights_0, weights_1 = x
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

@app.callback(
    dash.dependencies.Output('fitness', 'figure'),
    [dash.dependencies.Input('refresh', 'n_clicks')])
def _graph(n_clicks):
    return {
        'data': [
            {'y': means, 'name': 'mean'},
            {'y': dev_hi, 'name': 'dev_hi'},
            {'y': dev_lo, 'name': 'dev_lo'},
            {'y': bests, 'name': 'best'},
            {'y': worsts, 'name': 'worst'}],
        'layout': {'title': 'fitness'}}

def _plot_server():
    app.run_server(debug=False,  host='0.0.0.0')

if __name__ == '__main__':
    plot_thread = threading.Thread(target=_plot_server)
    plot_thread.start()
    winners = []
    bests = []
    worsts = []
    means = []
    deviations = []
    dev_hi = []
    dev_lo = []
    generation = random_generation()
    for gen in range(max_generations):
        world = World(RENDER=False)
        agents = []
        for agent in range(generation_size):
            w = copy.deepcopy(world)
            weights_0 = generation[agent]['weights_0']
            weights_1 = generation[agent]['weights_1']
            agents.append((w, weights_0, weights_1))
        with Pool(18) as p:
            fitnesses = p.map(run, agents)
        for i, score in enumerate(fitnesses):
            generation[i]['fitness'] = score
        best = max(fitnesses)
        worst = min(fitnesses)
        mean = statistics.mean(fitnesses)
        deviation = statistics.stdev(fitnesses, xbar=mean)
        # median = statistics.median(fitnesses)
        bests.append(best)
        worsts.append(worst)
        means.append(mean)
        deviations.append(deviation)
        dev_hi = [m + d for m, d in zip(means, deviations)]
        dev_lo = [m - d for m, d in zip(means, deviations)]
        # more than one agent may have highest fitness
        winners.append(random.choice([generation[agent] for agent in generation if generation[agent]['fitness'] == best]))
        sorted_generation = sorted(generation, key=lambda k: generation[k]['fitness'])
        # the weak die off, uniform distribution
        survivors = [s for i, s in enumerate(sorted_generation) if sigmoid(i) > random.random()]
        need = generation_size - len(survivors)
        # print('\t... culled {}'.format(need))
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

    n = input('\tview every nth generation: ')
    if n:
        for i, winner in enumerate(winners):
            if i % int(n) ==0 :
                w = World(WINDOW_TITLE='WINNER #{}'.format(i), RENDER=True)
                run((w, winner['weights_0'], winner['weights_1']))
