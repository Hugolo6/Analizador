import tkinter as tk
from tkinter import scrolledtext
import sys
import io

# Importamos las 3 fases de tu compilador
from lexico.reservadas import AnalizadorLexico
from sintactico.parser import Parser
from semantico.analizador import AnalizadorSemantico

def ejecutar_analisis():
    # 1. Limpiamos la consola de salida y tomamos el texto escrito
    salida_texto.delete("1.0", tk.END)
    codigo_fuente = entrada_texto.get("1.0", tk.END).strip()
    
    if not codigo_fuente:
        salida_texto.insert(tk.END, "Por favor, ingresa código para analizar.")
        return

    # 2. Redirigimos la salida (prints) a nuestra interfaz gráfica
    captura_consola = io.StringIO()
    sys.stdout = captura_consola

    try:
        print("=" * 60)
        print("INICIANDO COMPILACIÓN...")
        print("=" * 60)

        # FASE 1: LÉXICO
        lexer = AnalizadorLexico()
        tokens = lexer.tokenizar(codigo_fuente)
        if lexer.errores:
            print("\n[ERROR] ERRORES LÉXICOS:")
            lexer.imprimir_errores()
        else:
            print(f"\n[OK] Análisis Léxico: {len(tokens)} tokens generados.")

            # FASE 2: SINTÁCTICO
            parser = Parser(tokens)
            arbol = parser.parsear()
            if parser.errores:
                print("\n[ERROR] ERRORES SINTÁCTICOS:")
                parser.imprimir_errores()
            else:
                print("[OK] Análisis Sintáctico exitoso.")
                
                # FASE 3: SEMÁNTICO
                semantico = AnalizadorSemantico()
                errores_semanticos = semantico.analizar(arbol)
                if errores_semanticos:
                    print("\n[ERROR] ERRORES SEMÁNTICOS:")
                    for err in errores_semanticos:
                        print(err)
                else:
                    print("\n[OK] Análisis Semántico exitoso. Código 100% válido.")
                    
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Ocurrió un fallo inesperado: {e}")
    finally:
        # 3. Devolvemos la salida a la normalidad para no romper la terminal
        sys.stdout = sys.__stdout__

    # 4. Imprimimos todo lo capturado en la caja de texto verde
    salida_texto.insert(tk.END, captura_consola.getvalue())

# =======================================================
# CONFIGURACIÓN DE LA VENTANA PRINCIPAL (TEMA OSCURO)
# =======================================================
ventana = tk.Tk()
ventana.title("IDE - Analizador Léxico, Sintáctico y Semántico")
ventana.geometry("1100x650")
ventana.configure(bg="#1e1e1e") # Fondo oscuro tipo VS Code

# Contenedor principal
main_frame = tk.Frame(ventana, bg="#1e1e1e")
main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# --- PANEL IZQUIERDO (Entrada de Código) ---
frame_izq = tk.Frame(main_frame, bg="#1e1e1e")
frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

lbl_in = tk.Label(frame_izq, text="Código Fuente:", bg="#1e1e1e", fg="#569cd6", font=("Segoe UI", 12, "bold"))
lbl_in.pack(anchor=tk.W, pady=(0, 5))

# Caja de texto para escribir código
entrada_texto = scrolledtext.ScrolledText(frame_izq, width=45, bg="#2d2d2d", fg="#d4d4d4", font=("Consolas", 12), insertbackground="white", borderwidth=0)
entrada_texto.pack(fill=tk.BOTH, expand=True)

# Texto por defecto de ejemplo válido
codigo_ejemplo = """anb
    gz x = 10;
    gz y = 20;
    fl promedio = 0;
    wen x <= y {
        promedio = x + y;
        dru(promedio);
    }
end"""
entrada_texto.insert(tk.END, codigo_ejemplo)

# --- PANEL DERECHO (Consola de Salida) ---
frame_der = tk.Frame(main_frame, bg="#1e1e1e")
frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

lbl_out = tk.Label(frame_der, text="Terminal de Compilación:", bg="#1e1e1e", fg="#4ec9b0", font=("Segoe UI", 12, "bold"))
lbl_out.pack(anchor=tk.W, pady=(0, 5))

# Caja de texto verde tipo terminal
salida_texto = scrolledtext.ScrolledText(frame_der, width=55, bg="#000000", fg="#00ff00", font=("Consolas", 11), borderwidth=0)
salida_texto.pack(fill=tk.BOTH, expand=True)

# --- BOTÓN DE EJECUCIÓN ---
btn_frame = tk.Frame(ventana, bg="#1e1e1e")
btn_frame.pack(fill=tk.X, pady=(0, 15))

btn_compilar = tk.Button(btn_frame, text="▶ COMPILAR CÓDIGO", bg="#007acc", fg="white", font=("Segoe UI", 12, "bold"), borderwidth=0, padx=20, pady=10, cursor="hand2", command=ejecutar_analisis)
btn_compilar.pack()

# Arrancar la aplicación
ventana.mainloop()
