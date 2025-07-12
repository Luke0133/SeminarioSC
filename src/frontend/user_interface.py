import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Inicialização do app
app = ctk.CTk()
app.title("Assinatura Digital")

# Tela cheia
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{w}x{h}+0+0")

# Configurar layout de grade
app.grid_columnconfigure(0, weight=1)  # Centraliza coluna principal
app.grid_rowconfigure((0, 1, 2, 3), weight=1)  # Distribui espaço entre as linhas

# Título centralizado no topo
title_label = ctk.CTkLabel(
    app,
    text="Assinador Digital",
    font=ctk.CTkFont("Lato", 40, "bold")
)
title_label.grid(row=0, column=0, pady=(40, 20), sticky="n")

# Funções
def choose_file():
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Selecione o arquivo a ser assinado."
    )
    filename = os.path.basename(filepath)
    if filepath:
        print(f"Arquivo selecionado: {filename}")
    else:
        print("Nenhum arquivo selecionado.")

def choose_folder():
    filepath = filedialog.askdirectory()
    folder_name = os.path.basename(filepath)
    if filepath:
        print(f"Pasta Selecionada: {folder_name}")
    else:
        print("Nenhuma pasta selecionada.")

def message_success():
    messagebox.showinfo("Sucesso", "Arquivo assinado com sucesso!")

def message_error():
    messagebox.showerror("Falha ao assinar", "A assinatura falhou.")

# Botões (organizados verticalmente)
botao_arquivo = ctk.CTkButton(app, text="Escolher Arquivo", command=choose_file, width=200, height=40)
botao_arquivo.grid(row=1, column=0, pady=10)

botao_pasta = ctk.CTkButton(app, text="Escolher Pasta", command=choose_folder, width=200, height=40)
botao_pasta.grid(row=2, column=0, pady=10)
'''
botao_sucesso = ctk.CTkButton(app, text="Simular Sucesso", command=message_success, fg_color="green", width=200)
botao_sucesso.grid(row=3, column=0, pady=10)

botao_erro = ctk.CTkButton(app, text="Simular Erro", command=message_error, fg_color="red", width=200)
botao_erro.grid(row=4, column=0, pady=10)
'''
# Loop da interface
app.mainloop()
