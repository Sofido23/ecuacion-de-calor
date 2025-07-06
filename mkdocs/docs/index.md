## Proyecto final

## Ecuacion de Calor en Dos Dimensiones

**Universidad de Costa Rica**

**Nombre de los estudiantes:**

Alba Sofia Rojas Doza (C36873)

Oscar Alvarez Poveda (C003949) 

Ricardo Jose Suarez Sancho (C17810)

Karolay Alvarado Navarro (C20359)


**Julio 2025**


## Introduccion

La ecuación de calor en dos dimensiones es una ecuación en derivadas parciales de segundo orden que describe la evolución temporal de la temperatura en una región del espacio bajo condiciones físicas ideales. Esta ecuación toma la forma:

 <p$\frac{\partial u}{\partial t} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$</p>

en donde $u(x,y,t)$ representa la temperatura en la posicion $(x,y)$ en el tiempo $t$ y $c$ es una constante que depende del material y $\Delta^2$ es el operador Laplaciano, que en dos dimensiones toma la forma:

$\Delta^2u = \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$

Este modelo es válido bajo condiciones ideales, como materiales homogéneos, sin fuentes de calor internas y con propiedades térmicas constantes. La ecuación se utiliza para modelar la transferencia de calor en placas, láminas y superficies, siendo fundamental en campos como la ingeniería, la geofísica, la medicina y la ciencia de materiales.

Además,  permite analizar el comportamiento térmico de sistemas bidimensionales sujetos a distintas condiciones iniciales y de frontera.

En el desarrollo del proyecto, se resolvera dicha ecución tanto en Python como en C++, aplicando así prácticas estudiadas en el curso, como el uso apropiado de recursos de memoria, prinicipios de programacion orientada a objetos, paralelismo en memoria compartida y la documentacion y control de versiones con Git. 

Asimismo, debemos de experimentar con diferentes condiciones inciales y de frontera, y visualizar la evolucion temporal de la temperatura mediante mapas de colores. 


## Solución implementada en C++



## Codigo en Python
Dentro de este mismo repositorio hay un archivo.py en donde se encuentra el codigo en Python. Esta seccion se basa en la explicacion de dicho codigo. 

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))

for n in range(nt):
  
