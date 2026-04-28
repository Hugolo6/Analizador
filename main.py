
from lexico.reservadas import AnalizadorLexico, listar_palabras_reservadas
from lexico.Oplogicos import listar_operadores_logicos
 
 
def main():
    print("=" * 100)
    print("ANALIZADOR LÉXICO PARA COMPILADOR")
    print("=" * 100)
 
    # 1. Mostrar tablas de tokens reconocidos
    print("\n>>> PALABRAS RESERVADAS, TIPOS DE DATO Y OPERADORES SIMPLES <<<")
    listar_palabras_reservadas()
 
    print("\n>>> OPERADORES DE COMPARACIÓN Y LÓGICOS <<<")
    listar_operadores_logicos()
 
    # 2. Ejemplo de análisis sobre código fuente
    codigo_fuente = """
start
    Int x = 10;
    Int y = 20;
    float promedio = 0;
    if x <= y {
        promedio = x + y;
        imprimir(promedio);
    }
    while x > 0 {
        leer(x);
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