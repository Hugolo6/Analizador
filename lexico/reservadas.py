import re
from enum import Enum

class TipoToken(Enum):
    # Palabras reservadas
    INT = "INT"
    STRING = "STRING"
    FLOAT = "FLOAT"
    LEER = "LEER"
    IMPRIMIR = "IMPRIMIR"
    
    # Tipos de datos
    IDENTIFICADOR = "IDENTIFICADOR"
    ENTERO = "ENTERO"
    LETRA = "LETRA"
    
    # Especiales
    DESCONOCIDO = "DESCONOCIDO"
    EOF = "EOF"


class Token:
    
    def __init__(self, tipo, lexema, tk=None, linea=1, columna=1, es_reservada=False):
      
        self.tipo = tipo
        self.lexema = lexema
        self.tk = tk
        self.linea = linea
        self.columna = columna
        self.es_reservada = es_reservada
    
    def __repr__(self):
        """Representación en string del token"""
        return f"Token(tipo={self.tipo.value}, lexema='{self.lexema}', tk='{self.tk}', lin={self.linea}, col={self.columna})"
    
    def __str__(self):
        """Formato legible del token"""
        reservada_str = " [RESERVADA]" if self.es_reservada else ""
        return f"{self.lexema:<15} {self.tipo.value:<15} {self.tk:<10} L{self.linea}:C{self.columna}{reservada_str}"
    
    def to_dict(self):
        """Convierte el token a diccionario """
        return {
            'tipo': self.tipo.value,
            'lexema': self.lexema,
            'tk': self.tk,
            'linea': self.linea,
            'columna': self.columna,
            'es_reservada': self.es_reservada
        }


# Diccionario de palabras reservadas con sus características
PALABRAS_RESERVADAS = {
    'Int': {
        'tipo': TipoToken.INT,
        'token': 'Int',
        'lexema': 'Int',
        'tk': 'gz',
        'patron': r'^[Gg][anz]$',
        'descripcion': 'Letra G seguida de la letra a, n, z'
    },
    'String': {
        'tipo': TipoToken.STRING,
        'token': 'String',
        'lexema': 'String',
        'tk': 'str',
        'patron': r'^[Zz][a-zA-Z]+$',
        'descripcion': 'Letra z seguida de más letras'
    },
    'float': {
        'tipo': TipoToken.FLOAT,
        'token': 'float',
        'lexema': 'float',
        'tk': 'fl',
        'patron': r'^[Ff][lie\xDF]',
        'descripcion': 'Letra f seguida de la letra l, i, e, ß'
    },
    'leer': {
        'tipo': TipoToken.LEER,
        'token': 'leer',
        'lexema': 'leer',
        'tk': 'les',
        'patron': r'^[Ll][esen]+',
        'descripcion': 'Letra l seguida de la letra e, s, e, n'
    },
    'imprimir': {
        'tipo': TipoToken.IMPRIMIR,
        'token': 'imp',
        'lexema': 'imprimir',
        'tk': 'dru',
        'patron': r'^[Dd][ru]+',
        'descripcion': 'Letra d seguida de la letra r, u'
    }
}

# Diccionario de tipos de datos (no reservados pero reconocibles)
TIPOS_DATOS = {
    'identificador': {
        'tipo': TipoToken.IDENTIFICADOR,
        'token': 'Identificador',
        'tk': 'bez',
        'patron': r'^[a-zA-Z][a-zA-Z0-9]*$',
        'descripcion': 'Letra seguida de letra o dígito',
        'reservada': False
    },
    'entero': {
        'tipo': TipoToken.ENTERO,
        'token': 'entero',
        'tk': 'gan',
        'patron': r'^[1-9][0-9]*$',
        'descripcion': 'Dígito seguido de más dígitos',
        'reservada': False
    },
    'letra': {
        'tipo': TipoToken.LETRA,
        'token': 'letra',
        'tk': 'buc',
        'patron': r'^[a-zA-Z]+$',
        'descripcion': 'Letra seguida de más letras',
        'reservada': False
    }
}


class ErrorLexico:
  
    
    def __init__(self, tipo_error, lexema, linea, columna, mensaje):
       
        self.tipo_error = tipo_error
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.mensaje = mensaje
    
    def __str__(self):
    
        return f"Error léxico [L{self.linea}:C{self.columna}] {self.tipo_error}: {self.mensaje}"
    
    def __repr__(self):
        return f"ErrorLexico({self.tipo_error}, '{self.lexema}', L{self.linea}:C{self.columna})"


class AnalizadorLexico:
    
    def __init__(self):
       
        self.tokens = []
        self.errores = []
        self.linea_actual = 1
        self.columna_actual = 1
    
    def es_palabra_reservada(self, palabra):
        for clave, info in PALABRAS_RESERVADAS.items():
            if palabra.lower() == clave.lower():
                return info
        return None
    
 