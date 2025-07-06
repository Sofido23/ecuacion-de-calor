## Condiciones Iniciales
En la ecuacion de calor en 2D, las condiciones inciales definen como esta distribuida la temperatura en todo el dominio espacial en un tiempo inicial. Las condiciones inciales y de frontera son esenciales porque determinan completamente la evolucion temporal de la temperatura. 
A continuacion, se explicaran a detalle cada una de las condiciones iniciales que se utilizaron para la resolucion de la ecuacion de calor en 2D: 

**1) Pulso gaussiano centrado en (0.5, 0.5):**

    u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2))

Esta es una distribucion de temperatura con forma de campana gaussiana centrada en el centro del dominio; en donde su valor maximo es 1 en el centro y decrece suavemente hacia los bordes. Esta condicion inicial representa una fuente de calor de puntual suave ubicada en el centro de la placa, esta distribucion permite observar como se difunde el calor de forma homogenea hacia todas las direcciones. 

**2) COndiciones inciales definidas por opcion (ci_opcion)**

**3) Barra Centrada**

## Condiciones de Frontera 

**1) Dirichlet**

**2) Neumann**

**3) Robin**
