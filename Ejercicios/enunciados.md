

## Ejercicio 2

Escriba un código que lea el archivo `hamlet.txt` y encuentre las
`n_palabras` palabras de mas de `n_letras` que mas se repiten en el
texto. 
Por ejemplo, si `n_palabras=5` y `n_letras=3` el codigo debe encontrar
las cinco palabras de mas de tres letras que mas se repiten en el
texto.   

## Ejercicio 4

Escriba un codigo que dibuje [La Flor de la
Vida](https://es.wikipedia.org/wiki/Flor_de_la_Vida).  

## Ejercicio 7

## Tarea 1

Consideren un pueblo con 50 habitantes y 100 casas.
Las casas se distribuyen en una cuadricula de 10 por 10. 
Hay 25 habitantes de color verde y 25 habitantes de color rojo.
Vamos a simular un proceso de migracion dentro de la ciudad.
Para esto vamos a pensar en un total de 500 mudanzas que se
hacen de manera secuencial.

Cada proceso de mudanza implica los siguientes pasos.
1. Un ciudadano es elegido al azar.
2. Un lugar vacante es elegido al azar.
3. El ciudadano completa su mudanza si es mas feliz en el 
   lugar a donde llega.
   
La felicidad en esta simulacion es un numero real entre 0 y 1
y depende del numero de vecinos que tienen el mismo color que 
el ciudadano que quiere mudarse.

Si todos los vecinos son del otro color la felicidad es 0.
Si hay un balance perfecto entre colores de los vecinos la felicidad es 1.
Si todos los vecinos son de su mismo color la felicidad es 0.5.
(Ver la Figura 1 de [este enlace](http://nadaesgratis.es/jose-luis-ferreira/recordando-a-schelling-y-su-modelo-de-segregacion)).

Escriba un codigo que asigne aleatoriamente a los habitantes al comienzo
y luego complete 500 mudanzas. El codigo debe graficar el estado inicial y final del pueblo.




