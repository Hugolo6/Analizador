#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lexico.reservadas import AnalizadorLexico, listar_palabras_reservadas, Token

def main():
    """Función principal para demostrar el uso del analizador léxico"""
    
    print("=" * 100)
    print("ANALIZADOR LÉXICO PARA COMPILADOR - PALABRAS RESERVADAS")
    print("=" * 100)
    
    # Listar las palabras reservadas disponibles
    listar_palabras_reservadas()
    
    # Crear una instancia del analizador
    analizador = AnalizadorLexico()
    
    # Ejemplos de análisis con palabras reservadas y tipos de datos
    ejemplos = [
        # Ejemplo 1: Palabras reservadas básicas
        "Int String float leer imprimir",
        
        # Ejemplo 2: Variables e identificadores
        "variable1 nombre edad texto",
        
        # Ejemplo 3: Números enteros
        "123 45 789",
        
        # Ejemplo 4: Letras puras
        "abc xyz",
        
        # Ejemplo 5: Mezcla válida
        "Int x nombre 25",
        
        # Ejemplo 6: Con error - número inválido
        "2variable 5prueba",
    ]
    
    for ejemplo in ejemplos:
        print(f"\nAnalizando: '{ejemplo}'")
        print("─" * 100)
        
        analizador.analizar(ejemplo)
        print(analizador.obtener_reporte())
        
        # Mostrar tokens en formato JSON para usar en siguientes fases
        if analizador.tokens:
            print("Tokens en formato JSON (para siguientes fases del compilador):")
            print("-" * 100)
            for token in analizador.tokens:
                print(f"  {token.to_dict()}")
        
        print("\n" + "="*100)


if __name__ == "__main__":
    main()


