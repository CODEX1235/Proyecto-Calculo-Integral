from sympy import (symbols, sympify, series, latex, simplify, expand,
                   integrate, pretty, SympifyError, factorial, O)
from errores import validar_expresion, validar_parametros_taylor, manejar_error
 
x = symbols('x')
 
 
# ─── Serie de Taylor (punto arbitrario) ──────────────────────────────────────
 
def calcular_serie_taylor(expresion_str: str, punto: float = 0, orden: int = 6) -> dict:
    """
    Calcula la serie de Taylor de f(x) alrededor del punto 'a' hasta el orden dado.
    Si punto == 0 es equivalente a Maclaurin.
    """
    error = validar_expresion(expresion_str)
    if error:
        return error
    error = validar_parametros_taylor(str(punto), str(orden))
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
        a = sympify(str(punto))
 
        # n+1 para que el grado máximo sea exactamente 'orden'
        serie = series(f, x, a, orden + 1)
 
        serie_sin_o = expand(serie.removeO())
 
        terminos = _extraer_terminos_ordenados(serie_sin_o)
 
        return {
            "exito": True,
            "resultado": serie_sin_o,
            "latex": latex(serie_sin_o),
            "texto": str(serie_sin_o),
            "pretty": pretty(serie_sin_o, use_unicode=True),
            "terminos": terminos,
            "punto": str(a),
            "orden": orden,
            "funcion_original": str(f),
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))
 
 
# ─── Serie de Maclaurin (punto fijo = 0) ─────────────────────────────────────
 
def calcular_serie_maclaurin(expresion_str: str, orden: int = 6) -> dict:
    """
    Calcula la serie de Maclaurin de f(x) — es decir Taylor con a=0 —
    y muestra también la fórmula general de cada término: f^(n)(0)/n! · x^n
    """
    error = validar_expresion(expresion_str)
    if error:
        return error
    error = validar_parametros_taylor("0", str(orden))
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
 
        serie = series(f, x, 0, orden + 1)
        serie_sin_o = expand(serie.removeO())
 
        terminos = _extraer_terminos_ordenados(serie_sin_o)
 
        # Línea compacta: suma con notación de coeficientes
        texto_serie = str(serie_sin_o)
        pretty_serie = pretty(serie_sin_o, use_unicode=True)
 
        return {
            "exito": True,
            "resultado": serie_sin_o,
            "latex": latex(serie_sin_o),
            "texto": texto_serie,
            "pretty": pretty_serie,
            "terminos": terminos,
            "orden": orden,
            "funcion_original": str(f),
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))
 
 
# ─── Helpers ──────────────────────────────────────────────────────────────────
 
def _extraer_terminos_ordenados(expr) -> list:
    """Devuelve lista de strings de los términos ordenados por potencia de x."""
    try:
        terminos = expr.as_ordered_terms()
        # Ordenar de menor a mayor potencia
        def _grado(t):
            try:
                return t.as_poly(x).degree() if t.as_poly(x) else 0
            except Exception:
                return 0
        terminos_ord = sorted(terminos, key=_grado)
        return [str(t) for t in terminos_ord]
    except Exception:
        return [str(expr)]