from random import randint, random, seed
from math import exp
from time import time
from distancia_e_conversoes import file_input, custo
from plot import grafo_SA_gif, hist, grafo

def mover(v, Len):
    d = randint(0, Len)
    p = randint(0, Len)
    v[d], v[p] = v[p], v[d]
    return v

def aceitar(act, act_dist, best, best_dist, t):
    if best_dist > act_dist:
        return act, act_dist

    elif exp(-abs(act_dist-best_dist) / t) > random():
        return act, act_dist

    return best, best_dist

def SA(cycle_limit, temperatura, alfa, limite_convergencia, rota_inicial, n, matriz, r_list):
    grafos = []
    historico = []

    solucao_atual = rota_inicial
    n -= 1
    distancia_atual = custo(solucao_atual, matriz, r_list, n)
    min = float('inf')
    con = 0

    for i in range(cycle_limit):
        #print(f"\rProcessando: {i}/{Mcycle}\tmin = {distancia_atual:.2f}", end='')

        nova_solucao = mover(solucao_atual.copy(), n)

        nova_distancia = custo(nova_solucao, matriz, r_list, n)

        solucao_atual, distancia_atual = aceitar(nova_solucao, nova_distancia, solucao_atual, distancia_atual, temperatura)

        temperatura = temperatura*alfa

        #grafos.append(solucao_atual) #Only used for gifs
        historico.append(distancia_atual) #Plot convergence history

        if min > distancia_atual:
            min = distancia_atual
            con = 0

        elif min < distancia_atual:
            con = 0

        else:
            con += 1
            if con > limite_convergencia:
                break




    return solucao_atual, distancia_atual, historico, grafos

################### main ########################
n, Mtrx, Rx, coords, r_coords = file_input("\\test files\\52_pontos.txt")
rota_inicial = [i for i in range(n)]

seed(132)

#HyperParametros:
Mcycle = 100000
temp = 100
alfa = 0.99
limite_convergencia = 10000

lista = []

start = time()
for i in range(1):
    print(f"\r{i}", end='')
    melhor_rota, resultado, historico, grafos = SA(Mcycle, temp, alfa, limite_convergencia, rota_inicial.copy(), n, Mtrx.copy(), Rx.copy())
    lista.append(resultado)

print(f"\r{min(lista):.2f} {max(lista):.2f} {sum(lista)/len(lista):.2f}",end='')

print(f"\rMelhor rota encontrada: {melhor_rota}\nCusto: {resultado}\n\nTempo de execução: {time()-start:.3f}", end='')

grafo(melhor_rota, coords, r_coords)


if grafos != []:
    grafo_SA_gif(grafos, historico, coords, r_coords)

if historico != []:
    hist(historico)