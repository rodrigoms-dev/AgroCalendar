#Autor: Rodrigo Martins da Silva / RU: 4327978
#Data: 10/09/2023

import sqlite3
from tkinter import *
from tkinter import messagebox

def on_enter(e):
    entry_add.delete(0, 'end')

def on_leave(e):
    name = entry_add.get()
    if name == '':
        entry_add.insert(0, 'Digite sua Tarefa')

def on_enter_data(e):
    entry_data.delete(0, 'end')

def on_leave_data(e):
    name = entry_data.get()
    if name == '':
        entry_data.insert(0, 'DD/MM/YYYY')

def mover_foco(event):
    entry_data.focus_set()

#Função para Add tarefa
def adicionar_tarefa():
    tarefa = entry_add.get()
    data = entry_data.get()

    if tarefa == 'Digite sua Tarefa' or data == 'DD/MM/YYYY':
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    cursor.execute('INSERT INTO tarefas (data, tarefa) VALUES (?, ?)', (data, tarefa))
    conn.commit()
    entry_add.delete(0, END)
    entry_add.insert(0, 'Digite sua Tarefa')
    entry_data.delete(0, END)
    entry_data.insert(0, 'DD/MM/YYYY')
    atualizar_lista_tarefas()

    entry_add.focus_set()

#Função para excluir tarefas
def excluir_tarefa():
    selecionado = lista_tarefas.curselection()
    if selecionado:
        indice = selecionado[0]
        tarefa = lista_tarefas.get(indice)
        data, tarefa_text = tarefa.split(' - ', 1)
        cursor.execute('DELETE FROM tarefas WHERE data = ? AND tarefa = ?', (data, tarefa_text))
        conn.commit()
        lista_tarefas.delete(indice)

# Função para ordenar as datas no formato "DD/MM/YYYY"
def ordenar_data(data):
    partes = data.split('/')
    return partes[2], partes[1], partes[0]

#Função para atualizar a lista com o banco de dados
def atualizar_lista_tarefas():
    lista_tarefas.delete(0, END)  # Limpa a lista de tarefas antes de listar novamente
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    tarefas_ordenadas = sorted(tarefas, key=lambda x: ordenar_data(x[1]))
    for tarefa in tarefas_ordenadas:
        data, tarefa_text = tarefa[1], tarefa[2]
        lista_tarefas.insert(END, f'{data} - {tarefa_text}')



# Cores *******************
cor1 = '#f6b86f'
cor2 = '#2a7e44'
cor3 = '#8a1515'
cor4 = '#ffffff'
cor5 = '#32281d'

# Fontes *******************
font1 = 'Stardew Valley Regular'

# Configurações da Janela/Interface gráfica
janela = Tk()
janela.geometry('440x640')
janela.resizable(width=False, height=False)
janela.configure(background=cor1)
janela.title('AgroCalendar')

# Criar ou conectar a um banco de dados
conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

# Criar a tabela de tarefas se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY,
        data TEXT,
        tarefa TEXT
    )
''')
conn.commit()

#Título do programa
label_inicio = Label(janela, background=cor1, text='AgroCalendar', fg=cor5, font=(font1, 35))
label_inicio.grid(row=0, column=0)

# Cria um campo para digitar uma tarefa
entry_add = Entry(janela, background=cor1, borderwidth=6, fg=cor5, width=20, font=(font1, 20))
entry_add.place(x=2, y=65)
entry_add.bind('<Return>', lambda event=None: adicionar_tarefa())
entry_add.bind('<Return>', mover_foco)
entry_add.insert(0, 'Digite sua Tarefa')
entry_add.bind('<FocusIn>', on_enter)
entry_add.bind('<FocusOut>', on_leave)

# Cria um campo para digitar a data para realizar a tarefa
entry_data = Entry(janela, background=cor1, borderwidth=6, fg=cor5, width=10, font=(font1, 20))
entry_data.place(x=290, y=65)
entry_data.bind('<Return>', lambda event=None: botao_adicionar.invoke())
entry_data.insert(0, 'DD/MM/YYYY')
entry_data.bind('<FocusIn>', on_enter_data)
entry_data.bind('<FocusOut>', on_leave_data)

# Cria a lista de tarefas na tela
lista_tarefas = Listbox(janela, width=47, height=20, background=cor1, highlightthickness=0, borderwidth=6, font=(font1, 15))
lista_tarefas.place(x=2, y=120)
atualizar_lista_tarefas()

# Barra de rolagem vertical
scrollbar = Scrollbar(janela, command=lista_tarefas.yview)
scrollbar.place(x=440-15, y=120, height=25)

# Adiciona a barra de rolagem vertical na lista
lista_tarefas.config(yscrollcommand=scrollbar.set)

# Botões
botao_adicionar = Button(janela, background=cor2, activebackground=cor2,fg=cor4, text="Adicionar Tarefa", width=15, font=(font1, 15), borderwidth=6, overrelief='ridge', command=adicionar_tarefa)
botao_adicionar.place(x=295, y=10)

botao_excluir = Button(janela, background=cor3, activebackground=cor3,fg=cor4, text="Excluir Tarefa", width=15, font=(font1, 15), borderwidth=6, overrelief='ridge', command=excluir_tarefa)
botao_excluir.place(x=2, y=550)

# Configuração de layout
for i in range(1, 20):
    janela.grid_rowconfigure(i, weight=1)

# Main Loop
janela.mainloop()
