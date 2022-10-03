import os
from math import sqrt
import re

def file_input(file):
    coords = []
    p = []


    path = os.getcwd()+file
    with open(path) as f:
        for i, line in enumerate(f):
            #print(line)
            coords.append(tuple(map(float, re.split('\n | ', line))))
    R_coords = coords[0]
    coords.pop(0)

    return len(coords), gerar_matriz(coords), gerar_lR(coords, R_coords), coords, R_coords

def gerar_lR(lista, Rc):
    l_R = []

    for i in lista:
        l_R.append(sqrt(((i[0] - Rc[0]) ** 2) + ((i[1] - Rc[1]) ** 2)))

    return l_R

def gerar_matriz(pontos):
    matriz = [[sqrt(((i[0]-j[0])**2)+(((i[1]-j[1]))**2)) for j in pontos]for i in pontos]
    return matriz

def custo(lista_de_indices, matriz_adj, dist_R_ponto, len_lista):

    total = dist_R_ponto[lista_de_indices[0]]
    for i in range(len_lista):
        total += matriz_adj[lista_de_indices[i]][lista_de_indices[i + 1]]
    total += dist_R_ponto[lista_de_indices[len_lista]]

    return total

def minimo(lista):
    a = lista[0]
    for e in lista:
        if a > e:
            a = e
    return a

def maximo(lista):
    a = lista[0]
    for e in lista:
        if e > a:
            a = e
    return a

def media(lista):
    soma = 0
    for i in lista:
        soma += i

    return soma/len(lista)

def diferença(a, b):
    return abs(a-b)
