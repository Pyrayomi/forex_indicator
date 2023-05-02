import sys
import os
from threading import Thread
import sqlite3

import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from PIL import ImageTk, Image
from tradingview_ta import TA_Handler
from pygubu.widgets.scrolledframe import ScrolledFrame


#class CustomWidget_indicator(tk.Frame):
#    def __init__(self, parent, label, default=""):
#        tk.Frame.__init__(self, parent)
#
#        self.label = tk.Label(self, text=label, anchor="w")
#        self.entry = tk.Entry(self)
#        self.entry.insert(0, default)
#
#        self.label.pack(side="top", fill="x")
#        self.entry.pack(side="bottom", fill="x", padx=4)
#
#    def get(self):
#        return self.entry.get()


class Chatv1Widget(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(Chatv1Widget, self).__init__(master, **kw)
        self.frame_nome_contato = ttk.Frame(self)
        self.frame_nome_contato.configure(
            height=200, style="frame.TFrame", width=200)
        self.nome_contato = ttk.Label(self.frame_nome_contato)
        self.nome_contato.configure(
            compound="top",
            foreground="#f7f7f7",
            style="mylabel.TLabel")
        self.nome_contato.grid(column=0, row=0)
        self.frame_nome_contato.grid(column=1, row=0, sticky="nsew")
        self.frame_conversa = ScrolledFrame(self, scrolltype="vertical")
        self.frame_conversa.innerframe.configure(style="frame.TFrame")
        self.frame_conversa.configure(usemousewheel=True)
        self.frame_coversa_interior = ttk.Frame(self.frame_conversa.innerframe)
        self.frame_coversa_interior.configure(
            height=200, style="frame.TFrame", width=200)
        self.frame_coversa_interior.grid(column=0, row=0)
        self.frame_conversa.grid(column=1, row=1, sticky="nsew")
        self.frame_enviar = ttk.Frame(self)
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
        self.frame_contatos = ttk.Frame(self)
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
        #self.configure(height=200, style="frame.TFrame", width=200)
        self.grid(column=0, row=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

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


    def on_button_click(self):
        label = ttk.Label(self.frame_coversa_interior, text=self.text_mensagem.get('1.0', tk.END))
        label.pack(anchor="se")
        label.configure(style='mylabel_conversa.TLabel')
        self.text_mensagem.delete('1.0', tk.END)
        self.contador = self.contador + 1

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


class CustomWidgetIndicatorWidget(tk.Frame):
    def __init__(self, master, papel, **kw):
        super(CustomWidgetIndicatorWidget, self).__init__(master, **kw)
        frame2 = tk.Frame(self)
        frame2.configure(background="#091C2F", height=200, width=200)
        self.moeda = tk.Label(frame2)
        self.moeda.configure(
            background="#091C2F",
            font="{arial} 12 {bold}",
            foreground="#ffffff",
            text=papel)
        self.moeda.grid(column=0, row=0, sticky="w")
        self.recomend = tk.Label(frame2)
        self.recomend.configure(
            background="#091C2F",
            foreground="#ffffff",
            text='label5')
        self.recomend.grid(column=0, row=1, sticky="w")
        self.qtd_up = tk.Label(frame2)
        self.qtd_up.configure(
            background="#091C2F",
            foreground="#ffffff",
            text='qtd_up')
        self.qtd_up.grid(column=0, row=2, sticky="w")
        self.qtd_down = tk.Label(frame2)
        self.qtd_down.configure(
            background="#091C2F",
            foreground="#ffffff",
            text='qtd_down')
        self.qtd_down.grid(column=0, row=3, sticky="w")
        self.qtd_neutro = tk.Label(frame2)
        self.qtd_neutro.configure(
            background="#091C2F",
            foreground="#ffffff",
            text='label4')
        self.qtd_neutro.grid(column=0, row=4, sticky="w")
        frame2.grid(column=0, row=0, sticky="nsew")
        frame3 = tk.Frame(self)
        frame3.configure(background="#232E42", height=200, width=200)
        separator1 = ttk.Separator(self)
        separator1.configure(orient="vertical")
        separator1.grid(column=0, columnspan=2, row=1, sticky="ew")
        self.canvas1 = tk.Canvas(frame3)
        self.canvas1.configure(background="#3ae747", height=100, width=20)
        self.canvas1.grid(column=0, row=0)
        frame3.grid(column=1, row=0)
        self.configure(background="#232E42", height=200, width=200)
        self.grid(column=0, row=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #super(CustomWidgetIndicatorWidget, self).__init__(master, **kw)
        #frame2 = tk.Frame(self)
        #frame2.configure(height=200, width=200)
        #self.moeda = tk.Label(frame2)
        #self.moeda.configure(text='moeda')
        #self.moeda.grid(column=0, row=0)
        #self.recomend = tk.Label(frame2)
        #self.recomend.configure(text='label5')
        #self.recomend.grid(column=0, row=1)
        #self.qtd_up = tk.Label(frame2)
        #self.qtd_up.configure(text='qtd_up')
        #self.qtd_up.grid(column=0, row=2)
        #self.qtd_down = tk.Label(frame2)
        #self.qtd_down.configure(text='qtd_down')
        #self.qtd_down.grid(column=0, row=3)
        #self.qtd_neutro = tk.Label(frame2)
        #self.qtd_neutro.configure(text='label4')
        #self.qtd_neutro.grid(column=0, row=4)
        #frame2.grid(column=0, row=0, sticky="nsew")
        #frame3 = tk.Frame(self)
        #frame3.configure(height=200, width=200)
        #self.canvas1 = tk.Canvas(frame3)
        #self.canvas1.configure(background="#11ef05")
        #self.canvas1.grid(column=0, row=0, sticky="nsew")
        #frame3.grid(column=1, row=0, sticky="nsew")
        #frame3.rowconfigure(0, weight=1)
        #frame3.columnconfigure(0, weight=1)
        #self.configure(background="#f40000", height=200, width=200)
        #self.grid(column=0, row=0, sticky="nsew")
        #self.rowconfigure(0, weight=1)
        #self.columnconfigure(0, weight=1)


class MainInterface:

    def __init__(self):
        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # 2 - LENDO O ARQUIVO UI
        builder.add_from_file(r".\ui\main.ui")

        # 3 - CARREGANDO O CAMINHO DE IMAGENS
        try:
            img_path = os.getcwd() + r"\Imagens"
            img_path = os.path.abspath(img_path)
            self.img_path = img_path
            builder.add_resource_path(self.img_path)
        except Exception as ex:
            print("Não há o caminho de imagens")

        # 4 - CRIANDO A JANELA PRINCIPAL
        self.root = builder.get_object('toplevel_main')

        self.user = None
        builder.import_variables(self, ['user'])

        # 5 - CARREGANDO AS CLASSES ENTRY
        self.setup_ttk_styles()

        builder.connect_callbacks(self)

        builder.connect_callbacks(self)

        # 6 - CARREGANDO O FRAME DE INDICADORES
        self.frame_forex_indicator = self.builder.get_object("frame_indicator")

        # 7 - Dict com todos os papeis ativos
        self.all = {}

        # 8 - Buildando o campo de tempo
        self.entry_tempo = self.builder.get_object("entry_tempo")

        # 9 - Buildando tab meio
        self.notebook_meio = self.builder.get_object("notebook_meio")

        # 10 - Buildando a tab do chat
        self.tab_chat = self.builder.get_object("frame_chat")

        # 9 - Dict indicadores ativos
        # EUR/USD
        # USD/JPY
        # GBP/USD
        # AUD/USD
        # USD/CHF
        # GBP/JPY
        # CAD/CHF
        # USD/CAD
        # EUR/GBP
        # AUD/JPY


    def seleciona_notebook(self, event, notebook, tab):

        """
            Função responsável por fazer a troca de aba
            num objeto notebook tkinter
        :param notebook: tkinter_object
        :param tab: integer
        :return: None
        """
        try:
            notebook.select(tab)
        except Exception as ex:
            print(f"Não foi possível localizar a aba {tab}: {ex}")


    def orquestra_botoes(self):

        """
            Função responsável por definir ação nos botões da tela main
        :return: None
        """

        bt_eurusd = self.builder.get_object('bt_eurusd')
        bt_eurusd.bind("<Button-1>",
                         lambda event, arg=bt_eurusd: MainInterface.multiprocess_oprecao(self, event, "EUR/USD"))

        bt_usdjpy = self.builder.get_object('bt_usdjpy')
        bt_usdjpy.bind("<Button-1>",
                         lambda event, arg=bt_usdjpy: MainInterface.multiprocess_oprecao(self, event, "USD/JPY"))

        bt_gbpusd = self.builder.get_object('bt_gbpusd')
        bt_gbpusd.bind("<Button-1>",
                         lambda event, arg=bt_gbpusd: MainInterface.multiprocess_oprecao(self, event, "GBP/USD"))


        bt_audusd = self.builder.get_object('bt_audusd')
        bt_audusd.bind("<Button-1>",
                         lambda event, arg=bt_audusd: MainInterface.multiprocess_oprecao(self, event, "AUD/USD"))

        bt_usdchf = self.builder.get_object('bt_usdchf')
        bt_usdchf.bind("<Button-1>",
                         lambda event, arg=bt_usdchf: MainInterface.multiprocess_oprecao(self, event, "USD/CHF"))

        bt_gbpjpy = self.builder.get_object('bt_gbpjpy')
        bt_gbpjpy.bind("<Button-1>",
                         lambda event, arg=bt_gbpjpy: MainInterface.multiprocess_oprecao(self, event, "GBP/JPY"))

        bt_cadchf = self.builder.get_object('bt_cadchf')
        bt_cadchf.bind("<Button-1>",
                         lambda event, arg=bt_cadchf: MainInterface.multiprocess_oprecao(self, event, "CAD/CHF"))

        bt_usdcad = self.builder.get_object('bt_usdcad')
        bt_usdcad.bind("<Button-1>",
                         lambda event, arg=bt_usdcad: MainInterface.multiprocess_oprecao(self, event, "USD/CAD"))

        bt_eurgbp = self.builder.get_object('bt_eurgbp')
        bt_eurgbp.bind("<Button-1>",
                         lambda event, arg=bt_eurgbp: MainInterface.multiprocess_oprecao(self, event, "EUR/GBP"))

        bt_audjpy = self.builder.get_object('bt_audjpy')
        bt_audjpy.bind("<Button-1>",
                         lambda event, arg=bt_audjpy: MainInterface.multiprocess_oprecao(self, event, "AUD/JPY"))

        bt_canvas_mini_logo = self.builder.get_object('canvas_mini_logo')
        bt_canvas_mini_logo.bind("<Button-1>",
                         lambda event, arg=bt_canvas_mini_logo: MainInterface.seleciona_notebook(self, event, self.notebook_meio, 0))

        bt_perfil = self.builder.get_object('bt_perfil')
        bt_perfil.bind("<Button-1>",
                         lambda event, arg=bt_perfil: MainInterface.seleciona_notebook(self, event, self.notebook_meio, 1))

        bt_support = self.builder.get_object('bt_support')
        bt_support.bind("<Button-1>",
                         lambda event, arg=bt_support: MainInterface.seleciona_notebook(self, event, self.notebook_meio, 2))

        bt_chat = self.builder.get_object('bt_chat')
        bt_chat.bind("<Button-1>",
                         lambda event, arg=bt_chat: MainInterface.seleciona_notebook(self, event, self.notebook_meio, 3))


    def multiprocess_oprecao(self, event, papel):

        """
            INICIA O BKP EM DIFERENTES PROCESSOS PARA SEREM
            EXECUTADOS EM PARALELO

        @return:
        """
        self.all[papel] = event
        # SCHED TIMER DO BKP
        t = Thread(target=MainInterface.orquestra_sinais, args=(self, event, papel))
        #processes.append(p)
        t.start()


    @staticmethod
    def obtem_campo_texto(campo):

        valor = campo.get()

        return valor


    def orquestra_sinais(self, event, papel):
        t = True


        # Buildando o custom widget
        customwidget = CustomWidgetIndicatorWidget(self.frame_forex_indicator, papel)
        qtd_buildado = len(self.all)
        if qtd_buildado % 2 == 0:
            customwidget.grid(row=qtd_buildado-1, column=1, sticky="ew")
        else:
            customwidget.grid(row=qtd_buildado, column=0, sticky="ew")
        self.all[papel] = customwidget


        while t is True:

            try:

                tempo = MainInterface.obtem_campo_texto(self.entry_tempo)

                recomendacao = MainInterface.obtem_recomendacao(papel.replace('/', ''), str(tempo))

                MainInterface.preenche_recomendacao(customwidget, recomendacao)

                MainInterface.pinta_frame(self, customwidget.canvas1, recomendacao['RECOMMENDATION'])

                #valida = self.Checkbutton_parar.get()
                #if valida == str(1):
                #    t = False
                #else:
                #    pass
            except Exception as ex:
                pass


    def orquestra_chat(self):
        customwidget_chat = Chatv1Widget(self.tab_chat)
        customwidget_chat.grid()


    @staticmethod
    def obtem_recomendacao(simbolo, intervalo):
        handler = TA_Handler()
        handler.symbol = str(simbolo).upper()
        handler.interval = str(intervalo)
        handler.exchange = "FX_IDC"
        handler.screener = "forex"

        analysis = handler.get_analysis()

        #print(analysis.summary)
        #print(analysis.indicators)
        #print(analysis.oscillators)
        #print(analysis.moving_averages)

        return analysis.summary


    @staticmethod
    def preenche_recomendacao(widget, recomendacao):

        widget.qtd_up.config(text=f"Ind. Compra: {str(recomendacao['BUY'])}".upper())
        widget.qtd_down.config(text=f"Ind. Venda: {str(recomendacao['SELL'])}".upper())
        widget.qtd_neutro.config(text=f"Ind. Neutro: {str(recomendacao['NEUTRAL'])}".upper())
        widget.recomend.config(text=f"Recomendacao: {str(recomendacao['RECOMMENDATION'])}".upper())


    def pinta_frame(self, frame, recomendacao):

        if recomendacao == "STRONG_BUY":
            frame.configure(background="#00FF00")
        elif recomendacao == "STRONG_SELL":
            frame.configure(background="#ff0000")
        elif recomendacao == "NEUTRAL":
            frame.configure(background="#ffffff")
        elif recomendacao == "BUY":
            frame.configure(background="#99c140")
        elif recomendacao == "SELL":
            frame.configure(background="#db7b2b")
        else:
            pass


    def setup_ttk_styles(self):
        # ttk styles configuration
        self.style = style = ttk.Style()
        optiondb = style.master

        style.configure("Transparent.TEntry",
                        background="#081B2E",  # Cor de fundo transparente
                        fieldbackground="transparent",  # Cor de fundo do campo de texto transparente
                        highlightthickness=0,  # Remover borda
                        bd=0,  # Remover borda
                        insertbackground="black",  # Cor do cursor
                        font=('Arial', 12, 'bold'),
                        foreground='black'
                        )

        style.configure("mylabel.TLabel", background="black", foreground="white", font="Arial, 15")
        style.configure("mylabel_conversa.TLabel", background="black", foreground="white", font="Arial, 12")
        style.configure("frame.TFrame", background="black")


        style.theme_use('default')
        style.configure('NoTabs.TNotebook', background='#091b2e', foreground='#091b2e', padding=(0, 0, 0, 0), borderwidth=0, overrelief='flat', relief='flat')
        style.layout('NoTabs.TNotebook', [('Notebook.client', {'sticky': 'nswe'})])
        style.layout('NoTabs.TNotebook.Tab', [])

        style.configure("Transparent.TEntry",
                        background="#081B2E",  # Cor de fundo transparente
                        fieldbackground="transparent",  # Cor de fundo do campo de texto transparente
                        highlightthickness=0,  # Remover borda
                        bd=0,  # Remover borda
                        insertbackground="black",  # Cor do cursor
                        font=('Arial', 12, 'bold'),
                        foreground='white'
                        )
        style.configure('Tabless.TNotebook.Tab', background='#091b2e', foreground='#091b2e', padding=(0, 0, 0, 0),
                        borderwidth=0, overrelief='flat', relief='flat')
        # style.map('Tabless.TNotebook.Tab', background=[('selected', '#091b2e')])
        # Remover as abas do Tabless.TNotebook
        style.layout('Tabless.TNotebook.Tab', [])



    def insere_img_canvas(self, objeto_para_imagem, imagem, altura, largura):

        """

            INSERE IMAGEM NO CANVAS CRIADO NO USER INTERFACE.

            # Arguments
                objeto_para_imagem        - Required : Objeto Canvas. (UI)
                imagem                    - Required : Imagem a ser inserida no Canvas. (.jpg | .png)

            # Returns
                validador_query           - Required : Validador de execução da função. (Boolean)

        """

        try:
            # FUNÇÃO DEFINIDA PARA INSERIR IMAGEM NO CANVAS

            objeto_para_imagem.image = ImageTk.PhotoImage(imagem)
            objeto_para_imagem.create_image(altura,
                                            largura,
                                            image=objeto_para_imagem.image,
                                            anchor="nw")

            return True

        except Exception as ex:
            return False


    def seleciona_img_canvas(self, objeto, imagem, altura_imagem, largura_imagem):

        """

            SELECIONA IMAGEM A SER INSERIDO NO CANVAS CRIADO NO USER INTERFACE.

            # Arguments
                objeto                    - Required : Objeto Canvas. (UI)
                imagem                    - Required : Imagem a ser inserida no Canvas. (String)

            # Returns
                validador_query           - Required : Validador de execução da função. (Boolean)

        """

        validador = False

        while validador is False:

            try:
                img = Image.open(self.img_path + "\\" + imagem)

                # INSERINDO A IMAGEM
                validador = MainInterface.insere_img_canvas(self, objeto, img, altura_imagem, largura_imagem)

                return validador
            except Exception as ex:
                return False


    def carrega_img_canvas(self, objeto, imagem, altura_imagem, largura_imagem):

        """

            CARREGA IMAGEM A SER INSERIDO NO CANVAS CRIADO NO USER INTERFACE.

            # Arguments
                objeto                    - Required : Objeto Canvas. (UI)

            # Returns

        """

        try:
            # CANVAS_LOGO
            canvas_logo = self.builder.get_object(objeto)

            # SELECIONANDO A IMAGEM E CARREGANDO A IMAGEM - PESSOA
            MainInterface.seleciona_img_canvas(self, canvas_logo, imagem, altura_imagem, largura_imagem)
        except Exception as ex:
            print(ex)


    def centraliza_janela(self, tamanho_largura = None, tamanho_altura = None):

        """

            CENTRALIZA E DEFINE O TAMANHO DO FRAME PRINCIPAL SENDO RESPONSIVO EM RELAÇÃO AO TAMANHO DA TELA DO USUÁRIO.

            # Arguments

            # Returns

        """

        try:
            # FUNÇÃO DEFINIDA PARA CENTRALIZAR O FRAME

            janela_root = self.root

            janela_root.update_idletasks()

            # DEFININDO LARGURA
            if tamanho_largura == None:
                width = janela_root.winfo_width()
            else:
                width = tamanho_largura

            # DEFININDO ALTURA
            if tamanho_largura == None:
                height = janela_root.winfo_height()
            else:
                height = tamanho_altura

            x = (janela_root.winfo_screenwidth() // 2) - (width // 2)
            y = (janela_root.winfo_screenheight() // 2) - (height // 2)
            janela_root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        except Exception as ex:
            print(ex)


    def resizable(self, resizablelargura, resizablealtura):

        """

            DEFINE A POSSIBILIDADE DE REDIMENSIONAMENTO DA TELA.

            # Arguments
                resizablelargura        - Required : Redimensionamento horizontal. (Boolean)
                resizablealtura         - Required : Redimensionamento vertical. (Boolean)

            # Returns

        """

        try:
            # FUNÇÃO DEFINIDA PARA CONTROLAR O REDIMENSIONAMENTO

            self.root.resizable(resizablelargura, resizablealtura)

        except Exception as ex:
            print(ex)


    def execute(self):

        # O MAINLOOP MANTÉM O FRAME SENDO UTILIZADO EM LOOP
        self.root.mainloop()

        try:
            # O MAINLOOP É FINALIZADO
            self.root.destroy()
        except Exception as ex:
            pass

        # VALIDAÇÃO DO LOG DO USUÁRIO
        #if self.validador_login == True:
        #    Orquestrador_Atuacao()


def Orquestrador_main():

    # INICIANDO O APP
    app_proc = MainInterface()


    # INSERINDO LOGO
    app_proc.carrega_img_canvas("canvas_mini_logo", "forex_indicator_mini_logo.png", 0, 0)

    # Buildando os botões
    app_proc.orquestra_botoes()

    # Buildando o chat
    app_proc.orquestra_chat()

    # CONFIGURANDO
    app_proc.centraliza_janela(640, 480)
    app_proc.resizable(True, True)

    # EXECUTANDO
    app_proc.execute()

if __name__ == '__main__':
    sys.exit(Orquestrador_main())