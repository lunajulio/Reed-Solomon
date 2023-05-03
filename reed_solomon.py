import sympy
import itertools
import numpy as np

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


# Calcular la forma escalonada reducida por filas de la matriz en Z5
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
    factor = pow(int(gen_matrix[i][pivot]), -1, 5)
    for j in range(len(gen_matrix[i])):
        gen_matrix[i][j] = gen_matrix[i][j] * factor % 5
    # Hacer las otras entradas en la columna pivot iguales a cero
    for j in range(len(gen_matrix)):
        if j != i and gen_matrix[j][pivot] != 0:
            factor = gen_matrix[j][pivot]
            for k in range(len(gen_matrix[j])):
                gen_matrix[j][k] = (gen_matrix[j][k] -
                                    factor * gen_matrix[i][k]) % 5

# Imprimir la matriz escalonada reducida por filas en Z5
print("Generator matrix in standard form:")
for fila in gen_matrix:
    print([int(i) for i in fila])