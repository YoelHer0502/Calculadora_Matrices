"""
╔══════════════════════════════════════════════════════╗
║   LAS 9 PROPIEDADES DE LOS DETERMINANTES             ║
║         2 ejemplos por propiedad                     ║
╚══════════════════════════════════════════════════════╝

"""

# ══════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════

def linea(char="═", n=60):
    print(char * n)

def titulo_propiedad(n, texto):
    print(f"\n\n{'═'*60}")
    print(f"  PROPIEDAD {n}: {texto}")
    print(f"{'═'*60}")

def titulo_ejemplo(n):
    print(f"\n  ── Ejemplo {n} ──────────────────────────────────────────")

def imprimir_matriz(M, nombre):
    n = len(M)
    print(f"\n    {nombre}  ({n}×{n}) =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:8.4f}" if isinstance(v,float) else f"{v:8}" for v in fila) + "  │")
    print()

# ══════════════════════════════════════════════════════
#  OPERACIONES
# ══════════════════════════════════════════════════════

def copiar(M):
    return [f[:] for f in M]

def det(M):
    n = len(M)
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    a = M
    return (a[0][0]*a[1][1]*a[2][2]+a[0][1]*a[1][2]*a[2][0]+a[0][2]*a[1][0]*a[2][1]
           -a[0][2]*a[1][1]*a[2][0]-a[0][1]*a[1][0]*a[2][2]-a[0][0]*a[1][2]*a[2][1])

def transpuesta(M):
    n = len(M)
    return [[M[j][i] for j in range(n)] for i in range(n)]

def submatriz(M, fi, ci):
    return [[M[i][j] for j in range(len(M[0])) if j!=ci]
             for i in range(len(M)) if i!=fi]

def cofactor(M, i, j):
    m = submatriz(M, i, j)
    d = m[0][0]*m[1][1] - m[0][1]*m[1][0] if len(m)==2 else det(m)
    return ((-1)**(i+j)) * d

def mult_mat(A, B):
    n = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def inversa_gj(M):
    n = len(M)
    Aug = [M[i][:] + [1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        mx = max(range(col, n), key=lambda r: abs(Aug[r][col]))
        Aug[col], Aug[mx] = Aug[mx], Aug[col]
        p = Aug[col][col]
        Aug[col] = [x/p for x in Aug[col]]
        for f in range(n):
            if f != col:
                fac = Aug[f][col]
                Aug[f] = [Aug[f][k]-fac*Aug[col][k] for k in range(2*n)]
    return [Aug[i][n:] for i in range(n)]

def r(v, d=5):
    return round(v, d)

def ok(cond):
    return "✔ Correcto" if cond else "✗ Error"

# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 1: det(A) = det(Aᵀ)
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(1, "det(A) = det(Aᵀ)  [Transpuesta]")
print("  El determinante de una matriz es igual al de su transpuesta.")

titulo_ejemplo(1)
P1a = [                         
    [1, 2],
    [3, 4],
]
At = transpuesta(P1a)
imprimir_matriz(P1a, "A")
imprimir_matriz(At,  "Aᵀ")
dA, dAt = det(P1a), det(At)
print(f"    det(A)  = {dA:.4f}")
print(f"    det(Aᵀ) = {dAt:.4f}")
print(f"    {ok(abs(dA-dAt)<1e-9)}")

titulo_ejemplo(2)
P1b = [                        
    [2, 5],
    [7, 1],
]
At = transpuesta(P1b)
imprimir_matriz(P1b, "A")
imprimir_matriz(At,  "Aᵀ")
dA, dAt = det(P1b), det(At)
print(f"    det(A)  = {dA:.4f}")
print(f"    det(Aᵀ) = {dAt:.4f}")
print(f"    {ok(abs(dA-dAt)<1e-9)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 2: Fila de ceros → det = 0
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(2, "Fila (o columna) de ceros → det = 0")
print("  Si toda una fila o columna es de ceros, el determinante es 0.")

titulo_ejemplo(1)
P2a_orig = [                    
    [0, 0],
    [3, 5],
]
fila_cero_2a = 0             
P2a = copiar(P2a_orig)
P2a[fila_cero_2a] = [0]*len(P2a)
imprimir_matriz(P2a_orig, "A original")
imprimir_matriz(P2a,      f"A con fila {fila_cero_2a+1} = 0")
d = det(P2a)
print(f"    det(A) = {d:.4f}   {ok(abs(d)<1e-9)}")

titulo_ejemplo(2)
P2b_orig = [                    
    [2, 1],
    [0, 0],
]
fila_cero_2b = 1               
P2b = copiar(P2b_orig)
P2b[fila_cero_2b] = [0]*len(P2b)
imprimir_matriz(P2b_orig, "A original")
imprimir_matriz(P2b,      f"A con fila {fila_cero_2b+1} = 0")
d = det(P2b)
print(f"    det(A) = {d:.4f}   {ok(abs(d)<1e-9)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 3: Intercambio de filas → cambio de signo
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(3, "Intercambio de filas → cambio de signo del det")
print("  Si se intercambian dos filas, el determinante cambia de signo.")

titulo_ejemplo(1)
P3a = [                         
    [1, 2],
    [3, 4],
]
fi1_3a, fi2_3a = 0, 1         
P3a_swap = copiar(P3a)
P3a_swap[fi1_3a], P3a_swap[fi2_3a] = P3a_swap[fi2_3a][:], P3a_swap[fi1_3a][:]
imprimir_matriz(P3a,      "A original")
imprimir_matriz(P3a_swap, f"A (F{fi1_3a+1} ↔ F{fi2_3a+1})")
d1, d2 = det(P3a), det(P3a_swap)
print(f"    det(A)           = {d1:.4f}")
print(f"    det(A swap)      = {d2:.4f}")
print(f"    det(swap) = -det(A):  {ok(abs(d2+d1)<1e-9)}")

titulo_ejemplo(2)
P3b = [                         
    [2, 0],
    [5, 1],
]
fi1_3b, fi2_3b = 0, 1
P3b_swap = copiar(P3b)
P3b_swap[fi1_3b], P3b_swap[fi2_3b] = P3b_swap[fi2_3b][:], P3b_swap[fi1_3b][:]
imprimir_matriz(P3b,      "A original")
imprimir_matriz(P3b_swap, f"A (F{fi1_3b+1} ↔ F{fi2_3b+1})")
d1, d2 = det(P3b), det(P3b_swap)
print(f"    det(A)      = {d1:.4f}")
print(f"    det(swap)   = {d2:.4f}")
print(f"    {ok(abs(d2+d1)<1e-9)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 4: det(kA) = k^n · det(A)
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(4, "det(kA) = kⁿ · det(A)  [Factor escalar]")
print("  Al multiplicar toda la matriz por k, el det se multiplica por kⁿ.")

titulo_ejemplo(1)
P4a = [                         
    [1, 2],
    [3, 4],
]
k4a = 2                        
n = len(P4a)
kA = [[k4a*P4a[i][j] for j in range(n)] for i in range(n)]
imprimir_matriz(P4a, "A")
imprimir_matriz(kA,  f"{k4a}·A")
dA, dkA = det(P4a), det(kA)
esp = (k4a**n)*dA
print(f"    det(A)         = {dA:.4f}")
print(f"    det({k4a}·A)      = {dkA:.4f}")
print(f"    {k4a}^{n}·det(A) = {esp:.4f}")
print(f"    {ok(abs(dkA-esp)<1e-6)}")

titulo_ejemplo(2)
P4b = [                         
    [2, 1],
    [3, 0],
]
k4b = 3                       
n = len(P4b)
kB = [[k4b*P4b[i][j] for j in range(n)] for i in range(n)]
imprimir_matriz(P4b, "A")
imprimir_matriz(kB,  f"{k4b}·A")
dA, dkA = det(P4b), det(kB)
esp = (k4b**n)*dA
print(f"    det(A)           = {dA:.4f}")
print(f"    det({k4b}·A)    = {dkA:.4f}")
print(f"    ({k4b})^{n}·det(A) = {esp:.4f}")
print(f"    {ok(abs(dkA-esp)<1e-6)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 5: Filas iguales → det = 0
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(5, "Filas iguales (o proporcionales) → det = 0")
print("  Si dos filas son idénticas o proporcionales, el det es 0.")

titulo_ejemplo(1)
P5a = [                         
    [1,  2],
    [1,  2],   
]
imprimir_matriz(P5a, "A (F1 = F3)")
d = det(P5a)
print(f"    det(A) = {d:.4f}   {ok(abs(d)<1e-9)}")

titulo_ejemplo(2)
P5b = [                         
    [3,  5],
    [3,  5],   
]
imprimir_matriz(P5b, "A (F2 = ½·F1, proporcionales)")
d = det(P5b)
print(f"    det(A) = {d:.4f}   {ok(abs(d)<1e-9)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 6: Fᵢ + k·Fⱼ no cambia el det
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(6, "Fᵢ → Fᵢ + k·Fⱼ  no altera el det")
print("  Sumar a una fila un múltiplo de otra fila no cambia el determinante.")

titulo_ejemplo(1)
P6a = [                        
    [1, 2],
    [3, 4],
]
k6a   = 1                      
fi_destino_6a = 0              
fi_fuente_6a  =  1             
P6a_mod = copiar(P6a)
n = len(P6a)
for j in range(n):
    P6a_mod[fi_destino_6a][j] += k6a * P6a[fi_fuente_6a][j]
imprimir_matriz(P6a,     "A original")
imprimir_matriz(P6a_mod, f"A'  (F{fi_destino_6a+1} + {k6a}·F{fi_fuente_6a+1})")
d1, d2 = det(P6a), det(P6a_mod)
print(f"    det(A)  = {d1:.4f}")
print(f"    det(A') = {d2:.4f}")
print(f"    {ok(abs(d1-d2)<1e-9)}")

titulo_ejemplo(2)
P6b = [                         
    [2, 1],
    [3, 4],
]
k6b   = -3                     
fi_destino_6b = 0
fi_fuente_6b  = 1
P6b_mod = copiar(P6b)
n = len(P6b)
for j in range(n):
    P6b_mod[fi_destino_6b][j] += k6b * P6b[fi_fuente_6b][j]
imprimir_matriz(P6b,     "A original")
imprimir_matriz(P6b_mod, f"A'  (F{fi_destino_6b+1} + ({k6b})·F{fi_fuente_6b+1})")
d1, d2 = det(P6b), det(P6b_mod)
print(f"    det(A)  = {d1:.4f}")
print(f"    det(A') = {d2:.4f}")
print(f"    {ok(abs(d1-d2)<1e-9)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 7: det(A·B) = det(A) · det(B)
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(7, "det(A·B) = det(A) · det(B)  [Producto]")
print("  El det del producto de matrices es el producto de sus dets.")

titulo_ejemplo(1)
P7a_A = [                       
    [1, 0],
    [2, 1],
]
P7a_B = [                      
    [3, 1],
    [0, 2],
]
AB = mult_mat(P7a_A, P7a_B)
imprimir_matriz(P7a_A, "A")
imprimir_matriz(P7a_B, "B")
imprimir_matriz(AB,    "A·B")
dA, dB, dAB = det(P7a_A), det(P7a_B), det(AB)
print(f"    det(A)        = {dA:.4f}")
print(f"    det(B)        = {dB:.4f}")
print(f"    det(A)·det(B) = {dA*dB:.4f}")
print(f"    det(A·B)      = {dAB:.4f}")
print(f"    {ok(abs(dAB-dA*dB)<1e-6)}")

titulo_ejemplo(2)
P7b_A = [                       
    [2, 1],
    [1, 1],
]
P7b_B = [                       
    [1, 2],
    [3, 4],
]
AB = mult_mat(P7b_A, P7b_B)
imprimir_matriz(P7b_A, "A")
imprimir_matriz(P7b_B, "B")
imprimir_matriz(AB,    "A·B")
dA, dB, dAB = det(P7b_A), det(P7b_B), det(AB)
print(f"    det(A)        = {dA:.4f}")
print(f"    det(B)        = {dB:.4f}")
print(f"    det(A)·det(B) = {dA*dB:.4f}")
print(f"    det(A·B)      = {dAB:.4f}")
print(f"    {ok(abs(dAB-dA*dB)<1e-6)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 8: det(triangular) = producto de la diagonal
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(8, "det(triangular) = ∏ diagonal")
print("  Para matrices triangulares (sup. o inf.), det = producto diagonal.")

titulo_ejemplo(1)
P8a = [                        
    [2, 1],
    [0, 3]
]
imprimir_matriz(P8a, "A (triangular superior)")
n = len(P8a)
diag = [P8a[i][i] for i in range(n)]
prod_diag = 1
for d in diag: prod_diag *= d
d_real = det(P8a)
print(f"    Diagonal: {' × '.join(str(d) for d in diag)}")
print(f"    Producto diagonal = {prod_diag:.4f}")
print(f"    det(A) calculado  = {d_real:.4f}")
print(f"    {ok(abs(prod_diag-d_real)<1e-9)}")

titulo_ejemplo(2)
P8b = [                        
    [4, 2],
    [0, 5]
]
imprimir_matriz(P8b, "A (triangular inferior)")
n = len(P8b)
diag = [P8b[i][i] for i in range(n)]
prod_diag = 1
for d in diag: prod_diag *= d
d_real = det(P8b)
print(f"    Diagonal: {' × '.join(str(d) for d in diag)}")
print(f"    Producto diagonal = {prod_diag:.4f}")
print(f"    det(A) calculado  = {d_real:.4f}")
print(f"    {ok(abs(prod_diag-d_real)<1e-9)}")


# ══════════════════════════════════════════════════════════════════════════════
#  PROPIEDAD 9: det(A⁻¹) = 1 / det(A)
# ══════════════════════════════════════════════════════════════════════════════

titulo_propiedad(9, "det(A⁻¹) = 1/det(A)  [Inversa]")
print("  Si A es invertible, el det de su inversa es el recíproco del det de A.")

titulo_ejemplo(1)
P9a = [                         
    [1, 2],
    [3, 4],
]
imprimir_matriz(P9a, "A")
dA = det(P9a)
print(f"    det(A) = {dA:.4f}")
if abs(dA) < 1e-9:
    print("    ✗ det = 0, A no es invertible.")
else:
    Ainv = inversa_gj(P9a)
    imprimir_matriz([[round(v,5) for v in f] for f in Ainv], "A⁻¹")
    dAinv = det(Ainv)
    print(f"    det(A⁻¹) = {dAinv:.6f}")
    print(f"    1/det(A) = {1/dA:.6f}")
    print(f"    {ok(abs(dAinv-1/dA)<1e-6)}")

titulo_ejemplo(2)
P9b = [                         
    [2, 1],
    [1, 1],
]
imprimir_matriz(P9b, "A")
dA = det(P9b)
print(f"    det(A) = {dA:.4f}")
if abs(dA) < 1e-9:
    print("    ✗ det = 0, A no es invertible.")
else:
    Ainv = inversa_gj(P9b)
    imprimir_matriz([[round(v,5) for v in f] for f in Ainv], "A⁻¹")
    dAinv = det(Ainv)
    print(f"    det(A⁻¹) = {dAinv:.6f}")
    print(f"    1/det(A) = {1/dA:.6f}")
    print(f"    {ok(abs(dAinv-1/dA)<1e-6)}")


# ══════════════════════════════════════════════════════
linea()
print("  ✔  Las 9 propiedades verificadas  (2 ejemplos cada una)")
linea()
print()