from matplotlib import pyplot as plt
import os
import imageio
import numpy as np

def grafo(sol, coords, R):

    data = [coords[i] for i in sol]
    data = [R] + data + [R]

    x = [p[0] for p in data]
    y = [p[1] for p in data]
    _, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot(x, y, 'o-', color='blue')
    ax.grid(False)
    plt.show()

def hist(best, worst = [], average = []):
    x = [i for i, _ in enumerate(best)]

    _, ax = plt.subplots()
    ax.plot(x, best, color = 'blue')

    if worst != [] and average != []:
        ax.plot(x, worst, color='black')
        ax.plot(x, average, color='yellow')
    plt.grid()
    plt.show()

def grafo_gif(solucoes, dist, coords, R):
    filenames = []
    total = len(solucoes)
    for count, sol in enumerate(solucoes):
        print(f'\r loading gif {count}/{total}',end='')

        data = [coords[i] for i in sol]
        data = [R] + data + [R]

        x = [p[0] for p in data]
        y = [p[1] for p in data]
        _, ax = plt.subplots()
        plt.title(f"Rota: {dist[count]:.2f}")
        ax.plot(x, y, 'o-', linestyle='-', color = 'black')

        filename = f'gif\{count}.png'
        filenames.append(filename)

        plt.savefig(filename)
        plt.close()

    with imageio.get_writer('mygif.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

        # Remove files
    for filename in set(filenames):
        os.remove(filename)

def grafo_SA_gif(solucoes, dist, temp, coords, R):
    filenames = []
    total = len(solucoes)
    for count, sol in enumerate(solucoes):
        print(f'\r loading gif {count}/{total}',end='')

        data = [coords[i] for i in sol]
        data = [R] + data + [R]

        x = [p[0] for p in data]
        y = [p[1] for p in data]
        _, ax = plt.subplots()
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title(f"Rota: {dist[count]:.2f}\n Temperatura: {temp[count]}")
        ax.plot(x, y, 'd-', linestyle='-')

        filename = f'gif\{count}.png'
        filenames.append(filename)

        plt.savefig(filename)
        plt.close()

    with imageio.get_writer('mygif.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

        # Remove files
    for filename in set(filenames):
        os.remove(filename)