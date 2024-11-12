import time
import pyvista as pv
import numpy as np

N = 30  # Size of the fabric (N x N particles)
dt = 0.01  # Time step for updates
m = 0.2  # Mass of each cell
K = 30  # Elasticity constant
g = np.array([0, -9.8, 0])  # Gravity acceleration
R = 5  # Radius of the sphere
H = 20  # Initial height of the fabric

# Initialize positions, velocities, and accelerations
P = np.zeros((N, N, 3))  # Positions
V = np.zeros((N, N, 3))  # Velocities
A = np.zeros((N, N, 3))  # Accelerations

def set_mesh():
    for i in range(N):
        for j in range(N):
            # Initial position above the sphere
            P[i, j] = [i - N / 2, H, j - N / 2]

def calc_hook():
    Felastica = np.zeros((N, N, 3))
    for i in range(N):
        for j in range(N):
            if i > 0:  # Force with the neighbor on the left
                dist = P[i, j] - P[i - 1, j]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
            if i < N - 1:  # Force with the neighbor on the right
                dist = P[i, j] - P[i + 1, j]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
            if j > 0:  # Force with the neighbor below
                dist = P[i, j] - P[i, j - 1]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
            if j < N - 1:  # Force with the neighbor above
                dist = P[i, j] - P[i, j + 1]
                norm = np.linalg.norm(dist)
                if norm > 0:
                    Felastica[i, j] += -K * (norm - 1) * (dist / norm)
    return Felastica

def calc_positions():
    Felastica = calc_hook()
    for i in range(N):
        for j in range(N):
            # Total acceleration
            A[i, j] = (g * m + Felastica[i, j]) / m
            V[i, j] += A[i, j] * dt  # Update velocity
            nova_posicao = P[i, j] + V[i, j] * dt  # New position
            # Check collision with the sphere
            dist = nova_posicao - esfera_centro
            distancia = np.linalg.norm(dist)
            # If colliding with the sphere, keep on the surface
            if distancia < R:
                normal = dist / distancia
                nova_posicao = esfera_centro + normal * R
                V[i, j] = np.array([0, 0, 0])  # Stabilize velocity to zero
            # Update position
            P[i, j] = nova_posicao

esfera_centro = np.array([0, 0, 0])

# Initialize the mesh of the fabric
set_mesh()

# Set up the plotting window with PyVista
plotter = pv.Plotter()
# Create the sphere
esfera = pv.Sphere(radius=R, center=esfera_centro)
plotter.add_mesh(esfera, color='red', opacity=0.5)

# Create the initial mesh for the fabric
pontos = P.reshape(-1, 3)
cells = []
for i in range(N - 1):
    for j in range(N - 1):
        idx = i * N + j
        cells.append([4, idx, idx + 1, idx + N + 1, idx + N])
tecido = pv.PolyData(pontos, cells)
tecido_mesh = plotter.add_mesh(tecido, color='blue', show_edges=True, opacity=0.7)

# Show the scene and start the continuous animation loop
plotter.show(auto_close=False)  # Keep the window open for the loop

for _ in range(1000):
    calc_positions()  # Update the position of the fabric
    tecido.points = P.reshape(-1, 3)  # Update mesh points
    plotter.update()  # Render the plotter with new positions
    time.sleep(dt)  # Control the speed of the animation