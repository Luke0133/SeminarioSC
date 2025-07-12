import customtkinter as ctk
import os
import sys
from tkinter import filedialog, messagebox

#import operations as functions
#functions.generate_keys("bee")

# App initialization
app = ctk.CTk()
app.title("Assinatura Digital")

# Fullscreen
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{w}x{h}+0+0")

# Grid layout configuration
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure((0, 1, 2, 3), weight=1)

# Important variables
arquivo_selecionado = None
current_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.abspath(os.path.join(current_dir, ".."))

# Title
title_label = ctk.CTkLabel(
    app,
    text="Assinador Digital",
    font=ctk.CTkFont("Lato", 40, "bold")
)
title_label.grid(row=0, column=0, pady=(40, 20), sticky="n")

# File label
label_arquivo = ctk.CTkLabel(app, text="Nenhum arquivo selecionado.", font=ctk.CTkFont(size=16))
label_arquivo.grid(row=1, column=0, pady=(10, 5))

# Function to update buttons based on state
def atualizar_estado_botoes():
    if arquivo_selecionado:
        botao_assinar.configure(state="normal", fg_color="#03bb29", hover_color="#005227")
        botao_verificar.configure(state="normal", fg_color="#03bb29", hover_color="#005227")
    else:
        botao_assinar.configure(state="disabled", fg_color="gray", hover_color="gray")
        botao_verificar.configure(state="disabled", fg_color="gray", hover_color="gray")

# Function of signature window
def abrir_janela_assinatura():
    janela = ctk.CTkToplevel(app)
    janela.title("Assinar Arquivo")
    largura = 400
    altura = 200

    # Centralize
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    janela.resizable(False, False)
    janela.grab_set()
    janela.grid_columnconfigure(0, weight=1)

    label_instrucao = ctk.CTkLabel(janela, text="Digite sua senha:", font=ctk.CTkFont(size=16))
    label_instrucao.grid(row=0, column=0, pady=(20, 10), padx=20)

    entrada_assinatura = ctk.CTkEntry(janela, width=300)
    entrada_assinatura.grid(row=1, column=0, pady=10)

    def concluir_assinatura():
        assinatura = bytearray(entrada_assinatura.get().encode('utf-8'))
        print(assinatura.decode(encoding="utf-8"))
        if assinatura.decode(encoding="utf-8").strip() == "":
            messagebox.showwarning("Senha Inválida", "Por favor, digite sua senha.")
        else:
            messagebox.showinfo("Sucesso", "Arquivo assinado com sucesso.")
            janela.destroy()

    botao_concluir = ctk.CTkButton(
        janela,
        text="Concluir Assinatura",
        command=concluir_assinatura,
        fg_color="#03bb29",
        hover_color="#005227",
        width=200,
        height=40
    )
    botao_concluir.grid(row=2, column=0, pady=20)

# Function to choose file
def choose_file():
    global arquivo_selecionado
    filepath = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~/Downloads"),
        title="Selecione o arquivo a ser assinado."
    )
    if filepath:
        arquivo_selecionado = filepath
        nome = os.path.basename(filepath)
        label_arquivo.configure(text=f"Arquivo selecionado: {nome}")
        print(f"Arquivo selecionado: {nome}")
    else:
        arquivo_selecionado = None
        label_arquivo.configure(text="Nenhum arquivo selecionado")
        print("Nenhum arquivo selecionado.")
    atualizar_estado_botoes()

# "Choose file" button
botao_arquivo = ctk.CTkButton(
    app,
    text="Escolher Arquivo",
    command=choose_file,
    width=200,
    height=40,
    fg_color="#03bb29",
    hover_color="#005227"
)
botao_arquivo.grid(row=2, column=0, pady=(10, 5))

# Horizontal frame to have buttons side by side
botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
botoes_frame.grid(row=3, column=0, pady=(10, 10))

# "Sign file" button
botao_assinar = ctk.CTkButton(
    botoes_frame,
    text="Assinar Arquivo",
    command=abrir_janela_assinatura,
    width=200,
    height=40,
    fg_color="gray",
    hover_color="gray",
    state="disabled"
)
botao_assinar.grid(row=0, column=0, padx=10)

# "Verify file" button
botao_verificar = ctk.CTkButton(
    botoes_frame,
    text="Verificar Arquivo",
    command=lambda: print("Verificar função aqui"),
    width=200,
    height=40,
    fg_color="gray",
    hover_color="gray",
    state="disabled"
)
botao_verificar.grid(row=0, column=1, padx=10)

# Interface loop
app.mainloop()


'''
uma chave privada e várias chaves públicas

To do:
- Ao verificar arquivo, escolher qual chave pública utilizar (usuário procura a chave no sistema)
- 
-
'''