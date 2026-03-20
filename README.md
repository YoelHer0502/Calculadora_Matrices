# Calculadora_Matrices

Aplicativo de consola en Python para el estudio de **sistemas de ecuaciones lineales**, **determinantes** y las **9 propiedades de los determinantes**. Diseñado para construir y resolver ejercicios paso a paso, mostrando cada operación de forma detallada.

---

## 🚀 Requisitos

- Python 3.6 o superior
- No requiere librerías externas (solo módulos estándar: `os`, `sys`, `fractions`)

---

## ▶️ Cómo ejecutar

```bash
python3 algebra_lineal.py
```

Al iniciar verás el menú principal con tres módulos disponibles.

---

## 📋 Módulos

### [1] Sistemas de Ecuaciones Lineales 3×3

Resuelve sistemas de la forma **Ax = b** donde A es una matriz 3×3.

**Métodos disponibles:**

| Opción | Método | Descripción |
|--------|--------|-------------|
| 1 | Eliminación Gaussiana | Reduce la matriz aumentada [A\|b] con pivoteo parcial, mostrando cada operación de fila |
| 2 | Regla de Cramer | Calcula x, y, z usando determinantes auxiliares Aₓ, A_y, A_z |
| 3 | Ambos métodos | Ejecuta los dos y permite comparar resultados |

**Clasificación automática del sistema** (Teorema de Rouché-Frobenius):

El programa calcula `rang(A)` y `rang(A|b)` y clasifica el sistema en una de tres categorías:

```
✔  SISTEMA COMPATIBLE DETERMINADO    → Una única solución
   Condición: rang(A) = rang(A|b) = n

∞  SISTEMA COMPATIBLE INDETERMINADO  → Infinitas soluciones
   Condición: rang(A) = rang(A|b) < n

✗  SISTEMA INCOMPATIBLE              → Sin solución
   Condición: rang(A) ≠ rang(A|b)
```

**Ejemplo de ingreso:**

```
Sistema:  2x + y - z = 8
          x + 3y + 2z = 13
          x - y + 4z = 5

A[1][1] = 2    A[1][2] = 1    A[1][3] = -1
A[2][1] = 1    A[2][2] = 3    A[2][3] = 2
A[3][1] = 1    A[3][2] = -1   A[3][3] = 4

b₁ = 8    b₂ = 13    b₃ = 5
```

---

### [2] Determinantes 3×3

Calcula el determinante de una matriz 3×3 por tres métodos distintos.

| Opción | Método | Descripción |
|--------|--------|-------------|
| 1 | Gauss | Triangulación con pivoteo parcial; registra cada intercambio de filas y su efecto sobre el signo |
| 2 | Cofactores | Expansión por la fila 1; muestra cada menor, su cofactor y el signo correspondiente |
| 3 | Diagonalización | Reduce A a triangular superior U y calcula det(A) = signo × ∏ diagonal |
| 4 | Los tres métodos | Ejecuta los tres y presenta verificación cruzada con Sarrus como referencia |

---

### [3] Las 9 Propiedades de los Determinantes

Verificación interactiva de cada propiedad. Para cada una puedes elegir entre **matriz 2×2 o 3×3**, ingresar tus propios valores y ver la comprobación numérica con resultados detallados.

| N° | Propiedad | Descripción |
|----|-----------|-------------|
| 1 | **Transpuesta** | `det(A) = det(Aᵀ)` |
| 2 | **Fila de ceros** | Si una fila es cero → `det = 0` |
| 3 | **Intercambio de filas** | Intercambiar dos filas cambia el signo del determinante |
| 4 | **Factor escalar** | `det(kA) = kⁿ · det(A)` donde n es el orden de la matriz |
| 5 | **Filas iguales** | Si dos filas son idénticas → `det = 0` |
| 6 | **Operación de fila** | `Fᵢ → Fᵢ + k·Fⱼ` no altera el determinante |
| 7 | **Producto** | `det(A·B) = det(A) · det(B)` |
| 8 | **Matriz triangular** | `det = producto de la diagonal principal` |
| 9 | **Matriz inversa** | `det(A⁻¹) = 1 / det(A)` |

Cada propiedad muestra las matrices antes y después de la operación, los valores de los determinantes y confirma si la propiedad se verifica correctamente.

---

## ✏️ Ingreso de valores

El programa acepta los siguientes formatos para todos los elementos matriciales:

| Formato | Ejemplo |
|---------|---------|
| Entero | `3`, `-7`, `0` |
| Decimal | `1.5`, `-0.25` |
| Fracción | `1/2`, `3/4`, `-2/3` |

---

## 🗂️ Estructura del código

```
algebra_lineal.py
├── Utilidades de display          → imprimir_matriz, imprimir_sistema, titulo...
├── Operaciones matriciales        → copiar_matriz, transpuesta_n, submatriz...
├── Determinantes                  → determinante_2x2/3x3/nxn, det_por_gauss_n,
│                                    cofactor_nxn, inversa_gauss_jordan
├── Entrada de datos               → ingresar_matriz_nxn, ingresar_vector...
├── Módulo 1 — Sistemas            → rango_matriz, clasificar_sistema,
│                                    eliminacion_gaussiana_sistema, regla_cramer
├── Módulo 2 — Determinantes 3×3   → det_por_cofactores, menu_determinantes
└── Módulo 3 — Propiedades         → propiedad_1 ... propiedad_9, menu_propiedades
```

---

## 💡 Ejemplos de uso rápido

**Sistema con infinitas soluciones:**
```
A = [[1,2,3],[4,5,6],[7,8,9]]   b = [6,15,24]
→ rang(A) = rang(A|b) = 2 < 3  →  ∞ infinitas soluciones
```

**Sistema sin solución:**
```
A = [[1,2,3],[4,5,6],[7,8,9]]   b = [1,2,4]
→ rang(A) = 2  ≠  rang(A|b) = 3  →  ✗ sin solución
```

**Verificar propiedad 4 con matriz 2×2:**
```
A = [[3,1],[2,4]]   k = 3
det(A) = 10   →   det(3A) = 90   =   3² × 10  ✓
```

---

## 📌 Notas

- El código usa **pivoteo parcial** en la eliminación gaussiana para mayor estabilidad numérica.
- La inversa se calcula por el método de **Gauss-Jordan** (necesaria para la propiedad 9).
- Los determinantes se comparan con tolerancia `1e-6` para manejar errores de punto flotante.
- La clasificación de sistemas usa el algoritmo de rango por reducción escalonada, independiente del método de resolución elegido.
