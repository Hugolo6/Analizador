# Compilador — Documentación General

## Estructura del proyecto

```
compilador/
├── main.py              ← Punto de entrada por consola
├── interfaz.py          ← IDE gráfico (tkinter)
│
├── lexico/
│   ├── reservadas.py    ← Tokens, tabla de palabras reservadas, AnalizadorLexico
│   ├── Oplogicos.py     ← Operadores lógicos y de comparación
│   └── __init__.py
│
├── sintactico/
│   ├── parser.py        ← Nodos AST + Parser descendente recursivo
│   └── __init__.py
│
├── semantico/
│   ├── analizador.py    ← TablaSimbolos + AnalizadorSemantico
│   └── __init__.py
│
└── docs/
    ├── lexico/README.md
    ├── sintactico/README.md
    └── semantico/README.md
```

---

## Ejecutar el IDE gráfico

```bash
cd compilador
python interfaz.py
```

## Ejecutar por consola

```bash
cd compilador
python main.py
```

---

## Lenguaje soportado

El compilador procesa un lenguaje con sintaxis inspirada en palabras alemanas:

```
anb
    gz x = 10;
    gz y = 20;
    fl promedio = 0;

    wen x <= y {
        promedio = x + y;
        dru(promedio);
    }

    war x > 0 {
        les(x);
        x = x - 1;
    }

    fur (i = 0; i < 5; i = i + 1) {
        dru(i);
    }
end
```

### Tipos de datos

| TK | Tipo | Ejemplo |
|---|---|---|
| `gz`  | Entero  | `gz x = 10;` |
| `fl`  | Flotante | `fl pi = 3;` |
| `str` | Cadena  | (declaración, lectura/escritura) |

### Estructuras de control

| TK | Equivale a | Ejemplo |
|---|---|---|
| `wen ... { }` | `if`    | `wen x > 0 { dru(x); }` |
| `son { }`     | `else`  | `son { dru(y); }` |
| `war ... { }` | `while` | `war x > 0 { x = x - 1; }` |
| `fur (...) { }`| `for`  | `fur (i = 0; i < 5; i = i + 1) { }` |

### I/O

| TK | Acción |
|---|---|
| `les(x);` | Leer variable `x` |
| `dru(expr);` | Imprimir expresión |

---

## Fases de compilación

```
Código fuente
      │
      ▼
┌─────────────────┐
│  LÉXICO          │  → list[Token]   (errores: CARACTER_INVALIDO, TOKEN_DESCONOCIDO)
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  SINTÁCTICO      │  → AST (Programa) (errores: tokens inesperados, bloques sin cerrar)
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  SEMÁNTICO       │  → list[str] errores  (tipos, declaraciones, ámbitos)
└─────────────────┘
```

Cada fase **detiene el pipeline** si encuentra errores, evitando cascadas
de falsos positivos.

---

## Dependencias

- Python 3.10+
- `tkinter` (incluido en Python estándar)
- Sin dependencias externas

---

## Documentación por módulo

- [Analizador Léxico](docs/lexico/README.md)
- [Analizador Sintáctico](docs/sintactico/README.md)
- [Analizador Semántico](docs/semantico/README.md)
