from sympy import symbols, sympify, atan, latex, simplify, SympifyError
from errores import validar_expresion, manejar_error
 
x = symbols('x')
 
 
def calcular_atan(expresion_str: str) -> dict:
    """
    Calcula la arcotangente simbólica de una función f(x).
    Retorna un dict con resultado, latex y texto plano.
    """
    error = validar_expresion(expresion_str)
    if error:
        return error
 
    try:
        f = sympify(expresion_str)
        resultado = atan(f)
        resultado_simplificado = simplify(resultado)
 
        return {
            "exito": True,
            "resultado": resultado_simplificado,
            "latex": latex(resultado_simplificado),
            "texto": str(resultado_simplificado),
            "funcion_original": str(f),
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))
 
 
def calcular_atan_evaluado(expresion_str: str, valor: float) -> dict:
    """
    Calcula atan(f(x)) evaluado en un punto x = valor.
    """
    try:
        f = sympify(expresion_str)
        resultado = atan(f)
        valor_numerico = float(resultado.subs(x, valor))
 
        return {
            "exito": True,
            "valor_x": valor,
            "valor_resultado": round(valor_numerico, 6),
            "texto": f"atan(f({valor})) = {round(valor_numerico, 6)}",
        }
 
    except SympifyError:
        return {
            "exito": False,
            "error": f"No se pudo interpretar la expresión: '{expresion_str}'",
        }
    except Exception as e:
        return {
            "exito": False,
            "error": f"Error al evaluar atan: {str(e)}",
        }