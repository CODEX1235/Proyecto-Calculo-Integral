from sympy import (symbols, sympify, atan, latex, simplify, solve,
                   pretty, pi, sqrt, Rational, SympifyError)
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
            "pretty": pretty(resultado_simplificado, use_unicode=True),
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
 
 
def resolver_atan(expresion_str: str, valor_str: str) -> dict:
    """
    Resuelve la ecuación atan(f(x)) = valor.
    valor_str puede ser 'pi/4', 'pi/6', 'pi/3', '0', etc.
 
    Método:
      atan(f(x)) = c  →  f(x) = tan(c)  →  solve(f(x) - tan(c), x)
    Esto evita que SymPy pierda soluciones al trabajar directamente
    con la ecuación atan(f(x)) - c = 0.
    """
    error = validar_expresion(expresion_str)
    if error:
        return error
 
    try:
        from sympy import tan
        f = sympify(expresion_str)
        valor = sympify(valor_str)           # e.g. pi/4
 
        # Aplicar tan a ambos lados: f(x) = tan(valor)
        rhs = simplify(tan(valor))           # tan(pi/4) = 1, tan(pi/6) = sqrt(3)/3 …
        ecuacion = f - rhs
 
        soluciones = solve(ecuacion, x)
 
        if not soluciones:
            return {
                "exito": True,
                "texto": "Sin solución real",
                "pretty": "Sin solución real",
                "latex": r"\text{Sin solución real}",
                "soluciones": [],
                "decimal": "",
                "rhs": str(rhs),
            }
 
        sol_texto = ",  ".join([str(s) for s in soluciones])
        sol_decimal = []
        for s in soluciones:
            try:
                sol_decimal.append(str(round(float(s.evalf()), 6)))
            except Exception:
                sol_decimal.append("complejo")
        sol_decimal_str = ",  ".join(sol_decimal)
 
        return {
            "exito": True,
            "soluciones": soluciones,
            "latex": latex(soluciones),
            "texto": sol_texto,
            "pretty": pretty(soluciones, use_unicode=True),
            "decimal": sol_decimal_str,
            "rhs": str(rhs),          # valor de tan(c) para mostrar al usuario
        }
 
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))