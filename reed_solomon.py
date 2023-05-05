import sympy
import itertools
import numpy as np
from sympy import *

'''def polinomio(coeficients, values_coeficients):
    list = []
    # Sustituir valores de coeficientes en el polinomio usando ciclos anidados
    for a0_val in values_coeficients:
        p = sympy.Poly(sum([coeficients[i] * x**i for i in range(d)]), x)
        p_a0 = p.subs(coeficients[d-1], a0_val)  # Sustituir el primer coeficiente
        for coef_val in values_coeficients:
            p_ai = p_a0
            for i in range(d-1):
                p_ai = p_ai.subs(coeficients[i], coef_val)  # Sustituir los demás coeficientes
            print(p_ai)
            list.append(p_ai)
    return list '''


def decodificate():
    return ""


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
    print(f"La ecuación {posicion_despeje + 1} es: {ecuacion} = 0")
    solucion = solve(ecuacion, variable_despeje)

    # convertimos las ecuaciones al espacio Z_alpha
    for var in vars:
        coef = solucion[0].coeff(var)
        solucion[0] = solucion[0] - coef*var + (coef % alpha)*var

    # Imprimimos la ecuación y la solución
    print(str(variable_despeje), " = ", solucion[0])
    return solucion[0]


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

# Calculate the degree
k = n - d + 1
# We need to find the polinomies of the code
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

vector = [1]*len(gen_matrix[0])

for i in range(len(gen_matrix)):
    eq = calcular_ecuaciones(gen_matrix[i], i)
    eq = Poly(eq)
    coef_vector = eq.coeffs()
    vector[i] = coef_vector

H = np.zeros((len(vector[0]), len(gen_matrix[0])))
counter = 0

for i in range(len(vector)):
    if type(vector[i]) == type(vector):
        for j in range(len(vector[i])):
            H[j][i] = int((vector[i])[j])
    else:
        H[counter][i] = 1
        counter += 1

print(f"H = {H}")
