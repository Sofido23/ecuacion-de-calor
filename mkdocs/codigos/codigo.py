#Grafico de la distribucion de temperatura en t=0.100

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

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
plt.title("Distribución de temperatura en t = {:.3f}".format(T))
plt.xlabel("x")
plt.ylabel("y")
plt.show()



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
Nx, Ny = 20, 20
dx, dy = Lx / Nx, Ly / Ny

x = np.linspace(0, Lx, Nx+1)
y = np.linspace(0, Ly, Ny+1)
X, Y = np.meshgrid(x, y, indexing='ij')

T = 0.1
dt = 0.001
nt = int(T / dt)
alpha = 1.0

# Opciones que puedes cambiar:
ci_opcion = 'gaussiana'    # 'gradiente', 'doble_pulso'
cf_opcion = 'dirichlet'    # 'neumann', 'robin'

# ------------------------
# Condición inicial
# ------------------------

u = np.zeros((Nx+1, Ny+1))
u_new = np.zeros_like(u)

if ci_opcion == 'gaussiana':
    u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))
elif ci_opcion == 'gradiente':
    u[:, :] = X
elif ci_opcion == 'doble_pulso':
    u[:, :] = np.exp(-400 * ((X - 0.25)**2 + (Y - 0.75)**2)) + np.exp(-400 * ((X - 0.75)**2 + (Y - 0.25)**2))

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

# ------------------------
# Evolución temporal
# ------------------------

snapshots_dict = {}  # Para guardar u en momentos seleccionados
t_snapshots = [0.01, 0.025, 0.05, 0.1]


for n in range(nt + 1):
    current_time = n * dt
    aplicar_cf(u)
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
        cp = plt.contourf(X, Y, u_plot, 20, cmap='hot')
        plt.colorbar(cp)
        plt.title(f"2D: Temperatura en t = {t:.3f} s")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.tight_layout()
        plt.show()

        # --------- 3D ---------
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, u_plot, cmap='hot', edgecolor='k', linewidth=0.3)
        ax.set_title(f"3D: Temperatura en t = {t:.3f} s")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("Temperatura")
        fig.colorbar(surf, shrink=0.5, aspect=10)
        plt.tight_layout()
        plt.show()
    else:
        print(f"Warning: Snapshot for time {t:.3f} not found.")


#Grafico de la evolucion de la temperatura 

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from matplotlib.animation import FuncAnimation

# ------------------------
# Parámetros del problema
# ------------------------

Lx, Ly = 1.0, 1.0
Nx, Ny = 50, 50  # Más puntos = mejor resolución, más lento
dx, dy = Lx / Nx, Ly / Ny
x = np.linspace(0, Lx, Nx+1)
y = np.linspace(0, Ly, Ny+1)
X, Y = np.meshgrid(x, y, indexing='ij')

T = 0.1
dt = 0.001
nt = int(T / dt)
alpha = 1.0

# ------------------------
# Condición inicial: pulso gaussiano
# ------------------------

u = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))
u_new = np.zeros_like(u)

# ------------------------
# Condición de frontera: Dirichlet (bordes fijos en 0)
# ------------------------

def aplicar_cf(u):
    u[0, :] = 0
    u[-1, :] = 0
    u[:, 0] = 0
    u[:, -1] = 0

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

for n in range(nt):
    aplicar_cf(u)
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

# ------------------------
# Animación
# ------------------------

print(f"Number of snapshots saved: {len(snapshots)}")

fig, ax = plt.subplots(figsize=(6, 5))
cp = ax.contourf(X, Y, snapshots[0], 20, cmap='hot')
cb = plt.colorbar(cp)
ax.set_title("Evolución de la temperatura")
ax.set_xlabel("x")
ax.set_ylabel("y")

def update(frame):
    print(f"Accessing frame: {frame}") # Added print statement
    ax.clear()
    cp = ax.contourf(X, Y, snapshots[frame], 20, cmap='hot')
    ax.set_title(f"t = {frame * guardar_cada * dt:.3f} s")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return cp.collections

anim = FuncAnimation(fig, update, frames=len(snapshots), interval=80)

plt.tight_layout()
plt.show()

# ------------------------
# Para guardar como .mp4 o .gif (opcional)
# ------------------------

# anim.save("difusion_calor.mp4", writer="ffmpeg", fps=20)
# anim.save("difusion_calor.gif", writer="pillow", fps=20)
