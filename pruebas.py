from sympy import symbols, solve
import numpy as np

# Pedimos al usuario que ingrese el vector de coeficientes y la posición de la variable a despejar
coeficientes = list(map(int, input("Ingrese el vector de coeficientes separados por comas: ").split(",")))
posicion_despeje = int(input("Ingrese la posición de la variable a despejar (0 para x, 1 para y, 2 para z, 3 para a, 4 para b): "))

vars = ["" for i in range(5)]

for i in range(len(vars)):
    vars[i] = symbols(f'x{i+1}')

print(vars)

# Creamos una lista con las variables


# Creamos la ecuación a partir del vector de coeficientes
ecuacion = 0
for i in range(len(coeficientes)):
    if coeficientes[i] != 0:
        ecuacion += coeficientes[i]*vars[i]

# Despejamos la variable seleccionada
variable_despeje = vars[posicion_despeje]
print("La ecuación es:", ecuacion)
solucion = solve(ecuacion, variable_despeje)

# Imprimimos la ecuación y la solución

print("La solución de", str(variable_despeje), "es:", solucion[0])
