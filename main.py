from semantico.analizador import AnalizadorSemantico
from lexico.reservadas import AnalizadorLexico, listar_palabras_reservadas
from lexico.Oplogicos import listar_operadores_logicos
from sintactico.parser import Parser


def main():
    print("=" * 100)
    print("ANALIZADOR LÉXICO Y SINTÁCTICO")
    print("=" * 100)
    
    # 1. Mostrar tablas de tokens reconocidos
    """
    print("\n>>> PALABRAS RESERVADAS, TIPOS DE DATO Y OPERADORES SIMPLES <<<")
    listar_palabras_reservadas()
    
    print("\n>>> OPERADORES DE COMPARACIÓN Y LÓGICOS <<<")
    listar_operadores_logicos()
    """
    
    # 2. Ejemplo de análisis sobre código fuente CORRECTO
    codigo_fuente_valido = """
    
anb
    gz x = 10;
    gz y = 20;
    fl promedio = 0;
    wen x <= y {
        promedio = x + y;
        dru (promedio);
    }
    war x > 0 {
        les(x);
        x = x - 1;
    }
end
"""
    
    analizar_programa(codigo_fuente_valido)
    
    # 3. Ejemplo con errores sintácticos
    print("\n" + "=" * 100)
    print("EJEMPLO CON ERRORES SINTÁCTICOS")
    print("=" * 100)
    
    codigo_con_errores = """
anb
    gz x = 7
    wen x > 5 {
        dru(x);
    
end
"""
    
    analizar_programa(codigo_con_errores)


def analizar_programa(codigo_fuente):
    """Analiza un programa en el lenguaje definido."""
    print("\n>>> CÓDIGO FUENTE A ANALIZAR <<<")
    print(codigo_fuente)
    
    # FASE 1: ANÁLISIS LÉXICO
    analizador_lexico = AnalizadorLexico()
    tokens = analizador_lexico.tokenizar(codigo_fuente)
    
    if analizador_lexico.errores:
        print("\n>>> ERRORES LÉXICOS <<<")
        analizador_lexico.imprimir_errores()
        print(f"\nNo se puede proceder al análisis sintáctico debido a errores léxicos.")
        return
        
    # FASE 2: ANÁLISIS SINTÁCTICO
    print("\n" + "=" * 100)
    print("ANÁLISIS SINTÁCTICO")
    print("=" * 100)
    
    parser = Parser(tokens)
    arbol = parser.parsear()
    
    if parser.errores:
        print("\n[ERROR] Se encontraron ERRORES SINTÁCTICOS:")
        parser.imprimir_errores()
        return # Detenemos aquí si hay errores sintácticos
        
    print("[OK] Análisis sintáctico exitoso")
    
    # FASE 3: ANÁLISIS SEMÁNTICO (Aquí entras tú)
    print("\n" + "=" * 100)
    print("ANÁLISIS SEMÁNTICO")
    print("=" * 100)
    
    analizador_semantico = AnalizadorSemantico()
    errores_semanticos = analizador_semantico.analizar(arbol)
    
    if errores_semanticos:
        print("\n[ERROR] Se encontraron ERRORES SEMÁNTICOS:")
        for error in errores_semanticos:
            print(error)
    else:
        print("[OK] Análisis semántico exitoso. El código es 100% válido.")

if __name__ == "__main__":
    main()
