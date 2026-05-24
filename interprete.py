"""
INTÉRPRETE — Ejecuta el AST producido por el parser.
Recorre los nodos y realiza las operaciones reales.
"""
import sys
from sintactico.parser import (
    Programa, Declaracion, Asignacion, IfStatement, WhileStatement,
    ForStatement, Lectura, Escritura,
    ExpresionBinaria, ExpresionUnaria, Literal, LlamadaFuncion,
)
from lexico.reservadas import TipoToken


class ErrorEjecucion(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje


class EntornoEjecucion:
    """Pila de ámbitos para almacenar variables durante la ejecución."""

    def __init__(self):
        self.pila = [{}]   # cada dict es un ámbito

    def entrar(self):
        self.pila.append({})

    def salir(self):
        self.pila.pop()

    def declarar(self, nombre, valor):
        self.pila[-1][nombre] = valor

    def asignar(self, nombre, valor, linea=None):
        for ambito in reversed(self.pila):
            if nombre in ambito:
                ambito[nombre] = valor
                return
        pos = f" (línea {linea})" if linea else ""
        raise ErrorEjecucion(f"Variable '{nombre}' no declarada{pos}")

    def obtener(self, nombre, linea=None):
        for ambito in reversed(self.pila):
            if nombre in ambito:
                return ambito[nombre]
        pos = f" (línea {linea})" if linea else ""
        raise ErrorEjecucion(f"Variable '{nombre}' no declarada{pos}")


class Interprete:
    """Ejecuta el AST nodo por nodo."""

    MAX_ITERACIONES = 100_000   # seguro contra bucles infinitos

    def __init__(self, salida_fn=None):
        """
        salida_fn: función que recibe un string para mostrar output.
        Si es None usa print().
        """
        self.entorno = EntornoEjecucion()
        self.salida_fn = salida_fn or print
        self.errores = []
        self._iteraciones = 0

    # ──────────────────────────────────────────────────────────────────────────
    # Punto de entrada
    # ──────────────────────────────────────────────────────────────────────────

    def ejecutar(self, ast):
        self.errores = []
        self._iteraciones = 0
        try:
            self._ejecutar_nodo(ast)
        except ErrorEjecucion as e:
            self.errores.append(f"Error de ejecución: {e.mensaje}")
        except RecursionError:
            self.errores.append("Error de ejecución: Desbordamiento de pila (recursión infinita).")
        return self.errores

    # ──────────────────────────────────────────────────────────────────────────
    # Despachador
    # ──────────────────────────────────────────────────────────────────────────

    def _ejecutar_nodo(self, nodo):
        if nodo is None:
            return None
        nombre = f"_exec_{nodo.__class__.__name__}"
        metodo = getattr(self, nombre, self._exec_desconocido)
        return metodo(nodo)

    def _exec_desconocido(self, nodo):
        raise ErrorEjecucion(f"Nodo AST desconocido: {nodo.__class__.__name__}")

    # ──────────────────────────────────────────────────────────────────────────
    # Sentencias
    # ──────────────────────────────────────────────────────────────────────────

    def _exec_Programa(self, nodo):
        for sentencia in nodo.sentencias:
            self._ejecutar_nodo(sentencia)

    def _exec_Declaracion(self, nodo):
        valor = self._ejecutar_nodo(nodo.expresion)
        valor = self._coerce(valor, nodo.tipo_token.tipo)
        self.entorno.declarar(nodo.identificador.lexema, valor)

    def _exec_Asignacion(self, nodo):
        valor = self._ejecutar_nodo(nodo.expresion)
        self.entorno.asignar(nodo.identificador.lexema, valor, nodo.identificador.linea)

    def _exec_IfStatement(self, nodo):
        condicion = self._ejecutar_nodo(nodo.condicion)
        self.entorno.entrar()
        try:
            if self._es_verdadero(condicion):
                for stmt in nodo.bloque_if:
                    self._ejecutar_nodo(stmt)
            elif nodo.bloque_else:
                for stmt in nodo.bloque_else:
                    self._ejecutar_nodo(stmt)
        finally:
            self.entorno.salir()

    def _exec_WhileStatement(self, nodo):
        while self._es_verdadero(self._ejecutar_nodo(nodo.condicion)):
            self._iteraciones += 1
            if self._iteraciones > self.MAX_ITERACIONES:
                raise ErrorEjecucion(
                    f"Bucle infinito detectado: superó {self.MAX_ITERACIONES:,} iteraciones."
                )
            self.entorno.entrar()
            try:
                for stmt in nodo.bloque:
                    self._ejecutar_nodo(stmt)
            finally:
                self.entorno.salir()

    def _exec_ForStatement(self, nodo):
        self.entorno.entrar()
        try:
            if nodo.inicializacion:
                self._ejecutar_nodo(nodo.inicializacion)
            while self._es_verdadero(self._ejecutar_nodo(nodo.condicion)):
                self._iteraciones += 1
                if self._iteraciones > self.MAX_ITERACIONES:
                    raise ErrorEjecucion(
                        f"Bucle infinito detectado: superó {self.MAX_ITERACIONES:,} iteraciones."
                    )
                self.entorno.entrar()
                try:
                    for stmt in nodo.bloque:
                        self._ejecutar_nodo(stmt)
                finally:
                    self.entorno.salir()
                if nodo.actualizacion:
                    self._ejecutar_nodo(nodo.actualizacion)
        finally:
            self.entorno.salir()

    def _exec_Escritura(self, nodo):
        valor = self._ejecutar_nodo(nodo.expresion)
        self.salida_fn(self._formatear(valor))

    def _exec_Lectura(self, nodo):
        nombre = nodo.identificador.lexema
        try:
            entrada = input(f"  Ingresa valor para '{nombre}': ")
            # Intentamos convertir al tipo que sea más natural
            try:
                valor = int(entrada)
            except ValueError:
                try:
                    valor = float(entrada)
                except ValueError:
                    valor = entrada
            self.entorno.asignar(nombre, valor, nodo.identificador.linea)
        except EOFError:
            raise ErrorEjecucion(f"No se pudo leer la variable '{nombre}': entrada cerrada.")

    # ──────────────────────────────────────────────────────────────────────────
    # Expresiones (devuelven un valor)
    # ──────────────────────────────────────────────────────────────────────────

    def _exec_ExpresionBinaria(self, nodo):
        izq = self._ejecutar_nodo(nodo.izquierda)
        der = self._ejecutar_nodo(nodo.derecha)
        op  = nodo.operador.tipo

        try:
            if op == TipoToken.SUMA:    return izq + der
            if op == TipoToken.RESTA:   return izq - der
            if op == TipoToken.MULT:    return izq * der
            if op == TipoToken.DIV:
                if der == 0:
                    raise ErrorEjecucion(f"División por cero. L{nodo.operador.linea}")
                return izq / der if isinstance(izq, float) or isinstance(der, float) else izq // der
            if op == TipoToken.IGUAL:   return 1 if izq == der else 0
            if op == TipoToken.MENOR:   return 1 if izq <  der else 0
            if op == TipoToken.MAYOR:   return 1 if izq >  der else 0
            if op == TipoToken.MENOR_EQ:return 1 if izq <= der else 0
            if op == TipoToken.MAYOR_EQ:return 1 if izq >= der else 0
            if op in (TipoToken.AND, TipoToken.AND2):
                return 1 if (self._es_verdadero(izq) and self._es_verdadero(der)) else 0
            if op in (TipoToken.OR, TipoToken.OR2):
                return 1 if (self._es_verdadero(izq) or self._es_verdadero(der)) else 0
        except TypeError as e:
            raise ErrorEjecucion(
                f"Operación inválida entre '{izq}' y '{der}': {e}  L{nodo.operador.linea}"
            )
        raise ErrorEjecucion(f"Operador desconocido: {op}")

    def _exec_ExpresionUnaria(self, nodo):
        val = self._ejecutar_nodo(nodo.operando)
        if nodo.operador.tipo == TipoToken.RESTA:
            return -val
        return val

    def _exec_Literal(self, nodo):
        tok = nodo.token
        if tok.tipo == TipoToken.ENTERO:
            return int(tok.lexema)
        if tok.tipo in (TipoToken.LETRA, TipoToken.STRING):
            return tok.lexema
        if tok.tipo == TipoToken.IDENTIFICADOR:
            return self.entorno.obtener(tok.lexema, tok.linea)
        raise ErrorEjecucion(f"Literal desconocido: '{tok.lexema}'")

    def _exec_LlamadaFuncion(self, nodo):
        raise ErrorEjecucion(
            f"Funciones definidas por el usuario aún no están soportadas: '{nodo.nombre.lexema}'"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Utilidades
    # ──────────────────────────────────────────────────────────────────────────

    def _es_verdadero(self, valor):
        """0, 0.0 y "" son falsos; todo lo demás es verdadero."""
        if isinstance(valor, (int, float)):
            return valor != 0
        if isinstance(valor, str):
            return valor != ""
        return bool(valor)

    def _coerce(self, valor, tipo_token):
        """Convierte el valor al tipo declarado (gz=int, fl=float, str=str)."""
        try:
            if tipo_token == TipoToken.INT:
                return int(valor)
            if tipo_token == TipoToken.FLOAT:
                return float(valor)
            if tipo_token == TipoToken.STRING:
                return str(valor)
        except (ValueError, TypeError):
            pass
        return valor

    def _formatear(self, valor):
        """Convierte el valor a string para dru()."""
        if isinstance(valor, float) and valor == int(valor):
            return str(int(valor))
        return str(valor)
