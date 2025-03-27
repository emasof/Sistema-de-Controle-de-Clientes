# main.py
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from controller import Controller
from login_screen import LoginScreen

class MainScreen(Screen):
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controller  # Recebe o controller do build
        self.edit_mode = False
        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.tabela = GridLayout(cols=4, size_hint_y=None, row_default_height=40, spacing=5, padding=5)
        self.tabela.bind(minimum_height=self.tabela.setter('height'))

        with self.layout_principal.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=self.layout_principal.size, pos=self.layout_principal.pos)

        self.layout_principal.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)

        self.layout_titulo = BoxLayout(size_hint_y=None, height=50)
        self.titulo = Label(text="MAPA DE CONTROLE", color=(242/255, 81/255, 81/255, 1), font_size=30, bold=True)
        self.layout_titulo.add_widget(self.titulo)
        self.layout_principal.add_widget(self.layout_titulo)

        self.barra_superior = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.campo_pesquisa = TextInput(hint_text='Pesquisar: Nome ou Nº do Processo', size_hint=(0.7, None), height=40)
        self.botao_pesquisar = Button(text="Pesquisar", size_hint=(0.10, None), height=40)
        self.botao_pesquisar.bind(on_press=self.pesquisar_cliente)
        self.botao_cadastrar = Button(text="Cadastrar Cliente", size_hint=(0.17, None), height=40)
        self.botao_cadastrar.bind(on_press=self.ir_para_cadastro)
        self.botao_editar = Button(text="Editar", size_hint=(0.1, None), height=40)
        self.botao_editar.bind(on_press=self.ativar_edicao)

        self.barra_superior.add_widget(self.campo_pesquisa)
        self.barra_superior.add_widget(self.botao_pesquisar)
        self.barra_superior.add_widget(self.botao_cadastrar)
        self.barra_superior.add_widget(self.botao_editar)
        self.layout_principal.add_widget(self.barra_superior)

        self.layout_cabecalho = BoxLayout(size_hint_y=None, height=40)
        with self.layout_cabecalho.canvas.before:
            Color(181/255, 117/255, 117/255, 1)
            self.rect_cabecalho = Rectangle(size=self.layout_cabecalho.size, pos=self.layout_cabecalho.pos)
        self.layout_cabecalho.bind(size=self.atualizar_fundo_cabecalho, pos=self.atualizar_fundo_cabecalho)

        self.layout_cabecalho.add_widget(Label(text="Nº DO PROCESSO", bold=True, color=(1, 1, 1, 1)))
        self.layout_cabecalho.add_widget(Label(text="NOME DO CLIENTE", bold=True, color=(1, 1, 1, 1)))
        self.layout_cabecalho.add_widget(Label(text="PACOTE", bold=True, color=(1, 1, 1, 1)))
        self.layout_principal.add_widget(self.layout_cabecalho)

        self.scrollview = ScrollView(size_hint=(1, 1))
        self.scrollview.add_widget(self.tabela)
        self.layout_principal.add_widget(self.scrollview)

        self.add_widget(self.layout_principal)

    def atualizar_fundo(self, *args):
        self.rect.pos = self.layout_principal.pos
        self.rect.size = self.layout_principal.size

    def atualizar_fundo_cabecalho(self, *args):
        self.rect_cabecalho.size = self.layout_cabecalho.size
        self.rect_cabecalho.pos = self.layout_cabecalho.pos

    def atualizar_tabela(self, clientes=None):
        self.tabela.clear_widgets()
        if clientes is None:
            clientes = list(reversed(self.controlador.banco.buscar_clientes()))
        self.tabela.cols = 4

        for cliente in clientes:
            numero_processo = cliente[1]
            nome = cliente[2]
            pacote = cliente[3]

            self.tabela.add_widget(TextInput(text=numero_processo, multiline=False, disabled=not self.edit_mode))
            self.tabela.add_widget(TextInput(text=nome, multiline=False, disabled=not self.edit_mode))
            self.tabela.add_widget(TextInput(text=pacote, multiline=False, disabled=not self.edit_mode))

            if self.edit_mode:
                botao_excluir = Button(text="Excluir", size_hint=(0.1, 1), background_color=(1, 0.2, 0.2, 1), color=(1, 1, 1, 1))
                botao_excluir.bind(on_press=lambda _, processo=numero_processo: self.confirmar_exclusao(processo))
                self.tabela.add_widget(botao_excluir)
            else:
                self.tabela.add_widget(Label(size_hint=(0.1, 1)))

    def confirmar_exclusao(self, numero_processo):
        popup = Popup(title='Confirmar Exclusão', size_hint=(0.5, 0.5))
        layout = GridLayout(cols=2, padding=10, spacing=10)
        layout.add_widget(Label(text=f"Tem certeza que deseja excluir {numero_processo}?"))
        botao_confirmar = Button(text="Sim")
        botao_cancelar = Button(text="Não")
        botao_confirmar.bind(on_press=lambda _: (self.excluir_cliente(numero_processo), popup.dismiss()))
        botao_cancelar.bind(on_press=popup.dismiss)
        layout.add_widget(botao_confirmar)
        layout.add_widget(botao_cancelar)
        popup.content = layout
        popup.open()

    def excluir_cliente(self, numero_processo):
        self.controlador.excluir_cliente(numero_processo)
        self.atualizar_tabela()

    def ativar_edicao(self, _):
        self.edit_mode = not self.edit_mode
        self.botao_editar.text = "Salvar" if self.edit_mode else "Editar"
        if not self.edit_mode:
            for i in range(0, len(self.tabela.children), 4):
                campo_processo = self.tabela.children[i + 3]
                campo_nome = self.tabela.children[i + 2]
                campo_pacote = self.tabela.children[i + 1]
                self.controlador.banco.executar(
                    "UPDATE clientes SET numero_processo = ?, nome = ?, pacote = ? WHERE numero_processo = ?",
                    (campo_processo.text, campo_nome.text, campo_pacote.text, campo_processo.text)
                )
        self.atualizar_tabela()

    def pesquisar_cliente(self, _):
        valor = self.campo_pesquisa.text.strip()
        if valor:
            if valor.isdigit():
                clientes = self.controlador.pesquisar_cliente('numero_processo', valor)
            else:
                clientes = self.controlador.pesquisar_cliente('nome', valor)
        else:
            clientes = self.controlador.pesquisar_cliente('todos', '*')
        self.atualizar_tabela(clientes)

    def ir_para_cadastro(self, _):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        campo_num_processo = TextInput(hint_text="Nº do Processo")
        campo_nome = TextInput(hint_text="Nome do Cliente")
        campo_pacote = TextInput(hint_text="Pacote")
        botao_cadastrar = Button(text="Cadastrar")

        def cadastrar_cliente(*args):
            num_processo = campo_num_processo.text.strip()
            nome = campo_nome.text.strip()
            pacote = campo_pacote.text.strip()

            if num_processo and nome and pacote:
                if self.controlador.registrar_cliente(num_processo, nome, pacote):
                    popup_cadastro.dismiss()
                    self.atualizar_tabela()
                else:
                    Popup(title="Erro", content=Label(text="Número do processo já existe!"),
                          size_hint=(0.5, 0.5)).open()
            else:
                Popup(title="Erro", content=Label(text="Preencha todos os campos!"),
                      size_hint=(0.5, 0.5)).open()

        botao_cadastrar.bind(on_press=cadastrar_cliente)
        layout.add_widget(campo_num_processo)
        layout.add_widget(campo_nome)
        layout.add_widget(campo_pacote)
        layout.add_widget(botao_cadastrar)
        popup_cadastro = Popup(title="Cadastro de Cliente", content=layout, size_hint=(0.6, 0.6))
        popup_cadastro.open()

    def mostrar_erro(self, mensagem):
        popup = Popup(title="Erro", content=Label(text=mensagem), size_hint=(0.5, 0.5))
        popup.open()

class PrizaCreditoApp(App):
    def build(self):
        screen_manager = ScreenManager()
        controller = Controller("clientes.db")  # Cria uma única instância do Controller

        login_screen = LoginScreen(controller=controller, name="login")
        screen_manager.add_widget(login_screen)

        main_screen = MainScreen(controller=controller, name="main")  # Passa o controller para MainScreen
        screen_manager.add_widget(main_screen)

        return screen_manager

if __name__ == "__main__":
    PrizaCreditoApp().run()