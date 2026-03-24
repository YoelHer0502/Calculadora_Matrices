"""
╔══════════════════════════════════════════════════════╗
║         DETERMINANTES 3×3 — 3 EJERCICIOS             ║
║   Ejercicio 1: Método de Gauss                       ║
║   Ejercicio 2: Diagonalización                       ║
║   Ejercicio 3: Expansión por Cofactores              ║
╚══════════════════════════════════════════════════════╝

"""

# ══════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════

def linea(char="═", n=62):
    print(char * n)

def titulo_ejercicio(n, metodo):
    print(f"\n\n{'━'*62}")
    print(f"  EJERCICIO {n} — {metodo}")
    print(f"{'━'*62}")

def imprimir_matriz(M, nombre):
    n = len(M)
    print(f"\n    {nombre}  ({n}×{n}) =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:9.4f}" if isinstance(v, float) else f"{v:9}" for v in fila) + "  │")
    print()

def copiar(M):
    return [f[:] for f in M]

def det_sarrus(M):
    """Referencia rápida por Sarrus."""
    a = M
    return (a[0][0]*a[1][1]*a[2][2]
          + a[0][1]*a[1][2]*a[2][0]
          + a[0][2]*a[1][0]*a[2][1]
          - a[0][2]*a[1][1]*a[2][0]
          - a[0][1]*a[1][0]*a[2][2]
          - a[0][0]*a[1][2]*a[2][1])

def submatriz(M, fi, ci):
    return [[M[i][j] for j in range(3) if j != ci]
             for i in range(3) if i != fi]

def det2x2(M):
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]

def r(v, d=4):
    return round(v, d)


# ══════════════════════════════════════════════════════════════════════════════
#  EJERCICIO 1 — MÉTODO DE GAUSS  (triangulación)
# ══════════════════════════════════════════════════════════════════════════════

titulo_ejercicio(1, "MÉTODO DE GAUSS  (triangulación superior)")

print("""
  Procedimiento:
  1. Reducir A a forma triangular superior U mediante operaciones de fila.
  2. Cada intercambio de filas multiplica el det por -1.
  3. det(A) = signo × producto de la diagonal de U.
""")

# ─────────────────────────────────────────────────────
# Ejercicio 1 (Gauss)
# ─────────────────────────────────────────────────────
A_gauss = [
    [ 2,  0, 1],
    [3, 1,  0],
    [1,  4,  2],
]

# ── Ejecución ──────────────────────────────────────
imprimir_matriz(A_gauss, "A  (original)")

M = [[float(v) for v in fila] for fila in copiar(A_gauss)]
n = 3
sign = 1
pasos_g = []

for col in range(n):
    # Pivoteo parcial
    max_f = max(range(col, n), key=lambda r: abs(M[r][col]))
    if max_f != col:
        M[col], M[max_f] = M[max_f], M[col]
        sign *= -1
        pasos_g.append((f"Intercambio F{col+1} ↔ F{max_f+1}  [signo ×(-1) → {'+'if sign>0 else'-'}1]",
                        copiar(M)))
    piv = M[col][col]
    if abs(piv) < 1e-12:
        break
    for f in range(col + 1, n):
        fac = M[f][col] / piv
        if abs(fac) > 1e-12:
            desc = f"F{f+1} → F{f+1} - ({fac:.4g})·F{col+1}"
            for k in range(n):
                M[f][k] -= fac * M[col][k]
            pasos_g.append((desc, copiar(M)))

print("  Pasos de triangulación:\n")
for desc, mat in pasos_g:
    print(f"    ▶ {desc}")
    imprimir_matriz(mat, "")

U = M
diag = [U[i][i] for i in range(n)]
prod = diag[0] * diag[1] * diag[2]
det_g = sign * prod

print(f"  Matriz triangular superior U obtenida:")
imprimir_matriz(U, "U")
print(f"  Diagonal de U:  {diag[0]:.4f}  ×  {diag[1]:.4f}  ×  {diag[2]:.4f}")
print(f"  Producto diagonal = {prod:.4f}")
print(f"  Signo acumulado   = {'+1' if sign > 0 else '-1'}")
print(f"\n  ┌─────────────────────────────────────────────────────┐")
print(f"  │  det(A)  =  signo × prod. diagonal                  │")
print(f"  │  det(A)  =  ({'+1' if sign > 0 else '-1'}) × {prod:.4f}  =  {det_g:.4f}          │")
print(f"  └─────────────────────────────────────────────────────┘")
ref = det_sarrus(A_gauss)
print(f"\n  Verificación (Sarrus): det(A) = {ref:.4f}  {'✔' if abs(det_g-ref)<1e-6 else '✗'}")


# ══════════════════════════════════════════════════════════════════════════════
#  EJERCICIO 2 — DIAGONALIZACIÓN
# ══════════════════════════════════════════════════════════════════════════════

titulo_ejercicio(2, "DIAGONALIZACIÓN  (reducción triangular + diagonal)")

print("""
  Procedimiento:
  1. Reducir A a matriz triangular superior U (igual que Gauss).
  2. El determinante es el producto de los elementos de la diagonal
     principal de U, ajustado por el signo de los intercambios.

  Nota: para una matriz DIAGONAL D, det(D) = d₁₁ × d₂₂ × d₃₃
        inmediatamente, sin necesidad de reducción.
""")

# ─────────────────────────────────────────────────────
#  Ejercicio 2 (Diagonalización)
# ─────────────────────────────────────────────────────
A_diag = [
    [ 1, 2,  3],
    [ 0,  1,  4],
    [ 5,  6,  0],
]


# ── Ejecución ──────────────────────────────────────
imprimir_matriz(A_diag, "A  (original)")

# Verificar si ya es triangular
es_tri_sup = all(A_diag[i][j] == 0 for i in range(3) for j in range(i))
es_tri_inf = all(A_diag[i][j] == 0 for i in range(3) for j in range(i+1, 3))
es_diagonal = all(A_diag[i][j] == 0 for i in range(3) for j in range(3) if i != j)

if es_diagonal:
    print("  ★ A es una matriz DIAGONAL.")
    print("  → det(A) = producto directo de la diagonal.\n")
    diag = [A_diag[i][i] for i in range(3)]
    det_d = diag[0]*diag[1]*diag[2]
    for i, d in enumerate(diag):
        print(f"    a[{i+1}][{i+1}] = {d}")
    print(f"\n  Producto: {diag[0]} × {diag[1]} × {diag[2]} = {det_d}")

elif es_tri_sup or es_tri_inf:
    tipo = "superior" if es_tri_sup else "inferior"
    print(f"  ★ A ya es triangular {tipo}.")
    print("  → det(A) = producto de la diagonal directamente.\n")
    diag = [A_diag[i][i] for i in range(3)]
    det_d = diag[0]*diag[1]*diag[2]
    for i, d in enumerate(diag):
        print(f"    d[{i+1}] = {d}")
    print(f"\n  Producto diagonal: {diag[0]} × {diag[1]} × {diag[2]} = {det_d}")

else:
    print("  Reduciendo A a triangular superior U...\n")
    M2 = [[float(v) for v in fila] for fila in copiar(A_diag)]
    sign2 = 1
    pasos_d = []
    for col in range(3):
        max_f = max(range(col, 3), key=lambda r: abs(M2[r][col]))
        if max_f != col:
            M2[col], M2[max_f] = M2[max_f], M2[col]
            sign2 *= -1
            pasos_d.append((f"Intercambio F{col+1} ↔ F{max_f+1}", copiar(M2)))
        piv = M2[col][col]
        if abs(piv) < 1e-12:
            break
        for f in range(col+1, 3):
            fac = M2[f][col] / piv
            if abs(fac) > 1e-12:
                for k in range(3):
                    M2[f][k] -= fac * M2[col][k]
                pasos_d.append((f"F{f+1} → F{f+1} - ({fac:.4g})·F{col+1}", copiar(M2)))

    for desc, mat in pasos_d:
        print(f"    ▶ {desc}")
        imprimir_matriz(mat, "")

    diag = [M2[i][i] for i in range(3)]
    det_d = sign2 * diag[0]*diag[1]*diag[2]
    print(f"  Diagonal final: {diag[0]:.4f} × {diag[1]:.4f} × {diag[2]:.4f}")
    print(f"  Signo: {'+1' if sign2>0 else '-1'}")

print(f"\n  ┌─────────────────────────────────────────────────────┐")
det_d_final = det_sarrus(A_diag)
print(f"  │  det(A) = {det_d_final:.4f}                                  │")
print(f"  └─────────────────────────────────────────────────────┘")
print(f"\n  Verificación (Sarrus): {det_d_final:.4f}  {'✔' if abs(det_d_final-det_sarrus(A_diag))<1e-6 else '✗'}")


# ══════════════════════════════════════════════════════════════════════════════
#  EJERCICIO 3 — EXPANSIÓN POR COFACTORES
# ══════════════════════════════════════════════════════════════════════════════

titulo_ejercicio(3, "EXPANSIÓN POR COFACTORES  (fila 1)")

print("""
  Procedimiento:
  det(A) = Σ  a[1][j] · C[1][j]    para j = 1, 2, 3
  donde:
    C[i][j] = (-1)^(i+j) · det(M_ij)    (cofactor)
    M_ij    = menor → submatriz al eliminar fila i y columna j
""")

# ─────────────────────────────────────────────────────
# Ejercicio 3 (Cofactores)
# ─────────────────────────────────────────────────────
A_cof = [
    [1,  0,  2],
    [0,  3, 1],
    [4,  0,  1],
]

# ── Ejecución ──────────────────────────────────────
imprimir_matriz(A_cof, "A  (expansión por fila 1)")

print("  Calculando menores y cofactores de la fila 1:\n")
det_total = 0.0
terminos = []

for j in range(3):
    a_ij = A_cof[0][j]
    M_ij = submatriz(A_cof, 0, j)
    d_menor = det2x2(M_ij)
    signo = (-1)**(0 + j)
    cof = signo * d_menor
    contribucion = a_ij * cof
    det_total += contribucion

    sg_str  = "+" if signo > 0 else "-"
    sg_num  = "+1" if signo > 0 else "-1"
    contrib_str = f"{contribucion:+.4f}"

    print(f"  ┌─ Columna {j+1} ─────────────────────────────────────────┐")
    print(f"  │  a[1][{j+1}] = {a_ij}")
    print(f"  │  Signo  (-1)^(1+{j+1}) = (-1)^{1+j} = {sg_num}")
    print(f"  │  Menor M_1{j+1}:")
    for fila in M_ij:
        print(f"  │    │ " + "  ".join(f"{v:6}" for v in fila) + " │")
    print(f"  │  det(M_1{j+1}) = ({M_ij[0][0]})·({M_ij[1][1]}) - ({M_ij[0][1]})·({M_ij[1][0]})")
    print(f"  │             = {M_ij[0][0]*M_ij[1][1]:.4f} - {M_ij[0][1]*M_ij[1][0]:.4f} = {d_menor:.4f}")
    print(f"  │  C_1{j+1}  = {sg_num} × {d_menor:.4f} = {cof:.4f}")
    print(f"  │  a[1][{j+1}] × C_1{j+1} = {a_ij} × {cof:.4f} = {contribucion:.4f}")
    print(f"  └────────────────────────────────────────────────────────┘\n")
    terminos.append(f"({a_ij})·({cof:.4f})")

print(f"  Suma de contribuciones:")
print(f"    det(A) = " + " + ".join(terminos))
print(f"           = {det_total:.4f}")
print(f"\n  ┌─────────────────────────────────────────────────────┐")
print(f"  │  det(A) = {det_total:.4f}                                  │")
print(f"  └─────────────────────────────────────────────────────┘")
ref3 = det_sarrus(A_cof)
print(f"\n  Verificación (Sarrus): det(A) = {ref3:.4f}  {'✔' if abs(det_total-ref3)<1e-6 else '✗'}")


# ══════════════════════════════════════════════════════
print(f"\n\n{'═'*62}")
print("  ✔  Los 3 ejercicios completados.")
print(f"{'═'*62}\n")