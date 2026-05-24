# 📖 Documentación · Analizador Léxico

## ¿Qué hace?

El **Analizador Léxico** (también llamado *tokenizador* o *scanner*) es la primera
fase de la compilación. Lee el código fuente como una cadena de texto y lo
convierte en una lista de **tokens** — las unidades mínimas con significado del lenguaje.

---

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `reservadas.py` | Define `TipoToken`, `Token`, `ErrorLexico`, las tablas de palabras reservadas y `AnalizadorLexico` |
| `Oplogicos.py`  | Define la tabla de operadores de comparación y lógicos (`==`, `<=`, `and`, `or`, etc.) |
| `__init__.py`   | Marca el directorio como paquete Python |

---

## Tokens del lenguaje

### Palabras reservadas

| Keyword real | TK corto | Descripción |
|---|---|---|
| `start` / `int` | `anb` / `anf` | Inicio de bloque |
| `end`           | `end`         | Fin de bloque |
| `if`            | `wen`         | Condicional |
| `else`          | `son`         | Alternativa |
| `while`         | `war`         | Bucle mientras |
| `for`           | `fur`         | Bucle para |
| `Int`           | `gz`          | Tipo entero |
| `float`         | `fl`          | Tipo flotante |
| `String`        | `str`         | Tipo cadena |
| `leer`          | `les`         | Leer variable |
| `imprimir`      | `dru`         | Imprimir valor |

### Operadores lógicos y de comparación

| Token | TK  | Significado |
|---|---|---|
| `==`   | `==`  | Igual a |
| `<`    | `<`   | Menor que |
| `>`    | `>`   | Mayor que |
| `<=`   | `<=`  | Menor o igual |
| `>=`   | `>=`  | Mayor o igual |
| `and` / `&&` | `und` / `u2` | Y lógico |
| `or`  / `||` | `od`  / `||` | O lógico |

### Operadores aritméticos y delimitadores

`+` `-` `*` `/` `=` `;` `(` `)` `{` `}` `,` `"`

---

## Clase principal: `AnalizadorLexico`

```python
from lexico.reservadas import AnalizadorLexico

lexer = AnalizadorLexico()
tokens = lexer.tokenizar(codigo_fuente)   # Retorna list[Token]

if lexer.errores:
    # Iterar errores (son instancias de ErrorLexico)
    for err in lexer.errores:
        print(err)
```

### Método `tokenizar(fuente: str) → list[Token]`

Recorre el código fuente carácter a carácter aplicando el siguiente algoritmo
de prioridades:

1. **Espacios / saltos** → se ignoran; actualiza línea y columna.
2. **Bloques alfabéticos** → extrae la palabra completa y la compara contra
   la tabla de palabras reservadas. Si no coincide, la trata como identificador.
3. **Operadores dobles** (`==`, `<=`, `>=`, `&&`, `||`) → detectados antes
   que los simples para evitar ambigüedad.
4. **Operadores simples** (`+`, `-`, `=`, `;`, etc.).
5. **Números enteros** → secuencia de dígitos.
6. **Cualquier otro carácter** → genera `ErrorLexico` de tipo `CARACTER_INVALIDO`.

### Clase `Token`

```python
class Token:
    tipo:        TipoToken   # Enum con el tipo semántico
    lexema:      str         # Texto original del código fuente
    tk:          str         # Código corto del token
    linea:       int         # Línea donde aparece (desde 1)
    columna:     int         # Columna donde empieza (desde 1)
    es_reservada: bool       # True si es palabra reservada
```

### Clase `ErrorLexico`

```python
class ErrorLexico:
    tipo_error: str   # "TOKEN_DESCONOCIDO" | "CARACTER_INVALIDO"
    lexema:     str   # El texto que causó el error
    linea:      int
    columna:    int
    mensaje:    str
```

---

## Ejemplo de uso

```
Entrada:   gz x = 10;
Salida (tokens):
  gz         INT        gz    L1:C1  [RESERVADA]
  x          IDENTIFICADOR bez L1:C4
  =          ASIG       =     L1:C6  [RESERVADA]
  10         ENTERO     gan   L1:C8
  ;          PUNTO_CON  ;     L1:C10 [RESERVADA]
```

---

## Errores que detecta

| Tipo | Ejemplo | Mensaje |
|---|---|---|
| `CARACTER_INVALIDO` | `@x = 5;` | Carácter `@` no válido |
| `TOKEN_DESCONOCIDO` | `xyz123` | Lexema `xyz123` no reconocido |

> **Nota:** Si hay errores léxicos, la compilación se detiene aquí y no
> continúa a la fase sintáctica.
