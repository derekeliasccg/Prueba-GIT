# DOCUMENTACIÓN COMPLETA - JUEGO UNO
## Guía Técnica y Conceptual del Programa

---

## TABLA DE CONTENIDOS

1. [Visión General](#visión-general)
2. [Conceptos de POO Utilizados](#conceptos-de-poo-utilizados)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Módulos y Archivos](#módulos-y-archivos)
5. [Clases Detalladas](#clases-detalladas)
6. [Enumeraciones](#enumeraciones)
7. [Funciones y Métodos](#funciones-y-métodos)
8. [Flujo de Ejecución](#flujo-de-ejecución)
9. [Patrones de Diseño](#patrones-de-diseño)
10. [Manejo de Excepciones](#manejo-de-excepciones)
11. [Almacenamiento de Datos](#almacenamiento-de-datos)
12. [Cómo Expandir el Código](#cómo-expandir-el-código)

---

## VISIÓN GENERAL

**Proyecto:** Juego de Cartas UNO (Interactivo)

**Objetivo:** Implementar un juego funcional de UNO con:
- Jugador humano vs Máquina (IA)
- Reglas completas del juego
- Sistema de guardado/carga de partidas
- Interfaz de línea de comandos (CLI)

**Tipo de Proyecto:** Aplicación de escritorio orientada a objetos

**Lenguaje:** Python 3.8+

**Contexto Académico:** Proyecto de estudiantes de 2do semestre de Maestría POO

---

## CONCEPTOS DE POO UTILIZADOS

### 1. **Herencia (Inheritance)**

```python
# Ejemplo: CartaNumerica hereda de Carta
class Carta(ABC):           # Clase Padre (Abstracta)
    def es_compatible(self, otra_carta):
        pass

class CartaNumerica(Carta):  # Clase Hija
    def es_compatible(self, otra_carta):
        # Implementación específica
        pass
```

**Propósito:** Reutilizar código de la clase padre y permitir que cada subclase implemente su propia lógica.

**Ejemplo en el proyecto:**
- `Carta` → Clase abstracta base
- `CartaNumerica` → Cartas con número (0-9)
- `CartaEspecial` → Cartas especiales (Reverse, +2, etc.)

---

### 2. **Abstracción (Abstraction)**

```python
from abc import ABC, abstractmethod

class Carta(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass  # Obliga a las subclases a implementar este método
```

**Propósito:** Definir una interfaz común sin detalles de implementación.

**Ventaja:** Garantiza que toda carta implementa `__str__()`.

---

### 3. **Encapsulación (Encapsulation)**

```python
class Jugador:
    def __init__(self, nombre: str, baraja: Baraja):
        self.nombre = nombre        # Atributo público
        self.mano: List[Carta] = [] # Atributo privado (por convención)
    
    # Acceso controlado mediante métodos
    def jugar_carta(self, indice: int) -> Carta:
        if not 0 <= indice < len(self.mano):
            raise IndexError(...)
        return self.mano.pop(indice)  # Control de acceso
```

**Propósito:** Proteger datos internos y controlar cómo se modifican.

---

### 4. **Polimorfismo (Polymorphism)**

```python
# La misma interfaz, diferentes comportamientos
class CartaNumerica(Carta):
    def es_compatible(self, otra_carta: Carta) -> bool:
        if super().es_compatible(otra_carta):
            return True
        if isinstance(otra_carta, CartaNumerica):
            return self.numero == otra_carta.numero  # Lógica diferente
        return False

class CartaEspecial(Carta):
    def es_compatible(self, otra_carta: Carta) -> bool:
        if self.tipo == otra_carta.tipo:
            return True  # Lógica diferente
        return super().es_compatible(otra_carta)
```

**Propósito:** Diferentes tipos de cartas responden diferente al mismo método.

---

### 5. **Composición (Composition)**

```python
class JuegoUno:
    def __init__(self):
        self.baraja = Baraja()          # JuegoUno TIENE una Baraja
        self.humano = Jugador(...)      # JuegoUno TIENE un Jugador
        self.maquina = Jugador(...)     # JuegoUno TIENE otro Jugador
```

**Propósito:** Construir objetos complejos a partir de objetos más simples.

---

### 6. **Type Hints (Anotaciones de Tipo)**

```python
def jugar_carta(self, indice: int) -> Carta:
    # int = tipo de entrada esperado
    # Carta = tipo de salida esperado
    pass
```

**Propósito:** Documentar y verificar tipos en tiempo de desarrollo.

---

## ESTRUCTURA DEL PROYECTO

```
NUEVO PROYECTO UNO PY/
│
├── config.py              # Configuración centralizada
├── exceptions.py          # Excepciones personalizadas
├── models.py              # Enumeraciones (Color, TipoCarta)
├── cartas.py              # Clases de cartas (Carta, CartaNumerica, CartaEspecial)
├── baraja.py              # Gestión de mazo (Baraja)
├── jugador.py             # Jugadores (Jugador)
├── juego.py               # Lógica principal (JuegoUno)
├── main.py                # Punto de entrada (menú principal)
│
└── proyectouno_mejorado.py  # Versión anterior (archivo único)
```

### **Flujo de Imports**

```
main.py
    ├── juego.py
    │   ├── models.py
    │   ├── cartas.py
    │   │   └── models.py
    │   ├── baraja.py
    │   │   ├── models.py
    │   │   └── cartas.py
    │   └── jugador.py
    │       ├── models.py
    │       ├── cartas.py
    │       └── baraja.py
    └── (utilities)
```

---

## MÓDULOS Y ARCHIVOS

### **1. config.py - Configuración Centralizada**

```python
@dataclass
class UnoConfig:
    NUMEROS_POR_COLOR: Tuple[int, ...] = tuple(range(10))
    CARTAS_ESPECIALES_POR_TIPO: int = 2
    CARTAS_COMODIN_MAS2: int = 4
    CARTAS_COMODIN_MAS4: int = 4
    CARTAS_COMODIN_CAMBIOCOLOR: int = 4
    CARTAS_INICIALES_JUGADOR: int = 7
    CARTAS_ROBAR_MAS2: int = 2
    CARTAS_ROBAR_MAS4: int = 4
    EXTENSION_GUARDADO: str = ".pkl"
    RUTA_GUARDADOS: str = "./"
```

**Propósito:** Centralizar constantes para fácil mantenimiento.

**Concepto:** Usa `@dataclass` (Python 3.7+) para crear clases simples con atributos.

**Ventajas:**
- Cambiar valores en un único lugar
- Fácil de expandir con nuevas configuraciones
- Separación de la lógica

---

### **2. exceptions.py - Excepciones Personalizadas**

```python
class UnoException(Exception):
    """Excepción base"""
    pass

class CartaIncompatibleError(UnoException):
    """Se intenta jugar una carta no compatible"""
    pass

class JugadaInvalidaError(UnoException):
    """Índice de carta fuera de rango"""
    pass
```

**Propósito:** Manejar errores específicos del juego.

**Ventajas:**
- `try/except` más específicos
- Código más limpio
- Debugging más fácil

---

### **3. models.py - Enumeraciones**

#### **TipoCarta (Enum)**

```python
class TipoCarta(Enum):
    NUMERO = (False, "")
    REVERSE = (True, "^")
    BLOQUEO = (True, "&")
    MAS2 = (True, "+2")
    MAS4 = (True, "+4")
    CAMBIOCOLOR = (True, "%")

    @property
    def es_comodin(self) -> bool:
        return self._es_comodin
```

**Propósito:** Definir tipos de cartas como constantes.

**Atributos de cada tipo:**
- `es_comodin`: Si afecta a otros jugadores
- `simbolo`: Representación visual

**Valores:**
| Tipo | Comodín | Símbolo |
|------|---------|---------|
| NUMERO | No | (vacío) |
| REVERSE | Sí | ^ |
| BLOQUEO | Sí | & |
| MAS2 | Sí | +2 |
| MAS4 | Sí | +4 |
| CAMBIOCOLOR | Sí | % |

#### **Color (Enum)**

```python
class Color(Enum):
    ROJO = "R"
    AMARILLO = "A"
    VERDE = "V"
    AZUL = "Z"
    NEGRO = "N"
    NINGUNO = ""
```

**Propósito:** Definir colores disponibles.

**Nota:** NEGRO es para comodines que pueden cambiar color.

---

### **4. cartas.py - Jerarquía de Cartas**

#### **Clase Abstracta: Carta**

```python
from abc import ABC, abstractmethod

class Carta(ABC):
    def __init__(self, color: Color, tipo: TipoCarta):
        self.color = color
        self.tipo = tipo
    
    @abstractmethod
    def __str__(self) -> str:
        pass
```

**Responsabilidades:**
- Almacenar color y tipo
- Validar compatibilidad básica
- Proporcionar interfaz común

**Métodos:**
| Método | Retorno | Propósito |
|--------|---------|-----------|
| `es_compatible(otra)` | bool | ¿Se puede jugar sobre otra? |
| `set_color(color)` | None | Cambiar color (comodín) |
| `get_tipo()` | TipoCarta | Obtener tipo |
| `__str__()` | str | Representación visual |

#### **CartaNumerica (Subclase)**

```python
class CartaNumerica(Carta):
    def __init__(self, color: Color, numero: int):
        if not 0 <= numero <= 9:
            raise ValueError(...)
        super().__init__(color, TipoCarta.NUMERO)
        self.numero = numero
```

**Características:**
- Tiene un número (0-9)
- Compatible si: mismo color O mismo número
- Ejemplo: `CartaNumerica(Color.ROJO, 5)` → "R 5"

**Validación:** El constructor verifica que el número esté entre 0 y 9.

#### **CartaEspecial (Subclase)**

```python
class CartaEspecial(Carta):
    def __init__(self, color: Color, tipo: TipoCarta):
        if tipo == TipoCarta.NUMERO:
            raise ValueError("Use CartaNumerica...")
        super().__init__(color, tipo)
```

**Características:**
- Tipo especial (REVERSE, BLOQUEO, etc.)
- Compatible si: mismo tipo O mismo color O es negra
- Ejemplo: `CartaEspecial(Color.ROJO, TipoCarta.REVERSE)` → "^ R"

**Validación:** Rechaza tipos numéricos.

---

### **5. baraja.py - Gestión del Mazo**

```python
class Baraja:
    def __init__(self):
        self.cartas: List[Carta] = []
        self.descarte: List[Carta] = []
        self._inicializar()
```

**Responsabilidades:**
- Crear todas las cartas del juego
- Gestionar robo y descarte
- Reciclar cartas cuando se agota el mazo

**Composición de la baraja:**
- 40 cartas numéricas (10 números × 4 colores)
- 24 cartas especiales (Reverse, Bloqueo, +2 por color)
- 8 cartas comodín negras

**Total:** 72 cartas

**Métodos:**

| Método | Propósito | Retorno |
|--------|-----------|---------|
| `robar_carta()` | Obtiene una carta | Optional[Carta] |
| `descartar(carta)` | Guarda descartada | None |
| `_reciclar_descarte()` | Reaprovecha cartas descartadas | None |
| `contar_cartas()` | Total de cartas disponibles | int |

**Flujo de Robo:**
1. Si hay cartas, retorna la primera
2. Si no hay, recicla el descarte
3. Si aun así no hay, retorna None

---

### **6. jugador.py - Modelo del Jugador**

```python
class Jugador:
    def __init__(self, nombre: str, baraja: Baraja):
        self.nombre = nombre
        self.mano: List[Carta] = []
        
        for _ in range(7):  # Roba 7 cartas iniciales
            carta = baraja.robar_carta()
            if carta:
                self.mano.append(carta)
```

**Atributos:**
- `nombre`: Nombre del jugador
- `mano`: Lista de cartas en su poder

**Propiedades (Properties):**
- `nombre_jugador`: Retorna el nombre
- `mano_actual`: Copia de la mano (seguridad)
- `cantidad_cartas`: Número de cartas

**Métodos:**

| Método | Propósito |
|--------|-----------|
| `agregar_carta(carta)` | Añade una carta a la mano |
| `jugar_carta(indice)` | Extrae y retorna una carta |
| `tiene_jugada_posible(carta)` | ¿Puede jugar sobre esa carta? |
| `obtener_indice_carta_compatible(carta)` | Encuentra primera carta compatible |
| `mostrar_mano()` | Imprime mano del jugador |

---

### **7. juego.py - Lógica Principal**

```python
class JuegoUno:
    def __init__(self):
        self.baraja = Baraja()
        self.humano = Jugador("Jugador", self.baraja)
        self.maquina = Jugador("Máquina", self.baraja)
        self.carta_en_mesa: Optional[Carta] = None
        self.saltar_turno = False
        
        self._inicializar_carta_mesa()
```

**Composición:**
- Posee una Baraja
- Posee dos Jugadores (humano y máquina)

**Atributos:**
- `carta_en_mesa`: La carta actualmente jugada
- `saltar_turno`: Flag para turnos saltados

#### **Métodos Principales:**

**`_inicializar_carta_mesa()`**
- Roba cartas hasta obtener una NO comodín
- Coloca esa carta en la mesa

**`procesar_turno(actual, oponente)`**
- Maneja un turno completo
- Valida cartas
- Aplica efectos
- Retorna: bool (continúa juego?)

**Flujo dentro:**
1. Mostrar estado
2. Verificar si hay jugadas posibles
3. Si no: robar carta y pasar
4. Si sí: obtener entrada del jugador
5. Validar compatibilidad
6. Si es comodín: pedir color
7. Descartar anterior y poner nueva
8. Aplicar efectos (robo, saltos)

**`_aplicar_efectos(carta, oponente)`**
- Si MAS2: oponente roba 2 cartas
- Si MAS4: oponente roba 4 cartas
- Si REVERSE/BLOQUEO/MAS*/MAS4: saltar turno siguiente

**`guardar_partida(nombre)`**
- Serializa todo el objeto JuegoUno
- Usa pickle (binary protocol de Python)
- Permite continuar luego

**`cargar_partida(nombre)`** (estático)
- Deserializa archivo .pkl
- Retorna objeto JuegoUno

**`iniciar()`**
- Loop principal del juego
- Alterna turnos humano/máquina
- Verifica ganador
- Respeta saltos de turno

---

### **8. main.py - Punto de Entrada**

```python
def menu_principal() -> None:
    # Menú de inicio
    # Opciones: Nueva/Cargar/Salir
    pass

def listar_partidas_guardadas() -> List[str]:
    return glob.glob("*.pkl")
```

**Responsabilidades:**
- Mostrar menú
- Crear o cargar juego
- Iniciar sesión de juego

**Flujo:**
1. Mostrar opciones
2. Pedir entrada
3. Según opción:
   - **1:** Crear nuevo JuegoUno()
   - **2:** Listar archivos .pkl y cargar seleccionado
   - **3:** Salir

---

## CLASES DETALLADAS

### **Relación de Clases (Diagrama UML)**

```
                  ┌─────────────┐
                  │    Carta    │ (ABC)
                  └──────┬──────┘
                    ┌────┴──────┐
                    │           │
        ┌───────────▼──┐   ┌────▼──────────┐
        │CartaNumerica │   │CartaEspecial  │
        └──────────────┘   └───────────────┘

        ┌──────────┐      ┌────────┐      ┌────────────┐
        │ Jugador  │      │ Baraja │      │ JuegoUno   │
        └──────────┘      └────────┘      └────────────┘
              ▲                ▲                  ▲
              │                │                  │
        Composición      Composición         Composición
              │                │                  │
        ┌─────┴──────┬─────────┴──────────┬──────┘
        │            │                    │
    [Humano]   [Máquina]            [Baraja, Jugadores]
```

---

## ENUMERACIONES

### **TipoCarta**

Controla qué tipo de carta es y si tiene efecto especial.

```python
NUMERO = (False, "")       # Sin efecto, símbolo vacío
REVERSE = (True, "^")      # Invierte orden, símbolo ^
BLOQUEO = (True, "&")      # Salta turno, símbolo &
MAS2 = (True, "+2")        # Roba 2 y salta, símbolo +2
MAS4 = (True, "+4")        # Roba 4, cambia color, símbolo +4
CAMBIOCOLOR = (True, "%")  # Solo cambia color, símbolo %
```

### **Color**

Identifica el color de la carta.

```python
ROJO = "R"
AMARILLO = "A"
VERDE = "V"
AZUL = "Z"
NEGRO = "N"      # Solo para comodines
NINGUNO = ""
```

---

## FUNCIONES Y MÉTODOS

### **Por Categoría**

#### **Validación**

| Método | Clase | Verifica |
|--------|-------|----------|
| `es_compatible()` | Carta | Si carta es playable |
| `tiene_jugada_posible()` | Jugador | Si jugador puede jugar |
| `obtener_indice_carta_compatible()` | Jugador | Índice de playable |

#### **Gestión de Cartas**

| Método | Clase | Acción |
|--------|-------|--------|
| `agregar_carta()` | Jugador | Añade a mano |
| `jugar_carta()` | Jugador | Extrae de mano |
| `robar_carta()` | Baraja | Obtiene del mazo |
| `descartar()` | Baraja | Guarda en descarte |

#### **Lógica de Juego**

| Método | Clase | Propósito |
|--------|-------|-----------|
| `procesar_turno()` | JuegoUno | Un turno completo |
| `_aplicar_efectos()` | JuegoUno | Efectos especiales |
| `_obtener_jugada_ia()` | JuegoUno | Turno máquina |
| `_pedir_entrada_jugador()` | JuegoUno | Turno humano |
| `verificar_ganador()` | JuegoUno | ¿Alguien ganó? |

#### **Persistencia**

| Método | Tipo | Función |
|--------|------|---------|
| `guardar_partida()` | instancia | Guarda archivo .pkl |
| `cargar_partida()` | estático | Carga archivo .pkl |
| `listar_partidas_guardadas()` | función | Lista .pkl en carpeta |

---

## FLUJO DE EJECUCIÓN

### **Secuencia de Inicio**

```
python main.py
    │
    ├── menu_principal()
    │
    ├─┬─ Si opción "1":
    │ └─ JuegoUno() → __init__()
    │     ├── Baraja() → _inicializar()
    │     │   └── Crea 72 cartas
    │     ├── Jugador("Jugador", baraja)
    │     │   └── Roba 7 cartas
    │     ├── Jugador("Máquina", baraja)
    │     │   └── Roba 7 cartas
    │     └── _inicializar_carta_mesa()
    │         └── Busca carta no-comodín para mesa
    │
    ├─┬─ Si opción "2":
    │ └── listar_partidas_guardadas()
    │     └── cargar_partida(archivo)
    │         └── pickle.load(archivo)
    │
    └── juego.iniciar()
        └── Loop principal del juego
```

### **Secuencia de Turno**

```
Turno Jugador:
    ├── procesar_turno(humano, maquina)
    │   ├── Mostrar carta en mesa
    │   ├── Mostrar mano del jugador
    │   ├── Verificar si puede jugar
    │   ├── Si no puede:
    │   │   └── Robar una carta y retornar
    │   ├── Si puede:
    │   │   └── _pedir_entrada_jugador()
    │   │       ├── Pedir índice
    │   │       ├── Validar rango
    │   │       └── Validar compatibilidad
    │   ├── Jugar la carta
    │   ├── Si es negra:
    │   │   └── _pedir_color()
    │   ├── Descartar anterior
    │   ├── Poner nueva en mesa
    │   └── _aplicar_efectos()
    │       ├── Si +2: máquina roba 2
    │       ├── Si +4: máquina roba 4
    │       └── Marcar saltar turno
    │
Turno Máquina:
    ├── procesar_turno(maquina, humano)
    │   └── Igual pero:
    │       ├── _obtener_jugada_ia() en lugar de input
    │       └── elegir_color_random() para colores
```

---

## PATRONES DE DISEÑO

### **1. Patrón Factory (Implícito)**

```python
# Baraja crea instancias de cartas
class Baraja:
    def _inicializar(self):
        for color in colores:
            self.cartas.append(CartaNumerica(color, numero))
            self.cartas.append(CartaEspecial(color, tipo))
```

---

### **2. Patrón Strategy**

```python
# Diferentes estrategias de compatibilidad según tipo
class CartaNumerica:
    def es_compatible(self, otra):
        if super().es_compatible(otra):
            return True
        return self.numero == otra.numero

class CartaEspecial:
    def es_compatible(self, otra):
        if self.tipo == otra.tipo:
            return True
        return self.color == otra.color
```

---

### **3. Patrón Template Method**

```python
# Clase base define estructura, subclases implementan detalles
class Carta(ABC):
    def es_compatible(self, otra):  # Comportamiento base
        if self.color == Color.NEGRO:
            return True
        return self.color == otra.color
    
    @abstractmethod
    def __str__(self):  # Cada subclase implementa

class CartaNumerica(Carta):
    def es_compatible(self, otra):  # Extiende base
        if super().es_compatible(otra):
            return True
        ...
```

---

### **4. Patrón Singleton (Implícito)**

```python
# Solo una instancia de JuegoUno por sesión
juego = JuegoUno()
juego.iniciar()  # Se usa la misma instancia
```

---

## MANEJO DE EXCEPCIONES

### **Excepciones Capturadas**

```python
# En CartaNumerica.__init__
if not 0 <= numero <= 9:
    raise ValueError(f"Número inválido: {numero}")

# En Jugador.jugar_carta
if not 0 <= indice < len(self.mano):
    raise IndexError(f"Índice {indice} fuera de rango")

# En JuegoUno.guardar_partida
try:
    with open(nombre_archivo, "wb") as f:
        pickle.dump(self, f)
except Exception as e:
    print(f"Error al guardar: {e}")
```

### **Excepciones Personalizadas**

```python
class UnoException(Exception):
    pass  # Base para todas las excepciones del juego

class CartaIncompatibleError(UnoException):
    pass  # Cuando carta no es compatible

class JugadaInvalidaError(UnoException):
    pass  # Cuando índice de carta es inválido
```

**Ventaja:** Captura específica de errores en el juego.

```python
try:
    jugador.jugar_carta(indice)
except JugadaInvalidaError:
    print("Esa carta no existe en tu mano")
except CartaIncompatibleError:
    print("Esa carta no es compatible")
```

---

## ALMACENAMIENTO DE DATOS

### **Persistencia: Pickle**

```python
import pickle

# Guardar
with open("partida.pkl", "wb") as f:
    pickle.dump(juego, f)  # Serializa el objeto completo

# Cargar
with open("partida.pkl", "rb") as f:
    juego = pickle.load(f)  # Deserializa
```

**Ventajas:**
- Guarda objeto completo con su estado
- Preserva referencias internas
- Una sola línea para guardar/cargar

**Desventajas:**
- Formato binario (no legible)
- Riesgo si archivos están comprometidos

**Alternativas (no usadas aquí):**
- JSON: Legible pero requiere más conversiones
- SQLite: Para datos más complejos
- CSV: Para datos tabulares

---

## CÓMO EXPANDIR EL CÓDIGO

### **1. Agregar Nueva Carta Especial**

```python
# 1. Añadir en models.py/TipoCarta
class TipoCarta(Enum):
    CAMBIO_TURNO = (True, "~")  # Nueva carta

# 2. Crear en baraja.py
for _ in range(2):
    self.cartas.append(CartaEspecial(Color.ROJO, TipoCarta.CAMBIO_TURNO))

# 3. Implementar efecto en juego.py/_aplicar_efectos
if tipo == TipoCarta.CAMBIO_TURNO:
    self.saltar_turno = True
```

---

### **2. Mejorar la IA**

Actualmente: Juega la primera carta compatible.

```python
# Actual (jugador.py)
def obtener_indice_carta_compatible(self, carta_en_mesa):
    for indice, carta in enumerate(self.mano):
        if carta.es_compatible(carta_en_mesa):
            return indice  # Primera compatible
    return -1

# Mejorada: Prioriza cartas especiales
def obtener_indice_carta_optima(self, carta_en_mesa):
    especiales = []
    numeros = []
    
    for i, carta in enumerate(self.mano):
        if carta.es_compatible(carta_en_mesa):
            if carta.es_carta_comodin:
                especiales.append(i)
            else:
                numeros.append(i)
    
    return especiales[0] if especiales else numeros[0] if numeros else -1
```

---

### **3. Agregar Dificultad**

```python
# En config.py
@dataclass
class UnoConfig:
    DIFICULTAD: str = "normal"  # normal, fácil, difícil

# En juego.py
if self.config.DIFICULTAD == "difícil":
    # IA más estratégica
    return self._obtener_jugada_optima()
else:
    return self._obtener_jugada_simple()
```

---

### **4. Interfaz Gráfica**

Reemplazar CLI con GUI usando `tkinter` o `PyQt`:

```python
# tkinter_gui.py
import tkinter as tk
from juego import JuegoUno

root = tk.Tk()
juego = JuegoUno()

# Botones para cada carta
for i, carta in enumerate(juego.humano.get_mano()):
    btn = tk.Button(root, text=str(carta), 
                    command=lambda idx=i: juego.procesar_turno_gui(idx))
    btn.pack()

root.mainloop()
```

---

### **5. Multiplayer en Red**

Usar sockets para jugar contra otros:

```python
# servidor.py
import socket

server = socket.socket()
server.bind(("localhost", 5000))
server.listen(1)

conn, addr = server.accept()
juego = JuegoUno()
# Sincronizar estado del juego por red
```

---

## GLOSARIO DE TÉRMINOS

| Término | Significado |
|---------|------------|
| **ABC** | Abstract Base Class (clase abstracta) |
| **Enum** | Enumeración - conjunto de constantes |
| **Type Hints** | Anotaciones de tipo (int, str, bool, etc.) |
| **Dataclass** | Clase para almacenar datos con `@dataclass` |
| **Pickle** | Módulo para serializar objetos Python |
| **Polimorfismo** | Métodos con mismo nombre, diferente comportamiento |
| **Composición** | Un objeto contiene otros objetos |
| **Encapsulación** | Ocultar datos internos |
| **Herencia** | Una clase extiende otra |
| **Abstracción** | Interfaz sin detalles de implementación |
| **Properties** | Acceso a atributos como propiedades (`@property`) |
| **Optional[T]** | Tipo que puede ser T o None |
| **List[T]** | Lista de elementos tipo T |
| **Comodín** | Carta especial que afecta el juego |

---

## RESUMEN ARQUITECTÓNICO

**Patrón:** Modelo-Vista-Controlador (MVC) simplificado

```
Modelo (Lógica):
  ├── models.py (datos)
  ├── cartas.py (Cartas)
  ├── baraja.py (Baraja)
  ├── jugador.py (Jugadores)
  └── juego.py (Lógica)

Vista (Presentación):
  └── main.py (CLI)

Controlador (Entrada):
  └── JuegoUno.procesar_turno() (orquesta)
```

**Ventajas de esta estructura:**
- Modular y mantenible
- Fácil de testear
- Separación de responsabilidades
- Escalable

---

## CONCLUSIÓN

Este proyecto es una implementación completa y profesional del juego UNO que demuestra:

✅ Conceptos sólidos de POO (herencia, polimorfismo, encapsulación)
✅ Arquitectura modular y escalable
✅ Manejo de excepciones robusto
✅ Persistencia de datos
✅ Code style limpio y profesional

**Ideal para:** Estudiantes de 2do semestre de Maestría POO que necesitan referenciar cómo estructurar proyectos medianos.

---

*Documentación generada: 28 de enero de 2026*
*Versión: 1.0*
