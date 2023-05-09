# Teoría de códigos 2023-10

# Taller Reed Solomon G7 - Corte 3

## Universidad del Norte

**Profesora:** Darling Vasquez

**Estudiantes:** 

- Luna Julio Martínez 200165451
- Jason Estrada Russill 200191602

# Enunciado

Muestre la construcción del código [5,3] de Reed Solomon sobre 𝐹5, por medio de 
un programa el cual deberá calcular:

- Longitud.

- Dimensión.

- Distancia mínima o peso mínimo.

- Conjunto de polinomios $𝐹_5[𝑥]_3$.

- Matriz de generadora.

- Decodificación de la palabra recibida $𝑣 = 10210$.

# Pseudocódigo del programa

## Parámetros de entrada:

**Longitud de los codewords:** Se pide al usuario ingresar la longitud requerida para los codewords teniendo en cuenta que debe ser mayor que cero.

```python
Leer n
Mientras n <= 0 hacer
    Leer n
Fin mientras
```

**Distancia mínima:** El usuario tiene que ingresar la longitud mínima del código. La distancia mínima tiene que ser menor que la longitud y mayor que cero.

```python
Leer d
Mientras (n < d o d < 0) hacer
    Leer d
Fin mientras
```

**Espacio $F_n$:**  El usuario tiene que ingresar el espacio cardinalmente, es decir, $q$. Este valor tiene que cumplir la desigualdad $n \leq q$ y el espacio puede empezar desde binario hasta dónde el usuario requiera.

```python
Leer alpha
Mientras alpha < 2 o n > alpha hacer
    Leer alpha
Fin mientras
```

Si el usuario quiere confirmar los datos ingresados, simplemente se imprimen (igual también se pide mostrar la longitud, dimensión y distancia mínima)

```python
Escribir("La longitud es:" , n)
Escribir("La distancia mínima es:" , d)
Escribir("La cardinalidad del espacio es: ", alpha)
```

## ¿Cómo calculamos el conjunto de polinomios $F_5[x]_3$?

Primero se tiene que calcular el máximo grado de los polinomios, este será igual a: 

```python
k = n - d + 1
```

> Para este punto el usuario ya habrá ingresado el valor de $n$ (longitud) y la $d$ (distancia mínima).

Luego, por medio de una librería llamada **Sympy** (biblioteca de Python para matemáticas simbólicas que permite realizar cálculos matemáticos complejos de manera sencilla y eficiente) se crean los coeficientes necesarios para armar los polinomios hasta máximo un grado $k$.

```python
Para i desde 0 hasta k-1 hacer
    coefficients[i] = symbols('a' + i)
Fin Para
```

Después de crear los coeficientes, se creará una lista con los posibles valores que puede tomar cada coeficiente de los polinomios, es decir, el alfabeto $alpha$ que ingresó el usuario por medio de su cardinalidad. 

```python
Para i desde 0 hasta alpha-1 hacer
    values_coefficients[i] = i
Fin Para
```

Ahora, luego de tener los coeficientes y sus posibles valores, ¿cómo creo los polinomios con la variable 'x'?

Creamos el símbolo x, con la ayuda de **Sympy**.

```python
x = sympy.symbols('x')
```

Luego llamamos una función que nos devuelve todos los polinomios posibles con todos los elementos del espacio dado. Los parámetros de esta función serán: la lista de los coeficientes hasta un grado $k-1$ y los posibles  valores que puede tomar los respectivos coeficientes.

```python
Función polinomio(coefficients, values_coefficients)
    lista = []
    coef_combinations = generar_combinaciones(values_coefficients, longitud(coefficients))
    Para coef en coef_combinations hacer
        p = Poly(suma([coef[i] * x^i para i desde 0 hasta longitud(coefficients)-1]), x)
        lista.agregar(p.como_expresiónmat())
    Fin Para
    Devolver lista
Fin Función

polynomies = polinomio(coefficients, values_coefficients)
```

Listo, ya tenemos los polinomios!

```python
Escribir("Los polinomios generados son:")
Escribir(polynomies)
```

### Y si el usuario quiere visualizar los codewords?

Para calcular los codewords del código lineal generado a partir de los polinomios se tiene que evaluar cada elemento del alfabeto del espacio trabajado en cada uno de los polinomios en la variable $x$ e ir concatenando. 

```python
Para poly en polynomies hacer
    imprimir(poly)
    codeword = get_codeword(poly, values_coefficients, alpha)
    C.agregar(codeword)
Fin Para

imprimir("Codewords: ", C, "\n Total codewords: ", longitud de C)
```

La función **get_codeword** lo que hace es devolver el codeword del polinomio que se pasó como parámetro. También se le pasa la lista de los elementos del espacio para que los evalúe y la cardinalidad del espacio para estar seguros de que los resultados de las operaciones realizadas sean válidas en el espacio trabajado.

```python
Función get_codeword(poly, values_coefficients, alpha)
    codeword = ""
    Para val en values_coefficients hacer
        codeword += str(poly.subs(x, val) módulo alpha)
    Fin Para
    retornar codeword
Fin Función
```

## ¿Cómo se calcula la matriz generadora?

La matriz generadora para un código de Reed-Solomon está dada por la matriz de Valdermonde, es decir que el número de columnas de esta será igual a la longitud $n$ de los codewords ingresada por el usuario y el número de filas está dado por $k-1$.

> Tener en cuenta que en Python los ciclos llegan hasta uno menos del total.

Se llama a la función de la matriz generadora cuyos parámetros serán una lista de los elementos del espacio, el valor de $k$ y la cardinalidad del alfabeto $alpha$. Esta función lo que hace es que para cada elemento del alfabeto lo eleva hasta $k-1$, el valor de $k$ comienza en 0 así que la primera fila estará dada por unos, y seguirá elevando dependiendo el valor que tome $k$ a medida que se incrementa en el ciclo para.

```python
Función generator_matrix(values_coefficients, k, alpha)
    matriz = crear_matriz(k, longitud(values_coefficients))
    Para i desde 0 hasta k-1 hacer
        Para j desde 0 hasta longitud(values_coefficients)-1 hacer
            matriz[i][j] = ((values_coefficients[j]^i) mod alpha)
        Fin Para
    Fin Para
    Devolver matriz
Fin Función
```

```python
gen_matrix = generator_matrix(values_coefficients, k, alpha).tolist()
```

Ahora simplemente imprimimos la matriz generadora, guala!

```python
Escribir("Generator matrix:")
Para fila en gen_matrix hacer
    Escribir([entero(i) para i en fila])
Fin Para
```

## Decodificación de la palabra recibida $v = 10210$

Para realizar este punto hay una serie de pasos importantes que seguir:

1. **Hallar la matriz de control:** Teniendo la matriz generadora, a partir de esta se procederá a calcular la matriz de control o de paridad ya que la necesitaremos en un futuro. Pero, ¿cómo calculamos la matriz de control?
   
   Primero se tiene que buscar la forma escalonada reducida de la matriz generadora... Este código es tedioso para explicar cada línea de código paso a paso, pero basicamente la calcula y hay comentarios :).
   
   ```python
   # Calcular la forma escalonada reducida por filas de la matriz en Z_alpha
   Para i en rango(len(gen_matrix)) hacer
       # Encontrar el índice de la primera entrada no nula en la fila i
       pivot = -1
       Para j en rango(len(gen_matrix[i])) hacer
           Si gen_matrix[i][j] != 0 entonces
               pivot = j
               romper ciclo
           Fin Si
       Fin Para
       Si pivot == -1 entonces
           continuar
       Fin Si
       # Hacer la entrada pivot de la fila i igual a 1
       factor = pow(entero(gen_matrix[i][pivot]), -1, alpha)
       Para j en rango(len(gen_matrix[i])) hacer
           gen_matrix[i][j] = gen_matrix[i][j] * factor % alpha
       Fin Para
       # Hacer las otras entradas en la columna pivot iguales a cero
       Para j en rango(len(gen_matrix)) hacer
           Si j != i y gen_matrix[j][pivot] != 0 entonces
               factor = gen_matrix[j][pivot]
               Para k en rango(len(gen_matrix[j])) hacer
                   gen_matrix[j][k] = (gen_matrix[j][k] - factor * gen_matrix[i][k]) % alpha
               Fin Para
           Fin Si
       Fin Para
   Fin Para
   
   # Imprimir la matriz escalonada reducida por filas en Z_alpha
   Escribir("Generator matrix in standard form:")
   Para fila en gen_matrix hacer
       Escribir([entero(i) para i en fila])
   Fin Para
   ```
   
   Ahora, creamos un vector que nos ayudará a hallar la matriz de control.
   
   ```python
   vector = [1]*len(gen_matrix[0])
   ```
   
   Teniendo esto, es hora de hallar las ecuaciones para sacar los coeficientes y así armar la matriz de control. 
   
   ```python
   # Calculamos las ecuaciones para sacar sus coeficientes
   Para i en rango(0, longitud de gen_matrix):
       ecuacion = calcular_ecuaciones(gen_matrix[i], i)
       ecuacion = Poly(ecuacion)
       coeficientes = ecuacion.coeffs()
       vector[i] = coeficientes
   ```
   
   La función que calcula las ecuaciones está dada por:
   
   ```python
   Función calcular_ecuaciones(coeficientes, posicion_despeje)
       # cantidad de variables
       vars = ["" para i en rango(len(coeficientes))]
   
       # Creamos una lista con las variables
       para i en rango(len(vars))
           vars[i] = symbols(f'x{i+1}')
   
       # Creamos la ecuación a partir del vector de coeficientes
       ecuacion = 0
       para i en rango(len(coeficientes))
           si coeficientes[i] != 0 entonces
               ecuacion += (int(coeficientes[i]) módulo alpha)*vars[i]
   
       # Despejamos la variable seleccionada
       variable_despeje = vars[posicion_despeje]
       solucion = solve(ecuacion, variable_despeje)
   
       # convertimos las ecuaciones al espacio Z_alpha
       para var en vars
           coef = solucion[0].coeff(var)
           solucion[0] = solucion[0] - coef*var + (coef módulo alpha)*var
       retornar solucion[0]
   
   Fin Función
   ```
   
   Esta recibe como parámetro los coeficientes por fila de la matriz escalonada reducida que  se halló anteriormente y la posición que se va a despejar, esta va de $x_0$ hasta $x_{n-1}$.
   
   Luego se arma la matriz de control con los coeficientes de las ecuaciones que se hallaron  anteriormente y la imprimimos si queremos ver cómo queda!
   
   ```python
   Para i en rango de 0 hasta longitud del vector hacer
           Si el tipo de vector[i] es igual al tipo de vector entonces
               Para j en rango de 0 hasta longitud del vector[i] hacer
                   H[j][i] = entero(vector[i][j])
               Fin Para
           Sino
               H[counter][i] = 1
               counter += 1
           Fin Si
       Fin Para
       Imprimir "Matriz de control:"
       Para fila en H hacer
           Imprimir fila
   ```
   
   Ya que se tiene la matriz de control, ahora proderemos a hacer la decodificación del codeword ingresado por el usuario por medio de la **decodificación por síndrome**.

2. **Implementar la decodificación por síndrome:** Para realizar este decodificación necesitamos crear las clases laterales que se calculan $q^{n-d}$ , ese será el número de clases laterales distintas, las cuales se crean a partir de codewords del espacio pero que no se encuentran en la lista del código lineal que se halló desde el principio. Así que, necesitamos todos los códigos del espacio... 
   
   ```python
   Función generar_cadenas(n, alpha)
       Si n es igual a 0 entonces
           Devolver una lista que contenga una cadena vacía
       Sino
           cadenas = []
           Para cada cadena en generar_cadenas(n-1, alpha) hacer
               Para letra en rango(alpha) hacer
                   cadenas.agregar(cadena + convertir_a_cadena(letra))
               Fin Para
           Fin Para
           Devolver cadenas
       Fin Si
   Fin Función
   espacio = generar_cadenas(n, alpha)
   ```
   
   Luego buscamos en el espacio la cantidad de codewords $q^{n-d}$ para las clases laterales. Recordemos que estas no deben estar en el código lineal $C$. A su vez, cuando encontremos estos codewords, a cada uno de ellos se le sumará cada elemento del código $C$ y de esta forma se encontrarán las clases laterales que necesitamos, dando como resultado una lista para cada una.
   
   ```python
   Para lider en espacio hacer
       clase = []
       Si lider no está en el código entonces
           líderes.agregar(lider)
           Para cada codeword en C hacer
               suma = ''
               Para i en rango de 0 hasta longitud de codeword hacer
                   suma += convertir_a_cadena((entero(lider[i]) + entero(codeword[i])) módulo alpha)
               Fin Para
               Si suma no está en el código entonces
                   code.agregar(suma)
                   clase.agregar(suma)
               Fin Si
           Fin Para
           # guardar la clase lateral
           clases_laterales.agregar(clase)
       Fin Si
   Fin Para
   ```
   
   Ahora que ya se tienen las clases laterales, cada una con su líder, se procederá a calcular el síndrome de cada uno, ¿cómo hacemos eso?, pues llamamos una función  en la cúal los parámetros serán la matriz de control y el $c$ que viene siendo el líder de  la clase dada.
   
   ```PYTHON
   Función sindrome(H, c)
       lider = []
       Para i en c hacer
           lider.agregar(entero(i) módulo alpha)
       Fin Para
       lider = transponer(lider)
       # se multiplica H*liderT
       resultado = []
       Para fila en H hacer
           suma = 0
           Para i en rango de 0 hasta longitud de fila hacer
               suma += fila[i] * lider[0][i]
           Fin Para
           resultado.agregar(suma)
       Fin Para
       Devolver resultado
   Fin Función
   ```
   
   Esta función se llama para cada líder de la clase laterales:
   
   ```PYTHON
   sindromes = []
   Para cada lider en lideres hacer
       sindromes.agregar(sindrome(H, lider))
   Fin Para
   ```
   
   Ahora usamos esta función para convertir los sindromes en el alfabeto que se está trabajando es decir, $q$.
   
   ```python
   Para i en rango de 0 hasta longitud de sindromes hacer
       Para j en rango de 0 hasta longitud de sindromes[0] hacer
           sindromes[i][j][0] = sindromes[i][j][0] módulo alpha
       Fin Para
   Fin Para
   ```

3. **Corregir el codeword ingresado:** Primero le pedimos al usuario que ingrese el codeword para decodificarlo y ver si tiene algún error o está bien.
   
   ```python
   recivo = leer("Ingrese la palabra recibida: ")
   ```
   
   Luego de recibir el codeword, buscamos el síndrome del codeword ingresado llamando claramente a la función **sindrome** y lo convertimos al alfabeto respectivo.
   
   ```python
   sind = sindrome(H, recivo)
   Para num en sind hacer
      num[0] = num[0] módulo alpha
   Fin Para
   ```
   
   Después de esto, buscamos entre los líderes de las clases laterales para ver en cual de ellos se encuentra el síndrome que coincida con el síndrome del codeword ingresado. A su vez, cuando encontremos ese líder, lo que hacemos es restar el líder con el codeword recibido para que nos dé como resultado el codeword totalmente corregido y lo mostramos al usuario!
   
   ```python
   lid = lideres[sindromes.index(sind)]
   resta = ''
   Para i en rango de 0 hasta longitud de recivo hacer
      resta += str((int(recivo[i]) - int(lid[i])) módulo alpha)
   Fin Para
   imprimir("The correct codeword is: " + resta)
   ```
