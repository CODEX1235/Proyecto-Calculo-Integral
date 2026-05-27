from sympy import SympifyError
 
 
# ─── Tipos de error personalizados ───────────────────────────────────────────
 
class ErrorExpresion(Exception):
    """Se lanza cuando la expresión ingresada no es válida."""
    pass
 
class ErrorLimites(Exception):
    """Se lanza cuando los límites de integración son inválidos."""
    pass
 
class ErrorTaylor(Exception):
    """Se lanza cuando los parámetros de Taylor son incorrectos."""
    pass
 
class ErrorGrafica(Exception):
    """Se lanza cuando no se puede graficar la función."""
    pass
 
 
# ─── Mensajes personalizados por situación ────────────────────────────────────
 
MENSAJES = {
    # Expresión
    "expresion_vacia":       "⚠ El campo f(x) está vacío. Ingresa una función como: x**2 + 1",
    "expresion_invalida":    "⚠ La expresión '{expr}' no es válida. Usa notación Python: x**2, sin(x), exp(x).",
    "expresion_sin_x":       "ℹ La expresión no contiene la variable x. El resultado será una constante.",
    "division_por_cero":     "⚠ La función tiene una división por cero en el dominio evaluado.",
    "funcion_compleja":      "⚠ El resultado contiene números complejos. Revisa el dominio de la función.",
 
    # Integrales
    "limite_invalido":       "⚠ El límite '{limite}' no es un número válido. Usa valores como: 0, 1, -2, oo (infinito).",
    "limite_igual":          "⚠ El límite inferior y superior son iguales. El área sería cero.",
    "limite_invertido":      "ℹ El límite inferior es mayor que el superior. El resultado será negativo.",
    "integral_no_converge":  "⚠ La integral no converge en el intervalo dado.",
    "integral_sin_forma":    "⚠ SymPy no pudo encontrar una forma cerrada para esta integral.",
 
    # Taylor
    "orden_invalido":        "⚠ El orden debe ser un número entero positivo (ej: 4, 6, 8).",
    "orden_muy_alto":        "⚠ Un orden mayor a 20 puede tardar mucho. Se recomienda usar máximo 10.",
    "punto_invalido":        "⚠ El punto de expansión '{punto}' no es un número válido.",
    "taylor_no_converge":    "⚠ La serie de Taylor no converge en este punto para la función dada.",
 
    # Gráfica
    "matplotlib_ausente":    "⚠ Matplotlib no está instalado. Ejecuta: pip install matplotlib",
    "rango_invalido":        "⚠ El rango de graficación no es válido. Usa dos números distintos.",
    "funcion_no_graficable": "⚠ La función no se puede graficar en el rango dado. Prueba otro rango.",
 
    # General
    "error_inesperado":      "⚠ Ocurrió un error inesperado: {detalle}",
}
 
 
# ─── Función principal de manejo ──────────────────────────────────────────────
 
def manejar_error(tipo: str, **kwargs) -> dict:
    """
    Retorna un dict de error estándar con mensaje personalizado.
 
    Uso:
        manejar_error("expresion_invalida", expr="x^^2")
        manejar_error("limite_invalido", limite="abc")
        manejar_error("error_inesperado", detalle=str(e))
    """
    plantilla = MENSAJES.get(tipo, MENSAJES["error_inesperado"])
    mensaje = plantilla.format(**kwargs) if kwargs else plantilla
 
    return {
        "exito": False,
        "tipo_error": tipo,
        "error": mensaje,
    }
 
 
# ─── Validadores reutilizables ────────────────────────────────────────────────
 
def validar_expresion(expresion_str: str) -> dict | None:
    """
    Valida que la expresión no esté vacía y sea interpretable por SymPy.
    Retorna None si es válida, o un dict de error si no lo es.
    """
    from sympy import sympify
 
    if not expresion_str or not expresion_str.strip():
        return manejar_error("expresion_vacia")
 
    try:
        sympify(expresion_str)
        return None  # sin error
    except SympifyError:
        return manejar_error("expresion_invalida", expr=expresion_str)
    except Exception as e:
        return manejar_error("error_inesperado", detalle=str(e))
 
 
def validar_limites(limite_inf_str: str, limite_sup_str: str) -> dict | None:
    """
    Valida que los límites de integración sean números o 'oo'.
    Retorna None si son válidos, o un dict de error si no lo son.
    """
    from sympy import sympify
 
    for nombre, valor in [("inferior", limite_inf_str), ("superior", limite_sup_str)]:
        try:
            sympify(valor)
        except Exception:
            return manejar_error("limite_invalido", limite=valor)
 
    try:
        a = sympify(limite_inf_str)
        b = sympify(limite_sup_str)
        if a == b:
            return manejar_error("limite_igual")
    except Exception:
        pass
 
    return None  # sin error
 
 
def validar_parametros_taylor(punto_str: str, orden_str: str) -> dict | None:
    """
    Valida el punto de expansión y el orden de la serie de Taylor.
    Acepta números y expresiones simbólicas como pi, pi/4, sqrt(2), etc.
    Retorna None si son válidos, o un dict de error si no lo son.
    """
    from sympy import sympify, SympifyError
    try:
        sympify(punto_str)
    except (SympifyError, Exception):
        return manejar_error("punto_invalido", punto=punto_str)
 
    try:
        orden = int(orden_str)
        if orden <= 0:
            return manejar_error("orden_invalido")
        if orden > 20:
            return manejar_error("orden_muy_alto")
    except ValueError:
        return manejar_error("orden_invalido")
 
    return None  # sin error
 
 
 
 