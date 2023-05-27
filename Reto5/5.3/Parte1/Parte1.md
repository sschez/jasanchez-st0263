# Info de la materia: ST0263 Topicos Especiales en Telematica

# Estudiante: Jose Alejandro Sánchez Sánchez

# Profesor: Edwin Nelson Montoya, emontoya@eafit.brightspace.com

# Reto 5.3 - Parte 1

# Descripcion de la actividad

Ejercicios básicos de MapReduce con MRJOB en python

## Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Para el conjunto de datos: dataempleados.csv

  1. Calcular el promedio salarial por Sector Económico (SE).
  2. Determinar el salario promedio por empleado.
  3. Contar el número de SE por empleado a lo largo del período estadístico.

- Para el conjunto de datos: datempresas.csv

  1. Para cada acción, encontrar el día de menor valor y el día de mayor valor.
  2. Obtener la lista de acciones que siempre han experimentado aumentos o se han mantenido estables.
  3. Identificar el "Día Negro": el día en el que la mayor cantidad de acciones tienen el menor valor (desplome), asumiendo una inflación constante a lo largo del tiempo.

- Para el conjunto de datos: datapeliculas.csv

  1. Calcular el número de películas vistas por usuario y el promedio de calificación.
  2. Determinar el día en el que se han visto la mayor cantidad de películas.
  3. Identificar el día en el que se han visto la menor cantidad de películas.
  4. Contar el número de usuarios que han visto una misma película y calcular el promedio de calificación.
  5. Determinar el día en el que los usuarios han dado la peor evaluación en promedio.
  6. Identificar el día en el que los usuarios han dado la mejor evaluación.
  7. En cada género, encontrar la película mejor evaluada y la peor evaluada.

## Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se realizo lo que se propuso

# Descripcion del ambiente de ejecucion

- WSL - Ubuntu 22.04
- Windows 10
- Python3.10
  - MRJob

# Ejecucion de la actividad

Para ejecutar localmente los ejercicios se hace necesario instalar MRJob, una libreria para ejecutar map-reduce en python. La instalamos con el comando `pip install mrjob`

Despues de eso descargamos los datasets necesarios para el ejercicio. Estos son `datapeliculas`, `dataempresas` y `dataempleados`