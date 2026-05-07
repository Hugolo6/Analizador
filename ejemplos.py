# ===========================================================================
# EJEMPLOS DE PROGRAMAS PARA PROBAR EL PARSER
# ===========================================================================
# Este archivo contiene ejemplos de código válido e inválido
# para probar el analizador sintáctico.
# ===========================================================================

EJEMPLOS_VALIDOS = {
    "simple_declaracion": """
anb
    gz x = 10;
end
""",
    
    "multiples_declaraciones": """
anb
    gz x = 5;
    fl y = 3.14;
    str nombre = texto;
end
""",
    
    "asignacion": """
anb
    gz x = 10;
    x = 20;
    x = x + 5;
end
""",
    
    "expresion_aritmetica": """
anb
    gz resultado = 2 + 3 * 4;
    resultado = (5 + 6) * 7;
    resultado = -10 + 20;
end
""",
    
    "condicional_if": """
anb
    gz edad = 18;
    wen edad >= 18 {
        dru(edad);
    }
end
""",
    
    "condicional_if_else": """
anb
    gz x = 5;
    wen x > 10 {
        dru(x);
    } son {
        dru(0);
    }
end
""",
    
    "bucle_while": """
anb
    gz i = 1;
    war i <= 5 {
        dru(i);
        i = i + 1;
    }
end
""",
    
    "bucle_for": """
anb
    gz suma = 0;
    fur (i = 0; i < 10; i = i + 1) {
        suma = suma + i;
    }
    dru(suma);
end
""",
    
    "lectura": """
anb
    gz numero = 0;
    les(numero);
    dru(numero);
end
""",
    
    "escribir_expresion": """
anb
    gz x = 10;
    gz y = 20;
    dru(x + y);
    dru(x - y);
end
""",
    
    "operadores_logicos": """
anb
    gz a = 1;
    gz b = 0;
    wen a && b {
        dru(a);
    }
    wen a || b {
        dru(b);
    }
end
""",
    
    "comparaciones": """
anb
    gz x = 10;
    wen x == 10 {
        dru(x);
    }
    wen x < 15 {
        dru(x);
    }
    wen x > 5 {
        dru(x);
    }
end
""",
    
    "anidado": """
anb
    gz x = 5;
    wen x > 0 {
        wen x > 3 {
            dru(x);
        } son {
            dru(0);
        }
    }
end
""",
    
    "complejo": """
anb
    gz suma = 0;
    gz i = 1;
    war i <= 100 {
        wen i % 2 == 0 {
            suma = suma + i;
        }
        i = i + 1;
    }
    dru(suma);
end
""",
}

EJEMPLOS_INVALIDOS = {
    "falta_inicializacion": """
anb
    gz x;
end
""",
    
    "falta_punto_y_coma": """
anb
    gz x = 10
    dru(x);
end
""",
    
    "falta_asignacion": """
anb
    gz x =;
end
""",
    
    "parentesis_no_cerrado": """
anb
    dru(x;
end
""",
    
    "llave_no_cerrada": """
anb
    wen x > 5 {
        dru(x);
end
""",
    
    "operador_faltante": """
anb
    gz x = 5 3;
end
""",
    
    "falta_end": """
anb
    gz x = 10;
    dru(x);
""",
    
    "condicion_vacia": """
anb
    wen {
        dru(x);
    }
end
""",
    
    "for_incorrecto": """
anb
    fur i = 0; i < 10; i = i + 1 {
        dru(i);
    }
end
""",
    
    "identificador_esperado": """
anb
    les(10);
end
""",
}


def obtener_ejemplo_valido(nombre):
    """Obtiene un ejemplo válido por nombre."""
    return EJEMPLOS_VALIDOS.get(nombre, None)


def obtener_ejemplo_invalido(nombre):
    """Obtiene un ejemplo inválido por nombre."""
    return EJEMPLOS_INVALIDOS.get(nombre, None)


def listar_ejemplos():
    """Lista todos los ejemplos disponibles."""
    print("\n" + "=" * 80)
    print("EJEMPLOS VÁLIDOS")
    print("=" * 80)
    for nombre in EJEMPLOS_VALIDOS.keys():
        print(f"  • {nombre}")
    
    print("\n" + "=" * 80)
    print("EJEMPLOS INVÁLIDOS")
    print("=" * 80)
    for nombre in EJEMPLOS_INVALIDOS.keys():
        print(f"  • {nombre}")


if __name__ == "__main__":
    listar_ejemplos()
