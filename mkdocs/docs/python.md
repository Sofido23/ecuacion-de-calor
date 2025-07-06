# En el presente apartado explicaremos a detalle cada linea de codigo de la resolucion de la Ecuacion de calor realizada en Python.

## Grafico de la distribucion de la temperatura en t=0.100:

Primeramente, debemos de realizar las importaciones de las bibliotecas. 

Numpy para trabajar con arrays, matplotlib.pyplot para la visualizacion de la solucion, scipy.sparse.diags para construir matrices dispersas tridiagonales y spsolve para resolver sistemas lineales dispersos. 

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.sparse import diags
    from scipy.sparse.linalg import spsolve

Definimos las dimensiones físicas del dominio en x en y.
Estos son los largos del dominio en x e y respectivamente (dominio de 1x1 unidad), es decir, la longitud del dominio en x y en y.

    Lx, Ly = 1.0, 1.0  
    
Definimos la cantidad de divisiones del dominio

    Nx, Ny = 20, 20  

Calculamos el tamaño de paso espacial en x y en y. Es decir, la distancia entre nodos consecutivos en cada eje

    dx, dy = Lx / Nx, Ly / Ny  
    
Creamos los arreglos de coordenadas espaciales. 
Son los puntos equiespaciados de 0 a Lx (incluyendo extremos) y los puntos equiespaciados de 0 a Ly (incluyendo extremos). 

    x = np.linspace(0, Lx, Nx+1) 
    y = np.linspace(0, Ly, Ny+1)  
    
Parámetros de tiempo para la simulación. En donde T es el tiempo total de simulación, dt es el paso temporal y nt el número total de pasos de tiempo.

    T = 0.1     
    dt = 0.001  
    nt = int(T / dt)  

Constante de difusión térmica (puede representar conductividad térmica, por ejemplo)

    alpha = 1.0
    
Inicialización de la matriz de temperatura u en todo el dominio, se crea la condicion inicial. 

En donde u es la temperatura inicial en t = 0, u_new es la matriz que contendrá la temperatura actualizada.

X , Y genera la malla 2D (X, Y) para aplicar condiciones iniciales y u[:, :] asigna la condición inicial, es decir, se crea un pulso gaussiano centrado en (0.5, 0.5) que representa el calor localizado. 

    u = np.zeros((Nx+1, Ny+1))       
    u_new = np.zeros_like(u)         
    
    X, Y = np.meshgrid(x, y, indexing='ij')  # 'ij' para mantener coherencia con el orden u[i,j]
    
    u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))  # Pico de calor localizado

    
Cálculo de parámetros auxiliares para Crank-Nicolson en x en y. Se divide entre 2 porque este metodo usa promedios de tiempo. 

    rx = alpha * dt / (2 * dx**2)  
    ry = alpha * dt / (2 * dy**2)  
    
Construcción de matrices tridiagonales sparse (esparcidas) para el método implícito en x y en y. En donde Ax y Ay son matrices implicitas (lado izquierdo) y Bx y By son matrices explicitas (lado derecho).

Estas matrices surgen de discretizar la ecuacion de calor con Crank-Nicolson. Tienen forma diagonal porque segundas derivadas generan diferencias de 3 terminos. 

    Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))  
    Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1,0,1], shape=(Nx-1, Nx-1))    

    Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))  
    By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))    

    
Comienza el lazo de integración temporal, el for n in range(nt) es el bucle de tiempo principal, es decir, repite la solucion por cada paso de tiempo.

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
    
Actualizamos la solución completa para el siguiente paso de tiempo. Se copia el resultado actualizado de u_new a u. 
        u[:, :] = u_new[:, :]  

Visualización, se crea un mapa de calor con 20 niveles de contorno, usa la escala de colores 'hot' para mostrar la temperatura y muestra el estado final despues de todos los pasos de tiempo.

    plt.figure(figsize=(6,5))
    cp = plt.contourf(X, Y, u, 20, cmap='hot')
    plt.colorbar(cp)
    plt.title("Distribución de temperatura en t = {:.3f}".format(T))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

## Graficos en 2D y 3D en distintos tiempos

Se agrega Axes3D, el cual habilita graficos 3D. 

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.sparse import diags
    from scipy.sparse.linalg import spsolve
    from mpl_toolkits.mplot3d import Axes3D  # Para 3D

Parametros del problema; define el tamano fisico del dominio, lo divide en 20 intervalos y calcula el tamano de paso espacial. 
    
    Lx, Ly = 1.0, 1.0
    Nx, Ny = 20, 20
    dx, dy = Lx / Nx, Ly / Ny

Crea los puntos de la malla y genera matrices 2D X, Y para evaluar funciones sobre el dominio. 
    
    x = np.linspace(0, Lx, Nx+1)
    y = np.linspace(0, Ly, Ny+1)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    T = 0.1
    dt = 0.001
    nt = int(T / dt)
    alpha = 1.0
    
Opciones que puedes cambiar, en donde ci_opcion define la condicion inicial y cf_opcion elige el tipo de condicion de frontera. 

    ci_opcion = 'gaussiana'    # 'gradiente', 'doble_pulso'
    cf_opcion = 'dirichlet'    # 'neumann', 'robin'
    
Condición inicial

    u = np.zeros((Nx+1, Ny+1))
    u_new = np.zeros_like(u)

Creacion de distintas distribuciones iniciales de temperatura, la 'gaussiana' es un pico en el centro, la 'gradiente' la temperatura aumenta de izquierda a derecha y el 'doble_pulso' son dos puntos calientes. 

    if ci_opcion == 'gaussiana':
        u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))
    elif ci_opcion == 'gradiente':
        u[:, :] = X
    elif ci_opcion == 'doble_pulso':
        u[:, :] = np.exp(-400 * ((X - 0.25)**2 + (Y - 0.75)**2)) + np.exp(-400 * ((X - 0.75)**2 + (Y - 0.25)**2))
    
Construcción de matrices, en donde rx y ry es el calculo de parametros de estabilidad y Ax, Bx, Ay, By es la construccion de matrices implicitas y explicitas en x y en y. 
    
    rx = alpha * dt / (2 * dx**2)
    ry = alpha * dt / (2 * dy**2)
    
    Ax = diags([[-rx]*(Nx-1), [1+2*rx]*(Nx-1), [-rx]*(Nx-1)], [-1, 0, 1], shape=(Nx-1, Nx-1))
    Bx = diags([[rx]*(Nx-1), [1-2*rx]*(Nx-1), [rx]*(Nx-1)], [-1, 0, 1], shape=(Nx-1, Nx-1))
    
    Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1, 0, 1], shape=(Ny-1, Ny-1))
    By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1, 0, 1], shape=(Ny-1, Ny-1))

Condición de frontera, en 'dirichlet' la temperatura es fija en 0 en todos los bordes, en 'neumann' el flujo es cero, el borde copia al punto vecino y en 'robin' es una mezcla entre Dirichlet y Neumann. 
    
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

Evolución temporal, snapshots_dict y t_snapshots guardan soluciones intermedias para visualizarlas despues. 
el for n in range(nt + 1) aplica condiciones de frontera al estado actual, el for j in range(1, Ny) resuelve el sistema en direccion x para cada fila j, for i in range(1, Nx) resuelve en direccion y para cada columna i.

    snapshots_dict = {}  
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

Se aplica las condiciones de frontera al nuevo resultado y lo guarda:

        aplicar_cf(u_new)
        u[:, :] = u_new[:, :]
    
Se guarda la temperatura en t_snap si se esta en ese instante de tiempo.

        for t_snap in t_snapshots:
            if abs(current_time - t_snap) < dt/2:
                snapshots_dict[t_snap] = u.copy()
                break 

Visualizacion en 2D y 3D
    
    print(f"Number of snapshots saved: {len(snapshots_dict)}") #Muestra cuantas instantaneas se guardaron. 
    
    for t in t_snapshots:
        # Ensure there are enough snapshots to plot
        if t in snapshots_dict:
            u_plot = snapshots_dict[t]
    
2D
            plt.figure(figsize=(6, 5))
            cp = plt.contourf(X, Y, u_plot, 20, cmap='hot')
            plt.colorbar(cp)
            plt.title(f"2D: Temperatura en t = {t:.3f} s")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.tight_layout()
            plt.show()
    
3D
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
            print(f"Warning: Snapshot for time {t:.3f} not found.")  #Si no se pudo guardar la instantanea de un tiempo solicitado. 
