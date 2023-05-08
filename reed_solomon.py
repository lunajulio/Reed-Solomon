import sympy
import itertools
import numpy as np
from sympy import *


def get_codeword(poly, values_coefficients, alpha):
    codeword = ""
    for val in values_coefficients:
        codeword += str(poly.subs(x, val) % alpha)
    return codeword


def polinomio(coefficients, values_coefficients):
    list = []
    # Generar todas las posibles combinaciones de coeficientes en el alfabeto
    coef_combinations = itertools.product(
        values_coefficients, repeat=len(coefficients))
    for coef in coef_combinations:
        p = sympy.Poly(sum([coef[i] * x**i for i in range(k)]), x)
        list.append(p.as_expr())
    return list


def generator_matrix(values_coefficients, k, alpha):
    matrix = np.zeros((k, len(values_coefficients)))
    for i in range(k):
        for j in range(len(values_coefficients)):
            matrix[i][j] = ((values_coefficients[j]**i) % alpha)
    return matrix


def calcular_ecuaciones(coeficientes, posicion_despeje):
    # cantidad de variables
    vars = ["" for i in range(len(coeficientes))]

    # Creamos una lista con las variables
    for i in range(len(vars)):
        vars[i] = symbols(f'x{i+1}')

    # Creamos la ecuación a partir del vector de coeficientes
    ecuacion = 0
    for i in range(len(coeficientes)):
        if coeficientes[i] != 0:
            ecuacion += (int(coeficientes[i]) % alpha)*vars[i]

    # Despejamos la variable seleccionada
    variable_despeje = vars[posicion_despeje]
    solucion = solve(ecuacion, variable_despeje)

    # convertimos las ecuaciones al espacio Z_alpha
    for var in vars:
        coef = solucion[0].coeff(var)
        solucion[0] = solucion[0] - coef*var + (coef % alpha)*var
    return solucion[0]


def sindrome(H, c):
    lider = []
    for i in c:
        lider.append(int(i) % alpha)
    lider = list(map(list, zip(lider)))  # se transpone el lider
    # se multiplica H*liderT
    return ([[sum(x*y for x, y in zip(row, col)) for col in zip(*lider)] for row in H])


def generar_cadenas(n, alpha):
    if n == 0:
        return ['']
    cadenas = []
    for cadena in generar_cadenas(n-1, alpha):
        for letra in range(alpha):
            cadenas.append(cadena + str(letra))
    return cadenas


d = 9999
n = int(input("Enter lenght of code: "))
while n <= 0:
    n = int(input("Enter lenght of code again, this can´t be less than zero: : "))

d = int(input("Enter the minimun distance: "))
while (n < d or d < 0):
    d = int(input("Enter the minimun distance: "))

alpha = int(input("Which alphabet do you want to work in? \n Enter the number that you wanna do: \n 2- Binary \n 3- Ternary \n 4- Quaternary \n or more... \n"))

while alpha < 2:
    alpha = int(input("Which alphabet do you want to work in? \n Enter the number that you wanna do: \n 2- Binary \n 3- Ternary \n 4- Quaternary \n or more... \n"))

# Calculamos el grado k
k = n - d + 1
# Hallamos los polinomios del código
x = sympy.symbols('x')
coefficients = [sympy.symbols('a%d' % i) for i in range(k)]
print("coeficients: ", coefficients)

values_coefficients = list(range(alpha))
print(values_coefficients)

polynomies = polinomio(coefficients, values_coefficients)

C = []

for poly in polynomies:
    print(poly)
    C.append(get_codeword(poly, values_coefficients, alpha))

print("Codewords: ", C, "\n Total codewords: ", len(C))

gen_matrix = generator_matrix(values_coefficients, k, alpha).tolist()

print("Generator matrix:")
for fila in gen_matrix:
    print([int(i) for i in fila])


# Calcular la forma escalonada reducida por filas de la matriz en Z_alpha
for i in range(len(gen_matrix)):
    # Encontrar el índice de la primera entrada no nula en la fila i
    pivot = -1
    for j in range(len(gen_matrix[i])):
        if gen_matrix[i][j] != 0:
            pivot = j
            break
    if pivot == -1:
        continue
    # Hacer la entrada pivot de la fila i igual a 1
    factor = pow(int(gen_matrix[i][pivot]), -1, alpha)
    for j in range(len(gen_matrix[i])):
        gen_matrix[i][j] = gen_matrix[i][j] * factor % alpha
    # Hacer las otras entradas en la columna pivot iguales a cero
    for j in range(len(gen_matrix)):
        if j != i and gen_matrix[j][pivot] != 0:
            factor = gen_matrix[j][pivot]
            for k in range(len(gen_matrix[j])):
                gen_matrix[j][k] = (gen_matrix[j][k] -
                                    factor * gen_matrix[i][k]) % alpha

# Imprimir la matriz escalonada reducida por filas en Z_alpha
print("Generator matrix in standard form:")
for fila in gen_matrix:
    print([int(i) for i in fila])

# creamos el vector representativo que nos ayudará a hallar la matriz de control
vector = [1]*len(gen_matrix[0])

# calculamos las ecuaciones para sacar sus coeficientes
for i in range(len(gen_matrix)):
    eq = calcular_ecuaciones(gen_matrix[i], i)
    eq = Poly(eq)
    coef_vector = eq.coeffs()
    vector[i] = coef_vector

H = np.zeros((len(vector[0]), len(gen_matrix[0])))
counter = 0

# Armamos la matriz de control H con los coeficientes hallados
for i in range(len(vector)):
    if type(vector[i]) == type(vector):
        for j in range(len(vector[i])):
            H[j][i] = int((vector[i])[j])
    else:
        H[counter][i] = 1
        counter += 1

print("Control matrix:")
for fila in H:
    print(fila)


# ------------ decodificacion por síndrome -----------

code = C.copy()
lideres = [code[0]]
clases_laterales = [code]
espacio = generar_cadenas(n, alpha)

# buscamos un lider en el espacio
for lider in espacio:
    clase = []
    # si el elemento seleccionado no está en el código, sirve como lider de clase
    if not (lider in code):
        lideres.append(lider)
        # sumamos el lider con el código para hallar su clase lateral
        for codeword in C:
            suma = ''
            for i in range(len(codeword)):
                suma += str((int(lider[i])+int(codeword[i])) % alpha)
            if not (suma in code):
                code.append(suma)
                clase.append(suma)
        # guardamos la clase lateral
        clases_laterales.append(clase)

# calculamos los síndromes de los lideres
sindromes = []
for lider in lideres:
    sindromes.append(sindrome(H, lider))

# convertimos al espacio Z_alpha
for i in range(len(sindromes)):
    for j in range(len(sindromes[0])):
        (sindromes[i][j])[0] %= alpha

# corregimos el codeword  recivido
recivo = input("Enter the recived codeword: ")
# hallamos el síndrome del codeword recivido
sind = sindrome(H, recivo)
for num in sind:
    num[0] %= alpha
# encontramos al lider de la clase correspondiente del síndrome
lid = lideres[sindromes.index(sind)]
# restamos el codeword recivido y el lider de la clase lateral
resta = ''
for i in range(len(recivo)):
    resta += str((int(recivo[i])-int(lid[i])) % alpha)

print(f"The correct codeword is: {resta}")
