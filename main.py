
from lexico.reservadas import AnalizadorLexico, listar_palabras_reservadas
from lexico.Oplogicos import listar_operadores_logicos
 
 
def main():
    print("=" * 100)
    print("ANALIZADOR LÉXICO")
    print("=" * 100)
 
    # 1. Mostrar tablas de tokens reconocidos
    print("\n>>> PALABRAS RESERVADAS, TIPOS DE DATO Y OPERADORES SIMPLES <<<")
    listar_palabras_reservadas()
 
    print("\n>>> OPERADORES DE COMPARACIÓN Y LÓGICOS <<<")
    listar_operadores_logicos()
 
    # 2. Ejemplo de análisis sobre código fuente
    codigo_fuente = """
anf
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
 
    print("\n>>> CÓDIGO FUENTE A ANALIZAR <<<")
    print(codigo_fuente)
 
    analizador = AnalizadorLexico()
    tokens = analizador.tokenizar(codigo_fuente)
 
    print(">>> TOKENS GENERADOS <<<")
    analizador.imprimir_tokens()
 
    print("\n>>> ERRORES LÉXICOS <<<")
    analizador.imprimir_errores()
 
    print(f"\nTotal tokens : {len(tokens)}")
    print(f"Total errores: {len(analizador.errores)}")
 
 
if __name__ == "__main__":
    main()