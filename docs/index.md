#Proyecto final

#Ecuacion de Calor en Dos Dimensiones

**Universidad de Costa Rica**

**Nombre de los estudiantes:**

Alba Sofia Rojas Doza (C36873)

Oscar Alvarez Poveda (C003949) 

Ricardo Jose Suarez Sancho (C17810)

Karolay Alvarado Navarro (C20359)


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


## Codigo en C++



## Codigo en Python
Dentro de este mismo repositorio hay un archivo.py en donde se encuentra el codigo en Python. Esta seccion se basa en la explicacion de dicho codigo. 

Ay = diags([[-ry]*(Ny-1), [1+2*ry]*(Ny-1), [-ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))
By = diags([[ry]*(Ny-1), [1-2*ry]*(Ny-1), [ry]*(Ny-1)], [-1,0,1], shape=(Ny-1, Ny-1))

for n in range(nt):
  
