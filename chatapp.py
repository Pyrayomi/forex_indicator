#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
import sqlite3


#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame


class ChatApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel_chat = tk.Tk() if master is None else tk.Toplevel(master)
        self.toplevel_chat.configure(height=200, width=200)
        self.frame_chat = ttk.Frame(self.toplevel_chat)
        self.frame_chat.configure(height=200, style="frame.TFrame", width=200)
        self.frame_nome_contato = ttk.Frame(self.frame_chat)
        self.frame_nome_contato.configure(
            height=200, style="frame.TFrame", width=200)
        self.nome_contato = ttk.Label(self.frame_nome_contato)
        self.nome_contato.configure(
            compound="top",
            foreground="#f7f7f7",
            style="mylabel.TLabel")
        self.nome_contato.pack(side="top")
        self.frame_nome_contato.grid(column=1, row=0, sticky="nsew")
        self.frame_conversa = ScrolledFrame(
            self.frame_chat, scrolltype="vertical")
        self.frame_conversa.innerframe.configure(style="frame.TFrame")
        self.frame_conversa.configure(usemousewheel=True)
        self.frame_coversa_interior = ttk.Frame(self.frame_conversa.innerframe)
        self.frame_coversa_interior.configure(
            height=200, style="frame.TFrame", width=200)
        self.frame_coversa_interior.pack(fill="x", padx=10, side="top")
        self.frame_conversa.grid(column=1, row=1, sticky="nsew")
        self.frame_enviar = ttk.Frame(self.frame_chat)
        self.frame_enviar.configure(height=200, width=200)
        self.text_mensagem = tk.Text(self.frame_enviar)
        self.text_mensagem.configure(
            cursor="arrow",
            exportselection="true",
            font="TkTextFont",
            height=4,
            takefocus=True)
        self.text_mensagem.grid(column=0, row=0, sticky="ew")
        self.Enviar = ttk.Button(self.frame_enviar)
        self.Enviar.configure(
            default="normal",
            state="normal",
            takefocus=False,
            text='Enviar')
        self.Enviar.grid(
            column=1,
            ipadx=1,
            ipady=1,
            padx=1,
            pady=1,
            row=0,
            sticky="nsew")
        self.Enviar.configure(command=self.on_button_click)
        self.frame_enviar.grid(column=1, padx=1, row=2, sticky="nsew")
        self.frame_enviar.grid_anchor("ne")
        self.frame_enviar.rowconfigure(0, weight=1)
        self.frame_enviar.columnconfigure(0, weight=1)
        self.frame_contatos = ttk.Frame(self.frame_chat)
        self.frame_contatos.configure(
            height=200, style="frame.TFrame", width=200)
        self.treeview_contatos = ttk.Treeview(self.frame_contatos)
        self.treeview_contatos.configure(selectmode="extended")
        self.treeview_contatos_cols = ['column']
        self.treeview_contatos_dcols = ['column']
        self.treeview_contatos.configure(
            columns=self.treeview_contatos_cols,
            displaycolumns=self.treeview_contatos_dcols)
        self.treeview_contatos.column(
            "column",
            anchor="center",
            stretch="false",
            width=200,
            minwidth=20)
        self.treeview_contatos.heading(
            "column", anchor="center", text='Contatos')
        self.treeview_contatos.grid(column=0, row=0, sticky="nsew")
        self.frame_contatos.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.frame_contatos.rowconfigure(0, weight=1)
        self.frame_contatos.columnconfigure(0, weight=1)
        self.frame_chat.grid(column=0, row=0, sticky="nsew")
        self.frame_chat.rowconfigure(1, weight=1)
        self.frame_chat.columnconfigure(1, weight=1)
        self.toplevel_chat.rowconfigure(0, weight=1)
        self.toplevel_chat.columnconfigure(0, weight=1)

        # Main widget
        self.mainwindow = self.toplevel_chat


        self.setup_ttk_styles()


        self.treeview_contatos.column("#0", width=0, stretch=tk.NO)
        

        self.contador = 0
        banco = sqlite3.connect("cadastro.db")
        banco.text_factory = lambda x: str(x, 'latin1')
        cursor = banco.cursor()
        cursor.execute("SELECT NAME FROM TBL_USUARIO")
        
        for x in cursor:
            self.treeview_contatos.insert("", "end", values=(x,))
            
        banco.close()
        self.treeview_contatos.bind("<<TreeviewSelect>>", self.on_clicked_item)

    def run(self):
        self.mainwindow.mainloop()


    def on_button_click(self):
        label = ttk.Label(self.frame_coversa_interior, text=self.text_mensagem.get('1.0', tk.END))
        label.pack(anchor="se")
        label.configure(style='mylabel_conversa.TLabel')
        self.text_mensagem.delete('1.0', tk.END)
        self.contador = self.contador + 1

    def on_clicked_item(self, event):
        item = event.widget.focus()
        text = event.widget.item(item)["values"][0]
        self.nome_contato.configure(
            compound="top",
            foreground="#f7f7f7",
            style="mylabel.TLabel",
            text=text)
        for widget in self.frame_coversa_interior.winfo_children():
            widget.destroy() 


    def setup_ttk_styles(self):
        # ttk styles configuration
        self.style = style = ttk.Style()
        optiondb = style.master
        # --------------------
        # This file is used for defining Ttk styles.
        # Use the 'style' object to define styles.

        # Pygubu Designer will need to know which style definition file
        # you wish to use in your project.

        # To specify a style definition file in Pygubu Designer:
        # Go to: Edit -> Preferences -> Ttk Styles -> Browse (button)

        # In Pygubu Designer:
        # Assuming that you have specified a style definition file,
        # - Use the 'style' combobox drop-down menu in Pygubu Designer
        #   to select a style that you have defined.
        # - Changes made to the chosen style definition file will be
        #   automatically reflected in Pygubu Designer.
        # --------------------

        # Example code:
        style.configure(
            "mylabel.TLabel",
            background="black",
            foreground="white",
            font="Arial, 15")
        style.configure(
            "mylabel_conversa.TLabel",
            background="black",
            foreground="white",
            font="Arial, 12")
        style.configure("frame.TFrame", background="black")


if __name__ == "__main__":
    app = ChatApp()
    app.run()
