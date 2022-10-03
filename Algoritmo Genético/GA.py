from random import randint, random, seed
from time import time
from distancia_e_conversoes import custo, file_input
from plot import hist, grafo, grafo_gif


def criarPop(tamanho_da_populção, n, Mmin, Mmax):
    População = []
    novo = [i for i in range(n)]
    População.append(novo)
    n -= 1

    for i in range(tamanho_da_populção-1):
        for j in range(randint(Mmin, Mmax)):
            de = randint(0, n)
            para = randint(0, n)
            novo[de], novo[para] = novo[para], novo[de]
        População.append(novo.copy())

    return População

def aptidao(populacao, matrizAdj, RtoAll, ind):
    for i ,p in enumerate(populacao):
        populacao[i] = p, custo(p, matrizAdj, RtoAll, ind)

def cruzamento(pai1, pai2, taxa_cruzamento, comprimento_cromossomo):
    if taxa_cruzamento > random():
        quebra = randint(1, comprimento_cromossomo - 1)
        filho = PMX(pai1,pai2,quebra)
        return filho
    return pai1

def PMX(p1, p2, quebra):
    temp = p2

    for i in p1[:quebra]:
        temp.remove(i)

    filho = p1[:quebra] + temp
    return filho


def mutação(filhos, ind, taxa_mutação):
    for i in filhos:
        if taxa_mutação > random():
            de = randint(0, ind)
            para = randint(0, ind)
            i[de], i[para] = i[para], i[de]

def roleta(populacao, n_pop, taxa_cruzamento, n):
    pais = []
    filhos = []
    maxm = max(populacao, key = lambda x:x[1])[1] + 1
    k = 0

    for _ in range(4):
        temp = populacao.index((tempb := min(populacao, key=lambda x: x[1])))
        pais.append(tempb)
        populacao.pop(temp)


    target = ((n_pop-4)//2)

    while k < target:
        for i, p in enumerate(populacao):
            if (maxm - p[1]/maxm) > random():
                pais.append(p)
                populacao.pop(i)
                k += 1
                break

    for j in range(0,len(pais),2):
        filhos.append(cruzamento(pais[j][0].copy(), pais[j+1][0].copy(), taxa_cruzamento, n))
        filhos.append(cruzamento(pais[j+1][0].copy(), pais[j][0].copy(), taxa_cruzamento, n))


    return pais, filhos

def elitismo(populacao, max_pop, rand_chance):

    for j in range(max_pop//2):
        temp = 0
        for i, _ in enumerate(populacao):
            if populacao[i][1] > populacao[temp][1]:
                temp = i

            if random() > rand_chance:
                temp = randint(1, len(populacao)-1)

        populacao.pop(temp)

def GA(limite_de_geracoes, populacao_total, taxa_de_mutação, taxa_de_cruzamento,
       pressão_do_elitismo, limite_convergencia, n, Mtrx, Rx, plot_state):

    mini = float('inf')
    con = 0

    melhores = []
    media = []
    piores = []
    grafos = []

    População = criarPop(populacao_total, n, 5, 50)
    n -= 1
    aptidao(População, Mtrx, Rx, n)

    for Gen in range(limite_de_geracoes):
        #print(f"\r Processando... {Gen}/{limite_de_geracoes} minimo atual: {População[0][1]:.2f}", end='')

        População, filhos = roleta(População, populacao_total, taxa_de_cruzamento, n)

        mutação(filhos, n, taxa_de_mutação)
        aptidao(filhos, Mtrx, Rx, n)

        População = População + filhos

        elitismo(População, populacao_total, pressão_do_elitismo)

        if mini > População[0][1]:
            mini = População[0][1]
            con = 0

        elif mini == População[0][1]:
            con += 1
            if con > limite_convergencia:
                break

        if plot_state:
            melhores.append(min(População, key = lambda x:x[1])[1])
            piores.append(max(População, key = lambda x:x[1])[1])
            media.append((sum(i[1] for i in População)) // len(População))
            #grafos.append(População[0]) #Only for gifs




    return População[0] ,  melhores, piores, media, grafos


##########MAIN###################
size, Mtrx, Rx, coords, r_coords = file_input("\\test files\\56_pontos.txt")
seed(132)
start = time()

plot = True

#HyperParametros:
limite_de_geracoes = 100000
populacao_total = 200
taxa_de_mutação = 0.3
taxa_de_cruzamento = 0.8
pressão_do_elitismo = 0.6
limite_convergencia = 3000

lista = []

for i in range(1):
    print(f"\r{i}", end='')
    melhor_rota, melhores, piores, media, grafos = GA(limite_de_geracoes, populacao_total, taxa_de_mutação, taxa_de_cruzamento, pressão_do_elitismo, limite_convergencia, size, Mtrx, Rx, plot)
    lista.append(melhor_rota[1])

#print(f"\r{min(lista):.2f} {max(lista):.2f} {sum(lista)/len(lista):.2f} {time()-start}",end='')

print(f"\rMelhor rota encontrada: {melhor_rota[0]}\nCusto: {melhor_rota[1]}\n\nTempo de execução: {time() - start:.3f}", end='')

if melhores != []:
    hist(melhores, piores, media)
    grafo(melhor_rota[0], coords, r_coords)
    #grafo_gif(grafos, melhores, coords, r_coords)



print("\n",custo(melhor_rota[0], Mtrx, Rx, size-1))