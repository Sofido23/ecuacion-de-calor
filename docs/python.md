# En el presente apartado explicaremos a detalle cada linea de codigo de la resolucion de la Ecuacion de calor realizada en Python.

## Grafico de la distribucion de la temperatura en t=0.100:

Primeramente,kdsjcfsd

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.sparse import diags
    from scipy.sparse.linalg import spsolve

    #Definimos las dimensiones físicas del dominio en x e y
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
    
    Comienza el lazo de integración temporal
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
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
