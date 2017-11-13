import os
import copy
import math
import random
import statistics
from multiprocessing import Pool
import threading

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html

import genemixer
from world_03 import World


World.EPISODE_LIMIT = 5000
max_generations = 100
generation_size = 50
# neuralnet params
bias = True
input_nodes = 2
hidden_neurons = 3
output_neurons = 1

winners = []
bests = []
worsts = []
q10 = []
q20 = []
q30 = []
q40 = []
q50 = []
q60 = []
q70 = []
q80 = []
q90 = []

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(id='fitness', figure={}),
    dcc.Interval(id='interval-component', interval=10 * 1000)])

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
    x0 = (generation_size - 1) / 3
    return 1 / (1 + math.e ** -(k * (x - x0)))

@app.callback(
    dash.dependencies.Output('fitness', 'figure'),
    events=[dash.dependencies.Event('interval-component', 'interval')])
def _graph():
    return {
        'data': [
            {'y': bests, 'name': 'best', 'line': {'color': 'blue', 'width': 2, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': worsts, 'name': 'worst', 'line': {'color': 'blue', 'width': 2, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q10, 'name': '10th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q20, 'name': '20th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q30, 'name': '30th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q40, 'name': '40th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q50, 'name': '50th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q60, 'name': '60th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q70, 'name': '70th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q80, 'name': '80th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'},
            {'y': q90, 'name': '90th', 'line': {'color': 'blue', 'width': 1, 'dash': 'dash'}, 'mode': 'lines'}],
        'layout': {'title': 'fitness percentiles', 'showlegend': False}}

def _plot_server():
    app.run_server(debug=False,  host='0.0.0.0')

if __name__ == '__main__':
    reserved_cores = input('\treserve n cpu cores: ')
    reserved_cores = reserved_cores or 0
    plot_thread = threading.Thread(target=_plot_server)
    plot_thread.start()
    generation = random_generation()
    all_time_best = {'fitness': -1000}
    for gen in range(max_generations):
        world = World(RENDER=False)
        agents = []
        for agent in range(generation_size):
            w = copy.deepcopy(world)
            weights_0 = generation[agent]['weights_0']
            weights_1 = generation[agent]['weights_1']
            agents.append((w, weights_0, weights_1))
        with Pool(os.cpu_count() - int(reserved_cores)) as p:
            fitnesses = p.map(run, agents)
        for i, score in enumerate(fitnesses):
            generation[i]['fitness'] = score
        best = max(fitnesses)
        worst = min(fitnesses)
        bests.append(best)
        worsts.append(worst)
        q10.append(np.percentile(fitnesses, 10, interpolation='lower'))
        q20.append(np.percentile(fitnesses, 20, interpolation='lower'))
        q30.append(np.percentile(fitnesses, 30, interpolation='lower'))
        q40.append(np.percentile(fitnesses, 40, interpolation='lower'))
        q50.append(np.percentile(fitnesses, 50, interpolation='lower'))
        q60.append(np.percentile(fitnesses, 60, interpolation='lower'))
        q70.append(np.percentile(fitnesses, 70, interpolation='lower'))
        q80.append(np.percentile(fitnesses, 80, interpolation='lower'))
        q90.append(np.percentile(fitnesses, 90, interpolation='lower'))
        # more than one agent may have highest fitness
        winner = random.choice(
            [generation[agent] for agent in generation if generation[agent]['fitness'] == best])
        winners.append(winner)
        if winner['fitness'] > all_time_best['fitness']:
            all_time_best = winner
            all_time_best['generation'] = gen
        sorted_generation = sorted(generation, key=lambda k: generation[k]['fitness'])
        # the weak die off, uniform distribution
        survivors = [s for i, s in enumerate(sorted_generation) if sigmoid(i) > random.random()]
        need = generation_size - len(survivors)
        fitnesses.sort()
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
    print(all_time_best)
