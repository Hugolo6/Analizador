#!/usr/bin/env python3
"""
Ejemplo visual completo del Parser funcionando.
Muestra el AST de un programa más complejo.
"""

from lexico.reservadas import AnalizadorLexico
from sintactico.parser import Parser

# Programa más complejo para visualización
codigo = """
anb
    gz suma = 0;
    gz contador = 1;
    war contador <= 10 {
        suma = suma + contador;
        contador = contador + 1;
    }
    wen suma > 50 {
        dru(suma);
    } son {
        les(suma);
    }
end
"""

def analizar_y_mostrar(codigo):
    """Analiza código y muestra resultados detallados."""
    
    print("\n" + "=" * 100)
    print("EJEMPLO COMPLETO DEL PARSER - ANALIZADOR SINTÁCTICO")
    print("=" * 100)
    
    # FASE 1: ANÁLISIS LÉXICO
    print("\n" + "-" * 100)
    print("FASE 1: ANÁLISIS LÉXICO")
    print("-" * 100)
    
    print("\n>>> CÓDIGO FUENTE <<<")
    print(codigo)
    
    lexer = AnalizadorLexico()
    tokens = lexer.tokenizar(codigo)
    
    if lexer.errores:
        print(f"\n✗ Errores léxicos: {len(lexer.errores)}")
        for e in lexer.errores:
            print(f"  {e}")
        return False
    
    print(f"\n✓ Tokens generados: {len(tokens)}")
    print("\n>>> LISTADO DE TOKENS <<<")
    for i, tok in enumerate(tokens, 1):
        if tok.tipo.value != 'EOF':
            reservada = " [RESERVADA]" if tok.es_reservada else ""
            print(f"{i:2}. {tok.lexema:<15} {tok.tipo.value:<15} {tok.tk:<8} L{tok.linea}:C{tok.columna}{reservada}")
    
    # FASE 2: ANÁLISIS SINTÁCTICO
    print("\n" + "-" * 100)
    print("FASE 2: ANÁLISIS SINTÁCTICO")
    print("-" * 100)
    
    parser = Parser(tokens)
    arbol = parser.parsear()
    
    if parser.errores:
        print(f"\n✗ Errores sintácticos: {len(parser.errores)}")
        parser.imprimir_errores()
        return False
    
    print("\n✓ Análisis sintáctico exitoso")
    
    # FASE 3: VISUALIZACIÓN DEL AST
    print("\n" + "-" * 100)
    print("FASE 3: ÁRBOL DE SINTAXIS ABSTRACTA (AST)")
    print("-" * 100)
    print()
    parser.imprimir_arbol()
    
    # FASE 4: ANÁLISIS DEL AST
    print("\n" + "-" * 100)
    print("FASE 4: ANÁLISIS DEL AST")
    print("-" * 100)
    
    print(f"\n✓ Raíz del AST: {parser.arbol_ast}")
    print(f"✓ Total de sentencias: {len(parser.arbol_ast.sentencias)}")
    
    print("\n>>> DESGLOSE DE SENTENCIAS <<<")
    for i, stmt in enumerate(parser.arbol_ast.sentencias, 1):
        print(f"\n{i}. {stmt.__class__.__name__}")
        if hasattr(stmt, 'identificador'):
            print(f"   Identificador: {stmt.identificador.lexema}")
        if hasattr(stmt, 'tipo_token'):
            print(f"   Tipo: {stmt.tipo_token.lexema}")
        if hasattr(stmt, 'condicion'):
            print(f"   Condición: {stmt.condicion.__class__.__name__}")
        if hasattr(stmt, 'bloque'):
            print(f"   Sentencias en bloque: {len(stmt.bloque)}")
        if hasattr(stmt, 'bloque_if'):
            print(f"   Sentencias en IF: {len(stmt.bloque_if)}")
        if hasattr(stmt, 'bloque_else') and stmt.bloque_else:
            print(f"   Sentencias en ELSE: {len(stmt.bloque_else)}")
    
    print("\n" + "=" * 100)
    print("✓ ANÁLISIS COMPLETADO EXITOSAMENTE")
    print("=" * 100)
    
    return True


if __name__ == "__main__":
    analizar_y_mostrar(codigo)
