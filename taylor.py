
from sympy import symbols, sympify, series, latex, simplify, SympifyError, factorial, O
from errores import validar_expresion, validar_parametros_taylor, manejar_error
 
x = symbols('x')
 
 
def calcular_serie_taylor(expresion_str: str, punto: float = 0, orden: int = 6) -> dict:
    error = validar_expresion(expresion_str)
    if error:
        return error
    error = validar_parametros_taylor(str(punto), str(orden))
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
        a = sympify(str(punto))
 
        serie = series(f, x, a, orden)
 
        # Quitar el término O(x^n) para mostrar solo los términos finitos
        serie_sin_o = serie.removeO()
        serie_sin_o = simplify(serie_sin_o)
 
        # Construir representación de los términos individuales
        terminos = _extraer_terminos(serie, orden)
 
        return {
            "exito": True,
            "resultado": serie_sin_o,
            "serie_completa": serie,
            "latex": latex(serie_sin_o),
            "texto": str(serie_sin_o),
            "terminos": terminos,
            "punto": str(a),
            "orden": orden,
            "funcion_original": str(f),
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))
 
 
def _extraer_terminos(serie, orden: int) -> list:
    """
    Extrae los términos individuales de la serie como lista de strings.
    """
    try:
        serie_sin_o = serie.removeO()
        terminos_expr = serie_sin_o.as_ordered_terms()
        return [str(t) for t in terminos_expr]
    except Exception:
        return [str(serie.removeO())]
 
 
def calcular_taylor_evaluado(expresion_str: str, valor_x: float, punto: float = 0, orden: int = 6) -> dict:
    """
    Evalúa la aproximación de Taylor de f(x) en x = valor_x.
    Útil para comparar con el valor real de la función.
    """
    try:
        f = sympify(expresion_str)
        a = sympify(str(punto))
 
        serie = series(f, x, a, orden).removeO()
 
        aprox = float(serie.subs(x, valor_x))
        real = float(f.subs(x, valor_x))
        error = abs(real - aprox)
 
        return {
            "exito": True,
            "valor_x": valor_x,
            "aproximacion": round(aprox, 6),
            "valor_real": round(real, 6),
            "error_absoluto": round(error, 8),
            "orden": orden,
        }
 
    except SympifyError:
        return {
            "exito": False,
            "error": f"No se pudo interpretar la expresión: '{expresion_str}'",
        }
    except Exception as e:
        return {
            "exito": False,
            "error": f"Error al evaluar Taylor: {str(e)}",
        }
 
def calcular_taylor_integral(expresion_str: str, punto: float = 0, orden: int = 6) -> dict:
    """
    Calcula la serie de Taylor de f(x) y luego integra el polinomio resultante.
 
    Pasos:
        1. Genera T(x) = serie de Taylor de f(x) alrededor de 'punto' hasta 'orden'
        2. Calcula ∫T(x)dx de forma indefinida
    """
    from sympy import integrate, latex
    from errores import validar_expresion, validar_parametros_taylor, manejar_error
 
    error = validar_expresion(expresion_str)
    if error:
        return error
    error = validar_parametros_taylor(str(punto), str(orden))
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
        a = sympify(str(punto))
 
        # Paso 1: Serie de Taylor
        taylor = series(f, x, a, orden).removeO()
        taylor = simplify(taylor)
 
        # Paso 2: Integral indefinida del polinomio de Taylor
        integral = integrate(taylor, x)
        integral = simplify(integral)
 
        return {
            "exito": True,
            "taylor": taylor,
            "taylor_texto": str(taylor),
            "taylor_latex": latex(taylor),
            "integral": integral,
            "integral_texto": str(integral) + " + C",
            "integral_latex": latex(integral) + " + C",
            "punto": str(a),
            "orden": orden,
            "funcion_original": str(f),
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))