"""
╔══════════════════════════════════════════════════════╗
║         OPERACIONES CON MATRICES — EJEMPLOS          ║
║     Escalar · Suma · Resta  (3 ejemplos cada una)    ║
╚══════════════════════════════════════════════════════╝

"""

# ══════════════════════════════════════════════════════
#  UTILIDADES DE DISPLAY
# ══════════════════════════════════════════════════════

def linea(char="═", n=56):
    print(char * n)

def titulo_seccion(texto):
    print("\n")
    linea()
    print(f"  {texto}")
    linea()

def titulo_ejemplo(n, texto=""):
    print(f"\n  ┌─ Ejemplo {n}" + (f": {texto}" if texto else "") + " ─")

def imprimir_matriz(M, nombre):
    filas = len(M)
    cols  = len(M[0])
    print(f"\n    {nombre} =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:6}" for v in fila) + "  │")
    print()

def imprimir_resultado(M, nombre="Resultado"):
    filas = len(M)
    cols  = len(M[0])
    print(f"    {nombre} =")
    for fila in M:
        print("      ║ " + "  ".join(f"{v:6}" for v in fila) + "  ║")
    print()

# ══════════════════════════════════════════════════════
#  OPERACIONES MATRICIALES
# ══════════════════════════════════════════════════════

def escalar_x_matriz(k, M):
    return [[k * M[i][j] for j in range(len(M[0]))] for i in range(len(M))]

def suma_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def resta_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def mostrar_escalar(num_ej, k, M):
    titulo_ejemplo(num_ej)
    print(f"\n    Operación:  k · A   donde  k = {k}\n")
    imprimir_matriz(M, "A")
    R = escalar_x_matriz(k, M)
    print(f"    {k} ×")
    imprimir_resultado(R, f"{k} · A")

def mostrar_suma(num_ej, A, B):
    titulo_ejemplo(num_ej)
    print("\n    Operación:  A + B\n")
    imprimir_matriz(A, "A")
    imprimir_matriz(B, "B")
    R = suma_matrices(A, B)
    imprimir_resultado(R, "A + B")

def mostrar_resta(num_ej, A, B):
    titulo_ejemplo(num_ej)
    print("\n    Operación:  A - B\n")
    imprimir_matriz(A, "A")
    imprimir_matriz(B, "B")
    R = resta_matrices(A, B)
    imprimir_resultado(R, "A - B")


# ══════════════════════════════════════════════════════════════════════════════
#
#  SECCIÓN 1: ESCALAR POR UNA MATRIZ
#
# ══════════════════════════════════════════════════════════════════════════════

titulo_seccion("SECCIÓN 1 — ESCALAR × MATRIZ  (k · A)")

# ─────────────────────────────────────────────────────
#  Ejemplo 1 de Escalar
# ─────────────────────────────────────────────────────
k1 = 3                       

A1 = [                        
    [2, -3, 4],
    [0, 5, 1],
    [6, 7, -2],
]
mostrar_escalar(1, k1, A1)

# ─────────────────────────────────────────────────────
#  Ejemplo 2 de Escalar
# ─────────────────────────────────────────────────────
k2 = -2                       # ← escalar

A2 = [                        
    [-4, 1, 0],
    [3, -2, 5],
    [7, 6, -3],
]
mostrar_escalar(2, k2, A2)

# ─────────────────────────────────────────────────────
#  Ejemplo 3 de Escalar
# ─────────────────────────────────────────────────────
k3 = 1/2                      

A3 = [                        
    [5, -7, 2],
    [-1, 4, 8],
    [0, -3, 6],
]
mostrar_escalar(3, k3, A3)


# ══════════════════════════════════════════════════════════════════════════════
#
#  SECCIÓN 2: SUMA DE MATRICES
#
# ══════════════════════════════════════════════════════════════════════════════

titulo_seccion("SECCIÓN 2 — SUMA DE MATRICES  (A + B)")

# ─────────────────────────────────────────────────────
# Ejemplo 1 de Suma
# ─────────────────────────────────────────────────────
A4 = [                        
    [2, -5, 3],
    [0, 8, 10],
    [1, -1, 2],
]

B4 = [                        
    [4, -9, 8],
    [2, -4, 10],
    [1, 3, 11],
]
mostrar_suma(1, A4, B4)

# ─────────────────────────────────────────────────────
# Ejemplo 2 de Suma
# ─────────────────────────────────────────────────────
A5 = [
    [-3, 2,  1],
    [6, -5, 4],
    [0,  7, -2],
]

B5 = [
    [4, -1, 3],
    [-2, 8, 0],
    [3, -6, 9],
]
mostrar_suma(2, A5, B5)

# ─────────────────────────────────────────────────────
# Ejemplo 3 de Suma
# ─────────────────────────────────────────────────────
A6 = [                        
    [7, -3, 2],
    [-1, 4, 6],
    [8, 0, -5],
]

B6 = [                        
    [-2, 5, 1],
    [3, -4, 0],
    [6, -7, 2],
]
mostrar_suma(3, A6, B6)


# ══════════════════════════════════════════════════════════════════════════════
#
#   SECCIÓN 3: RESTA DE MATRICES
#
# ══════════════════════════════════════════════════════════════════════════════

titulo_seccion("SECCIÓN 3 — RESTA DE MATRICES  (A - B)")

# ─────────────────────────────────────────────────────
# Ejemplo 1 de Resta
# ─────────────────────────────────────────────────────
A7 = [
    [5, -2, 4],
    [3, 7, -1],
    [0, 6, 2],
]

B7 = [
    [1, 3, -5],
    [-4, 2, 6],
    [7, -1, 0],
]
mostrar_resta(1, A7, B7)

# ─────────────────────────────────────────────────────
# Ejemplo 2 de Resta
# ─────────────────────────────────────────────────────
A8 = [
    [ -6, 4,  2],
    [ 1,  -3, 5],
    [8,  7,  -2],
]

B8 = [
    [2,  -1,  0],
    [ -5, 6,  3],
    [ 4,  -2, 9],
]
mostrar_resta(2, A8, B8)

# ─────────────────────────────────────────────────────
# Ejemplo 3 de Resta
# ─────────────────────────────────────────────────────
A9 = [                        
    [3, 8, -4],
    [-2, 5, 7],
    [1, -6, 0],
]

B9 = [                        
    [-1, 2, 3],
    [4, -5, 6],
    [-7, 8, -9],
]
mostrar_resta(3, A9, B9)


# ══════════════════════════════════════════════════════
print("\n" + "═" * 56)
print("Todos los ejemplos completados.")
print("═" * 56 + "\n")