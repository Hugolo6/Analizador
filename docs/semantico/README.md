# 📖 Documentación · Analizador Semántico

## ¿Qué hace?

El **Analizador Semántico** es la tercera y última fase del compilador.
Recorre el AST generado por el Parser y verifica reglas que la gramática
**no puede expresar**, como:

- Que las variables estén declaradas antes de usarse.
- Que no se redeclare una variable en el mismo bloque.
- Que los tipos sean compatibles en asignaciones y operaciones.
- Que se respeten los ámbitos (*scopes*) anidados (`if`, `while`, `for`).

---

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `analizador.py` | `TablaSimbolos` + `AnalizadorSemantico` |
| `__init__.py`   | Marca el directorio como paquete Python |

---

## Clases principales

### `TablaSimbolos`

Implementa una **pila de diccionarios** (uno por ámbito/bloque) para
rastrear variables declaradas y sus tipos.

```python
class TablaSimbolos:
    def entrar_bloque(self)               # Abre un nuevo ámbito
    def salir_bloque(self)                # Cierra el ámbito actual
    def declarar(self, nombre, tipo) → bool  # False si ya existe en este ámbito
    def buscar(self, nombre) → TipoToken | None  # Busca de dentro hacia fuera
```

Ejemplo de pila para el siguiente código:

```
anb           ← ámbito global: {}
    gz x = 1;        →  { x: INT }
    wen x > 0 {
        gz y = 2;    →  { x: INT } , { y: INT }
    }                ← se descarta el ámbito del if
end
```

### `AnalizadorSemantico`

Recorre el AST con el patrón **Visitor**: por cada tipo de nodo existe un
método `visitar_<NombreClase>` que implementa la lógica de validación.

```python
from semantico.analizador import AnalizadorSemantico

semantico = AnalizadorSemantico()
errores   = semantico.analizar(ast)   # Retorna list[str]

for e in errores:
    print(e)
```

---

## Reglas de tipos

| Variable destino | Valor origen | ¿Permitido? |
|---|---|---|
| `gz` (INT)   | INT    | ✔ |
| `gz` (INT)   | FLOAT  | ✖ No se puede bajar precisión |
| `fl` (FLOAT) | INT    | ✔ Promoción implícita |
| `fl` (FLOAT) | FLOAT  | ✔ |
| `str` (STRING) | STRING | ✔ |
| cualquiera   | tipo diferente | ✖ Error de incompatibilidad |

### Operaciones aritméticas

- `INT op INT` → resultado `INT`
- `FLOAT op INT` o `INT op FLOAT` → resultado `FLOAT`
- `STRING op cualquiera` → **Error semántico**

---

## Métodos Visitor implementados

| Método | Nodo que visita |
|---|---|
| `visitar_Programa` | Itera las sentencias del programa |
| `visitar_Declaracion` | Registra variable; verifica redeclaración y tipo |
| `visitar_Asignacion` | Verifica que la variable exista y el tipo sea compatible |
| `visitar_IfStatement` | Valida condición; abre/cierra ámbito de cada bloque |
| `visitar_WhileStatement` | Valida condición; abre/cierra ámbito del bloque |
| `visitar_ForStatement` | Abre ámbito; valida init, condición, actualización y bloque |
| `visitar_Lectura` | Verifica que la variable esté declarada |
| `visitar_Escritura` | Visita la expresión (valida variables usadas) |
| `visitar_ExpresionBinaria` | Deduce y retorna el tipo resultante |
| `visitar_ExpresionUnaria` | Retorna el tipo del operando |
| `visitar_Literal` | Mapea `ENTERO→INT`, `LETRA→STRING`, `IDENTIFICADOR→buscar` |
| `visitar_LlamadaFuncion` | Reporta "no soportado" (funciones de usuario) |

---

## Errores que detecta

| Código de error | Ejemplo que lo produce |
|---|---|
| Variable no declarada | `x = 5;` sin declarar `x` antes |
| Redeclaración en mismo bloque | `gz x = 1; gz x = 2;` |
| Incompatibilidad en declaración | `gz x = 3.14;` (FLOAT→INT) |
| Incompatibilidad en asignación | `gz x = 0; x = hola;` (STRING→INT) |
| Operación entre tipos inválidos | `gz x = 1 + hola;` |
| Lectura de variable no declarada | `les(y);` sin declarar `y` |

---

## Ejemplo de ejecución

```
anb
    gz x = 10;
    gz x = 20;   ← redeclaración
    fl y = x;    ← OK: INT → FLOAT (promoción)
    gz z = y;    ← ERROR: FLOAT → INT no permitido
end
```

Errores reportados:
```
Error Semántico: La variable 'x' ya fue declarada en este ámbito. L3
Error Semántico: Incompatibilidad de tipos en declaración:
    No se puede asignar 'fl (Flotante)' a la variable 'z' de tipo 'gz (Entero)'. L4
```
