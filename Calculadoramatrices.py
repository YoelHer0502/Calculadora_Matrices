import os
import sys
from fractions import Fraction

# ══════════════════════════════════════════════════════
#  UTILIDADES DE DISPLAY
# ══════════════════════════════════════════════════════

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def linea(char="═", n=60):
    print(char * n)

def titulo(texto):
    linea()
    print(f"  {texto}")
    linea()

def subtitulo(texto):
    print(f"\n  ── {texto} ──")

def pausar():
    input("\n  Presiona ENTER para continuar...")

def imprimir_matriz(M, nombre="M"):
    print(f"\n  {nombre} =")
    for fila in M:
        fila_str = "  │ "
        for val in fila:
            if isinstance(val, float):
                fila_str += f"{val:9.4f}  "
            else:
                fila_str += f"{val:9}  "
        fila_str += "│"
        print(fila_str)
    print()

def imprimir_sistema(A, b):
    n = len(A)
    vars_ = ['x', 'y', 'z']
    print("\n  Sistema de ecuaciones:")
    for i in range(n):
        eq = "  "
        for j in range(n):
            coef = A[i][j]
            var = vars_[j]
            if j == 0:
                eq += f"{coef:+.4g}{var} "
            else:
                signo = "+" if coef >= 0 else "-"
                eq += f"{signo} {abs(coef):.4g}{var} "
        eq += f"= {b[i]:.4g}"
        print(eq)
    print()

# ══════════════════════════════════════════════════════
#  OPERACIONES MATRICIALES BÁSICAS
# ══════════════════════════════════════════════════════

def copiar_matriz(M):
    return [fila[:] for fila in M]

def submatriz(M, fila_ex, col_ex):
    return [
        [M[i][j] for j in range(len(M[0])) if j != col_ex]
        for i in range(len(M)) if i != fila_ex
    ]

def transpuesta_n(M):
    n = len(M)
    return [[M[j][i] for j in range(n)] for i in range(n)]

def multiplicar_matrices_nxn(A, B):
    n = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

# ══════════════════════════════════════════════════════
#  DETERMINANTES
# ══════════════════════════════════════════════════════

def determinante_2x2(M):
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]

def determinante_3x3(M):
    a = M
    return (a[0][0]*a[1][1]*a[2][2]
          + a[0][1]*a[1][2]*a[2][0]
          + a[0][2]*a[1][0]*a[2][1]
          - a[0][2]*a[1][1]*a[2][0]
          - a[0][1]*a[1][0]*a[2][2]
          - a[0][0]*a[1][2]*a[2][1])

def determinante_nxn(M):
    n = len(M)
    if n == 2:
        return determinante_2x2(M)
    return determinante_3x3(M)

def det_por_gauss_n(M_orig):
    """Det por eliminación gaussiana. Devuelve (det, pasos)."""
    n = len(M_orig)
    M = copiar_matriz(M_orig)
    sign = 1
    pasos = [("Matriz inicial", copiar_matriz(M), 1.0)]
    for col in range(n):
        max_fila = max(range(col, n), key=lambda r: abs(M[r][col]))
        if max_fila != col:
            M[col], M[max_fila] = M[max_fila], M[col]
            sign *= -1
            pasos.append((f"Intercambio F{col+1} ↔ F{max_fila+1}", copiar_matriz(M), sign))
        pivot = M[col][col]
        if abs(pivot) < 1e-12:
            return 0.0, pasos
        for fila in range(col + 1, n):
            factor = M[fila][col] / pivot
            if abs(factor) > 1e-12:
                desc = f"F{fila+1} → F{fila+1} - ({factor:.4g}) × F{col+1}"
                for k in range(n):
                    M[fila][k] -= factor * M[col][k]
                pasos.append((desc, copiar_matriz(M), sign))
    diag = 1.0
    for i in range(n):
        diag *= M[i][i]
    return sign * diag, pasos

def det_por_gauss(M_orig):
    return det_por_gauss_n(M_orig)

def cofactor_nxn(M, i, j):
    menor = submatriz(M, i, j)
    n_m = len(menor)
    if n_m == 1:
        m_det = menor[0][0]
    elif n_m == 2:
        m_det = determinante_2x2(menor)
    else:
        m_det = determinante_3x3(menor)
    return ((-1) ** (i + j)) * m_det

def inversa_gauss_jordan(M):
    n = len(M)
    Aug = [M[i][:] + [1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        max_f = max(range(col, n), key=lambda r: abs(Aug[r][col]))
        Aug[col], Aug[max_f] = Aug[max_f], Aug[col]
        pivot = Aug[col][col]
        if abs(pivot) < 1e-12:
            return None
        Aug[col] = [x / pivot for x in Aug[col]]
        for fila in range(n):
            if fila != col:
                factor = Aug[fila][col]
                Aug[fila] = [Aug[fila][k] - factor * Aug[col][k] for k in range(2*n)]
    return [Aug[i][n:] for i in range(n)]

# ══════════════════════════════════════════════════════
#  ENTRADA DE DATOS
# ══════════════════════════════════════════════════════

def ingresar_matriz_nxn(nombre="A", n=3):
    print(f"\n  Ingresa los elementos de {nombre} ({n}×{n}):")
    print("  (acepta enteros, decimales o fracciones como 1/2)\n")
    M = []
    for i in range(n):
        fila = []
        for j in range(n):
            while True:
                try:
                    val = float(Fraction(input(f"    {nombre}[{i+1}][{j+1}] = ").strip()))
                    fila.append(val)
                    break
                except:
                    print("    ✗ Valor inválido.")
        M.append(fila)
    return M

def ingresar_matriz_3x3(nombre="A"):
    return ingresar_matriz_nxn(nombre, 3)

def ingresar_vector(nombre="b", n=3):
    etiquetas = ["b₁", "b₂", "b₃"]
    print(f"\n  Ingresa el vector {nombre} (términos independientes):")
    v = []
    for i in range(n):
        while True:
            try:
                val = float(Fraction(input(f"    {etiquetas[i]} = ").strip()))
                v.append(val)
                break
            except:
                print("    ✗ Valor inválido.")
    return v

def ingresar_escalar(nombre="k"):
    while True:
        try:
            return float(input(f"    {nombre} = ").strip())
        except:
            print("    ✗ Valor inválido.")

def pedir_tamano():
    while True:
        op = input("  ¿Tamaño de la matriz? [2] 2×2   [3] 3×3 → ").strip()
        if op in ("2", "3"):
            return int(op)
        print("  ✗ Elige 2 o 3.")

# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 1: SISTEMAS DE ECUACIONES LINEALES 3×3
# ══════════════════════════════════════════════════════════════════════════════

def rango_matriz(M):
    n, m = len(M), len(M[0])
    R = copiar_matriz(M)
    rango = 0
    fila_actual = 0
    for col in range(m):
        max_f = -1
        for f in range(fila_actual, n):
            if abs(R[f][col]) > 1e-12:
                max_f = f
                break
        if max_f == -1:
            continue
        R[fila_actual], R[max_f] = R[max_f], R[fila_actual]
        pivot = R[fila_actual][col]
        for f in range(fila_actual + 1, n):
            factor = R[f][col] / pivot
            for k in range(m):
                R[f][k] -= factor * R[fila_actual][k]
        rango += 1
        fila_actual += 1
    return rango

def clasificar_sistema(A, b):
    """
    Clasifica el sistema Ax=b (Rouché-Frobenius).
    Retorna: ('unica'|'infinitas'|'sin_solucion', rA, rAb, n)
    """
    n = len(A)
    Ab = [A[i][:] + [b[i]] for i in range(n)]
    rA  = rango_matriz(A)
    rAb = rango_matriz(Ab)
    if rA != rAb:
        return 'sin_solucion', rA, rAb, n
    elif rA == n:
        return 'unica', rA, rAb, n
    else:
        return 'infinitas', rA, rAb, n

def imprimir_clasificacion(tipo, rA, rAb, n):
    print("\n" + "─"*60)
    print("  CLASIFICACIÓN  (Teorema de Rouché-Frobenius)")
    print("─"*60)
    print(f"  rang(A)          = {rA}")
    print(f"  rang(A|b)        = {rAb}")
    print(f"  N° de incógnitas = {n}")
    print()
    if tipo == 'unica':
        print("  ✔  SISTEMA COMPATIBLE DETERMINADO")
        print("     → Tiene UNA ÚNICA SOLUCIÓN")
        print(f"     Condición: rang(A) = rang(A|b) = n  →  {rA} = {rAb} = {n}")
    elif tipo == 'infinitas':
        grado = n - rA
        print("  ∞  SISTEMA COMPATIBLE INDETERMINADO")
        print("     → Tiene INFINITAS SOLUCIONES")
        print(f"     Condición: rang(A) = rang(A|b) < n  →  {rA} = {rAb} < {n}")
        print(f"     Grado de indeterminación: {grado} parámetro(s) libre(s)")
    else:
        print("  ✗  SISTEMA INCOMPATIBLE")
        print("     → NO TIENE SOLUCIÓN")
        print(f"     Condición: rang(A) ≠ rang(A|b)  →  {rA} ≠ {rAb}")
    print("─"*60)

def eliminacion_gaussiana_sistema(A_orig, b_orig):
    """Devuelve (sol_o_None, pasos, tipo, rA, rAb)."""
    n = len(A_orig)
    tipo, rA, rAb, _ = clasificar_sistema(A_orig, b_orig)
    M = [A_orig[i][:] + [b_orig[i]] for i in range(n)]
    pasos = [("Matriz aumentada inicial [A|b]", copiar_matriz(M))]

    for col in range(n):
        max_fila = max(range(col, n), key=lambda r: abs(M[r][col]))
        if max_fila != col:
            M[col], M[max_fila] = M[max_fila], M[col]
            pasos.append((f"Intercambio F{col+1} ↔ F{max_fila+1}", copiar_matriz(M)))
        pivot = M[col][col]
        if abs(pivot) < 1e-12:
            pasos.append(("Forma escalonada final", copiar_matriz(M)))
            return None, pasos, tipo, rA, rAb
        for fila in range(col + 1, n):
            factor = M[fila][col] / pivot
            if abs(factor) > 1e-12:
                desc = f"F{fila+1} → F{fila+1} - ({factor:.4g}) × F{col+1}"
                for k in range(col, n + 1):
                    M[fila][k] -= factor * M[col][k]
                pasos.append((desc, copiar_matriz(M)))

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n]
        for j in range(i + 1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]
    return x, pasos, tipo, rA, rAb

def regla_cramer(A, b):
    """Devuelve (sol_o_None, tipo, rA, rAb)."""
    tipo, rA, rAb, n = clasificar_sistema(A, b)
    det_A = determinante_3x3(A)
    if abs(det_A) < 1e-12:
        return None, tipo, rA, rAb
    soluciones = []
    for j in range(3):
        A_mod = copiar_matriz(A)
        for i in range(3):
            A_mod[i][j] = b[i]
        soluciones.append(determinante_3x3(A_mod) / det_A)
    return soluciones, tipo, rA, rAb

def menu_sistemas():
    while True:
        limpiar()
        titulo("SISTEMAS DE ECUACIONES LINEALES 3×3")
        print("""
  [1] Eliminación Gaussiana (con pasos)
  [2] Regla de Cramer
  [3] Ambos métodos (comparación)
  [0] Volver al menú principal
        """)
        op = input("  Elige una opción: ").strip()

        if op == "0":
            break
        elif op in ("1", "2", "3"):
            limpiar()
            titulo("INGRESO DEL SISTEMA  Ax = b")
            A = ingresar_matriz_3x3("A")
            b = ingresar_vector("b", 3)
            limpiar()
            titulo("SISTEMA INGRESADO")
            imprimir_sistema(A, b)
            imprimir_matriz(A, "A")

            det_A = determinante_3x3(A)

            if op in ("1", "3"):
                subtitulo("MÉTODO: ELIMINACIÓN GAUSSIANA")
                sol, pasos, tipo, rA, rAb = eliminacion_gaussiana_sistema(A, b)
                print("\n  Pasos de la eliminación:")
                for desc, mat in pasos:
                    print(f"\n  ▶ {desc}")
                    imprimir_matriz(mat)
                imprimir_clasificacion(tipo, rA, rAb, 3)
                if tipo == 'unica':
                    print("\n  ✔ SOLUCIÓN ÚNICA:")
                    print(f"    x = {sol[0]:.6g}")
                    print(f"    y = {sol[1]:.6g}")
                    print(f"    z = {sol[2]:.6g}")
                elif tipo == 'infinitas':
                    print("\n  ∞  El sistema tiene infinitas soluciones.")
                    print("     Existen variables libres (parámetros).")
                else:
                    print("\n  ✗  El sistema no tiene solución (inconsistente).")

            if op in ("2", "3"):
                subtitulo("MÉTODO: REGLA DE CRAMER")
                print(f"\n  det(A) = {det_A:.6g}")
                sol_c, tipo_c, rA_c, rAb_c = regla_cramer(A, b)
                imprimir_clasificacion(tipo_c, rA_c, rAb_c, 3)
                if tipo_c == 'unica':
                    vars_ = ['x', 'y', 'z']
                    for j in range(3):
                        A_mod = copiar_matriz(A)
                        for i in range(3):
                            A_mod[i][j] = b[i]
                        det_j = determinante_3x3(A_mod)
                        print(f"\n  Reemplazando columna {j+1} por b:")
                        imprimir_matriz(A_mod, f"A_{vars_[j]}")
                        print(f"  det(A_{vars_[j]}) = {det_j:.6g}")
                        print(f"  {vars_[j]} = {det_j:.6g} / {det_A:.6g} = {det_j/det_A:.6g}")
                elif tipo_c == 'infinitas':
                    print("\n  ∞  Cramer no aplica directamente (det=0 → infinitas soluciones).")
                else:
                    print("\n  ✗  Cramer no aplica (det=0 → sistema sin solución).")
            pausar()
        else:
            print("  ✗ Opción inválida.")
            pausar()


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 2: DETERMINANTES 3×3
# ══════════════════════════════════════════════════════════════════════════════

def det_por_cofactores(M, fila_exp=0):
    n = len(M)
    fila = fila_exp
    print(f"\n  Expansión por la fila {fila+1}:")
    det = 0.0
    terminos = []
    detalles = []
    for j in range(n):
        cof = cofactor_nxn(M, fila, j)
        aij = M[fila][j]
        signo_str = "+" if (fila + j) % 2 == 0 else "-"
        menor = submatriz(M, fila, j)
        det_menor = determinante_2x2(menor) if len(menor)==2 else determinante_3x3(menor)
        terminos.append(f"({aij:.4g})·({signo_str}{abs(det_menor):.4g})")
        det += aij * cof
        detalles.append((fila, j, aij, signo_str, menor, det_menor, cof))

    print("  det = " + " + ".join(terminos))
    print(f"      = {det:.6g}")
    print(f"\n  Detalle de menores y cofactores:")
    for (fi, j, aij, sgn, menor, det_m, cof) in detalles:
        print(f"\n    a[{fi+1}][{j+1}] = {aij:.4g}   →   Menor M{fi+1}{j+1}:")
        for row in menor:
            print("      | " + "  ".join(f"{v:8.4g}" for v in row) + " |")
        print(f"    det(M{fi+1}{j+1}) = {det_m:.4g}   C{fi+1}{j+1} = {sgn}{abs(det_m):.4g}")
    return det

def menu_determinantes():
    while True:
        limpiar()
        titulo("DETERMINANTES 3×3")
        print("""
  [1] Método de Gauss (triangulación)
  [2] Expansión por Cofactores
  [3] Diagonalización (triangular superior)
  [4] Los tres métodos (verificación cruzada)
  [0] Volver al menú principal
        """)
        op = input("  Elige una opción: ").strip()

        if op == "0":
            break
        elif op in ("1", "2", "3", "4"):
            limpiar()
            titulo("INGRESA LA MATRIZ A (3×3)")
            M = ingresar_matriz_3x3("A")
            limpiar()
            titulo("CÁLCULO DEL DETERMINANTE")
            imprimir_matriz(M, "A")

            det_g = det_c = 0.0

            if op in ("1", "4"):
                subtitulo("MÉTODO DE GAUSS")
                det_g, pasos = det_por_gauss(M)
                print("\n  Pasos:")
                for desc, mat, sg in pasos:
                    print(f"\n  ▶ {desc}  [signo acum.: {'+' if sg>0 else '-'}1]")
                    imprimir_matriz(mat)
                U = pasos[-1][1]
                diag = [U[i][i] for i in range(3)]
                print(f"  Diagonal triangular: {' × '.join(f'{d:.4g}' for d in diag)}")
                print(f"\n  ✔ det(A) por Gauss = {det_g:.6g}")

            if op in ("2", "4"):
                subtitulo("EXPANSIÓN POR COFACTORES")
                det_c = det_por_cofactores(M, fila_exp=0)
                print(f"\n  ✔ det(A) por Cofactores = {det_c:.6g}")

            if op in ("3", "4"):
                subtitulo("DIAGONALIZACIÓN (triangular superior)")
                det_d, pasos_d = det_por_gauss(M)
                U = pasos_d[-1][1]
                imprimir_matriz(U, "U (triangular superior)")
                diag = [U[i][i] for i in range(3)]
                print(f"  Producto diagonal: {' × '.join(f'{d:.4g}' for d in diag)} × signo = {det_d:.6g}")
                print(f"\n  ✔ det(A) por Diagonalización = {det_d:.6g}")

            if op == "4":
                print("\n" + "─"*50)
                print("  VERIFICACIÓN CRUZADA:")
                det_sarrus = determinante_3x3(M)
                print(f"    Gauss         → {det_g:.6g}")
                print(f"    Cofactores    → {det_c:.6g}")
                print(f"    Sarrus (ref)  → {det_sarrus:.6g}")
            pausar()
        else:
            print("  ✗ Opción inválida.")
            pausar()


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 3: PROPIEDADES DE LOS DETERMINANTES (2×2 o 3×3)
# ══════════════════════════════════════════════════════════════════════════════

def propiedad_1_transpuesta(M):
    n = len(M)
    titulo(f"PROPIEDAD 1: det(A) = det(Aᵀ)  [{n}×{n}]")
    print("\n  Si A es cuadrada, su determinante es igual al de su transpuesta.")
    imprimir_matriz(M, "A")
    Mt = transpuesta_n(M)
    imprimir_matriz(Mt, "Aᵀ")
    dA  = determinante_nxn(M)
    dAt = determinante_nxn(Mt)
    print(f"  det(A)  = {dA:.6g}")
    print(f"  det(Aᵀ) = {dAt:.6g}")
    print(f"\n  ✔ Son iguales: {'Sí ✓' if abs(dA - dAt) < 1e-9 else 'No ✗'}")

def propiedad_2_fila_ceros(M):
    n = len(M)
    titulo(f"PROPIEDAD 2: Fila de ceros → det = 0  [{n}×{n}]")
    print("\n  Si una fila (o columna) es de ceros, el determinante es 0.")
    M2 = copiar_matriz(M)
    while True:
        try:
            fila = int(input(f"  ¿Qué fila poner a ceros? (1-{n}): ").strip()) - 1
            if 0 <= fila < n:
                break
        except:
            pass
        print(f"  ✗ Elige entre 1 y {n}.")
    M2[fila] = [0.0] * n
    imprimir_matriz(M2, "A (fila cero)")
    d = determinante_nxn(M2)
    print(f"  det(A) = {d:.6g}  → {'✔ Correcto (= 0)' if abs(d) < 1e-9 else '¿Algo salió mal?'}")

def propiedad_3_intercambio(M):
    n = len(M)
    titulo(f"PROPIEDAD 3: Intercambio de filas → cambio de signo  [{n}×{n}]")
    print("\n  Si se intercambian dos filas, el determinante cambia de signo.")
    imprimir_matriz(M, "A original")
    d1 = determinante_nxn(M)
    M2 = copiar_matriz(M)
    M2[0], M2[1] = M2[1][:], M2[0][:]
    imprimir_matriz(M2, "A' (F1 ↔ F2)")
    d2 = determinante_nxn(M2)
    print(f"  det(A)   = {d1:.6g}")
    print(f"  det(A')  = {d2:.6g}")
    ok = abs(d2 + d1) < 1e-9
    print(f"\n  ✔ det(A') = -det(A)  →  {'Correcto ✓' if ok else 'Error ✗'}")

def propiedad_4_escalar(M):
    n = len(M)
    titulo(f"PROPIEDAD 4: det(kA) = k^n · det(A)  [{n}×{n}]")
    print(f"\n  Al multiplicar toda la matriz por k, el det se escala por k^{n}.")
    imprimir_matriz(M, "A")
    k = ingresar_escalar("k")
    kA  = [[k * M[i][j] for j in range(n)] for i in range(n)]
    imprimir_matriz(kA, f"k·A  (k={k})")
    dA   = determinante_nxn(M)
    dkA  = determinante_nxn(kA)
    esp  = (k**n) * dA
    print(f"  det(A)        = {dA:.6g}")
    print(f"  det(k·A)      = {dkA:.6g}")
    print(f"  k^{n}·det(A)  = ({k})^{n} × {dA:.6g} = {esp:.6g}")
    ok = abs(dkA - esp) < 1e-6
    print(f"\n  ✔ Verificación: {'Correcto ✓' if ok else 'Error ✗'}")

def propiedad_5_filas_iguales(M):
    n = len(M)
    titulo(f"PROPIEDAD 5: Filas iguales → det = 0  [{n}×{n}]")
    print("\n  Si dos filas son idénticas (o proporcionales), el determinante es 0.")
    M2 = copiar_matriz(M)
    M2[1] = M2[0][:]
    imprimir_matriz(M2, "A (F1 = F2)")
    d = determinante_nxn(M2)
    print(f"  det(A) = {d:.6g}  → {'✔ Correcto (= 0)' if abs(d) < 1e-9 else '¿Algo salió mal?'}")

def propiedad_6_combinacion_lineal(M):
    n = len(M)
    titulo(f"PROPIEDAD 6: Fᵢ + k·Fⱼ no cambia el det  [{n}×{n}]")
    print("\n  Sumar a una fila un múltiplo de otra no altera el determinante.")
    imprimir_matriz(M, "A")
    d1 = determinante_nxn(M)
    k = ingresar_escalar("k (F2 → F2 + k·F1)")
    M2 = copiar_matriz(M)
    for j in range(n):
        M2[1][j] += k * M2[0][j]
    imprimir_matriz(M2, f"A' (F2 + {k}·F1)")
    d2 = determinante_nxn(M2)
    print(f"  det(A)  = {d1:.6g}")
    print(f"  det(A') = {d2:.6g}")
    ok = abs(d1 - d2) < 1e-9
    print(f"\n  ✔ Son iguales: {'Correcto ✓' if ok else 'Error ✗'}")

def propiedad_7_producto(M):
    n = len(M)
    titulo(f"PROPIEDAD 7: det(A·B) = det(A) · det(B)  [{n}×{n}]")
    print("\n  El det del producto es el producto de los determinantes.")
    imprimir_matriz(M, "A")
    print(f"\n  Ingresa la segunda matriz B ({n}×{n}):")
    B = ingresar_matriz_nxn("B", n)
    limpiar()
    imprimir_matriz(M, "A")
    imprimir_matriz(B, "B")
    AB  = multiplicar_matrices_nxn(M, B)
    imprimir_matriz(AB, "A·B")
    dA  = determinante_nxn(M)
    dB  = determinante_nxn(B)
    dAB = determinante_nxn(AB)
    print(f"  det(A)        = {dA:.6g}")
    print(f"  det(B)        = {dB:.6g}")
    print(f"  det(A)·det(B) = {dA*dB:.6g}")
    print(f"  det(A·B)      = {dAB:.6g}")
    ok = abs(dAB - dA*dB) < 1e-6
    print(f"\n  ✔ Verificación: {'Correcto ✓' if ok else 'Pequeña diferencia numérica'}")

def propiedad_8_triangular(M):
    n = len(M)
    titulo(f"PROPIEDAD 8: det(triangular) = producto diagonal  [{n}×{n}]")
    print("\n  Para matrices triangulares, det = producto de la diagonal.")
    imprimir_matriz(M, "A")
    det_val, pasos = det_por_gauss_n(M)
    U = pasos[-1][1]
    imprimir_matriz(U, "U (triangular superior)")
    diag = [U[i][i] for i in range(n)]
    prod = 1.0
    for d in diag:
        prod *= d
    prod_str = " × ".join(f"{d:.4g}" for d in diag)
    print(f"  Diagonal: {prod_str}")
    print(f"  Producto diagonal = {prod:.6g}  (antes de signo por intercambios)")
    print(f"  det(A) = {det_val:.6g}  (con signo correcto)")
    print(f"\n  ✔ Producto diagonal × signo de intercambios = det(A)")

def propiedad_9_inversa(M):
    n = len(M)
    titulo(f"PROPIEDAD 9: det(A⁻¹) = 1/det(A)  [{n}×{n}]")
    print("\n  Si A es invertible, det(A⁻¹) = 1 / det(A).")
    imprimir_matriz(M, "A")
    dA = determinante_nxn(M)
    print(f"\n  det(A) = {dA:.6g}")
    if abs(dA) < 1e-9:
        print("  ✗ A no es invertible (det = 0). La propiedad no aplica.")
        return
    Ainv = inversa_gauss_jordan(M)
    if Ainv is None:
        print("  ✗ No se pudo calcular la inversa.")
        return
    imprimir_matriz(Ainv, "A⁻¹")
    dAinv = determinante_nxn(Ainv)
    print(f"\n  det(A⁻¹) = {dAinv:.6g}")
    print(f"  1/det(A) = {1/dA:.6g}")
    ok = abs(dAinv - 1/dA) < 1e-6
    print(f"\n  ✔ Verificación: {'Correcto ✓' if ok else 'Pequeña diferencia numérica'}")


PROPIEDADES = [
    ("det(A) = det(Aᵀ)            [Transpuesta]",    propiedad_1_transpuesta),
    ("Fila de ceros → det = 0",                       propiedad_2_fila_ceros),
    ("Intercambio de filas → cambio de signo",        propiedad_3_intercambio),
    ("det(kA) = k^n · det(A)      [Escalar]",         propiedad_4_escalar),
    ("Filas iguales → det = 0",                       propiedad_5_filas_iguales),
    ("Fᵢ + k·Fⱼ no cambia det    [Op. fila]",        propiedad_6_combinacion_lineal),
    ("det(A·B) = det(A)·det(B)    [Producto]",        propiedad_7_producto),
    ("det(triangular) = ∏ diagonal",                  propiedad_8_triangular),
    ("det(A⁻¹) = 1/det(A)         [Inversa]",         propiedad_9_inversa),
]

def menu_propiedades():
    while True:
        limpiar()
        titulo("LAS 9 PROPIEDADES DE LOS DETERMINANTES")
        print("  (Para cada propiedad puedes elegir matriz 2×2 o 3×3)\n")
        for i, (nombre, _) in enumerate(PROPIEDADES, 1):
            print(f"  [{i}] {nombre}")
        print("  [0] Volver al menú principal")
        print()
        op = input("  Elige la propiedad a verificar: ").strip()

        if op == "0":
            break
        try:
            idx = int(op) - 1
            if 0 <= idx < len(PROPIEDADES):
                limpiar()
                nombre_prop, func = PROPIEDADES[idx]
                print(f"\n  PROPIEDAD {idx+1}: {nombre_prop}\n")
                n = pedir_tamano()
                print(f"\n  Ingresa la matriz A de prueba:\n")
                M = ingresar_matriz_nxn("A", n)
                limpiar()
                func(M)
                pausar()
            else:
                print("  ✗ Opción fuera de rango.")
                pausar()
        except ValueError:
            print("  ✗ Opción inválida.")
            pausar()


# ══════════════════════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def menu_principal():
    while True:
        limpiar()
        print("""
╔══════════════════════════════════════════════════════════════╗
║              ÁLGEBRA LINEAL — CALCULADORA                    ║
║       Sistemas Lineales · Determinantes · Propiedades        ║
╚══════════════════════════════════════════════════════════════╝

  [1]  Sistemas de Ecuaciones Lineales 3×3
       └─ Eliminación Gaussiana / Regla de Cramer
       └─ Clasifica: única solución / infinitas / sin solución

  [2]  Determinantes 3×3
       └─ Gauss · Cofactores · Diagonalización

  [3]  Las 9 Propiedades de los Determinantes
       └─ Verificación interactiva  (elige 2×2 o 3×3)

  [0]  Salir
""")
        op = input("  Selecciona una opción: ").strip()
        if op == "1":
            menu_sistemas()
        elif op == "2":
            menu_determinantes()
        elif op == "3":
            menu_propiedades()
        elif op == "0":
            limpiar()
            print("\n  ¡Hasta luego!.\n")
            sys.exit(0)
        else:
            print("\n  ✗ Opción no válida.")
            pausar()

if __name__ == "__main__":
    menu_principal()