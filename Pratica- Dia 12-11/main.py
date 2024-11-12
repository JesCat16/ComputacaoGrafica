import time

import pyvista as pv
import numpy as np


N = 30 # Tamanho do tecido (N x N partículas)
dt = 0.01 # Delta T (intervalo para atualizações)
m = 0.2 # Massa de cada célula
K = 30 # Constante de elasticidade
g = np.array([0, -9.8, 0]) # Aceleração da gravidade
R = 5 # Raio da esfera
H = 20 # Altura inicial do tecido

esfera_centro = np.array([0, 0, 0])

P = np.zeros((N, N, 3)) # Posições
V = np.zeros((N, N, 3)) # Velocidades
A = np.zeros((N, N, 3)) # Aceleração
def set_mesh():
    for i in range(N):
        for j in range(N):
            # Posição inicial acima da esfera
            P[i, j] = [i - N / 2, H, j - N / 2]

def calc_hook():
    Felastica = np.zeros((N, N, 3))
    for i in range(N):
        for j in range(N):
            if i > 0: # Força com o vizinho da esquerda
                dist = P[i, j] - P[i - 1, j]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
            if i < N - 1: # Força com o vizinho da direita
                dist = P[i, j] - P[i + 1, j]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
            if j > 0:  # Força com o vizinho de baixo
                dist = P[i, j] - P[i, j - 1]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
            if j < N - 1:  # Força com o vizinho de cima
                dist = P[i, j] - P[i, j + 1]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
    return Felastica

def calc_posicoes():
    Felastica = calc_hook()
    for i in range(N):
        for j in range(N):
            # Aceleração total
            A[i, j] = (g * m + Felastica[i, j]) / m
            V[i, j] = V[i, j] + A[i, j] * dt # Atualizar velocidade
            nova_posicao = P[i, j] + V[i, j] * dt # nova posição
            # Verificar colisão com a esfera
            dist = nova_posicao - esfera_centro
            distancia = np.linalg.norm(dist)
            # Se colidir a esfera, manter na superfície
            if distancia < R:
                normal = dist / distancia
                nova_posicao = esfera_centro + normal * R
                V[i, j] = np.array([0, 0, 0])  # estabiliza em Zero
                # Atualizar posição
                P[i, j] = nova_posicao

# Inicializar a malha do tecido
set_mesh()
# Configuração da janela e plotagem com PyVista
plotter = pv.Plotter()
# Criar a esfera
esfera = pv.Sphere(radius=R, center=esfera_centro)
plotter.add_mesh(esfera, color="red", opacity=0.5)

pontos = P.reshape(-1, 3)
cells = []
for i in range(N - 1):
    for j in range(N - 1):
        idx = i * N + j
        cells.append([4, idx, idx + 1, idx + N + 1, idx + N])
        tecido = pv.PolyData(pontos, cells)
        tecido_mesh = plotter.add_mesh(tecido, color="blue",
        show_edges=True, opacity=0.7)
        # Mostrar a cena e iniciar o loop de animação contínua
plotter.show(auto_close=False) #Janela aberta para o loop

for _ in range(1000):
    calc_posicoes() # Atualizar a posição do tecido
    tecido.points = P.reshape(-1, 3) # Atualizar pontos da malha
    plotter.update() # Renderizar o plotter com as novas posições
    time.sleep(dt) # Controle de velocidade da animação