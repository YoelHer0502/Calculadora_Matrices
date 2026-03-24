"""
╔══════════════════════════════════════════════════════╗
║         INVERSA DE UNA MATRIZ — 4 MÉTODOS            ║
║  Sistemas de Ecuaciones · Gauss-Jordan ·             ║
║  Diagonalización · Cofactores                        ║
╚══════════════════════════════════════════════════════╝

"""

# ══════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════

def linea(char="═", n=60):
    print(char * n)

def titulo_seccion(texto):
    print("\n")
    linea()
    print(f"  {texto}")
    linea()

def imprimir_matriz(M, nombre, fmt=".4f"):
    print(f"\n    {nombre} =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:{fmt}}" if isinstance(v,float) else f"{v:8}" for v in fila) + "  │")
    print()

def copiar(M):
    return [fila[:] for fila in M]

def det3(M):
    a = M
    return (a[0][0]*a[1][1]*a[2][2]
          + a[0][1]*a[1][2]*a[2][0]
          + a[0][2]*a[1][0]*a[2][1]
          - a[0][2]*a[1][1]*a[2][0]
          - a[0][1]*a[1][0]*a[2][2]
          - a[0][0]*a[1][2]*a[2][1])

def submatriz(M, fi, ci):
    return [[M[i][j] for j in range(len(M[0])) if j!=ci]
             for i in range(len(M)) if i!=fi]

def cofactor(M, i, j):
    m = submatriz(M, i, j)
    d = m[0][0]*m[1][1] - m[0][1]*m[1][0]
    return ((-1)**(i+j)) * d

def redondear(M, dec=6):
    return [[round(v, dec) for v in fila] for fila in M]

# ══════════════════════════════════════════════════════════════════════════════
#  MÉTODO 1 — SISTEMA DE ECUACIONES  (A · A⁻¹ = I, columna a columna)
# ══════════════════════════════════════════════════════════════════════════════

def gauss_solve(A, b):
    """Resuelve Ax=b por eliminación gaussiana. Devuelve x."""
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        max_f = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[max_f] = M[max_f], M[col]
        piv = M[col][col]
        for f in range(col+1, n):
            fac = M[f][col] / piv
            for k in range(col, n+1):
                M[f][k] -= fac * M[col][k]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j]*x[j]
        x[i] /= M[i][i]
    return x

def inversa_sistemas(A):
    n = len(A)
    inv = []
    for j in range(n):
        b = [1.0 if i==j else 0.0 for i in range(n)]
        inv.append(gauss_solve(A, b))
    # transponer para obtener columnas como filas
    return [[inv[j][i] for j in range(n)] for i in range(n)]

def mostrar_metodo_sistemas(A):
    titulo_seccion("MÉTODO 1 — SISTEMA DE ECUACIONES  (A · x = eⱼ)")
    n = len(A)
    print("  La inversa se obtiene resolviendo n sistemas  A·xⱼ = eⱼ")
    print("  donde eⱼ es la j-ésima columna de la identidad.\n")
    imprimir_matriz(A, "A")
    det = det3(A)
    print(f"    det(A) = {det:.4f}\n")
    ejes = ["e₁=[1,0,0]", "e₂=[0,1,0]", "e₃=[0,0,1]"]
    cols = []
    for j in range(n):
        b = [1.0 if i==j else 0.0 for i in range(n)]
        x = gauss_solve(A, b)
        cols.append(x)
        print(f"    Sistema A·x = {ejes[j]}  →  x = [{', '.join(f'{v:.4f}' for v in x)}]")
    inv = [[cols[j][i] for j in range(n)] for i in range(n)]
    imprimir_matriz(redondear(inv), "A⁻¹  (columnas = soluciones de cada sistema)")

# ══════════════════════════════════════════════════════════════════════════════
#  MÉTODO 2 — GAUSS-JORDAN  [A | I] → [I | A⁻¹]
# ══════════════════════════════════════════════════════════════════════════════

def inversa_gauss_jordan(A):
    n = len(A)
    Aug = [A[i][:] + [1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    pasos = []
    for col in range(n):
        max_f = max(range(col, n), key=lambda r: abs(Aug[r][col]))
        if max_f != col:
            Aug[col], Aug[max_f] = Aug[max_f], Aug[col]
            pasos.append(f"Intercambio F{col+1} ↔ F{max_f+1}")
        piv = Aug[col][col]
        Aug[col] = [x/piv for x in Aug[col]]
        pasos.append(f"F{col+1} ÷ {piv:.4g}  (normalizar pivote)")
        for f in range(n):
            if f != col:
                fac = Aug[f][col]
                Aug[f] = [Aug[f][k] - fac*Aug[col][k] for k in range(2*n)]
                pasos.append(f"F{f+1} → F{f+1} - ({fac:.4g})·F{col+1}")
    return [Aug[i][n:] for i in range(n)], pasos

def mostrar_metodo_gauss_jordan(A):
    titulo_seccion("MÉTODO 2 — GAUSS-JORDAN  [ A | I ] → [ I | A⁻¹ ]")
    n = len(A)
    print("  Se forma la matriz aumentada [A|I] y se reduce A a la identidad.")
    print("  Las operaciones aplicadas transforman I en A⁻¹.\n")
    imprimir_matriz(A, "A")
    Aug_ini = [A[i][:] + [1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    imprimir_matriz(Aug_ini, "[A | I]  inicial")
    inv, pasos = inversa_gauss_jordan(A)
    print("    Pasos de reducción:")
    for p in pasos:
        print(f"      ▶ {p}")
    Aug_fin = [[1.0 if i==j else 0.0 for j in range(n)] + inv[i] for i in range(n)]
    imprimir_matriz(redondear(Aug_fin), "[I | A⁻¹]  resultado")
    imprimir_matriz(redondear(inv), "A⁻¹")

# ══════════════════════════════════════════════════════════════════════════════
#  MÉTODO 3 — DIAGONALIZACIÓN  (D⁻¹ para matrix diagonal)
#  Demostración con matriz diagonal → su inversa es trivial
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_metodo_diagonalizacion(A):
    titulo_seccion("MÉTODO 3 — DIAGONALIZACIÓN  (D⁻¹)")
    n = len(A)
    print("  Para una matriz DIAGONAL D, la inversa es simplemente")
    print("  D⁻¹[i][i] = 1 / D[i][i]  (invertir cada elemento diagonal).\n")
    print("  Para una matriz general A se factoriza como  A = P·D·P⁻¹")
    print("  y luego  A⁻¹ = P·D⁻¹·P⁻¹.  Aquí mostramos el caso diagonal.\n")
    imprimir_matriz(A, "D (diagonal)")
    diag = [A[i][i] for i in range(n)]
    print("    Elementos de la diagonal:")
    for i, d in enumerate(diag):
        print(f"      d[{i+1}] = {d}   →   1/d[{i+1}] = {1/d:.6f}")
    inv = [[0.0]*n for _ in range(n)]
    for i in range(n):
        inv[i][i] = 1.0 / A[i][i]
    imprimir_matriz(redondear(inv), "D⁻¹")
    print("    Verificación  D · D⁻¹ = I:")
    prod = [[sum(A[i][k]*inv[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    imprimir_matriz(redondear(prod), "D · D⁻¹")

# ══════════════════════════════════════════════════════════════════════════════
#  MÉTODO 4 — COFACTORES  A⁻¹ = (1/det) · adj(A)
# ══════════════════════════════════════════════════════════════════════════════

def inversa_cofactores(A):
    n = len(A)
    det = det3(A)
    # Matriz de cofactores
    C = [[cofactor(A, i, j) for j in range(n)] for i in range(n)]
    # Adjunta = transpuesta de cofactores
    adj = [[C[j][i] for j in range(n)] for i in range(n)]
    inv = [[adj[i][j]/det for j in range(n)] for i in range(n)]
    return inv, C, adj, det

def mostrar_metodo_cofactores(A):
    titulo_seccion("MÉTODO 4 — COFACTORES  A⁻¹ = (1/det) · adj(A)")
    print("  Paso 1: calcular det(A)")
    print("  Paso 2: calcular la matriz de cofactores C")
    print("  Paso 3: adj(A) = Cᵀ  (transpuesta de cofactores)")
    print("  Paso 4: A⁻¹ = (1/det) · adj(A)\n")
    imprimir_matriz(A, "A")
    inv, C, adj, det = inversa_cofactores(A)
    print(f"    det(A) = {det:.6f}\n")
    print("    Cofactores  C[i][j] = (-1)^(i+j) · det(M_ij):")
    for i in range(3):
        for j in range(3):
            m = submatriz(A, i, j)
            d = m[0][0]*m[1][1] - m[0][1]*m[1][0]
            print(f"      C[{i+1}][{j+1}] = (-1)^{i+j} · {d:.4g} = {C[i][j]:.4g}")
    imprimir_matriz(redondear(C), "Matriz de cofactores C")
    imprimir_matriz(redondear(adj), "adj(A) = Cᵀ")
    imprimir_matriz(redondear(inv), "A⁻¹ = (1/det) · adj(A)")
    print("    Verificación  A · A⁻¹ = I:")
    n = 3
    prod = [[sum(A[i][k]*inv[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    imprimir_matriz(redondear(prod), "A · A⁻¹")

# ══════════════════════════════════════════════════════════════════════════════
#  DATOS 
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────
#  MÉTODO 1 — Sistema de ecuaciones
# ─────────────────────────────────────────────────────
A_sistemas = [
    [2,  -1, 3],
    [1, 4,  0],
    [-2,  1,  5],
]

# ─────────────────────────────────────────────────────
#  MÉTODO 2 — Gauss-Jordan
# ─────────────────────────────────────────────────────
A_gauss = [
    [3, 1,  2],
    [2, 1,  0],
    [3, 1,  4],
]

# ─────────────────────────────────────────────────────
#  MÉTODO 3 — Diagonalización
# ─────────────────────────────────────────────────────
A_diagonal = [
    [4, 0, 0],
    [0, 2, 0],
    [0, 0, 5],
]

# ─────────────────────────────────────────────────────
#  MÉTODO 4 — Cofactores
# ─────────────────────────────────────────────────────
A_cofactores = [
    [3,  0,  2],
    [2,  0, -2],
    [0,  1,  1],
]

# ══════════════════════════════════════════════════════
#  EJECUCIÓN
# ══════════════════════════════════════════════════════

mostrar_metodo_sistemas(A_sistemas)
mostrar_metodo_gauss_jordan(A_gauss)
mostrar_metodo_diagonalizacion(A_diagonal)
mostrar_metodo_cofactores(A_cofactores)

linea()
print("  ✔  Todos los métodos completados.")
linea()
print()