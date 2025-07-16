import customtkinter as ctk
import os
import sys
from tkinter import filedialog, messagebox

# Important variables
arquivo_selecionado = None
chave_privada = None
current_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.abspath(os.path.join(current_dir, ".."))
pasta_pub = os.path.abspath(os.path.join(projeto_dir, "pub"))
backend_dir = os.path.abspath(os.path.join(projeto_dir, "backend"))
pasta_priv = os.path.abspath(os.path.join(projeto_dir, "priv"))

sys.path.insert(0, backend_dir)

import operations as op
import signature as sign

# App initialization
app = ctk.CTk()
app.title("Assinatura Digital")

# Screen size
'''
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{w}x{h}+0+0")
'''
app.geometry("800x450")

# Grid layout configuration
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

# Frame configuration
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.grid(row=0, column=0, rowspan=6, sticky="nsew", padx=60, pady=20)
main_frame.grid_columnconfigure(0, weight=1)

# Title
title_label = ctk.CTkLabel(
    main_frame,
    text="Assinador Digital",
    font=ctk.CTkFont("Lato", 40, "bold")
)
title_label.grid(row=0, column=0, pady=(40, 20), sticky="n")

# File label
label_arquivo = ctk.CTkLabel(main_frame, text="Nenhum arquivo selecionado.", font=ctk.CTkFont(size=16))
label_arquivo.grid(row=1, column=0, pady=(10, 15))

# Update buttons state
def atualizar_estado_botoes():
    if arquivo_selecionado:
        botao_assinar.configure(state="normal", fg_color="#03bb29", hover_color="#005227")
        botao_verificar.configure(state="normal", fg_color="#03bb29", hover_color="#005227")
    else:
        botao_assinar.configure(state="disabled", fg_color="gray", hover_color="gray")
        botao_verificar.configure(state="disabled", fg_color="gray", hover_color="gray")

# Signature window
def abrir_janela_assinatura():
    janela = ctk.CTkToplevel(app)
    janela.title("Assinar Arquivo")
    largura, altura = 500, 260
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.resizable(False, False)
    janela.wait_visibility()
    janela.grab_set()
    janela.grid_columnconfigure(0, weight=1)

    label_instrucao = ctk.CTkLabel(janela, text="Digite sua senha:", font=ctk.CTkFont(size=16))
    label_instrucao.grid(row=0, column=0, pady=(20, 10), padx=20)

    entrada_senha = ctk.CTkEntry(janela, width=300)
    entrada_senha.grid(row=1, column=0, pady=5)

    chave_privada = None
    label_chave = ctk.CTkLabel(janela, text="Nenhuma chave selecionada", font=ctk.CTkFont(size=14))
    label_chave.grid(row=2, column=0, pady=(10, 5))

    def escolher_chave_privada():
        nonlocal chave_privada
        filepath = filedialog.askopenfilename(
            initialdir=pasta_priv,
            title="Selecione a chave privada (.pem)",
            filetypes=[("Arquivos PEM", "*.pem")],
            parent=janela
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
        senha = bytearray(entrada_senha.get().encode('utf-8'))
        if senha.decode(encoding="utf-8").strip() == "":
            messagebox.showwarning("Senha Inválida", "Por favor, digite sua senha.")
        elif chave_privada is None:
            messagebox.showwarning("Chave Privada", "Por favor, selecione a chave privada.")
        else:
            try:
                if arquivo_selecionado:
                    op.sign_file(senha, arquivo_selecionado, chave_privada) 
                    for i in range(0, len(senha)): # Limpa a senha 
                        senha[i] = 0               # da memória
                    messagebox.showinfo("Sucesso", f"Arquivo assinado com sucesso.\nNome do arquivo: {os.path.basename(arquivo_selecionado)}", parent=janela)
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Nenhum arquivo selecionado", parent=janela)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao assinar arquivo: {str(e)}", parent=janela)

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

# Key generation window
def abrir_janela_gerar_chaves():
    janela = ctk.CTkToplevel(app)
    janela.title("Geração de Chaves")
    largura, altura = 400, 200
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.resizable(False, False)
    janela.wait_visibility()
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
            try:
                op.generate_keys(senha)
                for i in range(0, len(senha)): # Limpa a senha 
                    senha[i] = 0               # da memória
                messagebox.showinfo("Sucesso", "Chaves geradas com sucesso!", parent=janela)
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar chaves: {str(e)}", parent=janela)

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

# Key verification window
def abrir_janela_verificacao():
    janela = ctk.CTkToplevel(app)
    janela.title("Verificar Assinatura")
    largura, altura = 500, 220
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.resizable(False, False)
    janela.wait_visibility()
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
            filetypes=[("Arquivos PEM", "*.pem")],
            parent=janela
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
            try:
                sig_path = arquivo_selecionado + ".sig"
                if not os.path.exists(sig_path):
                    messagebox.showerror("Erro", "Arquivo de assinatura não encontrado. O arquivo deve ter sido assinado primeiro.", parent=janela)
                    return

                resultado = op.verify_file(arquivo_selecionado, sig_path, chave_publica)

                if resultado:
                    messagebox.showinfo("Assinatura Válida", "Arquivo assinado corretamente e a assinatura é válida.", parent=janela)
                else:
                    messagebox.showerror("Assinatura Inválida", "A assinatura do arquivo não é válida ou foi corrompida.", parent=janela)
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao verificar assinatura: {str(e)}", parent=janela)

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

# Select file
def choose_file():
    global arquivo_selecionado
    filepath = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~/Downloads"),
        title="Selecione o arquivo a ser assinado.",
    )
    if filepath:
        arquivo_selecionado = filepath
        nome = os.path.basename(filepath)
        label_arquivo.configure(text=f"Arquivo selecionado: {nome}")
    else:
        arquivo_selecionado = None
        label_arquivo.configure(text="Nenhum arquivo selecionado")
    atualizar_estado_botoes()

# Buttons frame
botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
botoes_frame.grid(row=4, column=0, pady=(10, 10), padx=10, sticky="n")
botoes_frame.grid_columnconfigure((0, 1), weight=1)

# Buttons
botao_arquivo = ctk.CTkButton(
    main_frame,
    text="Escolher Arquivo",
    command=choose_file,
    width=220,
    height=42,
    fg_color="#03bb29",
    hover_color="#005227"
)
botao_arquivo.grid(row=2, column=0, pady=(5, 10))

botao_gerar = ctk.CTkButton(
    main_frame,
    text="Gerar Chaves",
    command=abrir_janela_gerar_chaves,
    width=220,
    height=42,
    fg_color="#03bb29",
    hover_color="#005227"
)
botao_gerar.grid(row=3, column=0, pady=(5, 20))

botao_assinar = ctk.CTkButton(
    botoes_frame,
    text="Assinar Arquivo",
    command=abrir_janela_assinatura,
    width=180,
    height=40,
    fg_color="gray",
    hover_color="gray",
    state="disabled"
)
botao_assinar.grid(row=0, column=0, padx=20, pady=12)

botao_verificar = ctk.CTkButton(
    botoes_frame,
    text="Verificar Arquivo",
    command=abrir_janela_verificacao,
    width=180,
    height=40,
    fg_color="gray",
    hover_color="gray",
    state="disabled"
)
botao_verificar.grid(row=0, column=1, padx=20, pady=12)

# App Loop
app.mainloop()