<<<<<<< HEAD
#Grafico de la distribucion de temperatura en t=0.100

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

# Definimos las dimensiones físicas del dominio en x e y
Lx, Ly = 1.0, 1.0  # Estos son los largos del dominio en x e y respectivamente (dominio de 1x1 unidad)

# Definimos la cantidad de divisiones del dominio (número de puntos menos uno)
Nx, Ny = 20, 20  # Cantidad de divisiones en las direcciones x e y

# Calculamos el tamaño de paso espacial en x y en y
dx, dy = Lx / Nx, Ly / Ny  # Distancia entre nodos consecutivos en cada eje

# Creamos los arreglos de coordenadas espaciales
x = np.linspace(0, Lx, Nx+1)  # Puntos equiespaciados de 0 a Lx (incluyendo extremos)
y = np.linspace(0, Ly, Ny+1)  # Puntos equiespaciados de 0 a Ly (incluyendo extremos)

# Parámetros de tiempo para la simulación
T = 0.1      # Tiempo total de simulación
dt = 0.001   # Paso temporal
nt = int(T / dt)  # Número total de pasos de tiempo

# Constante de difusión térmica (puede representar conductividad térmica, por ejemplo)
alpha = 1.0

# Inicialización de la matriz de temperatura u en todo el dominio
u = np.zeros((Nx+1, Ny+1))       # Temperatura inicial en t = 0
u_new = np.zeros_like(u)         # Matriz que contendrá la temperatura actualizada

# Generamos la malla 2D (X, Y) para aplicar condiciones iniciales
X, Y = np.meshgrid(x, y, indexing='ij')  # 'ij' para mantener coherencia con el orden u[i,j]

# Asignamos condición inicial: un pulso gaussiano centrado en (0.5, 0.5)
u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))  # Pico de calor localizado

# Cálculo de parámetros auxiliares para Crank-Nicolson en x e y
rx = alpha * dt / (2 * dx**2)  # Parámetro de difusión en x, dividido entre 2 por Crank-Nicolson
ry = alpha * dt / (2 * dy**2)  # Igual pero en y

# Construcción de matrices tridiagonales sparse (esparcidas) para el método implícito en x
Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))  # Matriz del lado izquierdo (implícito) en x
Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))    # Matriz del lado derecho (explícito) en x

# Construcción de matrices tridiagonales para el método implícito en y
Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))  # Implícito en y
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))    # Explícito en y

# Comienza el lazo de integración temporal
for n in range(nt):
    # Paso intermedio: resolvemos en la dirección x, manteniendo y fijo
    u_star = np.zeros_like(u)  # Matriz temporal para almacenar resultados intermedios

    # Recorremos cada fila fija (j) y resolvemos en x (columnas)
    for j in range(1, Ny):
        rhs = Bx.dot(u[1:Nx, j])              # Lado derecho del sistema: combinación explícita
        u_star[1:Nx, j] = spsolve(Ax, rhs)    # Resolvemos el sistema lineal en x

    # Paso final: resolvemos en la dirección y, manteniendo x fijo
    for i in range(1, Nx):
        rhs = By.dot(u_star[i, 1:Ny])         # Lado derecho para dirección y
        u_new[i, 1:Ny] = spsolve(Ay, rhs)     # Solución del sistema lineal en y

    # Actualizamos la solución completa para el siguiente paso de tiempo
    u[:, :] = u_new[:, :]  # Se copia el resultado actualizado de u_new a u

# Visualización
plt.figure(figsize=(6,5))
cp = plt.contourf(X, Y, u, 20, cmap='hot')
plt.colorbar(cp)
plt.title("Distribución de temperatura en t = {:.3f}".format(T))
=======
#Codigo para la distribucion de temperatura en t = 0.100

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags 
from scipy.sparse.linag import spsolve

Lx, Ly = 1.0, 1.0 

Nx, Ny = 20, 20 

dx, dy = Lx / Nx, Ly / Ny

x = np.linspace(0, Lx, Nx+1)
y = np.linspace(0, Ly, Ny+1)

T = 0.1
dt = 0.001
nt = int(T / dt)

alpha = 1.0

u = np.zeros((Nx+1, Ny+1))
u_new = np.zeros_like(u)

X, Y = np.meshgrid(x, y, indexing='ij')

u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))

rx = alpha * dt / (2 * dx**2)
ry = alpha * dt / (2 * dy**2)

Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))
Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))

for n in range(nt):
    u_star = np.zeros_like(u)

    for j in range(1, Ny):
        rhs = Bx.dot(u[1:Nx, j])
        u_star[1:Nx, j] = spsolve(Ax, rhs)

    for i in range(1, Nx):
        rhs = By.dot(u_star[i, 1:Ny])
        u_new[i, 1:Ny] = spsolve(Ay, rhs)

    u[:, :] = u_new[:, :] 

plt.figure(figsize=(6,5))
cp = plt.contourf(X, Y, u, 20, cmap='hot')
plt.colorbar(cp)
plt.title("Distribucion de temperatura en t = {:.3f}".format(T))
>>>>>>> 6ffca75 (Actualizacion)
plt.xlabel("x")
plt.ylabel("y")
plt.show()


<<<<<<< HEAD

#Graficos en 2D y 3D en distintos tiempos

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from mpl_toolkits.mplot3d import Axes3D  # Para 3D

# ------------------------
# Parámetros del problema
# ------------------------

Lx, Ly = 1.0, 1.0
=======
# Codigo para graficos en 2D Y 3D variando su tiempo.

import numpy as np
import matplotlib.pyplot as plt 
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from mpl_toolkits.mplot3d import Axes3D 

Lx, Ly = 1.0, 1.0 
>>>>>>> 6ffca75 (Actualizacion)
Nx, Ny = 20, 20
dx, dy = Lx / Nx, Ly / Ny

x = np.linspace(0, Lx, Nx+1)
y = np.linspace(0, Ly, Ny+1)
X, Y = np.meshgrid(x, y, indexing='ij')

T = 0.1
dt = 0.001
nt = int(T / dt)
alpha = 1.0

<<<<<<< HEAD
# Opciones que puedes cambiar:
ci_opcion = 'gaussiana'    # 'gradiente', 'doble_pulso'
cf_opcion = 'dirichlet'    # 'neumann', 'robin'

# ------------------------
# Condición inicial
# ------------------------
=======
ci_opcion = 'gaussiana'
cf_opcion = 'dirichlet'
>>>>>>> 6ffca75 (Actualizacion)

u = np.zeros((Nx+1, Ny+1))
u_new = np.zeros_like(u)

if ci_opcion == 'gaussiana':
    u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))
elif ci_opcion == 'gradiente':
    u[:, :] = X
elif ci_opcion == 'doble_pulso':
    u[:, :] = np.exp(-400 * ((X - 0.25)**2 + (Y - 0.75)**2)) + np.exp(-400 * ((X - 0.75)**2 + (Y - 0.25)**2))

<<<<<<< HEAD
# ------------------------
# Construcción de matrices
# ------------------------

rx = alpha * dt / (2 * dx**2)
ry = alpha * dt / (2 * dy**2)

Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1, 0, 1], shape=(Nx-1, Nx-1))
Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1, 0, 1], shape=(Nx-1, Nx-1))

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1, 0, 1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1, 0, 1], shape=(Ny-1, Ny-1))

# ------------------------
# Condición de frontera
# ------------------------
=======
rx = alpha * dt / (2 * dx**2)
ry = alpha * dt / (2 * dy**2)

Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))
Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))
>>>>>>> 6ffca75 (Actualizacion)

def aplicar_cf(u):
    if cf_opcion == 'dirichlet':
        u[0, :] = 0
        u[-1, :] = 0
        u[:, 0] = 0
        u[:, -1] = 0
    elif cf_opcion == 'neumann':
        u[0, :] = u[1, :]
        u[-1, :] = u[-2, :]
        u[:, 0] = u[:, 1]
        u[:, -1] = u[:, -2]
    elif cf_opcion == 'robin':
        beta = 1.0
        u[0, :] = u[1, :] / (1 + beta * dx)
        u[-1, :] = u[-2, :] / (1 + beta * dx)
        u[:, 0] = u[:, 1] / (1 + beta * dy)
        u[:, -1] = u[:, -2] / (1 + beta * dy)

<<<<<<< HEAD
# ------------------------
# Evolución temporal
# ------------------------

snapshots_dict = {}  # Para guardar u en momentos seleccionados
t_snapshots = [0.01, 0.025, 0.05, 0.1]


=======
snapshots_dict = {}
t_snapshots = [0.01, 0.025, 0.05, 0.1]

>>>>>>> 6ffca75 (Actualizacion)
for n in range(nt + 1):
    current_time = n * dt
    aplicar_cf(u)
    u_star = np.zeros_like(u)
<<<<<<< HEAD
    for j in range(1, Ny):
=======
    for j in range (1, Ny):
>>>>>>> 6ffca75 (Actualizacion)
        rhs = Bx.dot(u[1:Nx, j])
        u_star[1:Nx, j] = spsolve(Ax, rhs)
    aplicar_cf(u_star)
    for i in range(1, Nx):
        rhs = By.dot(u_star[i, 1:Ny])
        u_new[i, 1:Ny] = spsolve(Ay, rhs)
    aplicar_cf(u_new)
    u[:, :] = u_new[:, :]

<<<<<<< HEAD
    # Save snapshots at specified times
    for t_snap in t_snapshots:
        if abs(current_time - t_snap) < dt/2:
            snapshots_dict[t_snap] = u.copy()
            break # Assuming unique snapshot times, we can break once a match is found


# ------------------------
# Visualización 2D y 3D
# ------------------------

print(f"Number of snapshots saved: {len(snapshots_dict)}")

for t in t_snapshots:
    # Ensure there are enough snapshots to plot
    if t in snapshots_dict:
        u_plot = snapshots_dict[t]

        # --------- 2D ---------
        plt.figure(figsize=(6, 5))
=======
    for t_snap in t_snapshots:
        if abs(current_time - t_snap) < dt/2:
            snapshots_dict[t_snap] = u.copy()
            break 

print(f"Numeros de snapshots guardados: {len(snapshots_dict)}")

for t in t_snapshots: 
    if t in snapshots_dict:
        u_plot = snapshots_dict[t]

        plt.figure(figsize=(6,5))
>>>>>>> 6ffca75 (Actualizacion)
        cp = plt.contourf(X, Y, u_plot, 20, cmap='hot')
        plt.colorbar(cp)
        plt.title(f"2D: Temperatura en t = {t:.3f} s")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.tight_layout()
        plt.show()

<<<<<<< HEAD
        # --------- 3D ---------
=======

>>>>>>> 6ffca75 (Actualizacion)
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, u_plot, cmap='hot', edgecolor='k', linewidth=0.3)
        ax.set_title(f"3D: Temperatura en t = {t:.3f} s")
        ax.set_xlabel("x")
<<<<<<< HEAD
        ax.set_ylabel("y")
=======
        ax.set_ylabel("x")
>>>>>>> 6ffca75 (Actualizacion)
        ax.set_zlabel("Temperatura")
        fig.colorbar(surf, shrink=0.5, aspect=10)
        plt.tight_layout()
        plt.show()
<<<<<<< HEAD
    else:
        print(f"Warning: Snapshot for time {t:.3f} not found.")


#Grafico de la evolucion de la temperatura 
=======

    else:
        print(f"Warning: Snapshot for time {t:.3f} not found.")

# Grafico de la evolucion de la temperatura
>>>>>>> 6ffca75 (Actualizacion)

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
<<<<<<< HEAD
from matplotlib.animation import FuncAnimation

# ------------------------
# Parámetros del problema
# ------------------------

Lx, Ly = 1.0, 1.0
Nx, Ny = 50, 50  # Más puntos = mejor resolución, más lento
dx, dy = Lx / Nx, Ly / Ny
=======
from matplotlob.animation import FuncAnimation 

Lx, Ly = 1.0, 1.0
Nx, Ny = 50, 50
dx, dy = Lx / Nx, Ly / Ny

>>>>>>> 6ffca75 (Actualizacion)
x = np.linspace(0, Lx, Nx+1)
y = np.linspace(0, Ly, Ny+1)
X, Y = np.meshgrid(x, y, indexing='ij')

T = 0.1
dt = 0.001
nt = int(T / dt)
alpha = 1.0

<<<<<<< HEAD
# ------------------------
# Condición inicial: pulso gaussiano
# ------------------------

u = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))
u_new = np.zeros_like(u)

# ------------------------
# Condición de frontera: Dirichlet (bordes fijos en 0)
# ------------------------

=======
u = np.exp(-100 * ((X -0.5)**2 + (Y - 0.5)**2))
u_new = np.zeros_like(u)

>>>>>>> 6ffca75 (Actualizacion)
def aplicar_cf(u):
    u[0, :] = 0
    u[-1, :] = 0
    u[:, 0] = 0
    u[:, -1] = 0

<<<<<<< HEAD
# ------------------------
# Construcción de matrices
# ------------------------

rx = alpha * dt / (2 * dx**2)
ry = alpha * dt / (2 * dy**2) # Changed | to *

Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1, 0, 1], shape=(Nx-1, Nx-1))
Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1, 0, 1], shape=(Nx-1, Nx-1))

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1, 0, 1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1, 0, 1], shape=(Ny-1, Ny-1))

# ------------------------
# Evolución temporal: guardamos muchos pasos
# ------------------------

snapshots = []
guardar_cada = 10  # guarda cada 10 pasos de tiempo
=======
rx = alpha * dt / (2 * dx**2)
ry = alpha * dt / (2 * dy**2)

Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))
Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))

snapshots = []
guardar_cada = 10
>>>>>>> 6ffca75 (Actualizacion)

for n in range(nt):
    aplicar_cf(u)
    u_star = np.zeros_like(u)

    for j in range(1, Ny):
        rhs = Bx.dot(u[1:Nx, j])
<<<<<<< HEAD
        u_star[1:Nx, j] = spsolve(Ax, rhs)

    aplicar_cf(u_star)

    for i in range(1, Nx):
        rhs = By.dot(u_star[i, 1:Ny])
        u_new[i, 1:Ny] = spsolve(Ay, rhs)

    aplicar_cf(u_new)
    u[:, :] = u_new[:, :]

    if n % guardar_cada == 0:
        snapshots.append(u.copy())

# ------------------------
# Animación
# ------------------------

print(f"Number of snapshots saved: {len(snapshots)}")
=======
        u_star = np.zeros_like(u)

        for j in range(1, Ny):
            rhs = Bx.dot(u[1:Nx, j])
            u_star[1:Nx, j] = spsolve(Ax, rhs)

        aplicar_cf(u_star)

        for i in range(1, Nx):
            rhs = By.dot(u_star[i, 1:Ny])
            u_new[i, 1:Ny] = spsolve(Ay, rhs)

        aplicar_cf(u_new)
        u[:, :] = u_new[:, :]

        if n % guardar_cada == 0:
            snapshots.append(u.copy())

print(f"Numeros de snapshots guardados: {len(snapshots)}")
>>>>>>> 6ffca75 (Actualizacion)

fig, ax = plt.subplots(figsize=(6, 5))
cp = ax.contourf(X, Y, snapshots[0], 20, cmap='hot')
cb = plt.colorbar(cp)
<<<<<<< HEAD
ax.set_title("Evolución de la temperatura")
=======
ax.set_title("Evolucion de la temperatura")
>>>>>>> 6ffca75 (Actualizacion)
ax.set_xlabel("x")
ax.set_ylabel("y")

def update(frame):
<<<<<<< HEAD
    print(f"Accessing frame: {frame}") # Added print statement
=======
    print(f"Accesing frame: {frame}")
>>>>>>> 6ffca75 (Actualizacion)
    ax.clear()
    cp = ax.contourf(X, Y, snapshots[frame], 20, cmap='hot')
    ax.set_title(f"t = {frame * guardar_cada * dt:.3f} s")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
<<<<<<< HEAD
    return cp.collections
=======
    return cp.collections 
>>>>>>> 6ffca75 (Actualizacion)

anim = FuncAnimation(fig, update, frames=len(snapshots), interval=80)

plt.tight_layout()
plt.show()

<<<<<<< HEAD
# ------------------------
# Para guardar como .mp4 o .gif (opcional)
# ------------------------

# anim.save("difusion_calor.mp4", writer="ffmpeg", fps=20)
# anim.save("difusion_calor.gif", writer="pillow", fps=20)
=======






>>>>>>> 6ffca75 (Actualizacion)
