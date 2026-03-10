from itertools import combinations

# Tu lista original
numeros = [1, 2, 3, 4, 5]

# Generamos combinaciones de 4 elementos
# El segundo argumento es el tamaño del grupo que deseas (n-1)
resultados = list(combinations(numeros, 4))

# Imprimimos cada objeto
for combo in resultados:
    print(list(combo))


    numeros = [1, 2, 3, 4, 5]

for i in range(len(numeros)):
    # Creamos una sublista uniendo lo que está antes y después del índice actual
    resultado = numeros[:i] + numeros[i+1:]
    print(resultado)