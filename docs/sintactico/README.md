# 📖 Documentación · Analizador Sintáctico (Parser)

## ¿Qué hace?

El **Analizador Sintáctico** recibe la lista de tokens producida por el
Analizador Léxico y verifica que su orden respeta la **gramática del lenguaje**.
Como salida genera un **Árbol de Sintaxis Abstracta (AST)** que representa
la estructura jerárquica del programa.

---

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `parser.py` | Nodos del AST + clase `Parser` (descendente recursivo) |
| `__init__.py` | Marca el directorio como paquete Python |

---

## Gramática (BNF)

```
programa    ::= START cuerpo END

cuerpo      ::= sentencia*

sentencia   ::= declaracion
              | asignacion
              | if_stmt
              | while_stmt
              | for_stmt
              | lectura
              | escritura

declaracion ::= tipo IDENTIFICADOR "=" expresion ";"
tipo        ::= "gz" | "fl" | "str"

asignacion  ::= IDENTIFICADOR "=" expresion ";"

if_stmt     ::= "wen" expresion "{" cuerpo "}"
                [ "son" "{" cuerpo "}" ]

while_stmt  ::= "war" expresion "{" cuerpo "}"

for_stmt    ::= "fur" "(" asig_sin_pc ";" expresion ";" asig_sin_pc ")"
                "{" cuerpo "}"

lectura     ::= "les" "(" IDENTIFICADOR ")" ";"
escritura   ::= "dru" "(" expresion ")" ";"

expresion   ::= or_expr
or_expr     ::= and_expr ( ("or" | "||") and_expr )*
and_expr    ::= comp_expr ( ("and" | "&&") comp_expr )*
comp_expr   ::= arit_expr ( ("==" | "<" | ">" | "<=" | ">=") arit_expr )*
arit_expr   ::= mul_expr ( ("+" | "-") mul_expr )*
mul_expr    ::= unaria_expr ( ("*" | "/") unaria_expr )*
unaria_expr ::= ("-" | "+")* primaria
primaria    ::= ENTERO | LETRA | IDENTIFICADOR
              | IDENTIFICADOR "(" argumentos ")"
              | "(" expresion ")"
```

---

## Nodos del AST

| Clase | Descripción | Atributos principales |
|---|---|---|
| `Programa` | Nodo raíz | `sentencias: list` |
| `Declaracion` | `gz x = 10;` | `tipo_token`, `identificador`, `expresion` |
| `Asignacion` | `x = x + 1;` | `identificador`, `expresion` |
| `IfStatement` | `wen cond { } son { }` | `condicion`, `bloque_if`, `bloque_else` |
| `WhileStatement` | `war cond { }` | `condicion`, `bloque` |
| `ForStatement` | `fur (init; cond; upd) { }` | `inicializacion`, `condicion`, `actualizacion`, `bloque` |
| `Lectura` | `les(x);` | `identificador` |
| `Escritura` | `dru(expr);` | `expresion` |
| `ExpresionBinaria` | `a + b` | `izquierda`, `operador`, `derecha` |
| `ExpresionUnaria` | `-a` | `operador`, `operando` |
| `Literal` | `42`, `x` | `token` |
| `LlamadaFuncion` | `f(a, b)` | `nombre`, `argumentos` |

---

## Clase principal: `Parser`

```python
from sintactico.parser import Parser

parser = Parser(tokens)     # tokens = salida del AnalizadorLexico
ast    = parser.parsear()   # Retorna Programa | None

if parser.errores:
    for e in parser.errores:
        print(e)
```

### Estrategia de manejo de errores

El parser usa **recuperación de errores simple**: cuando detecta un token
inesperado registra el error y **detiene el análisis de esa rama**, devolviendo
`None` y dejando que el llamador decida si abortar o seguir.

---

## Ejemplo de AST

Código:
```
anb
    gz x = 10;
    wen x > 5 { dru(x); }
end
```

AST resultante:
```
Programa
  Declaracion: x (gz)
    Literal: 10
  IfStatement (tiene_else=False)
    Condicion:
      OpBinaria: >
        Literal: x
        Literal: 5
    Bloque If:
      Escritura
        Literal: x
```

---

## Errores que detecta

| Situación | Ejemplo | Mensaje |
|---|---|---|
| Falta `;` al final | `gz x = 5` | Se esperaba `;` pero se encontró ... |
| Bloque sin cerrar | `wen x > 0 {` | Se esperaba `}` pero se encontró EOF |
| Token inesperado | `gz = 10;` | Se esperaba IDENTIFICADOR |
| Expresión inválida | `gz x = ;` | Expresión inesperada `;` |

> **Nota:** El Parser solo se ejecuta si el Analizador Léxico no reportó errores.
