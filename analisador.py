import tkinter as tk
from tkinter import ttk, messagebox
import ply.lex as lex
import ply.yacc as yacc

# Define tokens
tokens = [
    'AS',
    'PA',
    'PC',
    'CM',
    # 'CC',
    'CO',
    'LA',
    'LC',
    'OR',
    'TP',
    'ID',
    'NUMBER'
]

# Define reserved words
reserved = {
    'int': 'TP',
    'string': 'TP',
    'Fn': 'F',
    'contenido': 'C',
    'if': 'I',
    'else': 'E',
    'while': 'W',
    'switch': 'SW',
    'case': 'CE',
    'default': 'DT',
    'break': 'BR',
    'rtn': 'RT',
}

tokens += list(reserved.values())


# t_TP = r'int|string'
t_PA = r'\('
t_PC = r'\)'
t_LA = r'\{'
t_LC = r'\}'
t_CM = r'"'
# t_CC = r'"'
t_CO = r','
t_AS = r'=>'
t_OR = r'(<|>|==|>=|<=|!=)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# def p_empty(p):
#     'empty :'
#     pass

t_ignore = ' \t\n'

def t_error(t):
    error_table.insert('', 'end', values=(f"Illegal character '{t.value[0]}'",))
    t.lexer.skip(1)

lexer = lex.lex()

def p_PX(p):
    '''PX : V
            | RF
            | RI
            | RW
            | S'''
#VARIABLES
def p_V(p):
    '''V : ID AS TP VL'''
        
#FUNCION                
def p_RF(p):
    '''RF : F AS ID PR LA C R LC'''

#IF-ELSE               
def p_RI(p):
    '''RI : I CD AS LA C LC RE'''

#WHILE 
def p_RW(p):
    '''RW : W CD AS LA C LC'''
    
#SWITCH    
def p_S(p):
    '''S : SW OP AS LA CA RCA DF LC'''
                 
#PRODUCCIONES    
def p_VL(p):
    '''VL : PA CM ID CM PC
                 | PA NUMBER PC
                 | '''
          
def p_P(p):
    '''P : TP ID
                 | '''
    
def p_PR(p):
    '''PR : PA P RP PC'''
    
def p_RP(p):
    '''RP : CO P RP
            | '''
    
def p_CD(p):
    '''CD : PA ID OR RC PC'''
    
def p_RC(p):
    '''RC : ID
            | NUMBER'''

def p_RE(p):
    '''RE : E AS LA C LC
            | '''
                  
def p_OP(p):
    '''OP : PA ID PC'''
    
def p_CA(p):
    '''CA : CE NUMBER AS LA C BR LC'''
    
def p_RCA(p):
    '''RCA : CA RCA
            | '''
            
def p_DF(p):
    '''DF : DT AS LA C LC'''
    
def p_R(p):
    '''R : RT ORT
            | '''
            
def p_ORT(p):
    '''ORT : PA CM ID CM PC
            | PA ID PC
            | PA  NUMBER PC'''
                                       

                  
def p_error(p):
    if p:
        error_table.insert('', 'end', values=(f"Error de sintaxis en token '{p.value}'",))
    else:
        error_table.insert('', 'end', values=("Error de sintaxis en EOF",))

parser = yacc.yacc()

symbol_table = set()

def check_code():
    for i in token_table.get_children():
        token_table.delete(i)
    for i in error_table.get_children():
        error_table.delete(i)

    code = txt.get("1.0", tk.END).strip()
    if not code:
        result_label.config(text="No hay código para verificar.")
        return

    symbol_table.clear()

    lexer.input(code)

    for token in lexer:
        if token.type == 'DOUBLESTRING':
            value = token.value[1:-1]
        else:
            value = token.value
        token_table.insert('', 'end', values=(token.type, value))

    result = parser.parse(code, lexer=lexer)

    if not error_table.get_children():
        result_label.config(text="La sintaxis es correcta.")
    else:
        result_label.config(text="Se encontraron errores de sintaxis.")

root = tk.Tk()
root.title("Analizador Lexico y Sintactico")
root.configure(bg='white')

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

codigo = '''numero => int(99)'''
txt = tk.Text(main_frame, width=40, height=20)
txt.grid(row=0, column=0, padx=10, pady=10)
txt.insert(tk.END, codigo)

btn = tk.Button(main_frame, text="Analizar", command=check_code, width=10, height=2)
btn.grid(row=1, column=0, padx=10, pady=10)

token_frame = ttk.LabelFrame(main_frame, text="Tokens", padding=10)
token_frame.grid(row=0, column=1, padx=10, pady=10)

token_table = ttk.Treeview(token_frame, columns=('Type', 'Value'), show='headings')
token_table.heading('Type', text='Token')
token_table.heading('Value', text='Valor')
token_table.pack()

error_frame = ttk.LabelFrame(main_frame, text="Errores de Sintaxis", padding=10)
error_frame.grid(row=1, column=1, padx=10, pady=10)

error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings')
error_table.heading('Error', text='Mensaje de Error')
error_table.column('Error', width=200)
error_table.pack()

result_label = tk.Label(main_frame, text="", fg="red")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()




# ----------------------------------------------------------------
# def check_code():
#     for i in token_table.get_children():
#         token_table.delete(i)
#     for i in error_table.get_children():
#         error_table.delete(i)

#     code = txt.get("1.0", tk.END).strip()
#     if not code:
#         messagebox.showinfo('Resultado', 'No hay código para verificar.')
#         return

#     symbol_table.clear()

#     lexer.input(code)

#     for token in lexer:
#         if token.type == 'DOUBLESTRING':
#             value = token.value[1:-1]
#         else:
#             value = token.value
#         token_table.insert('', 'end', values=(token.type, value))

#     result = parser.parse(code, lexer=lexer)

#     if not error_table.get_children():
#         messagebox.showinfo('Resultado', 'La sintaxis es correcta.')
#     else:
#         messagebox.showerror('Resultado', 'Se encontraron errores de sintaxis.')

# root = tk.Tk()
# root.title("Analizador Lexico y Sintactico")
# root.configure(bg='white')  # Fondo blanco para la ventana principal

# # Crear un marco principal para organizar la interfaz
# main_frame = ttk.Frame(root, padding=10)
# main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# # Crear el cuadro de texto para el código
# codigo = '''numero => int(99)'''
# txt = tk.Text(main_frame, width=25, height=10)
# txt.grid(row=0, column=0, padx=10, pady=10)
# txt.insert(tk.END, codigo)

# # Crear el botón de análisis
# btn = tk.Button(main_frame, text="Analizar", command=check_code)
# btn.grid(row=1, column=0, padx=10, pady=10)

# # Crear un marco para mostrar los tokens
# token_frame = ttk.LabelFrame(main_frame, text="Tokens", padding=10)
# token_frame.grid(row=0, column=1, padx=10, pady=10)

# token_table = ttk.Treeview(token_frame, columns=('Type', 'Value'), show='headings')
# token_table.heading('Type', text='Token')
# token_table.heading('Value', text='Valor')
# token_table.pack()

# # Crear un marco para mostrar los errores de sintaxis
# error_frame = ttk.LabelFrame(main_frame, text="Errores de Sintaxis", padding=10)
# error_frame.grid(row=1, column=1, padx=10, pady=10)

# error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings')
# error_table.heading('Error', text='Mensaje de Error')
# error_table.column('Error', width=200)
# error_table.pack()

# root.mainloop()
