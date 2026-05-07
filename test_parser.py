#!/usr/bin/env python3
# ===========================================================================
# SCRIPT DE PRUEBA INTERACTIVO DEL PARSER
# ===========================================================================
# Uso: python test_parser.py [ejemplo]
# ===========================================================================

import sys
from lexico.reservadas import AnalizadorLexico
from sintactico.parser import Parser
from ejemplos import obtener_ejemplo_valido, obtener_ejemplo_invalido, listar_ejemplos


def analizar_programa(codigo_fuente, nombre_ejemplo=""):
    """
    Analiza un programa completo (léxico + sintáctico).
    
    Args:
        codigo_fuente: Código a analizar
        nombre_ejemplo: Nombre del ejemplo (para documentación)
    """
    
    titulo = f"ANALIZANDO: {nombre_ejemplo}" if nombre_ejemplo else "ANALIZANDO CÓDIGO"
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)
    
    print("\n>>> CÓDIGO FUENTE <<<")
    print(codigo_fuente)
    
    # ========================================================================
    # FASE 1: ANÁLISIS LÉXICO
    # ========================================================================
    print("\n" + "-" * 80)
    print("FASE 1: ANÁLISIS LÉXICO")
    print("-" * 80)
    
    lexer = AnalizadorLexico()
    tokens = lexer.tokenizar(codigo_fuente)
    
    print(f"\n✓ Tokens generados: {len(tokens)}")
    
    if lexer.errores:
        print(f"\n✗ Errores léxicos encontrados: {len(lexer.errores)}")
        lexer.imprimir_errores()
        return False
    
    print("\n>>> LISTADO DE TOKENS <<<")
    lexer.imprimir_tokens()
    
    # ========================================================================
    # FASE 2: ANÁLISIS SINTÁCTICO
    # ========================================================================
    print("\n" + "-" * 80)
    print("FASE 2: ANÁLISIS SINTÁCTICO")
    print("-" * 80)
    
    parser = Parser(tokens)
    arbol = parser.parsear()
    
    if parser.errores:
        print(f"\n✗ Errores sintácticos encontrados: {len(parser.errores)}")
        parser.imprimir_errores()
        return False
    
    print("\n✓ Análisis sintáctico exitoso")
    
    # ========================================================================
    # VISUALIZACIÓN DEL AST
    # ========================================================================
    print("\n" + "-" * 80)
    print("ÁRBOL DE SINTAXIS ABSTRACTA (AST)")
    print("-" * 80)
    print()
    parser.imprimir_arbol()
    
    return True


def main():
    """Función principal."""
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 80)
        print("PROBADOR DE PARSER - ANALIZADOR SINTÁCTICO")
        print("=" * 80)
        print("\nUso:")
        print("  python test_parser.py <ejemplo>")
        print("  python test_parser.py --valid <nombre>    # Ejemplos válidos")
        print("  python test_parser.py --invalid <nombre>  # Ejemplos inválidos")
        print("  python test_parser.py --list               # Listar ejemplos")
        print("  python test_parser.py --all                # Probar todos")
        print()
        print("Ejemplos de uso:")
        print("  python test_parser.py --list")
        print("  python test_parser.py --valid simple_declaracion")
        print("  python test_parser.py --invalid falta_punto_y_coma")
        print()
        return
    
    opcion = sys.argv[1]
    
    # ========================================================================
    # LISTAR EJEMPLOS
    # ========================================================================
    if opcion == "--list":
        listar_ejemplos()
        return
    
    # ========================================================================
    # PROBAR UN EJEMPLO VÁLIDO
    # ========================================================================
    elif opcion == "--valid":
        if len(sys.argv) < 3:
            print("Error: Especifica el nombre del ejemplo")
            print("Uso: python test_parser.py --valid <nombre>")
            return
        
        nombre = sys.argv[2]
        codigo = obtener_ejemplo_valido(nombre)
        
        if codigo is None:
            print(f"Error: Ejemplo válido '{nombre}' no encontrado")
            listar_ejemplos()
            return
        
        analizar_programa(codigo, f"Ejemplo válido: {nombre}")
    
    # ========================================================================
    # PROBAR UN EJEMPLO INVÁLIDO
    # ========================================================================
    elif opcion == "--invalid":
        if len(sys.argv) < 3:
            print("Error: Especifica el nombre del ejemplo")
            print("Uso: python test_parser.py --invalid <nombre>")
            return
        
        nombre = sys.argv[2]
        codigo = obtener_ejemplo_invalido(nombre)
        
        if codigo is None:
            print(f"Error: Ejemplo inválido '{nombre}' no encontrado")
            listar_ejemplos()
            return
        
        analizar_programa(codigo, f"Ejemplo inválido: {nombre}")
    
    # ========================================================================
    # PROBAR TODOS LOS EJEMPLOS
    # ========================================================================
    elif opcion == "--all":
        print("\n" + "=" * 80)
        print("PROBANDO TODOS LOS EJEMPLOS")
        print("=" * 80)
        
        estadisticas = {
            "validos_exito": 0,
            "validos_error": 0,
            "invalidos_error": 0,
            "invalidos_detecto_error": 0,
        }
        
        # Ejemplos válidos
        print("\n" + "=" * 80)
        print("EJEMPLOS VÁLIDOS")
        print("=" * 80)
        
        for nombre, codigo in obtener_ejemplo_valido("simple_declaracion").__class__.__dict__.items():
            if nombre.startswith("_"):
                continue
        
        from ejemplos import EJEMPLOS_VALIDOS, EJEMPLOS_INVALIDOS
        
        for nombre, codigo in EJEMPLOS_VALIDOS.items():
            exito = analizar_programa(codigo, f"[VÁLIDO] {nombre}")
            if exito:
                estadisticas["validos_exito"] += 1
            else:
                estadisticas["validos_error"] += 1
        
        # Ejemplos inválidos
        print("\n" + "=" * 80)
        print("EJEMPLOS INVÁLIDOS (deben fallar)")
        print("=" * 80)
        
        for nombre, codigo in EJEMPLOS_INVALIDOS.items():
            exito = analizar_programa(codigo, f"[INVÁLIDO] {nombre}")
            if not exito:  # Esperamos que fallen
                estadisticas["invalidos_detecto_error"] += 1
            else:
                estadisticas["invalidos_error"] += 1
        
        # Resumen
        print("\n" + "=" * 80)
        print("RESUMEN DE PRUEBAS")
        print("=" * 80)
        print(f"Ejemplos válidos exitosos:        {estadisticas['validos_exito']}")
        print(f"Ejemplos válidos con error:       {estadisticas['validos_error']}")
        print(f"Ejemplos inválidos que fallaron:  {estadisticas['invalidos_detecto_error']}")
        print(f"Ejemplos inválidos que NO fallaron: {estadisticas['invalidos_error']}")
        
        total_correcto = (
            estadisticas['validos_exito'] + 
            estadisticas['invalidos_detecto_error']
        )
        total_ejemplos = (
            len(EJEMPLOS_VALIDOS) + 
            len(EJEMPLOS_INVALIDOS)
        )
        
        print(f"\nTasa de éxito: {total_correcto}/{total_ejemplos} ({100*total_correcto//total_ejemplos}%)")
    
    # ========================================================================
    # ENTRADA PERSONALIZADA
    # ========================================================================
    elif opcion == "--custom":
        print("Modo personalizado: Ingresa tu código (Ctrl+D para terminar):")
        print("=" * 80)
        try:
            codigo = sys.stdin.read()
            analizar_programa(codigo, "Código personalizado")
        except KeyboardInterrupt:
            print("\nCancelado por el usuario")
    
    # ========================================================================
    # ASUMIR QUE ES UN EJEMPLO VÁLIDO
    # ========================================================================
    else:
        codigo = obtener_ejemplo_valido(opcion)
        if codigo is None:
            codigo = obtener_ejemplo_invalido(opcion)
        
        if codigo is None:
            print(f"Error: Ejemplo '{opcion}' no encontrado")
            listar_ejemplos()
            return
        
        analizar_programa(codigo, f"Ejemplo: {opcion}")


if __name__ == "__main__":
    main()
