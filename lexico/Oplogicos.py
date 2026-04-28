
 
from lexico.reservadas import TipoToken, Token
 
 
# ---------------------------------------------------------------------------
# Operadores de comparación y lógicos (dobles)
# ---------------------------------------------------------------------------
OPERADORES_LOGICOS = {
    '==': {
        'tipo': TipoToken.IGUAL,
        'token': '==',
        'tk': '==',
        'descripcion': 'Signo = seguido del signo =',
    },
    '<': {
        'tipo': TipoToken.MENOR,
        'token': '<',
        'tk': '<',
        'descripcion': 'Signo <',
    },
    '>': {
        'tipo': TipoToken.MAYOR,
        'token': '>',
        'tk': '>',
        'descripcion': 'Signo >',
    },
    '<=': {
        'tipo': TipoToken.MENOR_EQ,
        'token': '<=',
        'tk': '<=',
        'descripcion': 'Signo < seguido del signo =',
    },
    '>=': {
        'tipo': TipoToken.MAYOR_EQ,
        'token': '>=',
        'tk': '>=',
        'descripcion': 'Signo > seguido del signo =',
    },
    'and': {
        'tipo': TipoToken.AND,
        'token': 'and',
        'tk': 'und',
        'descripcion': 'Letra u seguida de n y d',
    },
    '&&': {
        'tipo': TipoToken.AND2,
        'token': '&&',
        'tk': 'u2',
        'descripcion': 'Símbolo & seguido del símbolo &',
    },
    'or': {
        'tipo': TipoToken.OR,
        'token': 'or',
        'tk': 'od',
        'descripcion': 'Letra o seguida de d, e, r',
    },
    '||': {
        'tipo': TipoToken.OR2,
        'token': '||',
        'tk': '||',
        'descripcion': '| símbolo seguido del símbolo |',
    },
}
 
 
def listar_operadores_logicos():
    """Imprime en consola la tabla de operadores de comparación/lógicos."""
    sep = "-" * 80
    print(sep)
    print("OPERADORES DE COMPARACIÓN Y LÓGICOS")
    print(sep)
    print(f"{'TOKEN':<10} {'TK':<8} {'DESCRIPCIÓN'}")
    print(sep)
    for simbolo, info in OPERADORES_LOGICOS.items():
        print(f"{info['token']:<10} {info['tk']:<8} {info['descripcion']}")
    print(sep)
 
 
def es_operador_logico(lexema: str):
    """Retorna el dict del operador lógico si el lexema es reconocido, o None."""
    return OPERADORES_LOGICOS.get(lexema, None)
 
 
def crear_token_logico(lexema: str, linea: int = 1, columna: int = 1):
    """
    Crea y retorna un Token para un operador lógico/comparación.
    Retorna None si el lexema no corresponde a ninguno.
    """
    info = es_operador_logico(lexema)
    if not info:
        return None
    return Token(
        tipo=info['tipo'],
        lexema=lexema,
        tk=info['tk'],
        linea=linea,
        columna=columna,
        es_reservada=True,
    )
 