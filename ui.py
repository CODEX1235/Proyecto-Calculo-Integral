import tkinter as tk
from tkinter import ttk, messagebox
import threading
 
from atan import calcular_atan
from integrales import calcular_integral_indefinida, calcular_integral_definida
from taylor import calcular_serie_taylor, calcular_taylor_integral
 
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
FONT_TITLE     = ("Segoe UI", 14, "bold")
FONT_LABEL     = ("Segoe UI", 10)
FONT_MONO      = ("Courier New", 11)
FONT_RESULT    = ("Segoe UI", 12)
FONT_SMALL     = ("Segoe UI", 9)
 
# ─── Botones matemáticos ──────────────────────────────────────────────────────
BOTONES_MATEMATICOS = [
    ("sin(", "sin("),  ("cos(", "cos("),  ("tan(", "tan("),
    ("atan(", "atan("),("exp(", "exp("),  ("log(", "log("),
    ("sqrt(", "sqrt("),("pi", "pi"),      ("x²", "x**2"),
    ("x³", "x**3"),   ("**", "**"),       ("( )", "()"),
    ("ⁿ√x", "root(,)"),
]
 
 
class CalculadoraApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora Matemática")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(True, True)
        self.root.minsize(560, 600)
 
        self._construir_ui()
        self._centrar_ventana(600, 750)
 
    # ── Layout principal ──────────────────────────────────────────────────────
 
    def _construir_ui(self):
        # Título
        header = tk.Frame(self.root, bg=COLOR_PRIMARY, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🧮  Calculadora Matemática",
                 font=("Segoe UI", 16, "bold"),
                 bg=COLOR_PRIMARY, fg="white").pack()
        tk.Label(header, text="Arcotangente · Integrales · Series de Taylor",
                 font=FONT_SMALL, bg=COLOR_PRIMARY, fg="#CECBF6").pack()
 
        # Cuerpo con scroll
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
        self._seccion_opciones_extra()
        self._seccion_calcular()
        self._seccion_resultado()
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
                            relief="flat", padx=8, pady=4,
                            cursor="hand2",
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
            ("atan", "Arcotangente  tan⁻¹(f(x))"),
            ("indefinida", "Integral indefinida  ∫f(x)dx"),
            ("definida", "Integral definida  ∫ₐᵇ f(x)dx"),
            ("taylor", "Serie de Taylor"),
            ("taylor_integral", "Taylor + Integral  ∫T(x)dx"),
        ]
        for valor, texto in ops:
            rb = tk.Radiobutton(card, text=texto, variable=self.operacion,
                                value=valor, font=FONT_LABEL,
                                bg=COLOR_CARD, fg=COLOR_TEXT,
                                activebackground=COLOR_CARD,
                                selectcolor=COLOR_BORDER,
                                command=self._actualizar_opciones)
            rb.pack(anchor="w", pady=2)
 
    # ── Sección: opciones extra (límites / Taylor) ────────────────────────────
 
    def _seccion_opciones_extra(self):
        self.frame_extra = self._card(self.frame_body)
        self._actualizar_opciones()
 
    def _actualizar_opciones(self):
        for w in self.frame_extra.winfo_children():
            w.destroy()
 
        op = self.operacion.get()
 
        if op == "definida":
            tk.Label(self.frame_extra, text="Límites de integración",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))
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
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))
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
        elif op == "taylor_integral":
            tk.Label(self.frame_extra, text="Parámetros de Taylor + Integral",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))
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
                                       cursor="hand2",
                                       command=self._calcular)
        self.btn_calcular.pack(side="right")
        self.btn_limpiar = tk.Button(frame, text="Limpiar",
                                      font=FONT_LABEL,
                                      bg=COLOR_BG, fg=COLOR_MUTED,
                                      activebackground=COLOR_BORDER,
                                      relief="flat", padx=12, pady=10,
                                      cursor="hand2",
                                      command=self._limpiar)
        self.btn_limpiar.pack(side="right", padx=(0, 8))
 
    # ── Sección: resultado ────────────────────────────────────────────────────
 
    def _seccion_resultado(self):
        card = self._card(self.frame_body)
        tk.Label(card, text="Resultado", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w", pady=(0, 6))
 
        self.texto_resultado = tk.Text(card, font=FONT_MONO, height=5,
                                        relief="flat", bg="#F1EFE8",
                                        fg=COLOR_TEXT, wrap="word",
                                        state="disabled",
                                        highlightthickness=1,
                                        highlightbackground=COLOR_BORDER)
        self.texto_resultado.pack(fill="x")
 
    # ── Sección: gráfica ─────────────────────────────────────────────────────
 
    def _seccion_grafica(self):
        card = self._card(self.frame_body)
        encabezado = tk.Frame(card, bg=COLOR_CARD)
        encabezado.pack(fill="x", pady=(0, 6))
        tk.Label(encabezado, text="Gráfica", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT).pack(side="left")
        tk.Button(encabezado, text="Graficar", font=FONT_SMALL,
                  bg=COLOR_ACCENT, fg="white",
                  activebackground="#0F6E56",
                  relief="flat", padx=10, pady=4,
                  cursor="hand2",
                  command=self._graficar).pack(side="right")
 
        self.fig = Figure(figsize=(5.5, 3), dpi=90, facecolor=COLOR_CARD)
        self.ax = self.fig.add_subplot(111)
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
            op = self.operacion.get()
            resultado = None
 
            if op == "atan":
                resultado = calcular_atan(expresion)
            elif op == "indefinida":
                resultado = calcular_integral_indefinida(expresion)
            elif op == "definida":
                try:
                    a = self.limite_inf.get().strip()
                    b = self.limite_sup.get().strip()
                    resultado = calcular_integral_definida(expresion, a, b)
                except Exception:
                    resultado = {"exito": False, "error": "Revisa los límites de integración."}
            elif op == "taylor":
                try:
                    punto = float(self.taylor_punto.get().strip())
                    orden = int(self.taylor_orden.get().strip())
                    resultado = calcular_serie_taylor(expresion, punto, orden)
                except ValueError:
                    resultado = {"exito": False, "error": "El punto y el orden deben ser números."}
            elif op == "taylor_integral":
                try:
                    punto = float(self.taylor_punto.get().strip())
                    orden = int(self.taylor_orden.get().strip())
                    resultado = calcular_taylor_integral(expresion, punto, orden)
                except ValueError:
                    resultado = {"exito": False, "error": "El punto y el orden deben ser números."}
 
            self.root.after(0, lambda: self._mostrar_resultado(resultado))
 
        threading.Thread(target=tarea, daemon=True).start()
 
    def _mostrar_resultado(self, resultado: dict):
        self.btn_calcular.config(state="normal", text="  Calcular  →")
        self.texto_resultado.config(state="normal")
        self.texto_resultado.delete("1.0", "end")
 
        if not resultado:
            return
 
        if resultado.get("exito"):
            op = self.operacion.get()
            lineas = []
 
            if op == "atan":
                lineas.append(f"atan(f(x)) = {resultado['texto']}")
            elif op == "indefinida":
                lineas.append(f"∫f(x)dx = {resultado['texto']}")
            elif op == "definida":
                lineas.append(f"∫f(x)dx = {resultado['texto']}")
                if resultado.get("valor_numerico") is not None:
                    lineas.append(f"Valor numérico ≈ {resultado['valor_numerico']}")
            elif op == "taylor":
                lineas.append(f"Serie de Taylor (orden {resultado['orden']}, a={resultado['punto']}):")
                lineas.append(resultado["texto"])
                if resultado.get("terminos"):
                    lineas.append("")
                    lineas.append("Términos: " + "  +  ".join(resultado["terminos"][:6]))
            elif op == "taylor_integral":
                lineas.append(f"Taylor orden {resultado['orden']} en a={resultado['punto']}:")
                lineas.append(f"  T(x) = {resultado['taylor_texto']}")
                lineas.append("")
                lineas.append(f"∫T(x)dx = {resultado['integral_texto']}")
 
            texto = "\n".join(lineas)
            self.texto_resultado.insert("1.0", texto)
            self.texto_resultado.config(fg=COLOR_SUCCESS)
        else:
            self.texto_resultado.insert("1.0", "⚠  " + resultado.get("error", "Error desconocido"))
            self.texto_resultado.config(fg=COLOR_ERROR)
 
        self.texto_resultado.config(state="disabled")
 
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
            else:
                graf.graficar_funcion(expresion, self.ax)
 
            self.fig.tight_layout()
            self.canvas_fig.draw()
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))
 
    # ── Helpers ───────────────────────────────────────────────────────────────
 
    def _insertar(self, texto: str):
        pos = self.entrada_fx.index(tk.INSERT)
        if texto == "()":
            self.entrada_fx.insert(pos, "()")
            self.entrada_fx.icursor(int(pos) + 1)
        elif texto == "root(,)":
            self.entrada_fx.insert(pos, "root(, )")
            # Posicionar cursor después de root( para escribir la expresión
            self.entrada_fx.icursor(int(pos) + 5)
        else:
            self.entrada_fx.insert(pos, texto)
        self.entrada_fx.focus()
 
    def _limpiar(self):
        self.entrada_fx.delete(0, "end")
        self.texto_resultado.config(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.config(state="disabled")
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
        x = (sw - ancho) // 2
        y = (sh - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
 
 
def iniciar_ui():
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()