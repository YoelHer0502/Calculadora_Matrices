"""
╔══════════════════════════════════════════════════════╗
║         MATRICES DE ROTACIÓN — 3 EJEMPLOS            ║
╚══════════════════════════════════════════════════════╝

  Una matriz de rotación R(θ) gira vectores un ángulo θ
  en sentido antihorario:

        R(θ) = │  cos θ  -sen θ │
               │  sen θ   cos θ │

"""

import math

# ══════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════

def linea(char="═", n=60):
    print(char * n)

def titulo_seccion(texto):
    print("\n"); linea()
    print(f"  {texto}"); linea()

def titulo_ejemplo(n, texto=""):
    print(f"\n  ┌─ Ejemplo {n}" + (f": {texto}" if texto else "") + " ─")

def imprimir_matriz2x2(M, nombre):
    print(f"\n    {nombre} =")
    for fila in M:
        print("      │ " + "  ".join(f"{v:9.5f}" for v in fila) + "  │")
    print()

def imprimir_vector(v, nombre):
    print(f"    {nombre} = [ {v[0]:9.5f}  {v[1]:9.5f} ]")

def redondear_mat(M, dec=6):
    return [[round(v, dec) for v in fila] for fila in M]

def r(v, dec=5):
    return round(v, dec)

# ══════════════════════════════════════════════════════
#  CONSTRUCCIÓN DE MATRIZ DE ROTACIÓN
# ══════════════════════════════════════════════════════

def matriz_rotacion(grados):
    """Devuelve R(θ) dado el ángulo en grados."""
    rad = math.radians(grados)
    c, s = math.cos(rad), math.sin(rad)
    return [[c, -s], [s, c]]

def rotar_vector(R, v):
    """Multiplica R (2×2) por vector v (2 elementos)."""
    return [R[0][0]*v[0] + R[0][1]*v[1],
            R[1][0]*v[0] + R[1][1]*v[1]]

def transpuesta2(M):
    return [[M[0][0], M[1][0]], [M[0][1], M[1][1]]]

def det2(M):
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]

def mult2x2(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0],  A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0],  A[1][0]*B[0][1]+A[1][1]*B[1][1]]]

# ══════════════════════════════════════════════════════
#  MOSTRAR EJEMPLO COMPLETO
# ══════════════════════════════════════════════════════

def mostrar_rotacion(num_ej, grados, vector):
    titulo_ejemplo(num_ej, f"Rotación de {grados}°")
    rad = math.radians(grados)
    c, s = math.cos(rad), math.sin(rad)
    R = matriz_rotacion(grados)
    Rt = transpuesta2(R)
    RRt = mult2x2(R, Rt)
    v_rot = rotar_vector(R, vector)

    print(f"\n    Ángulo de rotación: θ = {grados}°  =  {rad:.6f} rad")
    print(f"    cos({grados}°) = {c:.6f}")
    print(f"    sen({grados}°) = {s:.6f}\n")

    print("    ┌─ Construcción de R(θ) ─────────────────────────┐")
    print(f"    │   cos θ = {c:9.5f}    -sen θ = {-s:9.5f}     │")
    print(f"    │   sen θ = {s:9.5f}     cos θ = {c:9.5f}     │")
    print("    └────────────────────────────────────────────────┘")

    imprimir_matriz2x2(R, f"R({grados}°)")

    print("    ┌─ Verificación de propiedades ──────────────────┐")
    print(f"    │   det(R) = cos²θ + sen²θ = {r(det2(R))}               │")
    print("    │   R es ortogonal → R⁻¹ = Rᵀ                   │")
    print("    └────────────────────────────────────────────────┘")

    imprimir_matriz2x2(Rt, "Rᵀ = R⁻¹")
    imprimir_matriz2x2(redondear_mat(RRt), "R · Rᵀ = I  (verificación)")

    print("    ┌─ Aplicación al vector ─────────────────────────┐")
    imprimir_vector(vector, "v original  ")
    imprimir_vector(v_rot,  "v rotado    ")

    mag_orig = math.sqrt(vector[0]**2 + vector[1]**2)
    mag_rot  = math.sqrt(v_rot[0]**2  + v_rot[1]**2)
    print(f"\n    │  |v|  = {mag_orig:.5f}  →  |R·v| = {mag_rot:.5f}  (se conserva)")
    print("    └────────────────────────────────────────────────┘\n")

# ══════════════════════════════════════════════════════════════════════════════

linea()
print("  MATRICES DE ROTACIÓN  R(θ)")
linea()

# ─────────────────────────────────────────────────────
#  Ejemplo 1
# ─────────────────────────────────────────────────────
grados_1 = 250                 
vector_1 = [0, 2]               

mostrar_rotacion(1, grados_1, vector_1)

# ─────────────────────────────────────────────────────
# Ejemplo 2
# ─────────────────────────────────────────────────────
grados_2 = 270
vector_2 = [2, 1]

mostrar_rotacion(2, grados_2, vector_2)

# ─────────────────────────────────────────────────────
# Ejemplo 3
# ─────────────────────────────────────────────────────
grados_3 = 180
vector_3 = [4, 2]

mostrar_rotacion(3, grados_3, vector_3)

linea()
print("  ✔  Todos los ejemplos completados.")
linea()
print()