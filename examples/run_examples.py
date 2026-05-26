from pathlib import Path
import main

EXAMPLES = [
    ('hello_string', 'hello_string.src'),
    ('string_variable', 'string_variable.src'),
    ('mixed_types', 'mixed_types.src'),
    ('for_and_print', 'for_and_print.src'),
]

BASE = Path(__file__).parent

if __name__ == '__main__':
    for name, fname in EXAMPLES:
        path = BASE / fname
        print('\n' + '='*60)
        print(f'Ejemplo: {name} -> {path.name}')
        print('='*60)
        codigo = path.read_text(encoding='utf-8')
        print(codigo)
        resultado = main.compilar(codigo)
        main.imprimir_resultado(resultado)
