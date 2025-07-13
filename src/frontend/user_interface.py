import customtkinter as ctk
import os
import sys
from tkinter import filedialog, messagebox

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "..", "backend")
sys.path.insert(0, backend_dir)

import operations as op
import signature as sign

# App initialization
app = ctk.CTk()
app.title("Assinatura Digital")

# Fullscreen
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{w}x{h}+0+0")

# Grid layout configuration
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

# Important variables
arquivo_selecionado = None
chave_privada = None
current_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.abspath(os.path.join(current_dir, ".."))
pasta_pub = os.path.abspath(os.path.join(projeto_dir, "pub"))
backend_dir = os.path.abspath(os.path.join(projeto_dir, "backend"))
pasta_priv = os.path.abspath(os.path.join(projeto_dir, "priv"))

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

# Atualiza estado dos botões
def atualizar_estado_botoes():
    if arquivo_selecionado:
        botao_assinar.configure(state="normal", fg_color="#03bb29", hover_color="#005227")
        botao_verificar.configure(state="normal", fg_color="#03bb29", hover_color="#005227")
    else:
        botao_assinar.configure(state="disabled", fg_color="gray", hover_color="gray")
        botao_verificar.configure(state="disabled", fg_color="gray", hover_color="gray")

# Janela de assinatura
def abrir_janela_assinatura():
    janela = ctk.CTkToplevel(app)
    janela.title("Assinar Arquivo")
    largura, altura = 500, 260
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.resizable(False, False)
    janela.grab_set()
    janela.grid_columnconfigure(0, weight=1)

    label_instrucao = ctk.CTkLabel(janela, text="Digite sua senha:", font=ctk.CTkFont(size=16))
    label_instrucao.grid(row=0, column=0, pady=(20, 10), padx=20)

    entrada_senha = ctk.CTkEntry(janela, width=300)
    entrada_senha.grid(row=1, column=0, pady=5)

    label_chave = ctk.CTkLabel(janela, text="Nenhuma chave selecionada", font=ctk.CTkFont(size=14))
    label_chave.grid(row=2, column=0, pady=(10, 5))

    def escolher_chave_privada():
        filepath = filedialog.askopenfilename(
            initialdir=pasta_priv,
            title="Selecione a chave privada (.pem)",
            filetypes=[("Arquivos PEM", "*.pem")]
        )
        if filepath:
            chave_privada = filepath
            label_chave.configure(text=f"Chave: {os.path.basename(filepath)}")
        else:
            chave_privada = None
            label_chave.configure(text="Nenhuma chave selecionada")

    botao_chave = ctk.CTkButton(
        janela,
        text="Selecionar Chave Privada",
        command=escolher_chave_privada,
        width=200,
        height=40,
        fg_color="#03bb29",
        hover_color="#005227"
    )
    botao_chave.grid(row=3, column=0, pady=5)
    def concluir_assinatura():
        assinatura = bytearray(entrada_senha.get().encode('utf-8'))
        if assinatura.decode(encoding="utf-8").strip() == "":
            messagebox.showwarning("Senha Inválida", "Por favor, digite sua senha.")
        elif not chave_privada:
            messagebox.showwarning("Chave Privada", "Por favor, selecione a chave privada.")
        else:
            messagebox.showinfo("Sucesso", f"Arquivo assinado com sucesso.\nNome do arquivo: {arquivo_selecionado.split('/')[-1]}") #o local a ser salvo vai ser onde o arquivo original estava
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
    botao_concluir.grid(row=4, column=0, pady=20)

# Janela de geração de chaves
def abrir_janela_gerar_chaves():
    janela = ctk.CTkToplevel(app)
    janela.title("Geração de Chaves")
    largura, altura = 400, 200
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.resizable(False, False)
    janela.grab_set()
    janela.grid_columnconfigure(0, weight=1)

    label_senha = ctk.CTkLabel(janela, text="Digite uma senha para a chave privada:", font=ctk.CTkFont(size=16))
    label_senha.grid(row=0, column=0, pady=(20, 10), padx=20)

    entrada_senha = ctk.CTkEntry(janela, width=300)
    entrada_senha.grid(row=1, column=0, pady=10)

    def gerar_chaves():
        senha = bytearray(entrada_senha.get().encode('utf-8'))
        if senha.decode(encoding="utf-8").strip() == "":
            messagebox.showwarning("Senha vazia", "Por favor, digite uma senha.")
        else:
            op.generate_keys(senha)
            messagebox.showinfo("Sucesso", "Chaves geradas com sucesso!")
            janela.destroy()

    botao_gerar = ctk.CTkButton(
        janela,
        text="Gerar Chaves",
        command=gerar_chaves,
        width=200,
        height=40,
        fg_color="#03bb29",
        hover_color="#005227"
    )
    botao_gerar.grid(row=2, column=0, pady=10)

def abrir_janela_verificacao():
    janela = ctk.CTkToplevel(app)
    janela.title("Verificar Assinatura")
    largura, altura = 500, 220
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.resizable(False, False)
    janela.grab_set()
    janela.grid_columnconfigure(0, weight=1)

    chave_publica = None
    label_chave_pub = ctk.CTkLabel(janela, text="Nenhuma chave pública selecionada", font=ctk.CTkFont(size=14))
    label_chave_pub.grid(row=0, column=0, pady=(20, 10))

    def escolher_chave_publica():
        nonlocal chave_publica
        filepath = filedialog.askopenfilename(
            initialdir=pasta_pub,
            title="Selecione a chave pública (.pem)",
            filetypes=[("Arquivos PEM", "*.pem")]
        )
        if filepath:
            chave_publica = filepath
            label_chave_pub.configure(text=f"Chave: {os.path.basename(filepath)}")
        else:
            chave_publica = None
            label_chave_pub.configure(text="Nenhuma chave pública selecionada")

    botao_selecionar_chave = ctk.CTkButton(
        janela,
        text="Selecionar Chave Pública",
        command=escolher_chave_publica,
        width=200,
        height=40,
        fg_color="#03bb29",
        hover_color="#005227"
    )
    botao_selecionar_chave.grid(row=1, column=0, pady=5)

    def verificar_assinatura():
        if not chave_publica:
            messagebox.showwarning("Chave Pública", "Selecione uma chave pública.")
        elif not arquivo_selecionado:
            messagebox.showwarning("Arquivo", "Nenhum arquivo foi selecionado.")
        else:
            # Aqui entra a lógica real de verificação da assinatura
            # Por enquanto, simulando:
            resultado = True  # ou False
            if resultado:
                messagebox.showinfo("Assinatura Válida", "Arquivo assinado corretamente.")
            else:
                messagebox.showerror("Assinatura Inválida", "Arquivo não foi assinado corretamente.")
            janela.destroy()

    botao_verificar_assinatura = ctk.CTkButton(
        janela,
        text="Verificar Assinatura",
        command=verificar_assinatura,
        width=200,
        height=40,
        fg_color="#03bb29",
        hover_color="#005227"
    )
    botao_verificar_assinatura.grid(row=2, column=0, pady=20)

# Selecionar arquivo
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
    else:
        arquivo_selecionado = None
        label_arquivo.configure(text="Nenhum arquivo selecionado")
    atualizar_estado_botoes()

# Botão: Escolher arquivo
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

# Botão: Gerar chaves (abaixo do escolher arquivo)
botao_gerar = ctk.CTkButton(
    app,
    text="Gerar Chaves",
    command=abrir_janela_gerar_chaves,
    width=200,
    height=40,
    fg_color="#03bb29",
    hover_color="#005227"
)
botao_gerar.grid(row=3, column=0, pady=(5, 10))

# Frame para os botões de ação
botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
botoes_frame.grid(row=4, column=0, pady=(10, 10))

# Botão: Assinar
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

# Botão: Verificar
botao_verificar = ctk.CTkButton(
    botoes_frame,
    text="Verificar Arquivo",
    command=abrir_janela_verificacao,
    width=200,
    height=40,
    fg_color="gray",
    hover_color="gray",
    state="disabled"
)
botao_verificar.grid(row=0, column=1, padx=10)

# Loop
app.mainloop()