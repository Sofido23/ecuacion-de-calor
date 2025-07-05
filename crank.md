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
 