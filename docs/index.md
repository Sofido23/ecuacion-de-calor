#Proyecto final

#Ecuacion de Calor en Dos Dimensiones

**Universidad de Costa Rica**

**Nombre de los estudiantes:**

Alba Sofia Rojas Doza (C36873)

Oscar Alvarez Poveda (C003949 

Ricardo Jose Suarez Sancho (C17810)

Karolay..


**Julio 2025**


## Introduccion

El presente proyecto, referente a la ecuacion de calor en dos dimensiones, tiene como fin resolver dicha ecuacion, la cual, es una ecuacion en derivadas parciales que modela la distribucion de la temperatura en una region del plano a lo largo del tiempo. La ecuacion de calor es indispensable en la fisica y la ingenieria, puesto que describe procesos de difusion termica en medios homogeneos bajo condiciones ideales. 

La ecuacion de movimiento esta dada por 

$$ 
\frac{\partial u}{\partial t} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)
$$

en donde u(x,y,t) representa la temperatura en la posicion (x,y) en el tiempo t y c es una constante que depende del material. 

En el desarrollo del proyecto, se resolvera dicha ecucion tanto en Python como en C++, aplicando asi practicas estudiadas en el curso, comi el uso apropiado de recursos de memoria, prinicipios de programacion orientada a objetos, paralelismo en memoria compartida y la documentacion y control de versiones con Git. 

Asimismo, debemos de experimentar con diferentes condiciones inciales y de frontera, y visualizar la evolucion temporal de la temperatura mediante mapas de colores. 

La resolucion de la ecuacion de calor en dos dimensiones, integra conocimientos teoricos y practicos en analisis numericos, programacion cientifica y visualizacion de datos, con el fin de construir una simulacion robusta y eficiente del comportamiento termico de un sistema bidimensional. 


## Metodo de Crank-Nicolson

Este metodo consiste en una tecnica numerica para resolver ecuaciones diferenciales parciales, especialmente la ecuacion de calor o ecuacion de difusion. Es un metodo implicito y de segundo orden; por lo que combina la precision del metodo del punto medio y la estabilidad del metodo implicito. 
En sintesis, este metodo se basa en una promediacion entre el metodo explicito, que evalua  en el tiempo actual tn y el metodo implicito, que evalua en el siguiente tiempo tn+1. 
En el apartado de los codigos, se explicara a detalle los codigos realizados con el fin de comprender a totalidad como funciona el metodo de Crank-Nicolson para resolver la ecuacion de calor en 2D. 
  
  
## Beneficios y desventajas de Crank-Nicolson 
Se indicaran los beneficios y desventajas que posee el uso del metodo de Crank-Nicolson:

Beneficios:

1) Estabilidad incondicional: Es estable para cualquier tamano de paso en el tiempo, lo que permite hacer simulaciones con pasos grandes sin que el error explote. 

2) Mayor precision: Tanto el tiempo como el espacio es de segudno orden, significa que es mas preciso que los metodos de primer orden, como lo es el metodo explicito o el implicito simple. 

3) Simetria temporal: Este metodo es centrado en el tiempo, lo que lo hace ideal para problemas en donde se debe de conservar energia o simetria. 

Desventajas:

1) Se requiere resolver un sistema lineal en cada paso: Con el metodo de Crank-Nicolson tenemos que resolver matrices en cada paso del tiempo, lo que es mucho mas costoso computacionalmente. 

2) Oscilaciones no fisicas: Si esto se aplica a problemas de condiciones inciales, puede producir oscilaciones no reales.

3) Implementacion mas compleja: Este metodo requiere mas trabajo para programarlo, puesto que combina terminos del tiempo actual y del siguiente paso.
 

## Codigo en C++



## Codigo en Python
Dentro de este mismo repositorio hay un archivo.py en donde se encuentra el codigo en Python. Esta seccion se basa en la explicacion de dicho codigo.

##Codigo para la distribucion de temperatura en t = 0.100

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
  
