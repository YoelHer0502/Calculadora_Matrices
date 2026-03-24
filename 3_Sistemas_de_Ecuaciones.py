"""
╔══════════════════════════════════════════════════════╗
║     SISTEMAS DE ECUACIONES LINEALES 3×3              ║
║  2 ejercicios por tipo de solución                   ║
║  • Solución Única  • Infinitas  • Sin Solución       ║
╚══════════════════════════════════════════════════════╝

  Clasificación por Teorema de Rouché-Frobenius:
  ✔  rang(A) = rang(A|b) = n  →  ÚNICA SOLUCIÓN
  ∞  rang(A) = rang(A|b) < n  →  INFINITAS SOLUCIONES
  ✗  rang(A) ≠ rang(A|b)      →  SIN SOLUCIÓN

"""

# ══════════════════════════════════════════════════════
#  MOTOR: ÁLGEBRA LINEAL
# ══════════════════════════════════════════════════════

def copiar(M):
    return [f[:] for f in M]

def rango(M):
    n, m = len(M), len(M[0])
    R = copiar(M)
    rg = 0
    fila_act = 0
    for col in range(m):
        piv_f = next((f for f in range(fila_act, n) if abs(R[f][col]) > 1e-12), -1)
        if piv_f == -1:
            continue
        R[fila_act], R[piv_f] = R[piv_f], R[fila_act]
        piv = R[fila_act][col]
        for f in range(fila_act + 1, n):
            fac = R[f][col] / piv
            for k in range(m):
                R[f][k] -= fac * R[fila_act][k]
        rg += 1
        fila_act += 1
    return rg

def clasificar(A, b):
    n = len(A)
    Ab = [A[i][:] + [b[i]] for i in range(n)]
    rA  = rango(A)
    rAb = rango(Ab)
    if rA != rAb:       return "sin_solucion", rA, rAb, n
    elif rA == n:       return "unica",         rA, rAb, n
    else:               return "infinitas",     rA, rAb, n

def gauss_resolver(A_orig, b_orig):
    """Eliminación gaussiana con pivoteo. Devuelve (sol, pasos, M_final)."""
    n = len(A_orig)
    M = [A_orig[i][:] + [b_orig[i]] for i in range(n)]
    pasos = [("Matriz aumentada [A|b]", copiar(M))]
    for col in range(n):
        max_f = max(range(col, n), key=lambda r: abs(M[r][col]))
        if max_f != col:
            M[col], M[max_f] = M[max_f], M[col]
            pasos.append((f"Intercambio F{col+1} ↔ F{max_f+1}", copiar(M)))
        piv = M[col][col]
        if abs(piv) < 1e-12:
            pasos.append(("Pivote nulo — forma escalonada final", copiar(M)))
            return None, pasos, M
        for f in range(col + 1, n):
            fac = M[f][col] / piv
            if abs(fac) > 1e-12:
                desc = f"F{f+1} → F{f+1} - ({fac:.4g})·F{col+1}"
                for k in range(col, n + 1):
                    M[f][k] -= fac * M[col][k]
                pasos.append((desc, copiar(M)))
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j]*x[j]
        x[i] /= M[i][i]
    return x, pasos, M

# ══════════════════════════════════════════════════════
#  DISPLAY
# ══════════════════════════════════════════════════════

VARS = ['x', 'y', 'z']

def linea(char="═", n=62):
    print(char * n)

def titulo_bloque(texto):
    print(f"\n\n{'━'*62}")
    print(f"  {texto}")
    print(f"{'━'*62}")

def titulo_ejercicio(n, texto=""):
    print(f"\n  ┌─ Ejercicio {n}" + (f"  [{texto}]" if texto else "") + " ──────────────────────")

def imprimir_sistema(A, b):
    n = len(A)
    print("\n  Sistema de ecuaciones:")
    for i in range(n):
        eq = "    "
        for j in range(n):
            c = A[i][j]
            if j == 0:
                eq += f"{c:+.4g}{VARS[j]} "
            else:
                sg = "+" if c >= 0 else "-"
                eq += f"{sg} {abs(c):.4g}{VARS[j]} "
        eq += f"=  {b[i]:.4g}"
        print(eq)
    print()

def imprimir_mat_aug(M, etiqueta=""):
    n = len(M)
    cols = len(M[0])
    if etiqueta:
        print(f"\n    [{etiqueta}]")
    for i, fila in enumerate(M):
        izq = "  ".join(f"{v:8.4f}" for v in fila[:-1])
        der = f"{fila[-1]:8.4f}"
        sep = "│" if i == n//2 else "│"
        print(f"      │ {izq}  {sep}  {der}  │")
    print()

def imprimir_clasificacion(tipo, rA, rAb, n):
    print(f"\n  {'─'*58}")
    print("   CLASIFICACIÓN  (Rouché-Frobenius)")
    print(f"  {'─'*58}")
    print(f"   rang(A)          = {rA}")
    print(f"   rang(A|b)        = {rAb}")
    print(f"   Nº de incógnitas = {n}")
    print()
    if tipo == "unica":
        print("   ✔  SISTEMA COMPATIBLE DETERMINADO")
        print("      → UNA ÚNICA SOLUCIÓN")
        print(f"      rang(A) = rang(A|b) = n  →  {rA} = {rAb} = {n}")
    elif tipo == "infinitas":
        grado = n - rA
        print("   ∞  SISTEMA COMPATIBLE INDETERMINADO")
        print("      → INFINITAS SOLUCIONES")
        print(f"      rang(A) = rang(A|b) < n  →  {rA} = {rAb} < {n}")
        print(f"      Grado de indeterminación: {grado} parámetro(s) libre(s)")
    else:
        print("   ✗  SISTEMA INCOMPATIBLE")
        print("      → SIN SOLUCIÓN")
        print(f"      rang(A) ≠ rang(A|b)  →  {rA} ≠ {rAb}")
    print(f"  {'─'*58}")

def resolver_y_mostrar(num_ej, A, b):
    titulo_ejercicio(num_ej)
    imprimir_sistema(A, b)

    tipo, rA, rAb, n = clasificar(A, b)
    sol, pasos, M_final = gauss_resolver(A, b)

    print("  Pasos de eliminación gaussiana:")
    for desc, mat in pasos:
        print(f"\n    ▶ {desc}")
        imprimir_mat_aug(mat)

    imprimir_clasificacion(tipo, rA, rAb, n)

    if tipo == "unica":
        print("\n   SOLUCIÓN ÚNICA:")
        for i, v in enumerate(sol):
            print(f"     {VARS[i]} = {v:.6g}")
    elif tipo == "infinitas":
        print("\n   INFINITAS SOLUCIONES")
        print("   → El sistema tiene variables libres (parámetro t).")
        print("   → Expresa las variables dependientes en función de t.")
        print("   → Forma escalonada final:")
        imprimir_mat_aug(M_final, "forma escalonada")
    else:
        print("\n   SIN SOLUCIÓN  (sistema inconsistente)")
        print("   → Hay una ecuación del tipo  0 = k  (k ≠ 0)")
        print("   → Forma escalonada final:")
        imprimir_mat_aug(M_final, "forma escalonada")


# ══════════════════════════════════════════════════════════════════════════════
#  BLOQUE 1 — SOLUCIÓN ÚNICA
# ══════════════════════════════════════════════════════════════════════════════

titulo_bloque("BLOQUE 1 — SOLUCIÓN ÚNICA  ✔  (rang A = rang A|b = n)")

# ─────────────────────────────────────────────────────
# Solución Única · Ejercicio 1
# ─────────────────────────────────────────────────────
A1 = [
    [ 1,  1, 1],
    [2, -1,  1],
    [1,  2,  -1],
]
b1 = [6, 3, 3]

resolver_y_mostrar(1, A1, b1)


# ══════════════════════════════════════════════════════════════════════════════
#  BLOQUE 2 — INFINITAS SOLUCIONES
# ══════════════════════════════════════════════════════════════════════════════

titulo_bloque("BLOQUE 2 — INFINITAS SOLUCIONES  ∞  (rang A = rang A|b < n)")

# ─────────────────────────────────────────────────────
# Infinitas · Ejercicio 1
# ─────────────────────────────────────────────────────
A3 = [
    [1,  -1,  1],
    [2,  -2,  2],
    [3,  -3,  3],
]
b3 = [1, 2, 3]           # b3 = 2·b3[0], 3·b3[0] → consistente

resolver_y_mostrar(1, A3, b3)


# ══════════════════════════════════════════════════════════════════════════════
#  BLOQUE 3 — SIN SOLUCIÓN
# ══════════════════════════════════════════════════════════════════════════════

titulo_bloque("BLOQUE 3 — SIN SOLUCIÓN  ✗  (rang A ≠ rang A|b)")

# ─────────────────────────────────────────────────────
#  Sin Solución · Ejercicio 1
# ─────────────────────────────────────────────────────
A5 = [
    [1,  1,  1],
    [2,  2,  2],
    [1,  -1,  1],
]
b5 = [2, 5, 0]              # ← b[2] ≠ 3·b[0], inconsistente

resolver_y_mostrar(1, A5, b5)



# ══════════════════════════════════════════════════════
linea()
print("  ✔  Los 3 ejercicios completados.")
linea()
print()