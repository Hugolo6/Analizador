# 📋 DOCUMENTACIÓN DEL ANALIZADOR SINTÁCTICO (PARSER)

## Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura General](#arquitectura-general)
3. [Gramática Libre de Contexto](#gramática-libre-de-contexto)
4. [Estructura del AST](#estructura-del-ast)
5. [Guía de Uso](#guía-de-uso)
6. [Manejo de Errores](#manejo-de-errores)
7. [Ejemplos](#ejemplos)

---

## Resumen Ejecutivo

El **Analizador Sintáctico (Parser)** es un analizador **descendente recursivo** que:

✓ Recibe tokens del Analizador Léxico  
✓ Valida que los tokens sigan las reglas de la gramática definida  
✓ Construye un **Árbol de Sintaxis Abstracta (AST)**  
✓ Reporta errores sintácticos detallados con posición (línea:columna)  

**Método**: Análisis Descendente Recursivo (Recursive Descent Parsing)  
**Lenguaje implementado**: Python  
**Ubicación**: `sintactico/parser.py`

---

## Arquitectura General

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│ ANALIZADOR LÉXICO                                           │
│ (Convierte texto en tokens)                                 │
│ Entrada: código_fuente (string)                             │
│ Salida: lista de Token                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ ANALIZADOR SINTÁCTICO (PARSER)                              │
│ (Valida estructura y construye AST)                         │
│ Entrada: lista de Token                                     │
│ Salida: AST + lista de errores                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Árbol de Sintaxis   │
        │  Abstracta (AST)     │
        └──────────────────────┘
        
        [Próxima fase: Análisis Semántico/Ejecución]
```

### Clases del Parser

```python
class Parser:
    # Atributos
    tokens           # Lista de tokens del Lexer
    posicion         # Índice del token actual
    token_actual     # Token siendo procesado
    errores          # Lista de errores sintácticos
    arbol_ast        # Árbol de Sintaxis Abstracta generado
    
    # Métodos principales
    parsear()        # Punto de entrada
    analizar_sentencia()
    analizar_expresion()
```

---

## Gramática Libre de Contexto

### BNF (Backus-Naur Form)

```
<programa>     ::= START <cuerpo> END

<cuerpo>       ::= (<sentencia>)*

<sentencia>    ::= <declaracion>
                 | <asignacion>
                 | <if_stmt>
                 | <while_stmt>
                 | <for_stmt>
                 | <lectura>
                 | <escritura>

<declaracion>  ::= <tipo> IDENTIFICADOR ASIG <expresion> PUNTO_CON
                 Ej: gz x = 10;

<asignacion>   ::= IDENTIFICADOR ASIG <expresion> PUNTO_CON
                 Ej: x = x + 1;

<if_stmt>      ::= IF <expresion> LLAVE_IZQ <cuerpo> LLAVE_DER 
                    [ELSE LLAVE_IZQ <cuerpo> LLAVE_DER]
                 Ej: wen x > 5 { ... } son { ... }

<while_stmt>   ::= WHILE <expresion> LLAVE_IZQ <cuerpo> LLAVE_DER
                 Ej: war x < 100 { ... }

<for_stmt>     ::= FOR PAR_IZQ <asignacion> <expresion> PUNTO_CON 
                    <asignacion> PAR_DER LLAVE_IZQ <cuerpo> LLAVE_DER
                 Ej: fur (x = 0; x < 10; x = x + 1) { ... }

<lectura>      ::= LEER PAR_IZQ IDENTIFICADOR PAR_DER PUNTO_CON
                 Ej: les(x);

<escritura>    ::= IMPRIMIR PAR_IZQ <expresion> PAR_DER PUNTO_CON
                 Ej: dru(resultado);

<expresion>    ::= <or_expr>

<or_expr>      ::= <and_expr> ((OR | OR2) <and_expr>)*
                 Ej: a || b || c

<and_expr>     ::= <comp_expr> ((AND | AND2) <comp_expr>)*
                 Ej: a && b && c

<comp_expr>    ::= <arit_expr> ((IGUAL | MENOR | MAYOR | MENOR_EQ | MAYOR_EQ) <arit_expr>)*
                 Ej: x <= y, a == b

<arit_expr>    ::= <mul_expr> ((SUMA | RESTA) <mul_expr>)*
                 Ej: 5 + 3 - 2

<mul_expr>     ::= <unaria_expr> ((MULT | DIV) <unaria_expr>)*
                 Ej: 10 * 2 / 5

<unaria_expr>  ::= (RESTA | SUMA)* <primaria>
                 Ej: -x, +5, -(-a)

<primaria>     ::= LITERAL
                 | IDENTIFICADOR
                 | PAR_IZQ <expresion> PAR_DER
                 | <llamada_funcion>
                 Ej: 42, variable, (x + y), funcion(args)

<llamada_funcion> ::= IDENTIFICADOR PAR_IZQ [<expresion> (COMA <expresion>)*] PAR_DER

<tipo>         ::= INT | FLOAT | STRING
                 Ej: gz, fl, str

<literal>      ::= ENTERO | LETRA | IDENTIFICADOR
```

### Precedencia de Operadores

De **menor** a **mayor** precedencia (vinculación más débil a más fuerte):

| Precedencia | Operador | Asociatividad |
|-------------|----------|---------------|
| 1 (baja)    | OR, OR2  | Izquierda    |
| 2           | AND, AND2| Izquierda    |
| 3           | ==, <, >, <=, >= | Izquierda |
| 4           | +, -     | Izquierda    |
| 5           | *, /     | Izquierda    |
| 6 (alta)    | Unaria (+, -)| Derecha  |

---

## Estructura del AST

### Jerarquía de Clases

```
NodoAST (clase base)
├── Programa
├── Sentencia (clase base)
│   ├── Declaracion
│   ├── Asignacion
│   ├── IfStatement
│   ├── WhileStatement
│   ├── ForStatement
│   ├── Lectura
│   └── Escritura
└── Expresion (clase base)
    ├── ExpresionBinaria
    ├── ExpresionUnaria
    ├── Literal
    └── LlamadaFuncion
```

### Detalle de Nodos

#### `Programa`
```python
class Programa(NodoAST):
    sentencias: List[Sentencia]
    # Nodo raíz del AST
```

#### `Declaracion`
```python
class Declaracion(Sentencia):
    tipo_token: Token        # gz, fl, str
    identificador: Token     # Nombre de la variable
    expresion: Expresion     # Valor inicial
    
# Ejemplo de AST:
# gz x = 10;
# Declaracion(
#   tipo_token=Token(INT, "gz"),
#   identificador=Token(IDENTIFICADOR, "x"),
#   expresion=Literal(Token(ENTERO, "10"))
# )
```

#### `Asignacion`
```python
class Asignacion(Sentencia):
    identificador: Token     # Nombre de la variable
    expresion: Expresion     # Nuevo valor
    
# Ejemplo de AST:
# x = x + 5;
# Asignacion(
#   identificador=Token(IDENTIFICADOR, "x"),
#   expresion=ExpresionBinaria(
#     izquierda=Literal(Token(IDENTIFICADOR, "x")),
#     operador=Token(SUMA, "+"),
#     derecha=Literal(Token(ENTERO, "5"))
#   )
# )
```

#### `IfStatement`
```python
class IfStatement(Sentencia):
    condicion: Expresion           # Expresión booleana
    bloque_if: List[Sentencia]    # Sentencias en el if
    bloque_else: List[Sentencia]  # Sentencias en el else (opcional)
    
# Ejemplo de AST:
# wen x > 5 { dru(x); } son { dru(0); }
# IfStatement(
#   condicion=ExpresionBinaria(...),
#   bloque_if=[Escritura(...)],
#   bloque_else=[Escritura(...)]
# )
```

#### `WhileStatement`
```python
class WhileStatement(Sentencia):
    condicion: Expresion        # Expresión booleana
    bloque: List[Sentencia]    # Sentencias en el bucle
```

#### `ForStatement`
```python
class ForStatement(Sentencia):
    inicializacion: Asignacion  # x = 0
    condicion: Expresion        # x < 10
    actualizacion: Asignacion   # x = x + 1
    bloque: List[Sentencia]    # Cuerpo del for
```

#### `Lectura` y `Escritura`
```python
class Lectura(Sentencia):
    identificador: Token        # Variable donde guardar

class Escritura(Sentencia):
    expresion: Expresion        # Qué escribir
```

#### `ExpresionBinaria`
```python
class ExpresionBinaria(Expresion):
    izquierda: Expresion        # Lado izquierdo
    operador: Token             # +, -, *, /, ==, <, etc.
    derecha: Expresion          # Lado derecho
    
# Ejemplo: x + y
# ExpresionBinaria(
#   izquierda=Literal(Token(IDENTIFICADOR, "x")),
#   operador=Token(SUMA, "+"),
#   derecha=Literal(Token(IDENTIFICADOR, "y"))
# )
```

#### `ExpresionUnaria`
```python
class ExpresionUnaria(Expresion):
    operador: Token             # +, -
    operando: Expresion         # Operando
    
# Ejemplo: -x
# ExpresionUnaria(
#   operador=Token(RESTA, "-"),
#   operando=Literal(Token(IDENTIFICADOR, "x"))
# )
```

#### `Literal`
```python
class Literal(Expresion):
    token: Token                # ENTERO, LETRA, IDENTIFICADOR
    
# Ejemplo: 42
# Literal(Token(ENTERO, "42"))
```

#### `LlamadaFuncion`
```python
class LlamadaFuncion(Expresion):
    nombre: Token               # Nombre de la función
    argumentos: List[Expresion] # Argumentos pasados
    
# Ejemplo: funcion(a, b+c)
# LlamadaFuncion(
#   nombre=Token(IDENTIFICADOR, "funcion"),
#   argumentos=[
#     Literal(Token(IDENTIFICADOR, "a")),
#     ExpresionBinaria(...)
#   ]
# )
```

---

## Guía de Uso

### Paso 1: Tokenizar el código (Lexer)

```python
from lexico.reservadas import AnalizadorLexico

codigo = """
anb
    gz x = 10;
    wen x > 5 {
        dru(x);
    }
end
"""

lexer = AnalizadorLexico()
tokens = lexer.tokenizar(codigo)

# Verificar errores léxicos
if lexer.errores:
    print("Errores léxicos encontrados")
    exit(1)
```

### Paso 2: Crear el Parser y analizar

```python
from sintactico.parser import Parser

parser = Parser(tokens)
arbol = parser.parsear()
```

### Paso 3: Verificar resultados

```python
# Verificar si hay errores sintácticos
if parser.errores:
    parser.imprimir_errores()
else:
    print("✓ Análisis sintáctico exitoso")
    
# Visualizar el AST
parser.imprimir_arbol()
```

### Paso 4: Acceder al AST programáticamente

```python
# El AST es un grafo de objetos Python
arbol = parser.arbol_ast  # Objeto Programa

for sentencia in arbol.sentencias:
    if isinstance(sentencia, Declaracion):
        print(f"Variable: {sentencia.identificador.lexema}")
        print(f"Tipo: {sentencia.tipo_token.lexema}")
```

---

## Manejo de Errores

### Tipos de Errores Sintácticos Detectados

1. **Token no esperado**
   ```
   Error Sintáctico [L2:C10]: Se esperaba '; (punto y coma)' 
   pero se encontró 'gz'
   ```

2. **Token esperado no encontrado (EOF)**
   ```
   Error Sintáctico [L4:C1]: Se esperaba END (end) 
   pero se encontró EOF
   ```

3. **Expresión incompleta**
   ```
   Error Sintáctico [L2:C12]: Se esperaba una expresión 
   pero se encontró ';'
   ```

4. **Falta de paréntesis o llaves**
   ```
   Error Sintáctico [L3:C5]: Se esperaba '{ (llave izquierda)' 
   pero se encontró 'dru'
   ```

### Formato de Error

```
Error Sintáctico [L{línea}:C{columna}]: {mensaje}
    Token encontrado: '{lexema}' (tipo: {tipo_token})
```

### Métodos de Utilidad

```python
# Imprimir todos los errores formateados
parser.imprimir_errores()

# Acceder directamente a la lista de errores
for error in parser.errores:
    print(error)
```

---

## Ejemplos

### Ejemplo 1: Programa Simple

**Código fuente:**
```
anb
    gz edad = 25;
    dru(edad);
end
```

**Análisis:**
```
Programa
  Declaracion: edad (gz)
    Literal: 25 (ENTERO)
  Escritura
    Literal: edad (IDENTIFICADOR)
```

**Tokens esperados:**
```
START, INT, IDENTIFICADOR, ASIG, ENTERO, PUNTO_CON,
IMPRIMIR, PAR_IZQ, IDENTIFICADOR, PAR_DER, PUNTO_CON,
END
```

---

### Ejemplo 2: Condicional

**Código fuente:**
```
anb
    gz x = 10;
    wen x > 5 {
        dru(x);
    } son {
        dru(0);
    }
end
```

**Análisis:**
```
Programa
  Declaracion: x (gz)
    Literal: 10 (ENTERO)
  If
    Condicion:
      OpBinaria: >
        Izq:
          Literal: x (IDENTIFICADOR)
        Der:
          Literal: 5 (ENTERO)
    Bloque If:
      Escritura
        Literal: x (IDENTIFICADOR)
    Bloque Else:
      Escritura
        Literal: 0 (ENTERO)
```

---

### Ejemplo 3: Bucle

**Código fuente:**
```
anb
    gz suma = 0;
    gz i = 1;
    war i <= 10 {
        suma = suma + i;
        i = i + 1;
    }
    dru(suma);
end
```

**Análisis:**
```
Programa
  Declaracion: suma (gz)
    Literal: 0 (ENTERO)
  Declaracion: i (gz)
    Literal: 1 (ENTERO)
  While
    Condicion:
      OpBinaria: <=
        Izq:
          Literal: i (IDENTIFICADOR)
        Der:
          Literal: 10 (ENTERO)
    Bloque:
      Asignacion: suma
        OpBinaria: +
          Izq:
            Literal: suma (IDENTIFICADOR)
          Der:
            Literal: i (IDENTIFICADOR)
      Asignacion: i
        OpBinaria: +
          Izq:
            Literal: i (IDENTIFICADOR)
          Der:
            Literal: 1 (ENTERO)
  Escritura
    Literal: suma (IDENTIFICADOR)
```

---

### Ejemplo 4: Error Sintáctico

**Código fuente (incorrecto):**
```
anb
    gz x = ;
    dru(x);
end
```

**Errores detectados:**
```
Error Sintáctico [L2:C12]: Se esperaba una expresión 
pero se encontró ';'
    Token encontrado: ';' (tipo: PUNTO_CON)
```

---

## Referencia de Métodos Principales

### `parsear()`
```python
def parsear() -> Programa | None:
    """
    Punto de entrada del parser.
    
    Retorna:
        Programa: Árbol de sintaxis abstracta
        None: Si hay errores graves
    """
```

### `imprimir_arbol(nodo=None, nivel=0)`
```python
def imprimir_arbol(nodo=None, nivel=0):
    """
    Imprime el AST en formato indentado para visualización.
    
    Args:
        nodo: Nodo del AST (por defecto, la raíz)
        nivel: Nivel de indentación (uso interno)
    """
```

### `imprimir_errores()`
```python
def imprimir_errores():
    """Imprime todos los errores sintácticos encontrados."""
```

### `consumir(tipo_esperado, nombre_token=None) -> Token`
```python
def consumir(tipo_esperado: TipoToken, nombre_token: str = None) -> Token:
    """
    Consume el token actual si coincide con el tipo esperado.
    
    Args:
        tipo_esperado: Tipo de token esperado (TipoToken enum)
        nombre_token: Nombre legible del token para mensajes de error
    
    Retorna:
        Token: El token consumido
        False: Si no coincide
    """
```

---

## Notas de Implementación

### Análisis Descendente Recursivo

El parser utiliza **análisis descendente recursivo** con:
- **Método**: Una función recursiva por cada regla de la gramática
- **Ventajas**: Fácil de entender, estructura clara, buen manejo de errores
- **Desventajas**: Requiere gramática sin recursión izquierda (✓ cumplida aquí)

### Precedencia de Operadores

Se implementa mediante funciones anidadas de análisis:
```python
analizar_or_expr()      # Nivel 1 (baja precedencia)
  → analizar_and_expr()
    → analizar_comp_expr()
      → analizar_arit_expr()
        → analizar_mul_expr()
          → analizar_unaria_expr()
            → analizar_primaria()    # Nivel 6 (alta precedencia)
```

### Manejo de Errores Robusto

- Registra todos los errores sin detener
- Continúa analizando para encontrar más errores
- Proporciona contexto (línea, columna, tokens)

---

## Conclusión

Este parser implementa un **analizador sintáctico profesional** que:

✓ Validar la estructura gramatical del código  
✓ Genera un AST completo para procesamiento posterior  
✓ Proporciona mensajes de error detallados  
✓ Es extensible para agregar nuevas reglas gramaticales  

El AST generado es la base para las fases posteriores del compilador:
**Análisis Semántico → Generación de Código → Ejecución**

