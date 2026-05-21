from sympy import symbols, sympify, integrate, latex, simplify, SympifyError, oo
from errores import validar_expresion, validar_limites, manejar_error
 
x = symbols('x')
 
 
def calcular_integral_indefinida(expresion_str: str) -> dict:
    error = validar_expresion(expresion_str)
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
        resultado = integrate(f, x)
        resultado_simplificado = simplify(resultado)
 
        return {
            "exito": True,
            "resultado": resultado_simplificado,
            "latex": latex(resultado_simplificado) + " + C",
            "texto": str(resultado_simplificado) + " + C",
            "funcion_original": str(f),
            "tipo": "indefinida",
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))
 
 
def calcular_integral_definida(expresion_str: str, limite_inf, limite_sup) -> dict:
    error = validar_expresion(expresion_str)
    if error:
        return error
    error = validar_limites(str(limite_inf), str(limite_sup))
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
 
        a = sympify(str(limite_inf))
        b = sympify(str(limite_sup))
 
        resultado = integrate(f, (x, a, b))
        resultado_simplificado = simplify(resultado)
 
        try:
            valor_numerico = float(resultado_simplificado)
        except Exception:
            valor_numerico = None
 
        return {
            "exito": True,
            "resultado": resultado_simplificado,
            "latex": latex(resultado_simplificado),
            "texto": str(resultado_simplificado),
            "valor_numerico": round(valor_numerico, 6) if valor_numerico is not None else "No evaluable numéricamente",
            "funcion_original": str(f),
            "limite_inferior": str(a),
            "limite_superior": str(b),
            "tipo": "definida",
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))