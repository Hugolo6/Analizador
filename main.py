

from lexico.reservadas import AnalizadorLexico, listar_palabras_reservadas, Token

def main():
  
    
    print("=" * 100)
    print("ANALIZADOR LÉXICO PARA COMPILADOR - PALABRAS RESERVADAS")
    print("=" * 100)
    
    # Listar las palabras reservadas disponibles
    listar_palabras_reservadas()
    
    # Crear una instancia del analizador
    analizador = AnalizadorLexico()
    
    
  

if __name__ == "__main__":
    main()


