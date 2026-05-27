import tkinter as tk
from tkinter import ttk, messagebox
import threading
 
from atan import calcular_atan, resolver_atan
from integrales import calcular_integral_indefinida, calcular_integral_definida
from taylor import calcular_serie_taylor, calcular_serie_maclaurin
 
# Intentar importar matplotlib (opcional)
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import graficas as graf
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
 
# ─── Paleta de colores ────────────────────────────────────────────────────────
COLOR_BG       = "#F5F4FF"
COLOR_CARD     = "#FFFFFF"
COLOR_PRIMARY  = "#534AB7"
COLOR_PRIMARY2 = "#3C3489"
COLOR_ACCENT   = "#1D9E75"
COLOR_TEXT     = "#2C2C2A"
COLOR_MUTED    = "#888780"
COLOR_BORDER   = "#CECBF6"
COLOR_ERROR    = "#993C1D"
COLOR_SUCCESS  = "#085041"
COLOR_HINT_BG  = "#FFFBEA"
COLOR_HINT_BRD = "#E8D96A"
COLOR_HIST_BG  = "#EDEAFF"
COLOR_HIST_HDR = "#7B72D4"
FONT_LABEL     = ("Segoe UI", 10)
FONT_MONO      = ("Courier New", 11)
FONT_SMALL     = ("Segoe UI", 9)
 
MAX_HISTORIAL  = 10
 
# ─── Botones matemáticos ──────────────────────────────────────────────────────
BOTONES_MATEMATICOS = [
    ("sin(", "sin("),   ("cos(", "cos("),  ("tan(", "tan("),
    ("atan(", "atan("), ("exp(", "exp("),  ("log(", "log("),
    ("sqrt(", "sqrt("), ("pi", "pi"),      ("x²", "x**2"),
    ("x³", "x**3"),     ("**", "**"),      ("( )", "()"),
    ("ⁿ√x", "root(,)"),
    ("⌫ Borrar", "__BORRAR__"),
]
 
# ─── Manual de uso por operación ─────────────────────────────────────────────
MANUAL = {
    "atan": (
        "📌 Arcotangente  tan⁻¹(f(x))\n"
        "Escribe SOLO lo que va dentro del paréntesis.\n\n"
        "  Ejemplos:\n"
        "  · x            → atan(x)\n"
        "  · 3*x          → atan(3x)\n"
        "  · x**2 + 1     → atan(x²+1)\n"
        "  · sqrt(x)      → atan(√x)\n\n"
        "  ⚠ Recuerda usar * para multiplicar: 3*x, no 3x"
    ),
    "resolver_atan": (
        "📌 Resolver  atan(f(x)) = valor\n"
        "Escribe la función en f(x) y el valor en el campo '='.\n\n"
        "  f(x)   →  valor  →  resultado\n"
        "  3*x       pi/4     x = 1/3\n"
        "  x/2       pi/6     x = 2√3/3\n"
        "  x - 3     -pi/4    x = 2\n\n"
        "  Valores válidos: pi/4  pi/3  pi/6  pi/2  0  -pi/4"
    ),
    "indefinida": (
        "📌 Integral indefinida  ∫f(x)dx\n"
        "Escribe la función tal cual. El programa agrega '+ C'.\n\n"
        "  Ejemplos:\n"
        "  · x**2          → x³/3 + C\n"
        "  · 3*x**2 + 2*x  → x³ + x² + C\n"
        "  · sin(x)        → -cos(x) + C\n"
        "  · exp(x)        → e^x + C\n"
        "  · 1/(1 + x**2)  → atan(x) + C"
    ),
    "definida": (
        "📌 Integral definida  ∫ₐᵇ f(x)dx\n"
        "Escribe la función y los límites a y b.\n\n"
        "  Ejemplos:\n"
        "  · f(x)=x**2,  a=0, b=3   → 9\n"
        "  · f(x)=sin(x), a=0, b=pi → 2\n"
        "  · f(x)=exp(x), a=0, b=1  → e - 1 ≈ 1.718282\n\n"
        "  Límites especiales: oo = infinito,  -oo = -infinito\n"
        "  Puedes usar: pi, E, sqrt(2), etc."
    ),
    "taylor": (
        "📌 Serie de Taylor\n"
        "Expande f(x) alrededor del punto a con el orden pedido.\n\n"
        "  Ejemplos:\n"
        "  · sin(x),  a=0, orden=6  → x - x³/6 + x⁵/120\n"
        "  · cos(x),  a=0, orden=6  → 1 - x²/2 + x⁴/24\n"
        "  · exp(x),  a=0, orden=5  → 1 + x + x²/2 + x³/6 + x⁴/24\n\n"
        "  Orden recomendado: 4 a 10.\n"
        "  a=0 es lo mismo que Maclaurin."
    ),
    "maclaurin": (
        "📌 Serie de Maclaurin\n"
        "Caso especial de Taylor con punto a = 0.\n"
        "Solo necesitas la función y el orden.\n\n"
        "  Ejemplos:\n"
        "  · sin(x),   orden=7  → x - x³/6 + x⁵/120 - x⁷/5040\n"
        "  · cos(x),   orden=6  → 1 - x²/2 + x⁴/24 - x⁶/720\n"
        "  · exp(x),   orden=5  → 1 + x + x²/2 + x³/6 + x⁴/24\n"
        "  · log(1+x), orden=5  → x - x²/2 + x³/3 - x⁴/4\n"
        "  · 1/(1-x),  orden=5  → 1 + x + x² + x³ + x⁴"
    ),
}
 
 
class CalculadoraApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora Matemática")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(True, True)
        self.root.minsize(580, 620)
 
        self._historial   = []
        self._ultimo_texto = ""
 
        self._construir_ui()
        self._centrar_ventana(640, 830)
 
    # ── Layout principal ──────────────────────────────────────────────────────
 
    def _construir_ui(self):
        header = tk.Frame(self.root, bg=COLOR_PRIMARY, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🧮  Calculadora Matemática",
                 font=("Segoe UI", 16, "bold"),
                 bg=COLOR_PRIMARY, fg="white").pack()
        tk.Label(header, text="Arcotangente · Integrales · Series de Taylor / Maclaurin",
                 font=FONT_SMALL, bg=COLOR_PRIMARY, fg="#CECBF6").pack()
 
        canvas_scroll = tk.Canvas(self.root, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)
 
        self.frame_body = tk.Frame(canvas_scroll, bg=COLOR_BG, padx=18, pady=14)
        canvas_scroll.create_window((0, 0), window=self.frame_body, anchor="nw")
        self.frame_body.bind("<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
 
        self._seccion_entrada()
        self._seccion_botones_mat()
        self._seccion_operacion()
        self._seccion_manual()       # ← manual de uso (dinámico)
        self._seccion_opciones_extra()
        self._seccion_calcular()
        self._seccion_resultado()
        self._seccion_historial()
        if MATPLOTLIB_DISPONIBLE:
            self._seccion_grafica()
 
    # ── Sección: entrada f(x) ─────────────────────────────────────────────────
 
    def _seccion_entrada(self):
        card = self._card(self.frame_body)
        tk.Label(card, text="Función  f(x)", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w")
        tk.Label(card, text="Usa notación Python: x**2, sin(x), exp(x), log(x)",
                 font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_MUTED).pack(anchor="w")
 
        self.entrada_fx = tk.Entry(card, font=FONT_MONO, relief="flat",
                                   bg="#F1EFE8", fg=COLOR_TEXT,
                                   insertbackground=COLOR_PRIMARY,
                                   highlightthickness=1,
                                   highlightbackground=COLOR_BORDER,
                                   highlightcolor=COLOR_PRIMARY)
        self.entrada_fx.pack(fill="x", pady=(6, 0), ipady=7)
        self.entrada_fx.insert(0, "x**2 + 1")
 
    # ── Sección: botonera matemática ──────────────────────────────────────────
 
    def _seccion_botones_mat(self):
        card = self._card(self.frame_body)
        tk.Label(card, text="Insertar símbolo", font=("Segoe UI", 9, "bold"),
                 bg=COLOR_CARD, fg=COLOR_MUTED).pack(anchor="w", pady=(0, 6))
 
        grid = tk.Frame(card, bg=COLOR_CARD)
        grid.pack(fill="x")
        for i, (etiqueta, valor) in enumerate(BOTONES_MATEMATICOS):
            btn = tk.Button(grid, text=etiqueta, font=("Segoe UI", 9),
                            bg=COLOR_BG, fg=COLOR_PRIMARY2,
                            activebackground=COLOR_BORDER,
                            relief="flat", padx=8, pady=4, cursor="hand2",
                            command=lambda v=valor: self._insertar(v))
            btn.grid(row=i // 6, column=i % 6, padx=3, pady=3, sticky="ew")
        for c in range(6):
            grid.columnconfigure(c, weight=1)
 
    # ── Sección: selección de operación ──────────────────────────────────────
 
    def _seccion_operacion(self):
        card = self._card(self.frame_body)
        tk.Label(card, text="Operación", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w", pady=(0, 8))
 
        self.operacion = tk.StringVar(value="atan")
        ops = [
            ("atan",          "Arcotangente  tan⁻¹(f(x))"),
            ("resolver_atan", "Resolver  atan(f(x)) = valor  →  despeja x"),
            ("indefinida",    "Integral indefinida  ∫f(x)dx"),
            ("definida",      "Integral definida  ∫ₐᵇ f(x)dx"),
            ("taylor",        "Serie de Taylor  (punto a libre)"),
            ("maclaurin",     "Serie de Maclaurin  (a = 0)"),
        ]
        for valor, texto in ops:
            rb = tk.Radiobutton(card, text=texto, variable=self.operacion,
                                value=valor, font=FONT_LABEL,
                                bg=COLOR_CARD, fg=COLOR_TEXT,
                                activebackground=COLOR_CARD,
                                selectcolor=COLOR_BORDER,
                                command=self._on_operacion_cambia)
            rb.pack(anchor="w", pady=2)
 
    # ── Sección: manual de uso ────────────────────────────────────────────────
 
    def _seccion_manual(self):
        """Tarjeta amarilla con ayuda contextual para la operación seleccionada."""
        self.card_manual = tk.Frame(self.frame_body, bg=COLOR_HINT_BG,
                                    highlightthickness=1,
                                    highlightbackground=COLOR_HINT_BRD,
                                    padx=14, pady=10)
        self.card_manual.pack(fill="x", pady=4)
        self.lbl_manual = tk.Label(self.card_manual, text="",
                                   font=("Courier New", 9),
                                   bg=COLOR_HINT_BG, fg="#5A4A00",
                                   justify="left", anchor="w")
        self.lbl_manual.pack(fill="x")
        self._actualizar_manual()
 
    def _actualizar_manual(self):
        op = self.operacion.get()
        texto = MANUAL.get(op, "")
        self.lbl_manual.config(text=texto)
 
    # ── Sección: opciones extra ────────────────────────────────────────────────
 
    def _seccion_opciones_extra(self):
        self.frame_extra = self._card(self.frame_body)
        self._actualizar_opciones()
 
    def _on_operacion_cambia(self):
        self._actualizar_manual()
        self._actualizar_opciones()
 
    def _actualizar_opciones(self):
        for w in self.frame_extra.winfo_children():
            w.destroy()
 
        op = self.operacion.get()
 
        if op == "resolver_atan":
            tk.Label(self.frame_extra, text="Valor igual a:",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=3,
                                                        sticky="w", pady=(0, 6))
            tk.Label(self.frame_extra, text="atan(f(x)) =", font=FONT_LABEL,
                     bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=0, sticky="w", padx=(0, 6))
            self.valor_atan = tk.Entry(self.frame_extra, width=14, font=FONT_MONO,
                                       relief="flat", bg="#F1EFE8",
                                       highlightthickness=1, highlightbackground=COLOR_BORDER)
            self.valor_atan.insert(0, "pi/4")
            self.valor_atan.grid(row=1, column=1, padx=(0, 8))
            tk.Label(self.frame_extra, text="Ej: pi/4  pi/3  pi/6  0  -pi/4",
                     font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=2, sticky="w")
 
        elif op == "definida":
            tk.Label(self.frame_extra, text="Límites de integración",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=4,
                                                        sticky="w", pady=(0, 6))
            tk.Label(self.frame_extra, text="Desde:", font=FONT_LABEL,
                     bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=0, sticky="w", padx=(0, 4))
            self.limite_inf = tk.Entry(self.frame_extra, width=8, font=FONT_MONO,
                                       relief="flat", bg="#F1EFE8",
                                       highlightthickness=1, highlightbackground=COLOR_BORDER)
            self.limite_inf.insert(0, "0")
            self.limite_inf.grid(row=1, column=1, padx=(0, 12))
            tk.Label(self.frame_extra, text="Hasta:", font=FONT_LABEL,
                     bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=2, sticky="w", padx=(0, 4))
            self.limite_sup = tk.Entry(self.frame_extra, width=8, font=FONT_MONO,
                                       relief="flat", bg="#F1EFE8",
                                       highlightthickness=1, highlightbackground=COLOR_BORDER)
            self.limite_sup.insert(0, "1")
            self.limite_sup.grid(row=1, column=3)
 
        elif op == "taylor":
            tk.Label(self.frame_extra, text="Parámetros de Taylor",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=4,
                                                        sticky="w", pady=(0, 6))
            tk.Label(self.frame_extra, text="Punto a:", font=FONT_LABEL,
                     bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=0, sticky="w", padx=(0, 4))
            self.taylor_punto = tk.Entry(self.frame_extra, width=8, font=FONT_MONO,
                                         relief="flat", bg="#F1EFE8",
                                         highlightthickness=1, highlightbackground=COLOR_BORDER)
            self.taylor_punto.insert(0, "0")
            self.taylor_punto.grid(row=1, column=1, padx=(0, 12))
            tk.Label(self.frame_extra, text="Orden:", font=FONT_LABEL,
                     bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=2, sticky="w", padx=(0, 4))
            self.taylor_orden = tk.Entry(self.frame_extra, width=6, font=FONT_MONO,
                                          relief="flat", bg="#F1EFE8",
                                          highlightthickness=1, highlightbackground=COLOR_BORDER)
            self.taylor_orden.insert(0, "6")
            self.taylor_orden.grid(row=1, column=3)
 
        elif op == "maclaurin":
            tk.Label(self.frame_extra, text="Parámetros de Maclaurin  (a = 0 fijo)",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=4,
                                                        sticky="w", pady=(0, 6))
            tk.Label(self.frame_extra, text="Orden:", font=FONT_LABEL,
                     bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=0, sticky="w", padx=(0, 4))
            self.maclaurin_orden = tk.Entry(self.frame_extra, width=6, font=FONT_MONO,
                                             relief="flat", bg="#F1EFE8",
                                             highlightthickness=1, highlightbackground=COLOR_BORDER)
            self.maclaurin_orden.insert(0, "6")
            self.maclaurin_orden.grid(row=1, column=1, padx=(0, 12))
            tk.Label(self.frame_extra, text="Ej: 4, 6, 8, 10",
                     font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_MUTED).grid(row=1, column=2, sticky="w")
 
        else:
            tk.Label(self.frame_extra, text="Sin parámetros adicionales",
                     font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_MUTED).pack()
 
    # ── Sección: botón calcular ───────────────────────────────────────────────
 
    def _seccion_calcular(self):
        frame = tk.Frame(self.frame_body, bg=COLOR_BG, pady=6)
        frame.pack(fill="x")
        self.btn_calcular = tk.Button(frame, text="  Calcular  →",
                                       font=("Segoe UI", 12, "bold"),
                                       bg=COLOR_PRIMARY, fg="white",
                                       activebackground=COLOR_PRIMARY2,
                                       relief="flat", padx=24, pady=10,
                                       cursor="hand2", command=self._calcular)
        self.btn_calcular.pack(side="right")
        self.btn_limpiar = tk.Button(frame, text="Limpiar",
                                      font=FONT_LABEL,
                                      bg=COLOR_BG, fg=COLOR_MUTED,
                                      activebackground=COLOR_BORDER,
                                      relief="flat", padx=12, pady=10,
                                      cursor="hand2", command=self._limpiar)
        self.btn_limpiar.pack(side="right", padx=(0, 8))
 
    # ── Sección: resultado ────────────────────────────────────────────────────
 
    def _seccion_resultado(self):
        card = self._card(self.frame_body)
 
        enc = tk.Frame(card, bg=COLOR_CARD)
        enc.pack(fill="x", pady=(0, 6))
        tk.Label(enc, text="Resultado", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(side="left")
        self.btn_copiar = tk.Button(enc, text="📋 Copiar",
                                     font=FONT_SMALL,
                                     bg=COLOR_BG, fg=COLOR_PRIMARY2,
                                     activebackground=COLOR_BORDER,
                                     relief="flat", padx=10, pady=3,
                                     cursor="hand2",
                                     command=self._copiar_resultado)
        self.btn_copiar.pack(side="right")
 
        self.texto_resultado = tk.Text(card, font=FONT_MONO, height=6,
                                        relief="flat", bg="#F1EFE8",
                                        fg=COLOR_TEXT, wrap="word",
                                        state="disabled",
                                        highlightthickness=1,
                                        highlightbackground=COLOR_BORDER)
        self.texto_resultado.pack(fill="x")
 
    # ── Sección: historial ────────────────────────────────────────────────────
 
    def _seccion_historial(self):
        self.card_historial = self._card(self.frame_body)
 
        enc = tk.Frame(self.card_historial, bg=COLOR_CARD)
        enc.pack(fill="x", pady=(0, 6))
        tk.Label(enc, text="📋  Historial  (últimos 10)",
                 font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(side="left")
        tk.Button(enc, text="Limpiar", font=FONT_SMALL,
                  bg=COLOR_BG, fg=COLOR_MUTED,
                  activebackground=COLOR_BORDER,
                  relief="flat", padx=8, pady=3,
                  cursor="hand2",
                  command=self._limpiar_historial).pack(side="right")
 
        self.frame_lista_hist = tk.Frame(self.card_historial, bg=COLOR_CARD)
        self.frame_lista_hist.pack(fill="x")
        self._lbl_hist_vacio = tk.Label(self.frame_lista_hist,
                                        text="Aún no hay cálculos.",
                                        font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_MUTED)
        self._lbl_hist_vacio.pack(anchor="w", pady=4)
 
    # ── Sección: gráfica ─────────────────────────────────────────────────────
 
    def _seccion_grafica(self):
        card = self._card(self.frame_body)
        enc = tk.Frame(card, bg=COLOR_CARD)
        enc.pack(fill="x", pady=(0, 6))
        tk.Label(enc, text="Gráfica", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(side="left")
        tk.Button(enc, text="Graficar", font=FONT_SMALL,
                  bg=COLOR_ACCENT, fg="white",
                  activebackground="#0F6E56",
                  relief="flat", padx=10, pady=4,
                  cursor="hand2", command=self._graficar).pack(side="right")
 
        self.fig = Figure(figsize=(5.5, 3), dpi=90, facecolor=COLOR_CARD)
        self.ax  = self.fig.add_subplot(111)
        self.ax.set_facecolor("#F5F4FF")
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=card)
        self.canvas_fig.get_tk_widget().pack(fill="x")
 
    # ── Lógica de cálculo ─────────────────────────────────────────────────────
 
    def _calcular(self):
        expresion = self.entrada_fx.get().strip()
        if not expresion:
            messagebox.showwarning("Campo vacío", "Ingresa una función f(x) primero.")
            return
 
        self.btn_calcular.config(state="disabled", text="Calculando...")
        self.root.update()
 
        def tarea():
            op  = self.operacion.get()
            res = None
 
            if op == "atan":
                res = calcular_atan(expresion)
 
            elif op == "resolver_atan":
                try:
                    valor = self.valor_atan.get().strip()
                    if not valor:
                        res = {"exito": False, "error": "Ingresa el valor al que es igual (ej: pi/4)"}
                    else:
                        res = resolver_atan(expresion, valor)
                except Exception:
                    res = {"exito": False, "error": "Revisa el valor ingresado."}
 
            elif op == "indefinida":
                res = calcular_integral_indefinida(expresion)
 
            elif op == "definida":
                try:
                    a = self.limite_inf.get().strip()
                    b = self.limite_sup.get().strip()
                    res = calcular_integral_definida(expresion, a, b)
                except Exception:
                    res = {"exito": False, "error": "Revisa los límites de integración."}
 
            elif op == "taylor":
                try:
                    punto = self.taylor_punto.get().strip()
                    orden = int(self.taylor_orden.get().strip())
                    res = calcular_serie_taylor(expresion, punto, orden)
                except ValueError:
                    res = {"exito": False, "error": "El orden debe ser un número entero."}
 
            elif op == "maclaurin":
                try:
                    orden = int(self.maclaurin_orden.get().strip())
                    res = calcular_serie_maclaurin(expresion, orden)
                except ValueError:
                    res = {"exito": False, "error": "El orden debe ser un número entero."}
 
            self.root.after(0, lambda: self._mostrar_resultado(res, expresion, op))
 
        threading.Thread(target=tarea, daemon=True).start()
 
    def _mostrar_resultado(self, resultado: dict, expresion: str, op: str):
        self.btn_calcular.config(state="normal", text="  Calcular  →")
        self.texto_resultado.config(state="normal")
        self.texto_resultado.delete("1.0", "end")
 
        if not resultado:
            return
 
        if resultado.get("exito"):
            lineas = []
 
            if op == "atan":
                lineas.append(f"atan({expresion}) =")
                lineas.append(resultado.get("pretty", resultado["texto"]))
 
            elif op == "resolver_atan":
                valor_c = self.valor_atan.get().strip()
                rhs = resultado.get("rhs", "")
                lineas.append(f"atan({expresion}) = {valor_c}")
                if rhs:
                    lineas.append(f"  →  {expresion} = tan({valor_c}) = {rhs}")
                lineas.append("")
                if resultado["soluciones"]:
                    lineas.append("x =  " + resultado.get("pretty", resultado["texto"]))
                    lineas.append(f"x ≈  {resultado['decimal']}")
                else:
                    lineas.append("Sin solución real")
 
            elif op == "indefinida":
                lineas.append(f"∫ {expresion} dx =")
                lineas.append(resultado.get("pretty", resultado["texto"]))
 
            elif op == "definida":
                a = self.limite_inf.get().strip()
                b = self.limite_sup.get().strip()
                lineas.append(f"∫ {expresion} dx  de {a} a {b} =")
                lineas.append(resultado.get("pretty", resultado["texto"]))
                num = resultado.get("valor_numerico")
                if num is not None:
                    lineas.append(f"Valor numérico ≈  {num}")
 
            elif op == "taylor":
                a = self.taylor_punto.get().strip()
                n = self.taylor_orden.get().strip()
                lineas.append(f"Taylor({expresion},  a={a},  orden={n}) =")
                lineas.append(resultado.get("pretty", resultado["texto"]))
 
            elif op == "maclaurin":
                n = self.maclaurin_orden.get().strip()
                lineas.append(f"Maclaurin({expresion},  orden={n}) =")
                lineas.append(resultado.get("pretty", resultado["texto"]))
 
            texto = "\n".join(lineas)
            self._ultimo_texto = texto
            self.texto_resultado.insert("1.0", texto)
            self.texto_resultado.config(fg=COLOR_SUCCESS)
            self._agregar_historial(op, expresion, resultado)
 
        else:
            texto_err = "⚠  " + resultado.get("error", "Error desconocido")
            self._ultimo_texto = texto_err
            self.texto_resultado.insert("1.0", texto_err)
            self.texto_resultado.config(fg=COLOR_ERROR)
 
        self.texto_resultado.config(state="disabled")
 
    # ── Copiar ────────────────────────────────────────────────────────────────
 
    def _copiar_resultado(self):
        if not self._ultimo_texto:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self._ultimo_texto)
        self.btn_copiar.config(text="✓ Copiado!", fg=COLOR_ACCENT)
        self.root.after(1500, lambda: self.btn_copiar.config(text="📋 Copiar", fg=COLOR_PRIMARY2))
 
    # ── Historial ─────────────────────────────────────────────────────────────
 
    def _agregar_historial(self, op: str, expresion: str, resultado: dict):
        etiquetas = {
            "atan": "atan", "resolver_atan": "Resolver atan",
            "indefinida": "∫ indef.", "definida": "∫ def.",
            "taylor": "Taylor", "maclaurin": "Maclaurin",
        }
        resumen_map = {
            "atan":          lambda: f"atan({expresion}) = {resultado.get('texto','')}",
            "resolver_atan": lambda: f"atan({expresion}) = ... → x = {resultado.get('texto','')}",
            "indefinida":    lambda: f"∫({expresion})dx = {resultado.get('texto','')}",
            "definida":      lambda: f"∫({expresion})dx ≈ {resultado.get('valor_numerico', resultado.get('texto',''))}",
            "taylor":        lambda: f"Taylor({expresion}, a={resultado.get('punto','')}, n={resultado.get('orden','')})",
            "maclaurin":     lambda: f"Maclaurin({expresion}, n={resultado.get('orden','')}) = {resultado.get('texto','')[:50]}",
        }
        entrada = {
            "etiqueta": etiquetas.get(op, op),
            "resumen":  resumen_map.get(op, lambda: expresion)(),
        }
        self._historial.insert(0, entrada)
        self._historial = self._historial[:MAX_HISTORIAL]
        self._refrescar_historial()
 
    def _refrescar_historial(self):
        for w in self.frame_lista_hist.winfo_children():
            w.destroy()
        if not self._historial:
            tk.Label(self.frame_lista_hist, text="Aún no hay cálculos.",
                     font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_MUTED).pack(anchor="w", pady=4)
            return
        for entrada in self._historial:
            fila = tk.Frame(self.frame_lista_hist, bg=COLOR_HIST_BG,
                            highlightthickness=1, highlightbackground=COLOR_BORDER)
            fila.pack(fill="x", pady=2, padx=2)
            tk.Label(fila, text=f" {entrada['etiqueta']} ",
                     font=("Segoe UI", 8, "bold"),
                     bg=COLOR_HIST_HDR, fg="white",
                     padx=6, pady=2).pack(side="left")
            texto = entrada["resumen"]
            if len(texto) > 72:
                texto = texto[:69] + "..."
            tk.Label(fila, text=texto,
                     font=("Courier New", 9),
                     bg=COLOR_HIST_BG, fg=COLOR_TEXT,
                     anchor="w", padx=8, pady=4).pack(side="left", fill="x", expand=True)
 
    def _limpiar_historial(self):
        self._historial = []
        self._refrescar_historial()
 
    # ── Lógica de gráfica ─────────────────────────────────────────────────────
 
    def _graficar(self):
        if not MATPLOTLIB_DISPONIBLE:
            return
        expresion = self.entrada_fx.get().strip()
        if not expresion:
            messagebox.showwarning("Campo vacío", "Ingresa una función f(x) primero.")
            return
        self.ax.clear()
        self.ax.set_facecolor("#F5F4FF")
        op = self.operacion.get()
        try:
            if op == "definida":
                a = float(self.limite_inf.get())
                b = float(self.limite_sup.get())
                graf.graficar_integral(expresion, self.ax, a, b)
            elif op == "taylor":
                punto = float(self.taylor_punto.get())
                orden = int(self.taylor_orden.get())
                graf.graficar_taylor(expresion, self.ax, punto, orden)
            elif op == "maclaurin":
                orden_mac = int(self.maclaurin_orden.get())
                graf.graficar_taylor(expresion, self.ax, 0, orden_mac,
                                     etiqueta=f"Maclaurin orden {orden_mac}")
            else:
                graf.graficar_funcion(expresion, self.ax)
            self.fig.tight_layout()
            self.canvas_fig.draw()
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))
 
    # ── Helpers ───────────────────────────────────────────────────────────────
 
    def _insertar(self, texto: str):
        if texto == "__BORRAR__":
            pos = self.entrada_fx.index(tk.INSERT)
            if pos > 0:
                self.entrada_fx.delete(pos - 1, pos)
            self.entrada_fx.focus()
            return
        pos = self.entrada_fx.index(tk.INSERT)
        if texto == "()":
            self.entrada_fx.insert(pos, "()")
            self.entrada_fx.icursor(int(pos) + 1)
        elif texto == "root(,)":
            self.entrada_fx.insert(pos, "root(, )")
            self.entrada_fx.icursor(int(pos) + 5)
        else:
            self.entrada_fx.insert(pos, texto)
        self.entrada_fx.focus()
 
    def _limpiar(self):
        self.entrada_fx.delete(0, "end")
        self.texto_resultado.config(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.config(state="disabled")
        self._ultimo_texto = ""
        if MATPLOTLIB_DISPONIBLE:
            self.ax.clear()
            self.ax.set_facecolor("#F5F4FF")
            self.canvas_fig.draw()
 
    def _card(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=COLOR_CARD,
                         highlightthickness=1,
                         highlightbackground=COLOR_BORDER,
                         padx=14, pady=12)
        frame.pack(fill="x", pady=6)
        return frame
 
    def _centrar_ventana(self, ancho: int, alto: int):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - ancho) // 2
        y  = (sh - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
 
 
def iniciar_ui():
    root = tk.Tk()
    app  = CalculadoraApp(root)
    root.mainloop()