"""
Interfaz gráfica del compilador (tkinter).
Ejecuta las cuatro fases: léxico → sintáctico → semántico → ejecución.
"""
import tkinter as tk
from tkinter import scrolledtext
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import compilar

# ─────────────────────────────────────────────────────────────────────────────
# COLORES DEL TEMA
BG_DARK     = "#1e1e1e"
BG_PANEL    = "#252526"
BG_EDITOR   = "#1e1e1e"
BG_TERMINAL = "#0c0c0c"
FG_EDITOR   = "#d4d4d4"
FG_TERMINAL = "#cccccc"
FG_OK       = "#4ec9b0"
FG_ERROR    = "#f44747"
FG_WARNING  = "#dcdcaa"
FG_TITLE    = "#569cd6"
FG_ACCENT   = "#ce9178"
FG_OUTPUT   = "#b5cea8"   # verde claro para la salida del programa
BTN_BG      = "#0e639c"
BTN_HOVER   = "#1177bb"
BTN_FG      = "#ffffff"
LINENO_BG   = "#252526"
LINENO_FG   = "#858585"

CODIGO_EJEMPLO = """\
anb
    gz x = 10;
    gz y = 20;
    fl promedio = 0;
    wen x <= y {
        promedio = x + y;
        dru(promedio);
    }
    war x > 0 {
        dru(x);
        x = x - 1;
    }
end"""


class LineNumbers(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.text_widget = text_widget
        self.config(width=40, bg=LINENO_BG, highlightthickness=0)
        for evt in ("<KeyRelease>", "<MouseWheel>", "<Button-4>",
                    "<Button-5>", "<Configure>"):
            self.text_widget.bind(evt, lambda e: self.after(10, self.redraw))

    def redraw(self, *_):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(36, y + 8, anchor="ne", text=linenum,
                             fill=LINENO_FG, font=("Consolas", 10))
            i = self.text_widget.index(f"{i}+1line")
            if i == self.text_widget.index(f"{i}linestart"):
                break


class IDECompilador(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Compilador IDE  ·  Léxico / Sintáctico / Semántico / Ejecución")
        self.geometry("1400x760")
        self.minsize(900, 550)
        self.configure(bg=BG_DARK)

        self._build_menu()
        self._build_toolbar()
        self._build_body()
        self._build_statusbar()

        self.editor.insert("1.0", CODIGO_EJEMPLO)
        self._linenos.redraw()
        self._actualizar_estado("Listo. Escribe código y presiona ▶ Compilar y Ejecutar.", FG_OK)

    # ── MENU ──────────────────────────────────────────────────────────────────

    def _build_menu(self):
        menubar = tk.Menu(self, bg=BG_PANEL, fg=FG_EDITOR, tearoff=False,
                          activebackground=BTN_BG, activeforeground=BTN_FG)

        archivo = tk.Menu(menubar, bg=BG_PANEL, fg=FG_EDITOR, tearoff=False,
                          activebackground=BTN_BG, activeforeground=BTN_FG)
        archivo.add_command(label="Nuevo",            command=self._nuevo,             accelerator="Ctrl+N")
        archivo.add_command(label="Limpiar terminal", command=self._limpiar_terminal)
        archivo.add_separator()
        archivo.add_command(label="Salir",            command=self.destroy)
        menubar.add_cascade(label="Archivo", menu=archivo)

        ejemplos = tk.Menu(menubar, bg=BG_PANEL, fg=FG_EDITOR, tearoff=False,
                           activebackground=BTN_BG, activeforeground=BTN_FG)
        ejemplos.add_command(label="Código válido",      command=self._ejemplo_valido)
        ejemplos.add_command(label="Código con errores", command=self._ejemplo_errores)
        ejemplos.add_command(label="Ejemplo con for",    command=self._ejemplo_for)
        menubar.add_cascade(label="Ejemplos", menu=ejemplos)

        self.config(menu=menubar)
        self.bind_all("<Control-n>",      lambda e: self._nuevo())
        self.bind_all("<Control-Return>", lambda e: self._compilar())

    # ── TOOLBAR ───────────────────────────────────────────────────────────────

    def _build_toolbar(self):
        bar = tk.Frame(self, bg=BG_PANEL, height=44)
        bar.pack(fill=tk.X, side=tk.TOP)

        tk.Label(bar, text="  ⚙  Compilador",
                 bg=BG_PANEL, fg=FG_TITLE,
                 font=("Segoe UI", 13, "bold")).pack(side=tk.LEFT, padx=(8, 20), pady=6)

        self._btn(bar, "▶  Compilar y Ejecutar  (Ctrl+Enter)",
                  self._compilar, BTN_BG).pack(side=tk.LEFT, padx=4, pady=6)

        self._btn(bar, "✕  Limpiar",
                  self._nuevo, "#3a3d41").pack(side=tk.LEFT, padx=4, pady=6)

        self._fase_var = tk.StringVar(value="")
        tk.Label(bar, textvariable=self._fase_var,
                 bg=BG_PANEL, fg=FG_WARNING,
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=16)

    def _btn(self, parent, text, cmd, color):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=BTN_FG,
                      font=("Segoe UI", 10, "bold"),
                      relief=tk.FLAT, cursor="hand2",
                      padx=14, pady=4,
                      activebackground=BTN_HOVER,
                      activeforeground=BTN_FG)
        b.bind("<Enter>", lambda e, b=b: b.config(bg=BTN_HOVER))
        b.bind("<Leave>", lambda e, b=b, c=color: b.config(bg=c))
        return b

    # ── BODY ──────────────────────────────────────────────────────────────────

    def _build_body(self):
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL,
                               bg=BG_DARK, sashwidth=5, sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo: editor
        left = tk.Frame(paned, bg=BG_DARK)
        paned.add(left, minsize=350)

        tk.Label(left, text="  📝  Código Fuente",
                 bg=BG_PANEL, fg=FG_TITLE,
                 font=("Segoe UI", 10, "bold"),
                 anchor="w", pady=4).pack(fill=tk.X)

        editor_frame = tk.Frame(left, bg=BG_DARK)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            bg=BG_EDITOR, fg=FG_EDITOR,
            font=("Consolas", 12),
            insertbackground="white",
            selectbackground="#264f78",
            relief=tk.FLAT, wrap=tk.NONE, undo=True,
            padx=8, pady=6,
        )
        self._linenos = LineNumbers(editor_frame, self.editor)
        self._linenos.pack(side=tk.LEFT, fill=tk.Y)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel derecho: paneles apilados verticalmente
        right = tk.Frame(paned, bg=BG_DARK)
        paned.add(right, minsize=400)

        vpaned = tk.PanedWindow(right, orient=tk.VERTICAL,
                                bg=BG_DARK, sashwidth=5, sashrelief=tk.FLAT)
        vpaned.pack(fill=tk.BOTH, expand=True)

        # Terminal de análisis (arriba)
        top_right = tk.Frame(vpaned, bg=BG_DARK)
        vpaned.add(top_right, minsize=200)

        tk.Label(top_right, text="  🔍  Terminal de Análisis",
                 bg=BG_PANEL, fg=FG_ACCENT,
                 font=("Segoe UI", 10, "bold"),
                 anchor="w", pady=4).pack(fill=tk.X)

        self.terminal = scrolledtext.ScrolledText(
            top_right,
            bg=BG_TERMINAL, fg=FG_TERMINAL,
            font=("Consolas", 11),
            relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD,
            padx=10, pady=8,
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)
        for tag, fg in [("ok", FG_OK), ("error", FG_ERROR), ("warning", FG_WARNING),
                        ("title", FG_TITLE), ("accent", FG_ACCENT), ("normal", FG_TERMINAL)]:
            self.terminal.tag_config(tag, foreground=fg)

        # Terminal de salida del programa (abajo)
        bot_right = tk.Frame(vpaned, bg=BG_DARK)
        vpaned.add(bot_right, minsize=120)

        tk.Label(bot_right, text="  🖥  Salida del Programa",
                 bg=BG_PANEL, fg=FG_OK,
                 font=("Segoe UI", 10, "bold"),
                 anchor="w", pady=4).pack(fill=tk.X)

        self.salida = scrolledtext.ScrolledText(
            bot_right,
            bg="#0a1a0a", fg=FG_OUTPUT,
            font=("Consolas", 12),
            relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD,
            padx=10, pady=8,
        )
        self.salida.pack(fill=tk.BOTH, expand=True)
        self.salida.tag_config("output", foreground=FG_OUTPUT)
        self.salida.tag_config("error",  foreground=FG_ERROR)
        self.salida.tag_config("prompt", foreground=FG_WARNING)

    # ── STATUSBAR ─────────────────────────────────────────────────────────────

    def _build_statusbar(self):
        bar = tk.Frame(self, bg="#007acc", height=22)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        self._status_var = tk.StringVar()
        tk.Label(bar, textvariable=self._status_var,
                 bg="#007acc", fg="white",
                 font=("Segoe UI", 9), anchor="w", padx=10).pack(side=tk.LEFT, fill=tk.Y)

    def _actualizar_estado(self, texto, color="#ffffff"):
        self._status_var.set(f"  {texto}")

    # ── LÓGICA ────────────────────────────────────────────────────────────────

    def _compilar(self):
        codigo = self.editor.get("1.0", tk.END).strip()
        if not codigo:
            self._escribir_terminal("Sin código para compilar.\n", "warning")
            return

        self._limpiar_terminal()
        self._limpiar_salida()
        self._fase_var.set("Compilando…")
        self.update_idletasks()

        # La salida del programa llega en tiempo real vía callback
        def mostrar_salida(linea):
            self._escribir_salida(linea + "\n", "output")
            self.update_idletasks()

        resultado = compilar(codigo, salida_fn=mostrar_salida)

        self._escribir_terminal("═" * 56 + "\n", "title")
        self._escribir_terminal("  COMPILADOR — RESULTADO\n", "title")
        self._escribir_terminal("═" * 56 + "\n\n", "title")

        # Léxico
        self._escribir_terminal("▌ FASE 1 · ANÁLISIS LÉXICO\n", "accent")
        if resultado["lexico"]["ok"]:
            n = len(resultado["lexico"]["tokens"])
            self._escribir_terminal(f"  ✔  {n} tokens generados sin errores.\n\n", "ok")
        else:
            self._escribir_terminal("  ✖  Errores léxicos:\n", "error")
            for e in resultado["lexico"]["errores"]:
                self._escribir_terminal(f"      {e}\n", "error")
            self._fase_var.set("✖ Error léxico")
            self._actualizar_estado("Error léxico detectado.", FG_ERROR)
            return

        # Sintáctico
        self._escribir_terminal("▌ FASE 2 · ANÁLISIS SINTÁCTICO\n", "accent")
        if resultado["sintactico"]["ok"]:
            self._escribir_terminal("  ✔  AST construido sin errores.\n\n", "ok")
        else:
            self._escribir_terminal("  ✖  Errores sintácticos:\n", "error")
            for e in resultado["sintactico"]["errores"]:
                self._escribir_terminal(f"      {e}\n", "error")
            self._fase_var.set("✖ Error sintáctico")
            self._actualizar_estado("Error sintáctico detectado.", FG_ERROR)
            return

        # Semántico
        self._escribir_terminal("▌ FASE 3 · ANÁLISIS SEMÁNTICO\n", "accent")
        if resultado["semantico"]["ok"]:
            self._escribir_terminal("  ✔  Sin errores semánticos.\n\n", "ok")
        else:
            self._escribir_terminal("  ✖  Errores semánticos:\n", "error")
            for e in resultado["semantico"]["errores"]:
                self._escribir_terminal(f"      {e}\n", "error")
            self._fase_var.set("✖ Error semántico")
            self._actualizar_estado("Error semántico detectado.", FG_ERROR)
            return

        # Ejecución
        self._escribir_terminal("▌ FASE 4 · EJECUCIÓN\n", "accent")
        if resultado["ejecucion"]["ok"]:
            n_lineas = len(resultado["ejecucion"]["salida"])
            self._escribir_terminal(f"  ✔  Programa ejecutado — {n_lineas} línea(s) de salida.\n\n", "ok")
            self._escribir_terminal("═" * 56 + "\n", "ok")
            self._escribir_terminal("  ✅  COMPILACIÓN Y EJECUCIÓN EXITOSA.\n", "ok")
            self._escribir_terminal("═" * 56 + "\n", "ok")
            self._fase_var.set("✔ Ejecución exitosa")
            self._actualizar_estado("Compilación y ejecución exitosa.", FG_OK)
        else:
            self._escribir_terminal("  ✖  Errores durante la ejecución:\n", "error")
            for e in resultado["ejecucion"]["errores"]:
                self._escribir_terminal(f"      {e}\n", "error")
                self._escribir_salida(f"  Error: {e}\n", "error")
            self._fase_var.set("✖ Error en ejecución")
            self._actualizar_estado("Error durante la ejecución.", FG_ERROR)

    # ── Escritura en terminales ───────────────────────────────────────────────

    def _escribir_terminal(self, texto, tag="normal"):
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, texto, tag)
        self.terminal.config(state=tk.DISABLED)
        self.terminal.see(tk.END)

    def _escribir_salida(self, texto, tag="output"):
        self.salida.config(state=tk.NORMAL)
        self.salida.insert(tk.END, texto, tag)
        self.salida.config(state=tk.DISABLED)
        self.salida.see(tk.END)

    def _limpiar_terminal(self):
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete("1.0", tk.END)
        self.terminal.config(state=tk.DISABLED)
        self._fase_var.set("")

    def _limpiar_salida(self):
        self.salida.config(state=tk.NORMAL)
        self.salida.delete("1.0", tk.END)
        self.salida.config(state=tk.DISABLED)

    def _nuevo(self):
        self.editor.delete("1.0", tk.END)
        self._limpiar_terminal()
        self._limpiar_salida()
        self._actualizar_estado("Editor limpiado. Listo.")
        self._linenos.redraw()

    # ── Ejemplos ─────────────────────────────────────────────────────────────

    def _ejemplo_valido(self):
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", CODIGO_EJEMPLO)
        self._linenos.redraw()
        self._limpiar_terminal()
        self._limpiar_salida()
        self._actualizar_estado("Ejemplo válido cargado.")

    def _ejemplo_errores(self):
        codigo = """\
anb
    gz x = 7
    wen x > 5 {
        dru(x);
    
end"""
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", codigo)
        self._linenos.redraw()
        self._limpiar_terminal()
        self._limpiar_salida()
        self._actualizar_estado("Ejemplo con errores cargado.")

    def _ejemplo_for(self):
        codigo = """\
anb
    gz i = 0;
    gz suma = 0;
    fur (i = 0; i < 5; i = i + 1) {
        suma = suma + i;
    }
    dru(suma);
end"""
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", codigo)
        self._linenos.redraw()
        self._limpiar_terminal()
        self._limpiar_salida()
        self._actualizar_estado("Ejemplo con for cargado.")


if __name__ == "__main__":
    app = IDECompilador()
    app.mainloop()
