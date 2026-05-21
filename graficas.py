import numpy as np
from sympy import symbols, sympify, lambdify, SympifyError, series
 
x = symbols('x')
 
 
def graficar_funcion(expresion_str: str, ax, rango=(-10, 10), color="#534AB7", label=None):
    """
    Grafica f(x) en el Axes de matplotlib proporcionado.
 
    Parámetros:
        expresion_str: función como string
        ax:            objeto Axes de matplotlib donde dibujar
        rango:         tupla (x_min, x_max)
        color:         color de la línea
        label:         etiqueta para la leyenda
    """
    try:
        f = sympify(expresion_str)
        f_num = lambdify(x, f, modules=["numpy"])
 
        xs = np.linspace(rango[0], rango[1], 800)
        ys = f_num(xs)
 
        # Filtrar valores fuera de rango para evitar discontinuidades
        ys = np.where(np.abs(ys) > 1e6, np.nan, ys)
 
        lbl = label if label else f"f(x) = {expresion_str}"
        ax.plot(xs, ys, color=color, linewidth=2, label=lbl)
        ax.axhline(0, color="#888", linewidth=0.7, linestyle="--")
        ax.axvline(0, color="#888", linewidth=0.7, linestyle="--")
        ax.legend(fontsize=9)
        ax.set_xlabel("x", fontsize=10)
        ax.set_ylabel("f(x)", fontsize=10)
        ax.grid(True, alpha=0.3)
 
        return True
 
    except Exception as e:
        ax.text(0.5, 0.5, f"Error al graficar:\n{str(e)}",
                ha="center", va="center", transform=ax.transAxes,
                color="red", fontsize=10)
        return False
 
 
def graficar_integral(expresion_str: str, ax, limite_inf: float, limite_sup: float, rango=(-10, 10)):
    """
    Grafica f(x) y sombrea el área bajo la curva entre los límites dados.
    """
    try:
        f = sympify(expresion_str)
        f_num = lambdify(x, f, modules=["numpy"])
 
        xs = np.linspace(rango[0], rango[1], 800)
        ys = f_num(xs)
        ys = np.where(np.abs(ys) > 1e6, np.nan, ys)
 
        ax.plot(xs, ys, color="#534AB7", linewidth=2, label=f"f(x) = {expresion_str}")
 
        # Área sombreada
        xs_area = np.linspace(limite_inf, limite_sup, 400)
        ys_area = f_num(xs_area)
        ax.fill_between(xs_area, ys_area, alpha=0.3, color="#1D9E75",
                        label=f"Área [{limite_inf}, {limite_sup}]")
 
        ax.axhline(0, color="#888", linewidth=0.7, linestyle="--")
        ax.axvline(0, color="#888", linewidth=0.7, linestyle="--")
        ax.legend(fontsize=9)
        ax.set_xlabel("x", fontsize=10)
        ax.set_ylabel("f(x)", fontsize=10)
        ax.grid(True, alpha=0.3)
 
        return True
 
    except Exception as e:
        ax.text(0.5, 0.5, f"Error al graficar:\n{str(e)}",
                ha="center", va="center", transform=ax.transAxes,
                color="red", fontsize=10)
        return False
 
 
def graficar_taylor(expresion_str: str, ax, punto: float = 0, orden: int = 6, rango=(-5, 5)):
    """
    Grafica f(x) y su aproximación de Taylor superpuestas.
    """
    try:
        f = sympify(expresion_str)
        a = sympify(str(punto))
 
        serie = series(f, x, a, orden).removeO()
 
        f_num = lambdify(x, f, modules=["numpy"])
        t_num = lambdify(x, serie, modules=["numpy"])
 
        xs = np.linspace(rango[0], rango[1], 800)
 
        ys_f = f_num(xs)
        ys_t = t_num(xs)
 
        ys_f = np.where(np.abs(ys_f) > 1e6, np.nan, ys_f)
        ys_t = np.where(np.abs(ys_t) > 1e6, np.nan, ys_t)
 
        ax.plot(xs, ys_f, color="#534AB7", linewidth=2, label=f"f(x) = {expresion_str}")
        ax.plot(xs, ys_t, color="#D85A30", linewidth=2, linestyle="--",
                label=f"Taylor orden {orden} en x={punto}")
 
        ax.axhline(0, color="#888", linewidth=0.7, linestyle="--")
        ax.axvline(0, color="#888", linewidth=0.7, linestyle="--")
        ax.legend(fontsize=9)
        ax.set_xlabel("x", fontsize=10)
        ax.set_ylabel("f(x)", fontsize=10)
        ax.grid(True, alpha=0.3)
 
        return True
 
    except Exception as e:
        ax.text(0.5, 0.5, f"Error al graficar:\n{str(e)}",
                ha="center", va="center", transform=ax.transAxes,
                color="red", fontsize=10)
        return False