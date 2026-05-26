# ===========================================================================
# ANALIZADOR SINTÁCTICO - PARSER DESCENDENTE RECURSIVO
# ===========================================================================
# Reconoce la gramática libre de contexto del lenguaje definido en el Lexer.
# Genera un Árbol de Sintaxis Abstracta (AST) completo.
# Incluye manejo robusto de errores sintácticos.
# ===========================================================================

from enum import Enum
from lexico.reservadas import TipoToken


# ===========================================================================
# NODOS DEL ÁRBOL DE SINTAXIS ABSTRACTA (AST)
# ===========================================================================

class NodoAST:
    """Clase base para todos los nodos del AST."""
    def __repr__(self):
        return f"{self.__class__.__name__}"


class Programa(NodoAST):
    """Nodo raíz del programa."""
    def __init__(self, sentencias):
        self.sentencias = sentencias  # List[Sentencia]
    
    def __repr__(self):
        return f"Programa(sentencias={len(self.sentencias)})"


class Sentencia(NodoAST):
    """Clase base para todas las sentencias."""
    pass


class Declaracion(Sentencia):
    """Declaración de variable: tipo IDENTIFICADOR = EXPRESION;"""
    def __init__(self, tipo_token, identificador, expresion):
        self.tipo_token = tipo_token  # Token del tipo (gz, fl, str)
        self.identificador = identificador  # Token del identificador
        self.expresion = expresion  # NodoAST (Expresión)
    
    def __repr__(self):
        return f"Declaracion(tipo={self.tipo_token.lexema}, id={self.identificador.lexema})"


class Asignacion(Sentencia):
    """Asignación a variable: IDENTIFICADOR = EXPRESION;"""
    def __init__(self, identificador, expresion):
        self.identificador = identificador  # Token del identificador
        self.expresion = expresion  # NodoAST (Expresión)
    
    def __repr__(self):
        return f"Asignacion(id={self.identificador.lexema})"


class IfStatement(Sentencia):
    """Condicional: if CONDICION { BLOQUE } [else { BLOQUE }]"""
    def __init__(self, condicion, bloque_if, bloque_else=None):
        self.condicion = condicion  # NodoAST (Expresión)
        self.bloque_if = bloque_if  # List[Sentencia]
        self.bloque_else = bloque_else  # List[Sentencia] o None
    
    def __repr__(self):
        return f"IfStatement(tiene_else={self.bloque_else is not None})"


class WhileStatement(Sentencia):
    """Bucle: while CONDICION { BLOQUE }"""
    def __init__(self, condicion, bloque):
        self.condicion = condicion  # NodoAST (Expresión)
        self.bloque = bloque  # List[Sentencia]
    
    def __repr__(self):
        return f"WhileStatement()"


class ForStatement(Sentencia):
    """Bucle for: for (ASIGNACION; CONDICION; ASIGNACION) { BLOQUE }"""
    def __init__(self, inicializacion, condicion, actualizacion, bloque):
        self.inicializacion = inicializacion  # NodoAST
        self.condicion = condicion  # NodoAST
        self.actualizacion = actualizacion  # NodoAST
        self.bloque = bloque  # List[Sentencia]
    
    def __repr__(self):
        return f"ForStatement()"


class Lectura(Sentencia):
    """Lectura: les(IDENTIFICADOR)"""
    def __init__(self, identificador):
        self.identificador = identificador  # Token
    
    def __repr__(self):
        return f"Lectura(id={self.identificador.lexema})"


class Escritura(Sentencia):
    """Escritura: dru(EXPRESION)"""
    def __init__(self, expresion):
        self.expresion = expresion  # NodoAST (Expresión)
    
    def __repr__(self):
        return f"Escritura()"


# ===========================================================================
# EXPRESIONES
# ===========================================================================

class Expresion(NodoAST):
    """Clase base para expresiones."""
    pass


class ExpresionBinaria(Expresion):
    """Expresión binaria: IZQUIERDA OPERADOR DERECHA"""
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda  # NodoAST (Expresión)
        self.operador = operador  # Token
        self.derecha = derecha  # NodoAST (Expresión)
    
    def __repr__(self):
        return f"ExpBinaria(op={self.operador.lexema})"


class ExpresionUnaria(Expresion):
    """Expresión unaria: OPERADOR OPERANDO"""
    def __init__(self, operador, operando):
        self.operador = operador  # Token
        self.operando = operando  # NodoAST (Expresión)
    
    def __repr__(self):
        return f"ExpUnaria(op={self.operador.lexema})"


class Literal(Expresion):
    """Literal: número, cadena, o identificador"""
    def __init__(self, token):
        self.token = token  # Token (ENTERO, LETRA, IDENTIFICADOR)
    
    def __repr__(self):
        return f"Literal(valor={self.token.lexema})"


class LlamadaFuncion(Expresion):
    """Llamada a función: IDENTIFICADOR(ARGUMENTOS)"""
    def __init__(self, nombre, argumentos):
        self.nombre = nombre  # Token (identificador)
        self.argumentos = argumentos  # List[Expresion]
    
    def __repr__(self):
        return f"LlamadaFuncion(nombre={self.nombre.lexema})"


# ===========================================================================
# CLASE PRINCIPAL DEL PARSER
# ===========================================================================

class Parser:
    """
    Parser descendente recursivo para el lenguaje definido en el Lexer.
    
    GRAMÁTICA (BNF):
    ================
    programa    ::= START cuerpo END
    cuerpo      ::= (sentencia)*
    sentencia   ::= declaracion | asignacion | if_stmt | while_stmt | 
                    for_stmt | lectura | escritura
    
    declaracion ::= tipo IDENTIFICADOR ASIG expresion PUNTO_CON
    asignacion  ::= IDENTIFICADOR ASIG expresion PUNTO_CON
    if_stmt     ::= IF expresion LLAVE_IZQ cuerpo LLAVE_DER 
                    [ELSE LLAVE_IZQ cuerpo LLAVE_DER]
    while_stmt  ::= WHILE expresion LLAVE_IZQ cuerpo LLAVE_DER
    for_stmt    ::= FOR PAR_IZQ asignacion expresion PUNTO_CON 
                    asignacion PAR_DER LLAVE_IZQ cuerpo LLAVE_DER
    lectura     ::= LEER PAR_IZQ IDENTIFICADOR PAR_DER PUNTO_CON
    escritura   ::= IMPRIMIR PAR_IZQ expresion PAR_DER PUNTO_CON
    
    expresion   ::= or_expr
    or_expr     ::= and_expr ((OR | OR2) and_expr)*
    and_expr    ::= comp_expr ((AND | AND2) comp_expr)*
    comp_expr   ::= arit_expr ((IGUAL | MENOR | MAYOR | MENOR_EQ | MAYOR_EQ) 
                               arit_expr)*
    arit_expr   ::= mul_expr ((SUMA | RESTA) mul_expr)*
    mul_expr    ::= unaria_expr ((MULT | DIV) unaria_expr)*
    unaria_expr ::= (RESTA | SUMA)* primaria
    primaria    ::= LITERAL | IDENTIFICADOR | PAR_IZQ expresion PAR_DER |
                    llamada_funcion
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.token_actual = self.tokens[self.posicion] if tokens else None
        self.errores = []
        self.arbol_ast = None  # Árbol generado
    
    # =========================================================================
    # UTILIDADES
    # =========================================================================
    
    def error_sintactico(self, mensaje, token=None):
        """Registra un error sintáctico con contexto."""
        t = token or self.token_actual
        if t:
            error_msg = (
                f"Error Sintáctico [L{t.linea}:C{t.columna}]: {mensaje}\n"
                f"    Token encontrado: '{t.lexema}' (tipo: {t.tipo.value})"
            )
        else:
            error_msg = f"Error Sintáctico: {mensaje}\n    Final inesperado del archivo"
        self.errores.append(error_msg)
    
    def consumir(self, tipo_esperado, nombre_token=None):
        """Consume el token actual si es del tipo esperado, de lo contrario error."""
        if not self.token_actual:
            self.error_sintactico(f"Se esperaba {nombre_token or tipo_esperado.value} pero se encontró EOF")
            return False
        
        if self.token_actual.tipo != tipo_esperado:
            self.error_sintactico(
                f"Se esperaba '{nombre_token or tipo_esperado.value}' "
                f"pero se encontró '{self.token_actual.lexema}'"
            )
            return False
        
        token = self.token_actual
        self.avanzar()
        return token
    
    def avanzar(self):
        """Avanza al siguiente token."""
        self.posicion += 1
        if self.posicion < len(self.tokens):
            self.token_actual = self.tokens[self.posicion]
        else:
            self.token_actual = None
    
    def es_tipo_dato(self):
        """Verifica si el token actual es un tipo de dato."""
        return self.token_actual and self.token_actual.tipo in (
            TipoToken.INT, TipoToken.FLOAT, TipoToken.STRING
        )
    
    def es_operador_binario(self):
        """Verifica si el token actual es un operador binario."""
        return self.token_actual and self.token_actual.tipo in (
            TipoToken.SUMA, TipoToken.RESTA, TipoToken.MULT, TipoToken.DIV,
            TipoToken.IGUAL, TipoToken.MENOR, TipoToken.MAYOR, 
            TipoToken.MENOR_EQ, TipoToken.MAYOR_EQ,
            TipoToken.AND, TipoToken.AND2, TipoToken.OR, TipoToken.OR2
        )
    
    # =========================================================================
    # REGLAS DE LA GRAMÁTICA (ANÁLISIS DESCENDENTE RECURSIVO)
    # =========================================================================
    
    def parsear(self):
        """Punto de entrada: programa -> START cuerpo END"""
        if not self.token_actual:
            self.error_sintactico("Archivo vacío")
            return None
        
        # Esperamos START (anb/anf)
        if not self.consumir(TipoToken.START, "START (anb/anf)"):
            return None
        
        # Analizamos el cuerpo
        sentencias = self.analizar_cuerpo()
        
        # Esperamos END
        if not self.consumir(TipoToken.END, "END (end)"):
            return None
        
        # Creamos el árbol
        self.arbol_ast = Programa(sentencias)
        return self.arbol_ast
    
    def analizar_cuerpo(self):
        """Analiza una secuencia de sentencias: (sentencia)*
        Se detiene cuando encuentra END o LLAVE_DER (cierre de bloque)"""
        sentencias = []
        
        while self.token_actual and self.token_actual.tipo not in (TipoToken.END, TipoToken.LLAVE_DER):
            sentencia = self.analizar_sentencia()
            if sentencia:
                sentencias.append(sentencia)
        
        return sentencias
    
    def analizar_sentencia(self):
        """Determina qué tipo de sentencia procesar."""
        if not self.token_actual:
            return None
        
        tipo = self.token_actual.tipo
        
        # Declaración de variable
        if self.es_tipo_dato():
            return self.analizar_declaracion()
        
        # Condicional if
        elif tipo == TipoToken.IF:
            return self.analizar_if()
        
        # Bucle while
        elif tipo == TipoToken.WHILE:
            return self.analizar_while()
        
        # Bucle for
        elif tipo == TipoToken.FOR:
            return self.analizar_for()
        
        # Lectura (les)
        elif tipo == TipoToken.LEER:
            return self.analizar_lectura()
        
        # Escritura (dru)
        elif tipo == TipoToken.IMPRIMIR:
            return self.analizar_escritura()
        
        # Asignación o expresión
        elif tipo == TipoToken.IDENTIFICADOR:
            return self.analizar_asignacion()
        
        else:
            self.error_sintactico(f"Sentencia inesperada: '{self.token_actual.lexema}'")
            self.avanzar()
            return None
    
    def analizar_declaracion(self):
        """
        declaracion ::= tipo IDENTIFICADOR ASIG expresion PUNTO_CON
        Ejemplo: gz x = 10;
        """
        tipo_token = self.token_actual
        if not self.consumir(tipo_token.tipo):
            return None
        
        id_token = self.consumir(TipoToken.IDENTIFICADOR, "IDENTIFICADOR")
        if not id_token:
            return None
        
        if not self.consumir(TipoToken.ASIG, "= (asignación)"):
            return None
        
        expresion = self.analizar_expresion()
        if not expresion:
            return None
        
        if not self.consumir(TipoToken.PUNTO_CON, "; (punto y coma)"):
            return None
        
        return Declaracion(tipo_token, id_token, expresion)
    
    def analizar_asignacion(self):
        """
        asignacion ::= IDENTIFICADOR ASIG expresion PUNTO_CON
        Ejemplo: x = x + 1;
        """
        id_token = self.consumir(TipoToken.IDENTIFICADOR, "IDENTIFICADOR")
        if not id_token:
            return None
        
        if not self.consumir(TipoToken.ASIG, "= (asignación)"):
            return None
        
        expresion = self.analizar_expresion()
        if not expresion:
            return None
        
        if not self.consumir(TipoToken.PUNTO_CON, "; (punto y coma)"):
            return None
        
        return Asignacion(id_token, expresion)
    
    def analizar_if(self):
        """
        if_stmt ::= IF expresion LLAVE_IZQ cuerpo LLAVE_DER 
                    [ELSE LLAVE_IZQ cuerpo LLAVE_DER]
        Ejemplo: wen x > 5 { ... } son { ... }
        """
        if not self.consumir(TipoToken.IF, "IF (wen)"):
            return None
        
        condicion = self.analizar_expresion()
        if not condicion:
            return None
        
        if not self.consumir(TipoToken.LLAVE_IZQ, "{ (llave izquierda)"):
            return None
        
        bloque_if = self.analizar_cuerpo()
        
        if not self.consumir(TipoToken.LLAVE_DER, "} (llave derecha)"):
            return None
        
        bloque_else = None
        if self.token_actual and self.token_actual.tipo == TipoToken.ELSE:
            self.consumir(TipoToken.ELSE, "ELSE (son)")
            
            if not self.consumir(TipoToken.LLAVE_IZQ, "{ (llave izquierda)"):
                return None
            
            bloque_else = self.analizar_cuerpo()
            
            if not self.consumir(TipoToken.LLAVE_DER, "} (llave derecha)"):
                return None
        
        return IfStatement(condicion, bloque_if, bloque_else)
    
    def analizar_while(self):
        """
        while_stmt ::= WHILE expresion LLAVE_IZQ cuerpo LLAVE_DER
        Ejemplo: war x < 100 { ... }
        """
        if not self.consumir(TipoToken.WHILE, "WHILE (war)"):
            return None
        
        condicion = self.analizar_expresion()
        if not condicion:
            return None
        
        if not self.consumir(TipoToken.LLAVE_IZQ, "{ (llave izquierda)"):
            return None
        
        bloque = self.analizar_cuerpo()
        
        if not self.consumir(TipoToken.LLAVE_DER, "} (llave derecha)"):
            return None
        
        return WhileStatement(condicion, bloque)
    
    def analizar_for(self):
        """
        for_stmt ::= FOR PAR_IZQ inicializacion PUNTO_CON condicion PUNTO_CON 
                     actualizacion PAR_DER LLAVE_IZQ cuerpo LLAVE_DER
        Ejemplo: fur (x = 0; x < 10; x = x + 1) { ... }
        """
        if not self.consumir(TipoToken.FOR, "FOR (fur)"):
            return None
        
        if not self.consumir(TipoToken.PAR_IZQ, "( (paréntesis izquierdo)"):
            return None
        
        # Inicialización: puede ser una asignación o una declaración (ej. gz i = 0)
        inicializacion = None
        if self.token_actual:
            if self.token_actual.tipo == TipoToken.IDENTIFICADOR:
                inicializacion = self.analizar_asignacion_sin_punto()
            elif self.es_tipo_dato():
                inicializacion = self.analizar_declaracion_sin_punto()
        
        if not self.consumir(TipoToken.PUNTO_CON, "; (punto y coma)"):
            return None
        
        # Condición
        condicion = self.analizar_expresion()
        if not condicion:
            return None
        
        if not self.consumir(TipoToken.PUNTO_CON, "; (punto y coma)"):
            return None
        
        # Actualización
        actualizacion = None
        if self.token_actual and self.token_actual.tipo == TipoToken.IDENTIFICADOR:
            actualizacion = self.analizar_asignacion_sin_punto()
        
        if not self.consumir(TipoToken.PAR_DER, ") (paréntesis derecho)"):
            return None
        
        if not self.consumir(TipoToken.LLAVE_IZQ, "{ (llave izquierda)"):
            return None
        
        bloque = self.analizar_cuerpo()
        
        if not self.consumir(TipoToken.LLAVE_DER, "} (llave derecha)"):
            return None
        
        return ForStatement(inicializacion, condicion, actualizacion, bloque)
    
    def analizar_asignacion_sin_punto(self):
        """Analiza una asignación sin punto y coma final (para el FOR)."""
        id_token = self.token_actual
        if id_token.tipo != TipoToken.IDENTIFICADOR:
            return None
        
        self.avanzar()
        
        if not self.consumir(TipoToken.ASIG, "= (asignación)"):
            return None
        
        expresion = self.analizar_expresion()
        return Asignacion(id_token, expresion) if expresion else None

    def analizar_declaracion_sin_punto(self):
        """
        Analiza una declaración dentro de un contexto sin punto y coma final
        (por ejemplo, la inicialización dentro de un `for`).
        Forma: tipo IDENTIFICADOR ASIG expresion
        """
        tipo_token = self.token_actual
        if not self.es_tipo_dato():
            return None

        # Consumimos el token de tipo (gz, fl, str)
        if not self.consumir(tipo_token.tipo):
            return None

        id_token = self.consumir(TipoToken.IDENTIFICADOR, "IDENTIFICADOR")
        if not id_token:
            return None

        if not self.consumir(TipoToken.ASIG, "= (asignación)"):
            return None

        expresion = self.analizar_expresion()
        if not expresion:
            return None

        return Declaracion(tipo_token, id_token, expresion)
    
    def analizar_lectura(self):
        """
        lectura ::= LEER PAR_IZQ IDENTIFICADOR PAR_DER PUNTO_CON
        Ejemplo: les(x);
        """
        if not self.consumir(TipoToken.LEER, "LEER (les)"):
            return None
        
        if not self.consumir(TipoToken.PAR_IZQ, "( (paréntesis izquierdo)"):
            return None
        
        id_token = self.consumir(TipoToken.IDENTIFICADOR, "IDENTIFICADOR")
        if not id_token:
            return None
        
        if not self.consumir(TipoToken.PAR_DER, ") (paréntesis derecho)"):
            return None
        
        if not self.consumir(TipoToken.PUNTO_CON, "; (punto y coma)"):
            return None
        
        return Lectura(id_token)
    
    def analizar_escritura(self):
        """
        escritura ::= IMPRIMIR PAR_IZQ expresion PAR_DER PUNTO_CON
        Ejemplo: dru(x + 5);
        """
        if not self.consumir(TipoToken.IMPRIMIR, "IMPRIMIR (dru)"):
            return None
        
        if not self.consumir(TipoToken.PAR_IZQ, "( (paréntesis izquierdo)"):
            return None
        
        expresion = self.analizar_expresion()
        if not expresion:
            return None
        
        if not self.consumir(TipoToken.PAR_DER, ") (paréntesis derecho)"):
            return None
        
        if not self.consumir(TipoToken.PUNTO_CON, "; (punto y coma)"):
            return None
        
        return Escritura(expresion)
    
    # =========================================================================
    # ANÁLISIS DE EXPRESIONES (Precedencia de operadores)
    # =========================================================================
    
    def analizar_expresion(self):
        """Punto de entrada para expresiones: or_expr"""
        return self.analizar_or_expr()
    
    def analizar_or_expr(self):
        """or_expr ::= and_expr ((OR | OR2) and_expr)*"""
        izquierda = self.analizar_and_expr()
        if not izquierda:
            return None
        
        while self.token_actual and self.token_actual.tipo in (TipoToken.OR, TipoToken.OR2):
            operador = self.token_actual
            self.avanzar()
            derecha = self.analizar_and_expr()
            if not derecha:
                return None
            izquierda = ExpresionBinaria(izquierda, operador, derecha)
        
        return izquierda
    
    def analizar_and_expr(self):
        """and_expr ::= comp_expr ((AND | AND2) comp_expr)*"""
        izquierda = self.analizar_comp_expr()
        if not izquierda:
            return None
        
        while self.token_actual and self.token_actual.tipo in (TipoToken.AND, TipoToken.AND2):
            operador = self.token_actual
            self.avanzar()
            derecha = self.analizar_comp_expr()
            if not derecha:
                return None
            izquierda = ExpresionBinaria(izquierda, operador, derecha)
        
        return izquierda
    
    def analizar_comp_expr(self):
        """comp_expr ::= arit_expr ((IGUAL | <, >, <=, >=) arit_expr)*"""
        izquierda = self.analizar_arit_expr()
        if not izquierda:
            return None
        
        while self.token_actual and self.token_actual.tipo in (
            TipoToken.IGUAL, TipoToken.MENOR, TipoToken.MAYOR,
            TipoToken.MENOR_EQ, TipoToken.MAYOR_EQ
        ):
            operador = self.token_actual
            self.avanzar()
            derecha = self.analizar_arit_expr()
            if not derecha:
                return None
            izquierda = ExpresionBinaria(izquierda, operador, derecha)
        
        return izquierda
    
    def analizar_arit_expr(self):
        """arit_expr ::= mul_expr ((SUMA | RESTA) mul_expr)*"""
        izquierda = self.analizar_mul_expr()
        if not izquierda:
            return None
        
        while self.token_actual and self.token_actual.tipo in (TipoToken.SUMA, TipoToken.RESTA):
            operador = self.token_actual
            self.avanzar()
            derecha = self.analizar_mul_expr()
            if not derecha:
                return None
            izquierda = ExpresionBinaria(izquierda, operador, derecha)
        
        return izquierda
    
    def analizar_mul_expr(self):
        """mul_expr ::= unaria_expr ((MULT | DIV) unaria_expr)*"""
        izquierda = self.analizar_unaria_expr()
        if not izquierda:
            return None
        
        while self.token_actual and self.token_actual.tipo in (TipoToken.MULT, TipoToken.DIV):
            operador = self.token_actual
            self.avanzar()
            derecha = self.analizar_unaria_expr()
            if not derecha:
                return None
            izquierda = ExpresionBinaria(izquierda, operador, derecha)
        
        return izquierda
    
    def analizar_unaria_expr(self):
        """unaria_expr ::= (RESTA | SUMA)* primaria"""
        operadores = []
        
        while self.token_actual and self.token_actual.tipo in (TipoToken.SUMA, TipoToken.RESTA):
            operadores.append(self.token_actual)
            self.avanzar()
        
        primaria = self.analizar_primaria()
        if not primaria:
            return None
        
        # Aplicamos los operadores unarios de derecha a izquierda
        for operador in reversed(operadores):
            primaria = ExpresionUnaria(operador, primaria)
        
        return primaria
    
    def analizar_primaria(self):
        """primaria ::= LITERAL | IDENTIFICADOR | PAR_IZQ expresion PAR_DER | llamada_funcion"""
        if not self.token_actual:
            self.error_sintactico("Se esperaba una expresión pero se encontró EOF")
            return None
        
        tipo = self.token_actual.tipo
        
        # Literal entero
        if tipo == TipoToken.ENTERO:
            token = self.token_actual
            self.avanzar()
            return Literal(token)
        
        # Literal letra/cadena
        elif tipo == TipoToken.LETRA:
            token = self.token_actual
            self.avanzar()
            return Literal(token)
        
        # Identificador o llamada de función
        elif tipo == TipoToken.IDENTIFICADOR:
            id_token = self.token_actual
            self.avanzar()
            
            # Verificamos si es una llamada de función
            if self.token_actual and self.token_actual.tipo == TipoToken.PAR_IZQ:
                self.avanzar()  # Consumimos (
                argumentos = []
                
                # Parseamos argumentos
                if self.token_actual and self.token_actual.tipo != TipoToken.PAR_DER:
                    expresion = self.analizar_expresion()
                    if expresion:
                        argumentos.append(expresion)
                    
                    while self.token_actual and self.token_actual.tipo == TipoToken.COMA:
                        self.avanzar()  # Consumimos ,
                        expresion = self.analizar_expresion()
                        if expresion:
                            argumentos.append(expresion)
                
                if not self.consumir(TipoToken.PAR_DER, ") (paréntesis derecho)"):
                    return None
                
                return LlamadaFuncion(id_token, argumentos)
            
            return Literal(id_token)
        
        # Expresión entre paréntesis
        elif tipo == TipoToken.PAR_IZQ:
            self.avanzar()  # Consumimos (
            expresion = self.analizar_expresion()
            if not expresion:
                return None
            
            if not self.consumir(TipoToken.PAR_DER, ") (paréntesis derecho)"):
                return None
            
            return expresion
        
        else:
            self.error_sintactico(f"Expresión inesperada: '{self.token_actual.lexema}'")
            return None
    
    # =========================================================================
    # UTILIDADES PARA DEPURACIÓN Y REPORTE
    # =========================================================================
    
    def imprimir_errores(self):
        """Imprime todos los errores sintácticos encontrados."""
        if not self.errores:
            print("No se encontraron errores sintácticos.")
        else:
            print("\n" + "=" * 80)
            print("ERRORES SINTÁCTICOS DETECTADOS")
            print("=" * 80)
            for i, error in enumerate(self.errores, 1):
                print(f"\n[Error {i}]")
                print(error)
            print("\n" + "=" * 80)
    
    def imprimir_arbol(self, nodo=None, nivel=0):
        """Imprime el AST en forma de árbol indentado."""
        if nodo is None:
            nodo = self.arbol_ast
        
        if nodo is None:
            print("AST vacío")
            return
        
        indentacion = "  " * nivel
        
        if isinstance(nodo, Programa):
            print(f"{indentacion}Programa")
            for sentencia in nodo.sentencias:
                self.imprimir_arbol(sentencia, nivel + 1)
        
        elif isinstance(nodo, Declaracion):
            print(f"{indentacion}Declaracion: {nodo.identificador.lexema} ({nodo.tipo_token.lexema})")
            self.imprimir_arbol(nodo.expresion, nivel + 1)
        
        elif isinstance(nodo, Asignacion):
            print(f"{indentacion}Asignacion: {nodo.identificador.lexema}")
            self.imprimir_arbol(nodo.expresion, nivel + 1)
        
        elif isinstance(nodo, IfStatement):
            print(f"{indentacion}If")
            print(f"{indentacion}  Condicion:")
            self.imprimir_arbol(nodo.condicion, nivel + 2)
            print(f"{indentacion}  Bloque If:")
            for stmt in nodo.bloque_if:
                self.imprimir_arbol(stmt, nivel + 2)
            if nodo.bloque_else:
                print(f"{indentacion}  Bloque Else:")
                for stmt in nodo.bloque_else:
                    self.imprimir_arbol(stmt, nivel + 2)
        
        elif isinstance(nodo, WhileStatement):
            print(f"{indentacion}While")
            print(f"{indentacion}  Condicion:")
            self.imprimir_arbol(nodo.condicion, nivel + 2)
            print(f"{indentacion}  Bloque:")
            for stmt in nodo.bloque:
                self.imprimir_arbol(stmt, nivel + 2)
        
        elif isinstance(nodo, ForStatement):
            print(f"{indentacion}For")
            if nodo.inicializacion:
                print(f"{indentacion}  Inicializacion:")
                self.imprimir_arbol(nodo.inicializacion, nivel + 2)
            print(f"{indentacion}  Condicion:")
            self.imprimir_arbol(nodo.condicion, nivel + 2)
            if nodo.actualizacion:
                print(f"{indentacion}  Actualizacion:")
                self.imprimir_arbol(nodo.actualizacion, nivel + 2)
            print(f"{indentacion}  Bloque:")
            for stmt in nodo.bloque:
                self.imprimir_arbol(stmt, nivel + 2)
        
        elif isinstance(nodo, Lectura):
            print(f"{indentacion}Lectura: {nodo.identificador.lexema}")
        
        elif isinstance(nodo, Escritura):
            print(f"{indentacion}Escritura")
            self.imprimir_arbol(nodo.expresion, nivel + 1)
        
        elif isinstance(nodo, ExpresionBinaria):
            print(f"{indentacion}OpBinaria: {nodo.operador.lexema}")
            print(f"{indentacion}  Izq:")
            self.imprimir_arbol(nodo.izquierda, nivel + 2)
            print(f"{indentacion}  Der:")
            self.imprimir_arbol(nodo.derecha, nivel + 2)
        
        elif isinstance(nodo, ExpresionUnaria):
            print(f"{indentacion}OpUnaria: {nodo.operador.lexema}")
            self.imprimir_arbol(nodo.operando, nivel + 1)
        
        elif isinstance(nodo, Literal):
            print(f"{indentacion}Literal: {nodo.token.lexema} ({nodo.token.tipo.value})")
        
        elif isinstance(nodo, LlamadaFuncion):
            print(f"{indentacion}LlamadaFunc: {nodo.nombre.lexema}")
            for arg in nodo.argumentos:
                self.imprimir_arbol(arg, nivel + 1)
        
        else:
            print(f"{indentacion}{nodo}")