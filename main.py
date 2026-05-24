"""
Compilador — Punto de entrada por consola.
Ejecuta las cuatro fases: léxico, sintáctico, semántico y ejecución.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexico.reservadas import AnalizadorLexico
from sintactico.parser import Parser
from semantico.analizador import AnalizadorSemantico
from interprete import Interprete


def compilar(codigo_fuente: str, salida_fn=None) -> dict:
    """
    Ejecuta las cuatro fases sobre el código fuente.
    salida_fn: función que recibe cada línea de salida del programa (dru).
    Retorna un dict con resultados de cada fase.
    """
    resultado = {
        "lexico":    {"ok": False, "tokens": [], "errores": []},
        "sintactico": {"ok": False, "ast": None,   "errores": []},
        "semantico":  {"ok": False, "errores": []},
        "ejecucion":  {"ok": False, "errores": [], "salida": []},
    }

    # ── FASE 1: LÉXICO ────────────────────────────────────────────────────────
    lexer = AnalizadorLexico()
    tokens = lexer.tokenizar(codigo_fuente)
    resultado["lexico"]["tokens"] = tokens

    if lexer.errores:
        resultado["lexico"]["errores"] = [str(e) for e in lexer.errores]
        return resultado
    resultado["lexico"]["ok"] = True

    # ── FASE 2: SINTÁCTICO ────────────────────────────────────────────────────
    parser = Parser(tokens)
    ast = parser.parsear()
    resultado["sintactico"]["ast"] = ast

    if parser.errores:
        resultado["sintactico"]["errores"] = parser.errores
        return resultado
    resultado["sintactico"]["ok"] = True

    # ── FASE 3: SEMÁNTICO ─────────────────────────────────────────────────────
    semantico = AnalizadorSemantico()
    errores_sem = semantico.analizar(ast)

    if errores_sem:
        resultado["semantico"]["errores"] = errores_sem
        return resultado
    resultado["semantico"]["ok"] = True

    # ── FASE 4: EJECUCIÓN ─────────────────────────────────────────────────────
    lineas_salida = []

    def capturar_salida(texto):
        lineas_salida.append(texto)
        if salida_fn:
            salida_fn(texto)

    interprete = Interprete(salida_fn=capturar_salida)
    errores_ej = interprete.ejecutar(ast)
    resultado["ejecucion"]["salida"] = lineas_salida

    if errores_ej:
        resultado["ejecucion"]["errores"] = errores_ej
    else:
        resultado["ejecucion"]["ok"] = True

    return resultado


def imprimir_resultado(resultado: dict):
    sep = "=" * 70

    print(f"\n{sep}")
    print("  FASE 1 · ANÁLISIS LÉXICO")
    print(sep)
    if resultado["lexico"]["ok"]:
        n = len(resultado["lexico"]["tokens"])
        print(f"  [OK]  {n} tokens generados sin errores.")
    else:
        print("  [ERROR] Errores léxicos encontrados:")
        for e in resultado["lexico"]["errores"]:
            print(f"    · {e}")
        return

    print(f"\n{sep}")
    print("  FASE 2 · ANÁLISIS SINTÁCTICO")
    print(sep)
    if resultado["sintactico"]["ok"]:
        print("  [OK]  Árbol AST construido sin errores.")
    else:
        print("  [ERROR] Errores sintácticos encontrados:")
        for e in resultado["sintactico"]["errores"]:
            print(f"    · {e}")
        return

    print(f"\n{sep}")
    print("  FASE 3 · ANÁLISIS SEMÁNTICO")
    print(sep)
    if resultado["semantico"]["ok"]:
        print("  [OK]  Sin errores semánticos.")
    else:
        print("  [ERROR] Errores semánticos encontrados:")
        for e in resultado["semantico"]["errores"]:
            print(f"    · {e}")
        return

    print(f"\n{sep}")
    print("  FASE 4 · EJECUCIÓN")
    print(sep)
    if resultado["ejecucion"]["salida"]:
        print("  Salida del programa:")
        for linea in resultado["ejecucion"]["salida"]:
            print(f"    {linea}")
    if resultado["ejecucion"]["ok"]:
        print("  [OK]  Programa ejecutado sin errores.")
    else:
        print("  [ERROR] Errores durante la ejecución:")
        for e in resultado["ejecucion"]["errores"]:
            print(f"    · {e}")


# ── EJEMPLOS ──────────────────────────────────────────────────────────────────
CODIGO_VALIDO = """\
anb
    gz x = 10;
    gz y = 20;
    fl promedio = 0;
    wen x <= y {
        promedio = x + y;
        dru(promedio);
    }
    war x > 0 {
        dru(x);
        x = x - 1;
    }
end
"""

CODIGO_CON_ERRORES = """\
anb
    gz x = 7
    wen x > 5 {
        dru(x);
    
end
"""

CODIGO_FOR = """\
anb
    gz i = 0;
    gz suma = 0;
    fur (i = 0; i < 5; i = i + 1) {
        suma = suma + i;
    }
    dru(suma);
end
"""


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  COMPILADOR · EJEMPLO VÁLIDO")
    print("=" * 70)
    print(CODIGO_VALIDO)
    imprimir_resultado(compilar(CODIGO_VALIDO))

    print("\n\n" + "=" * 70)
    print("  COMPILADOR · EJEMPLO CON ERRORES")
    print("=" * 70)
    print(CODIGO_CON_ERRORES)
    imprimir_resultado(compilar(CODIGO_CON_ERRORES))

    print("\n\n" + "=" * 70)
    print("  COMPILADOR · EJEMPLO WITH FOR")
    print("=" * 70)
    print(CODIGO_FOR)
    imprimir_resultado(compilar(CODIGO_FOR))
