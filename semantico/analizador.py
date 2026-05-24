from lexico.reservadas import TipoToken

class ErrorSemantico(Exception):
    pass

class TablaSimbolos:
    """Maneja los ámbitos (scopes) y las variables declaradas."""
    def __init__(self):
        # Usamos una pila de diccionarios para manejar bloques anidados (como los if o while)
        self.pila_ambitos = [{}]

    def entrar_bloque(self):
        self.pila_ambitos.append({})

    def salir_bloque(self):
        self.pila_ambitos.pop()

    def declarar(self, nombre, tipo):
        ambito_actual = self.pila_ambitos[-1]
        if nombre in ambito_actual:
            return False # Ya existe en este bloque
        ambito_actual[nombre] = tipo
        return True

    def buscar(self, nombre):
        # Busca la variable desde el bloque más interno hacia afuera
        for ambito in reversed(self.pila_ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None
## gola mafr

class AnalizadorSemantico:
    """Recorre el AST para verificar tipos y declaraciones."""
    
    def __init__(self):
        self.tabla_simbolos = TablaSimbolos()
        self.errores = []

    def registrar_error(self, mensaje):
        self.errores.append(f"Error Semántico: {mensaje}")

    def analizar(self, nodo_ast):
        """Punto de entrada principal."""
        self.errores = []
        self.visitar(nodo_ast)
        return self.errores

    def visitar(self, nodo):
        """Despachador que llama al método visitar_ correspondiente."""
        if nodo is None:
            return None
        
        nombre_metodo = f'visitar_{nodo.__class__.__name__}'
        visitante = getattr(self, nombre_metodo, self.visitar_desconocido)
        return visitante(nodo)

    def visitar_desconocido(self, nodo):
        raise ErrorSemantico(f"No hay método visitar_ para {nodo.__class__.__name__}")

    # =========================================================================
    # RECORRIDO DE SENTENCIAS
    # =========================================================================

    def visitar_Programa(self, nodo):
        for sentencia in nodo.sentencias:
            self.visitar(sentencia)

    def visitar_Declaracion(self, nodo):
        nombre_var = nodo.identificador.lexema
        tipo_declarado = nodo.tipo_token.tipo # Ej: TipoToken.INT (gz)
        
        # Validar que no se redeclare
        if not self.tabla_simbolos.declarar(nombre_var, tipo_declarado):
            self.registrar_error(f"La variable '{nombre_var}' ya fue declarada en este ámbito. L{nodo.identificador.linea}")
            return
        
        # Validar tipo de la expresión
        tipo_expresion = self.visitar(nodo.expresion)
        if tipo_expresion and not self.tipos_compatibles(tipo_declarado, tipo_expresion):
            self.registrar_error(f"Incompatibilidad de tipos en declaración: No se puede asignar '{self.obtener_nombre_tipo(tipo_expresion)}' a la variable '{nombre_var}' de tipo '{self.obtener_nombre_tipo(tipo_declarado)}'. L{nodo.identificador.linea}")

    def visitar_Asignacion(self, nodo):
        nombre_var = nodo.identificador.lexema
        tipo_variable = self.tabla_simbolos.buscar(nombre_var)
        
        if tipo_variable is None:
            self.registrar_error(f"Variable '{nombre_var}' no declarada. L{nodo.identificador.linea}")
            return

        tipo_expresion = self.visitar(nodo.expresion)
        if tipo_expresion and not self.tipos_compatibles(tipo_variable, tipo_expresion):
            self.registrar_error(f"Incompatibilidad de tipos en asignación: No se puede asignar '{self.obtener_nombre_tipo(tipo_expresion)}' a '{nombre_var}' ({self.obtener_nombre_tipo(tipo_variable)}). L{nodo.identificador.linea}")

    def visitar_IfStatement(self, nodo):
        self.visitar(nodo.condicion) # Normalmente verificaríamos que retorne booleano
        
        self.tabla_simbolos.entrar_bloque()
        for stmt in nodo.bloque_if:
            self.visitar(stmt)
        self.tabla_simbolos.salir_bloque()

        if nodo.bloque_else:
            self.tabla_simbolos.entrar_bloque()
            for stmt in nodo.bloque_else:
                self.visitar(stmt)
            self.tabla_simbolos.salir_bloque()

    def visitar_WhileStatement(self, nodo):
        self.visitar(nodo.condicion)
        self.tabla_simbolos.entrar_bloque()
        for stmt in nodo.bloque:
            self.visitar(stmt)
        self.tabla_simbolos.salir_bloque()

    def visitar_ForStatement(self, nodo):
        self.tabla_simbolos.entrar_bloque()
        if nodo.inicializacion:
            self.visitar(nodo.inicializacion)
        
        self.visitar(nodo.condicion)
        
        if nodo.actualizacion:
            self.visitar(nodo.actualizacion)
            
        for stmt in nodo.bloque:
            self.visitar(stmt)
        self.tabla_simbolos.salir_bloque()

    def visitar_Lectura(self, nodo):
        nombre_var = nodo.identificador.lexema
        if self.tabla_simbolos.buscar(nombre_var) is None:
            self.registrar_error(f"Intento de leer la variable no declarada '{nombre_var}'. L{nodo.identificador.linea}")

    def visitar_Escritura(self, nodo):
        self.visitar(nodo.expresion)

    # =========================================================================
    # RECORRIDO DE EXPRESIONES (DEVUELVEN UN TIPO)
    # =========================================================================

    def visitar_ExpresionBinaria(self, nodo):
        tipo_izq = self.visitar(nodo.izquierda)
        tipo_der = self.visitar(nodo.derecha)

        if not tipo_izq or not tipo_der:
            return None # El error ya se detectó más abajo

        # Operadores matemáticos (+, -, *, /)
        if nodo.operador.tipo in (TipoToken.SUMA, TipoToken.RESTA, TipoToken.MULT, TipoToken.DIV):
            if tipo_izq in (TipoToken.INT, TipoToken.FLOAT) and tipo_der in (TipoToken.INT, TipoToken.FLOAT):
                # Si alguno es float, el resultado es float
                if tipo_izq == TipoToken.FLOAT or tipo_der == TipoToken.FLOAT:
                    return TipoToken.FLOAT
                return TipoToken.INT
            else:
                self.registrar_error(f"Operación inválida: No se pueden usar operadores matemáticos entre '{self.obtener_nombre_tipo(tipo_izq)}' y '{self.obtener_nombre_tipo(tipo_der)}'. L{nodo.operador.linea}")
                return None
                
        # Operadores lógicos/comparación devuelven INT (asumiendo 0 o 1) o un pseudo-booleano
        return TipoToken.INT 

    def visitar_ExpresionUnaria(self, nodo):
        return self.visitar(nodo.operando)

    def visitar_Literal(self, nodo):
        # Mapea los literales del Lexer a los tipos declarativos
        if nodo.token.tipo == TipoToken.ENTERO:
            return TipoToken.INT
        elif nodo.token.tipo == TipoToken.LETRA:
            return TipoToken.STRING
        elif nodo.token.tipo == TipoToken.IDENTIFICADOR:
            tipo = self.tabla_simbolos.buscar(nodo.token.lexema)
            if tipo is None:
                self.registrar_error(f"Variable '{nodo.token.lexema}' no declarada. L{nodo.token.linea}")
            return tipo
        return None

    def visitar_LlamadaFuncion(self, nodo):
        # El lexer no parece definir funciones completas, pero si existe en el AST:
        self.registrar_error(f"Llamadas a funciones aún no soportadas semánticamente: {nodo.nombre.lexema}")
        return None

    # =========================================================================
    # UTILIDADES
    # =========================================================================
    def tipos_compatibles(self, tipo_var, tipo_expr):
        """Verifica si el tipo_expr puede guardarse en tipo_var"""
        if tipo_var == tipo_expr:
            return True
        # Se permite guardar un INT en un FLOAT
        if tipo_var == TipoToken.FLOAT and tipo_expr == TipoToken.INT:
            return True
        return False
        
    def obtener_nombre_tipo(self, tipo_enum):
        if tipo_enum == TipoToken.INT: return "gz (Entero)"
        if tipo_enum == TipoToken.FLOAT: return "fl (Flotante)"
        if tipo_enum == TipoToken.STRING: return "str (Cadena)"
        return str(tipo_enum)
    