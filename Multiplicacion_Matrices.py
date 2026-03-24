
"""
╔══════════════════════════════════════════════════════╗
║       MULTIPLICACIÓN DE MATRICES — 3 EJEMPLOS        ║
╚══════════════════════════════════════════════════════╝

"""

# ══════════════════════════════════════════════════════
#  UTILIDADES DE DISPLAY
# ══════════════════════════════════════════════════════

def linea(char="═", n=56):
    print(char * n)

def titulo_ejemplo(n, texto=""):
    print(f"\n  ┌─ Ejemplo {n}" + (f": {texto}" if texto else "") + " ─")

def imprimir_matriz(M, nombre):
    print(f"\n    {nombre}  ({len(M)}×{len(M[0])}) =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:7.3g}" for v in fila) + "  │")
    print()

def imprimir_resultado(M, nombre):
    print(f"    {nombre} =")
    for fila in M:
        print("      ║ " + "  ".join(f"{v:7.3g}" for v in fila) + "  ║")
    print()

def mostrar_pasos(A, B, R):
    """Muestra la tabla de multiplicación fila × columna."""
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    print("    Cálculo elemento por elemento  (fila de A · columna de B):\n")
    for i in range(filas_A):
        for j in range(cols_B):
            terminos = " + ".join(
                f"({A[i][k]}×{B[k][j]})" for k in range(cols_A)
            )
            print(f"      R[{i+1}][{j+1}] = {terminos} = {R[i][j]:.3g}")
    print()

# ══════════════════════════════════════════════════════
#  OPERACIÓN
# ══════════════════════════════════════════════════════

def multiplicar(A, B):
    filas_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    R = [[0]*cols_B for _ in range(filas_A)]
    for i in range(filas_A):
        for j in range(cols_B):
            for k in range(cols_A):
                R[i][j] += A[i][k] * B[k][j]
    return R

def mostrar_multiplicacion(num_ej, A, B, titulo=""):
    titulo_ejemplo(num_ej, titulo)
    filas_A, cols_A = len(A), len(A[0])
    filas_B, cols_B = len(B), len(B[0])
    print(f"\n    Dimensiones: A({filas_A}×{cols_A}) · B({filas_B}×{cols_B})"
          f"  →  Resultado({filas_A}×{cols_B})\n")
    imprimir_matriz(A, "A")
    imprimir_matriz(B, "B")
    R = multiplicar(A, B)
    mostrar_pasos(A, B, R)
    imprimir_resultado(R, "A · B")

# ══════════════════════════════════════════════════════════════════════════════

linea()
print("  MULTIPLICACIÓN DE MATRICES")
linea()

# ─────────────────────────────────────────────────────
# Ejemplo 1
#  A es 3×3  y  B es 3×3  →  resultado 3×3
# ─────────────────────────────────────────────────────
A1 = [
    [1,  2, 3],
    [3, 2, 1],
    [1, 2, 1],
]
B1 = [
    [0, 1, 2],
    [2, 1,  3],
    [1, 0,  3],
]
mostrar_multiplicacion(1, A1, B1, "Matriz 3×3 · Matriz 3×3")
# ─────────────────────────────────────────────────────
#  Ejemplo 2
#  A es 2×3  y  B es 3×2  →  resultado 2×2
# ─────────────────────────────────────────────────────
A2 = [
    [2, 0, 1],
    [3, 5, 6],
]
B2 = [
    [1,  2],
    [0,  3],
    [4, 5],
]
mostrar_multiplicacion(2, A2, B2, "Matriz 2×3 · Matriz 3×2")


# ─────────────────────────────────────────────────────
#  Ejemplo 3
#  A es 3×2  y  B es 2×3  →  resultado 3×3
# ─────────────────────────────────────────────────────
A3 = [
    [1, -1],
    [2, 3],
    [4, 0],
]
B3 = [
    [2, 1, 3],
    [0, -2,  4],
]
mostrar_multiplicacion(3, A3, B3, "Matriz 3×2 · Matriz 2×3")

linea()
print("  ✔  Todos los ejemplos completados.")
linea()
print()
