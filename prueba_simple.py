#!/usr/bin/env python3
"""Script simple para verificar que el parser funciona correctamente."""

from lexico.reservadas import AnalizadorLexico
from sintactico.parser import Parser

# Código simple para probar
codigo = """
anb
    gz x = 10;
    dru(x);
end
"""

print("=" * 80)
print("PRUEBA SIMPLE DEL PARSER")
print("=" * 80)

print("\n>>> CÓDIGO FUENTE <<<")
print(codigo)

# Léxico
print("\n>>> ANÁLISIS LÉXICO <<<")
lexer = AnalizadorLexico()
tokens = lexer.tokenizar(codigo)

if lexer.errores:
    print("✗ Errores léxicos:")
    for e in lexer.errores:
        print(f"  {e}")
else:
    print(f"✓ {len(tokens)} tokens generados")
    for tok in tokens:
        if tok.tipo.value != 'EOF':
            print(f"  {tok}")

# Sintáctico
print("\n>>> ANÁLISIS SINTÁCTICO <<<")
parser = Parser(tokens)
arbol = parser.parsear()

if parser.errores:
    print("✗ Errores sintácticos:")
    for e in parser.errores:
        print(f"  {e}")
else:
    print("✓ Análisis sintáctico exitoso\n")
    parser.imprimir_arbol()
