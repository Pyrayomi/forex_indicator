
import os
import sys
from threading import Thread

from PIL import ImageTk, Image
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
import pygubu

from main import Orquestrador_main

class LoginInterface:

    def __init__(self):
        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # 2 - LENDO O ARQUIVO UI
        builder.add_from_file(r".\ui\login.ui")

        # 3 - CARREGANDO O CAMINHO DE IMAGENS
        try:
            img_path = os.getcwd() + r"\Imagens"
            img_path = os.path.abspath(img_path)
            self.img_path = img_path
            builder.add_resource_path(self.img_path)
        except Exception as ex:
            print("Não há o caminho de imagens")

        # 4 - CRIANDO A JANELA PRINCIPAL
        self.root = builder.get_object('Toplevel_login')

        self.user = None
        builder.import_variables(self, ['user'])

        # 5 - CARREGANDO AS CLASSES ENTRY
        self.setup_ttk_styles()

        builder.connect_callbacks(self)

        # 6 - DEFININDO A VARIÁVEL DE VALIDAÇÃO DE LOGIN
        self.validador_login = False


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
                validador = LoginInterface.insere_img_canvas(self, objeto, img, altura_imagem, largura_imagem)

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
            LoginInterface.seleciona_img_canvas(self, canvas_logo, imagem, altura_imagem, largura_imagem)
        except Exception as ex:
            print(ex)


    def clear_search(event, objeto_event):

        """

            LIMPA CAMPOS QUE JÁ POSSUEM TEXTO PRÉ DEFINIDO.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)

            # Returns

        """

        try:
            # DELETANDO O TEXTO INICIAL DO OBJETO.
            objeto_event.delete(0, tk.END)
        except Exception as ex:
            print(ex)


    def events_entrys(self, objeto_usuario, objeto_senha):

        """

            DEFINE OS EVENTOS DE LIMPEZA DOS CAMPOS USUÁRIO E SENHA APÓS GET FOCUS..
            A LIMPEZA RETIRA OS RÓTULOS PRÉ DEFINIDOS.

            # Arguments
                objeto_usuario             - Required : Objeto para entrada do usuário. (UI)
                objeto_senha               - Required : Objeto para entrada da senha. (UI)

            # Returns

        """

        try:
            # ENTRY USUÁRIO

            # EVENTO APÓS GET FOCUS
            entry_usuario = self.builder.get_object(objeto_usuario)
            entry_usuario.bind("<Button-1>", lambda event, arg=entry_usuario: LoginInterface.clear_search(event, arg))

            # EVENTO APÓS LOST FOCUS
            entry_usuario = self.builder.get_object(objeto_usuario)
            entry_usuario.bind("<FocusOut>", lambda event, arg=entry_usuario: LoginInterface.verifica_pos_lost_focus(event,
                                                                                                                  arg,
                                                                                                                  "Usuário"))

            # ENTRY SENHA

            # EVENTO APÓS GET FOCUS
            entry_senha = self.builder.get_object(objeto_senha)
            entry_senha.bind("<Button-1>", lambda event, arg=entry_senha: LoginInterface.clear_search(event, arg))

            # EVENTO APÓS LOST FOCUS
            entry_senha = self.builder.get_object(objeto_senha)
            entry_senha.bind("<FocusOut>",
                             lambda event, arg=entry_senha: LoginInterface.verifica_pos_lost_focus(event,
                                                                                                arg,
                                                                                                "Senha"))
        except Exception as ex:
            print(ex)


    def verifica_pos_lost_focus(self, objeto_event, texto_original):

        """

            VERIFICA SE OS CAMPOS APÓS PERDEREM O FOCUS, TIVERAM ALGO PREENCHIDO, CASO NÃO, RETORNA AO TEXTO ORIGINAL.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)

            # Returns

        """

        # VERIFICANDO SE HÁ ALGO DIGITADO
        if objeto_event.get() == "":
            # CASO NÃO TENHA NADA DIGITADO, SUBSTITUI PELO TEXTO ORIGINAL
            try:
                # INSERINDO O TEXTO INICIAL DO OBJETO.
                objeto_event.insert(0, texto_original)
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


    def fecha_frame(self):

        """

            DEFINE A POSSIBILIDADE DE REDIMENSIONAMENTO DA TELA.

            # Arguments

            # Returns

        """

        try:
            self.root.quit()
        except Exception as ex:
            print(ex)


    def define_estado_botao(self, objeto, status_botao):

        """

            FUNÇÃO QUE DEFINE O ESTADO DE UM BOTÃO COMO HABILITADO/DESABILITADO.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)
                status_botao               - Required : Estado do botão (enabled/disabled). (String)

            # Returns

        """

        try:
            frame_1 = self.builder.get_object(objeto)
            frame_1["state"] = status_botao
        except Exception as ex:
            print(ex)


    def retorna_value_funcao_objeto(self, componente_funcao, config_funcao):

        """

            FUNÇÃO GEMÉRICA PARA RETORNAR O VALOR DE UMA CONFIGURAÇÃO DO OBJETO.
            Exemplo: Obter o texto contigo em um objeto (object["text"]).

            # Arguments
                componente_funcao           - Required : Objeto para obter config. (UI)
                config_funcao               - Required : Configuração do Objeto que será obtido. (String)

            # Returns
                componente[config_funcao]   - Required : Valor da configuração. (String)

        """

        try:
            # OBTENDO COMPONENTE
            componente = self.builder.get_object(componente_funcao)

            return componente[config_funcao]
        except Exception as ex:
            print(ex)



    def bt_entrar_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE ENTRAR.
            OBTÉM-SE OS VALORES DIGITADOS NOS CAMPOS DE ENTRY USUÁRIO E ENTRY SENHA.
            CHAMA A VALIDAÇÃO DOS PREENCHIMENTOS E DO LOGIN NO MAR2.

            # Arguments

            # Returns

        """

        # DESABILITANDO BOTÃO DE ENTRAR
        LoginInterface.define_estado_botao(self, "Button_login", "disabled")

        # OBTENDO USUÁRIO
        entry_usuario = self.builder.get_object("Entry_login")
        value_usuario = entry_usuario.get().upper()

        # OBTENDO SENHA
        entry_senha = self.builder.get_object("Entry_pwd")
        value_senha = entry_senha.get().upper()

        # VALIDANDO O LOGIN
        self.t = Thread(target=LoginInterface.valida_login, name="nome", daemon=True, args=(self, value_usuario, value_senha,))
        self.t.start()
        #LoginInterface.valida_login(self, value_usuario, value_senha)


    def valida_login(self, usuario, senha):

        # INICIANDO A VARIÁVEL DE VALIDADOR DA EXECUÇÃO DO ORQUESTRADOR (VALIDA_LOGIN).
        validador = False

        if usuario != "" and usuario != "FUNCIONAL DO USUÁRIO":
            if senha != "" and senha != "SENHA":

                # VERIFICANDO SE O BOTÃO ESTÁ COM LABEL - ENTRAR OU NOVO
                if LoginInterface.retorna_value_funcao_objeto(self, "Button_login", "text") == "ENTRAR":

                    # REALIZA A CONSULTA NO BANCO DE DADOS
                    # validador, resultado_consulta_login = LoginInterface.executa_consulta_login_bd(self, self.bd_path, usuario, senha)

                    # CHAMANDO A THREAD DA BARRA DE PROGRESSO

                    #LoginInterface.thread_open(self, LoginInterface.carrega_bar, "ProgressBar", self.queue)

                    # REALIZA A CONSULTA NA API - MAR2
                    #validador, resultado_consulta_login = LoginInterface.executa_consulta_login_mar2(self, self.api_mar2,
                    #                                                                              path_chromedriver, usuario, senha)
                    validador = True
                    resultado_consulta_login = True

                    if validador is True:
                        #validador = False

                        # ELIMINANDO A THREAD ATIVA
                        #LoginInterface.kill_threads(self, self.queue)

                        # VALIDA O RESULTADO
                        # validador = LoginInterface.valida_consulta_login_bd(self, resultado_consulta_login)

                        # VALIDA O RESULTADO DA API - MAR2
                        #validador = LoginInterface.valida_consulta_login_mar2(self, resultado_consulta_login)

                        if validador is True:
                            messagebox.showinfo("Forex Indicator", "LOGIN REALIZADO COM SUCESSO")
                            LoginInterface.fecha_frame(self)

                            self.validador_login = True

                        else:
                            messagebox.showinfo("Forex Indicator", "USUÁRIO OU SENHA INVÁLIDO")

                            """MsgBox = messagebox.askquestion("Forex Indicator", "NOVO USUÁRIO\nDESEJA SE CADASTRAR?",
                                                            icon='warning')
                            if MsgBox == 'yes':
                                # BOTÃO DE ENTRAR ALTERA PARA NOVO
                                LoginInterface.altera_componente_texto(self, "Button_login", "text", "NOVO")
                            else:
                                messagebox.showinfo("Forex Indicator", "TENTE LOGAR NOVAMENTE")
                                # BOTÃO DE NOVO ALTERA PARA ENTRAR
                                LoginInterface.altera_componente_texto(self, "Button_login", "text", "ENTRAR")"""

                else:
                    #LoginInterface.realiza_cadastro(self, self.bd_path, usuario, senha)
                    LoginInterface.fecha_frame(self)
            else:
                messagebox.showinfo("Forex Indicator", "DIGITE UMA SENHA")
        else:
            messagebox.showinfo("Forex Indicator", "DIGITE O USUÁRIO")
        # HABILITANDO BOTÃO DE ENTRAR
        LoginInterface.define_estado_botao(self, "Button_login", "normal")

        try:
            self.t.join()
        except Exception as ex:
            pass


    def execute(self):

        # O MAINLOOP MANTÉM O FRAME SENDO UTILIZADO EM LOOP
        self.root.mainloop()

        try:
            # O MAINLOOP É FINALIZADO
            self.root.destroy()
        except Exception as ex:
            pass

        # VALIDAÇÃO DO LOG DO USUÁRIO
        if self.validador_login == True:
            Orquestrador_main()

def Orquestrador_Login():

    # INICIANDO O APP
    app_proc = LoginInterface()

    # INSERINDO LOGO
    app_proc.carrega_img_canvas("Canvas_logo", "forex_indicator_logo.png", 0, 0)

    # CONFIGURANDO
    app_proc.centraliza_janela(382, 412)
    app_proc.resizable(False, False)

    # DEFININDO EVENTS
    app_proc.events_entrys("Entry_login", "Entry_pwd")

    # EXECUTANDO
    app_proc.execute()


if __name__ == "__main__":
    sys.exit(Orquestrador_Login())