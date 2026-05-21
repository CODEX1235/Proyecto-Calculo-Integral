🧮 Calculadora Matemática
Una herramienta de cálculo simbólico con interfaz gráfica desarrollada en Python. Permite al usuario ingresar funciones matemáticas y aplicarles operaciones como arcotangente, integrales y series de Taylor, con resultados visuales claros y opcionalmente gráficas.

📌 Descripción
Este proyecto es una calculadora matemática avanzada que combina una interfaz gráfica intuitiva con un motor de cálculo simbólico. A diferencia de una calculadora numérica común, este sistema trabaja con expresiones matemáticas reales: puede resolver integrales, generar series de Taylor y calcular funciones trigonométricas inversas de forma simbólica.
El usuario escribe una función como x**2 + 1, selecciona la operación deseada y el sistema procesa y muestra el resultado, ya sea como expresión matemática o como gráfica.

🛠️ Tecnologías utilizadas
Tecnología Rol :  Instalación PythonLenguaje principalpython.orgSymPyMotor 

matemático : (integrales, Taylor, atan, derivadas) ´pip install´ sympyTkinterInterfaz gráfica (ventanas, botones, inputs) Incluido con PythonMatplotlibGráficas de funciones (opcional) 
pip install matplotlib.

📁 Estructura del proyecto
CalculadoraMatematica/
│
├── main.py           # Punto de entrada. Inicia la aplicación.
├── ui.py             # Interfaz gráfica: ventanas, botones, menús, estilos.
├── atan.py           # Módulo para calcular arcotangente: tan⁻¹(f(x))
├── integrales.py     # Módulo para integrales definidas e indefinidas.
├── taylor.py         # Módulo para series de Taylor.
├── graficas.py       # Visualización de funciones con Matplotlib.
│
├── assets/
│   └── iconos/       # Íconos y recursos visuales.
│
└── requirements.txt  # Dependencias del proyecto.

⚙️ Instalación

Clona el repositorio:

bash   git clone https://github.com/tu-usuario/calculadora-matematica.git
   cd calculadora-matematica

Instala las dependencias:

bash   pip install -r requirements.txt

Ejecuta la aplicación:

bash   python main.py

🚀 Funcionalidades

Arcotangente — Calcula tan⁻¹(f(x)) de cualquier función ingresada.
Integrales — Resuelve integrales indefinidas y áreas bajo la curva.
Series de Taylor — Genera la expansión en serie de Taylor alrededor de un punto.
Gráficas (opcional) — Visualiza funciones, áreas y aproximaciones de Taylor.
Botones matemáticos — Atajos para insertar sin, cos, atan, π, x², entre otros.
Validación de errores — Detecta expresiones inválidas y muestra mensajes claros.


🧠 ¿Cómo funciona?
Usuario escribe f(x)
        ↓
    UI (Tkinter) recibe el texto
        ↓
    SymPy convierte con sympify()   ← parte más crítica
        ↓
    Módulo matemático opera (atan / integral / Taylor)
        ↓
    UI muestra resultado + gráfica (opcional)
La clave del sistema es sympify(), la función de SymPy que convierte texto plano en una expresión matemática real que el motor puede procesar.

📦 Dependencias (requirements.txt)
sympy
matplotlib
numpy

👨‍💻 Autores
Desarrollado como proyecto universitario.

📄 Licencia
Este proyecto es de uso académico.
