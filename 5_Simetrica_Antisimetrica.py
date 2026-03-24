"""
╔══════════════════════════════════════════════════════╗
║     MATRICES SIMÉTRICAS Y ANTISIMÉTRICAS             ║
║         3 ejemplos de cada tipo                      ║
╚══════════════════════════════════════════════════════╝

  SIMÉTRICA:      A = Aᵀ          →  a[i][j] = a[j][i]
  ANTISIMÉTRICA:  A = -Aᵀ         →  a[i][j] = -a[j][i]
                  (la diagonal principal siempre es 0)

  Cualquier matriz A se puede descomponer como:
       A = S + K
       S = (A + Aᵀ)/2   →  parte simétrica
       K = (A - Aᵀ)/2   →  parte antisimétrica
"""

# ══════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════

def linea(char="═", n=60):
    print(char * n)

def titulo_seccion(texto):
    print("\n"); linea("─", 60)
    print(f"  ▶  {texto}"); linea("─", 60)

def titulo_ejemplo(n, texto=""):
    print(f"\n  ┌─ Ejemplo {n}" + (f": {texto}" if texto else "") + " ─")

def imprimir_matriz(M, nombre):
    n = len(M)
    print(f"\n    {nombre}  ({n}×{n}) =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:6}" if isinstance(v, int) else f"{v:7.3f}" for v in fila) + "  │")
    print()

def transpuesta(M):
    n = len(M)
    return [[M[j][i] for j in range(n)] for i in range(n)]

def suma_mat(A, B):
    n = len(A)
    return [[A[i][j]+B[i][j] for j in range(n)] for i in range(n)]

def escalar_mat(k, M):
    n = len(M)
    return [[k*M[i][j] for j in range(n)] for i in range(n)]

def redondear_mat(M, dec=4):
    return [[round(v, dec) for v in fila] for fila in M]

# ══════════════════════════════════════════════════════
#  VERIFICACIONES
# ══════════════════════════════════════════════════════

def verificar_simetrica(A):
    n = len(A)
    ok = all(abs(A[i][j] - A[j][i]) < 1e-9 for i in range(n) for j in range(n))
    return ok

def verificar_antisimetrica(A):
    n = len(A)
    diag_ok  = all(abs(A[i][i]) < 1e-9 for i in range(n))
    anti_ok  = all(abs(A[i][j] + A[j][i]) < 1e-9 for i in range(n) for j in range(n))
    return diag_ok and anti_ok

# ══════════════════════════════════════════════════════
#  MOSTRAR EJEMPLOS
# ══════════════════════════════════════════════════════

def mostrar_simetrica(num_ej, A, desc=""):
    titulo_ejemplo(num_ej, desc)
    n = len(A)
    At = transpuesta(A)
    imprimir_matriz(A,  "A")
    imprimir_matriz(At, "Aᵀ")
    ok = verificar_simetrica(A)
    print("    Condición  A = Aᵀ:")
    for i in range(n):
        for j in range(n):
            estado = "✔" if abs(A[i][j]-A[j][i]) < 1e-9 else "✗"
            print(f"      a[{i+1}][{j+1}] = {A[i][j]}  ==  a[{j+1}][{i+1}] = {A[j][i]}  {estado}")
    print(f"\n    Resultado: {'✔ MATRIZ SIMÉTRICA' if ok else '✗ NO es simétrica'}\n")

def mostrar_antisimetrica(num_ej, A, desc=""):
    titulo_ejemplo(num_ej, desc)
    n = len(A)
    At = transpuesta(A)
    mAt = escalar_mat(-1, At)
    imprimir_matriz(A,   "A")
    imprimir_matriz(At,  "Aᵀ")
    imprimir_matriz(mAt, "-Aᵀ")
    ok = verificar_antisimetrica(A)
    print("    Condición  A = -Aᵀ  (y diagonal = 0):")
    print(f"      Diagonal principal: {[A[i][i] for i in range(n)]}")
    for i in range(n):
        for j in range(i+1, n):
            estado = "✔" if abs(A[i][j]+A[j][i]) < 1e-9 else "✗"
            print(f"      a[{i+1}][{j+1}] = {A[i][j]}  vs  a[{j+1}][{i+1}] = {A[j][i]}  →  suma = {A[i][j]+A[j][i]}  {estado}")
    print(f"\n    Resultado: {'✔ MATRIZ ANTISIMÉTRICA' if ok else '✗ NO es antisimétrica'}\n")

def mostrar_descomposicion(A):
    """Muestra que cualquier A = S + K."""
    n = len(A)
    At = transpuesta(A)
    S = redondear_mat(escalar_mat(0.5, suma_mat(A, At)))
    K = redondear_mat(escalar_mat(0.5, suma_mat(A, escalar_mat(-1, At))))
    print("    ┌─ Descomposición A = S + K ──────────────────────┐")
    imprimir_matriz(A, "A  (original)")
    imprimir_matriz(S, "S = (A + Aᵀ)/2  →  parte SIMÉTRICA")
    imprimir_matriz(K, "K = (A - Aᵀ)/2  →  parte ANTISIMÉTRICA")
    S_ok = verificar_simetrica(S)
    K_ok = verificar_antisimetrica(K)
    print(f"    S es simétrica:      {'✔' if S_ok else '✗'}")
    print(f"    K es antisimétrica:  {'✔' if K_ok else '✗'}")
    print("    └────────────────────────────────────────────────┘\n")


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 1: MATRICES SIMÉTRICAS
# ══════════════════════════════════════════════════════════════════════════════

linea()
print("  MATRICES SIMÉTRICAS Y ANTISIMÉTRICAS")
linea()

titulo_seccion("SECCIÓN 1 — MATRICES SIMÉTRICAS  (A = Aᵀ)")

# ─────────────────────────────────────────────────────
# Simétrica 1
# ─────────────────────────────────────────────────────
S1 = [
    [4,  2,  -1],
    [2,  5,  3],
    [-1,  3,  6],
]
mostrar_simetrica(1, S1)

# ─────────────────────────────────────────────────────
# Simétrica 2
# ─────────────────────────────────────────────────────
S2 = [
    [9,  1,  4],
    [1,  -2,  7],
    [4,  7,  3],
]
mostrar_simetrica(2, S2)


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 2: MATRICES ANTISIMÉTRICAS
# ══════════════════════════════════════════════════════════════════════════════

titulo_seccion("SECCIÓN 2 — MATRICES ANTISIMÉTRICAS  (A = -Aᵀ)")

# ─────────────────────────────────────────────────────
# Antisimétrica 1
# ─────────────────────────────────────────────────────
K1 = [
    [ 0,  7, -4],
    [-7,  0,  2],
    [ 4, -2,  0],
]
mostrar_antisimetrica(1, K1)

# ─────────────────────────────────────────────────────
#  Antisimétrica 2
# ─────────────────────────────────────────────────────
K2 =  [
    [ 0,  3, -8],
    [3,  0,  -6],
    [-8, 6,  0],
]
mostrar_antisimetrica(2, K2)

linea()
print("  ✔  Todos los ejemplos completados.")
linea()
print()