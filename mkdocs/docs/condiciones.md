## Condiciones Iniciales
En la ecuacion de calor en 2D, las condiciones inciales definen como esta distribuida la temperatura en todo el dominio espacial en un tiempo inicial. Las condiciones inciales y de frontera son esenciales porque determinan completamente la evolucion temporal de la temperatura. 
A continuacion, se explicaran a detalle cada una de las condiciones iniciales que se utilizaron para la resolucion de la ecuacion de calor en 2D: 

**1) Campana Gaussiana Centrada:**

    u[:, :] = np.exp(-100 * ((X - 0.5)**2 + (Y - 0.5)**2)) 

**2) Paraboloide Centrado:**

**3) Onda Senosoidal:**

----------------------------------------------------------------------------------------------------------------------

## Condiciones de Frontera 

**1) Dirichlet:**

**2) Neumann:**

**3) Robin:**
