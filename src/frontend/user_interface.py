import customtkinter as ctk
import os
from tkinter import filedialog, Menu, messagebox
from PIL import Image, ImageTk


app = ctk.CTk()
current_dir = os.path.dirname(os.path.abspath(__file__))
ctk.set_appearance_mode("dark")
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry("%dx%d+0+0" % (w, h))
app.title("Assinatura Digital")
app.mainloop()