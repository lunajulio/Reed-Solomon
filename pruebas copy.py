from sympy import symbols, solve

# Solicitar al usuario que ingrese los coeficientes de las variables
a = float(input("Ingrese el coeficiente de x: "))
b = float(input("Ingrese el coeficiente de y: "))
c = float(input("Ingrese el coeficiente de z: "))

# Definir las variables y la expresión lineal
x, y, z, d = symbols(f'x y z d')

print(type(x))
expr = a*x + b*y + c*z

expr += 5*d + 0

print(expr)

# Resolver la ecuación lineal en términos de x
sol = solve(expr, x)

# Imprimir la solución
print("El valor de x es:", sol[0])
