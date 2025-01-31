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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Controlador para gerenciar os clientes
        self.controlador = Controller()
        self.edit_mode = False  # Estado de edição

        # Layout principal
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Configuração do GridLayout no __init__
        self.tabela = GridLayout(
            cols=4,  # Nº do Processo, Nome, Pacote, Botão Excluir
            size_hint_y=None,
            row_default_height=40,
            spacing=5,
            padding=5
        )
        self.tabela.bind(minimum_height=self.tabela.setter('height'))

        # Adicionando o fundo com canvas
        with self.layout_principal.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Cor de fundo cinza claro
            self.rect = Rectangle(size=self.layout_principal.size, pos=self.layout_principal.pos)

        # Atualiza o fundo quando o layout for redimensionado
        self.layout_principal.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)

        # Título
        self.layout_titulo = BoxLayout(size_hint_y=None, height=50)
        self.titulo = Label(
            text="MAPA DE CONTROLE",
            color=(242 / 255, 81 / 255, 81 / 255, 1),
            font_size=30,
            bold=True
        )
        self.layout_titulo.add_widget(self.titulo)
        self.layout_principal.add_widget(self.layout_titulo)

        # Barra superior com pesquisa, cadastro e edição
        self.barra_superior = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.campo_pesquisa = TextInput(
            hint_text='Pesquisar: Nome ou Nº do Processo',
            size_hint=(0.7, None),
            height=40
        )
        self.botao_pesquisar = Button(
            text="Pesquisar",
            size_hint=(0.10, None),
            height=40
        )
        self.botao_pesquisar.bind(on_press=self.pesquisar_cliente)

        self.botao_cadastrar = Button(
            text="Cadastrar Cliente",
            size_hint=(0.17, None),
            height=40
        )
        self.botao_cadastrar.bind(on_press=self.ir_para_cadastro)

        self.botao_editar = Button(
            text="Editar",
            size_hint=(0.1, None),
            height=40
        )
        self.botao_editar.bind(on_press=self.ativar_edicao)

        self.barra_superior.add_widget(self.campo_pesquisa)
        self.barra_superior.add_widget(self.botao_pesquisar)
        self.barra_superior.add_widget(self.botao_cadastrar)
        self.barra_superior.add_widget(self.botao_editar)
        self.layout_principal.add_widget(self.barra_superior)

        # Cabeçalho da tabela com fundo colorido
        self.layout_cabecalho = BoxLayout(size_hint_y=None, height=40)

        with self.layout_cabecalho.canvas.before:
            Color(181 / 255, 117 / 255, 117 / 255, 1)  # Cor de fundo RGB(181, 117, 117)
            self.rect_cabecalho = Rectangle(size=self.layout_cabecalho.size, pos=self.layout_cabecalho.pos)

        self.layout_cabecalho.bind(size=self.atualizar_fundo_cabecalho, pos=self.atualizar_fundo_cabecalho)

        self.layout_cabecalho.add_widget(Label(text="Nº DO PROCESSO", bold=True, color=(1, 1, 1, 1)))
        self.layout_cabecalho.add_widget(Label(text="NOME DO CLIENTE", bold=True, color=(1, 1, 1, 1)))
        self.layout_cabecalho.add_widget(Label(text="PACOTE", bold=True, color=(1, 1, 1, 1)))
        self.layout_principal.add_widget(self.layout_cabecalho)

        # Tabela de clientes com ScrollView
        self.scrollview = ScrollView(size_hint=(1, 1))
        self.tabela = GridLayout(
            cols=3,  # Três colunas (Nº do Processo, Nome, Pacote)
            size_hint_y=None,
            row_default_height=40,  # Altura das linhas
            spacing=(0, 5),  # Sem espaçamento horizontal; apenas entre linhas
            padding=0
        )
        self.tabela.bind(minimum_height=self.tabela.setter('height'))

        # Adicionar a tabela ao ScrollView
        self.scrollview.add_widget(self.tabela)
        self.layout_principal.add_widget(self.scrollview)

        # Adiciona o layout principal à tela
        self.add_widget(self.layout_principal)

        # Atualiza a tabela ao inicializar
        self.atualizar_tabela()

    def atualizar_fundo(self, *args):
        """Atualiza o fundo quando o layout for redimensionado."""
        self.rect.pos = self.layout_principal.pos
        self.rect.size = self.layout_principal.size

    def atualizar_fundo_cabecalho(self, *args):
        """Atualiza o fundo do cabeçalho da tabela quando o tamanho ou a posição mudar."""
        self.rect_cabecalho.size = self.layout_cabecalho.size
        self.rect_cabecalho.pos = self.layout_cabecalho.pos

    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup

    def atualizar_tabela(self, clientes=None):
        """
        Atualiza a tabela exibindo os clientes cadastrados ou os resultados da pesquisa.

        :param clientes: Lista de clientes (se None, busca todos os clientes).
        """
        self.tabela.clear_widgets()  # Limpa todos os widgets da tabela

        if clientes is None:
            # Busca todos os clientes se nenhum for passado
            clientes = list(reversed(self.controlador.banco.buscar_clientes()))

        # Define o número de colunas (3 campos + 1 botão/excluir ou espaço)
        self.tabela.cols = 4

        for cliente in clientes:
            # Extração dos campos do cliente
            numero_processo = cliente[3]  # Nº do Processo
            nome = cliente[2]  # Nome do Cliente
            pacote = cliente[1]  # Pacote

            # Adiciona os campos na ordem correta
            self.tabela.add_widget(TextInput(
                text=numero_processo,
                multiline=False,
                disabled=not self.edit_mode
            ))
            self.tabela.add_widget(TextInput(
                text=nome,
                multiline=False,
                disabled=not self.edit_mode
            ))
            self.tabela.add_widget(TextInput(
                text=pacote,
                multiline=False,
                disabled=not self.edit_mode
            ))

            # Adiciona o botão excluir, apenas se estiver no modo de edição
            if self.edit_mode:
                botao_excluir = Button(
                    text="Excluir",
                    size_hint=(0.1, 1),
                    background_color=(1, 0.2, 0.2, 1),  # Botão vermelho
                    color=(1, 1, 1, 1)  # Texto branco
                )
                botao_excluir.bind(on_press=lambda _, processo=numero_processo: self.confirmar_exclusao(processo))
                self.tabela.add_widget(botao_excluir)
            else:
                # Adiciona um espaço vazio para alinhamento
                self.tabela.add_widget(Label(size_hint=(0.1, 1)))

            # Garantir preenchimento correto por linha
            while len(self.tabela.children) % 4 != 0:
                self.tabela.add_widget(Label())  # Preenche espaços vazios para manter a estrutura

    def confirmar_exclusao(self, numero_processo):
        """Exibe uma mensagem de confirmação antes de excluir o cliente."""
        # Cria um Popup para confirmação
        popup = Popup(
            title='Confirmar Exclusão',
            size_hint=(0.5, 0.5),
            content=Label(
                text=f"Tem certeza que deseja excluir o cadastro {numero_processo}?",
                halign='center'
            )
        )

        # Botões de confirmação
        layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None)
        botao_confirmar = Button(text="Sim", background_color=(0.2, 0.7, 0.2, 1))
        botao_cancelar = Button(text="Não", background_color=(1, 0.2, 0.2, 1))

        # Ação do botão confirmar
        botao_confirmar.bind(on_press=lambda _: (
            self.excluir_cliente(numero_processo),
            popup.dismiss()
        ))
        # Ação do botão cancelar
        botao_cancelar.bind(on_press=popup.dismiss)

        # Adiciona os botões ao layout do Popup
        layout.add_widget(botao_confirmar)
        layout.add_widget(botao_cancelar)
        popup.content = layout
        popup.open()

    def excluir_cliente(self, numero_processo):
        """Exclui o cliente do banco de dados."""
        self.controlador.banco.excluir_cliente(numero_processo)
        self.atualizar_tabela()  # Atualiza a tabela após a exclusão

    def ativar_edicao(self, _):
        """Ativa ou desativa o modo de edição."""
        self.edit_mode = not self.edit_mode
        self.botao_editar.text = "Salvar" if self.edit_mode else "Editar"

        if not self.edit_mode:  # Salvar as alterações ao sair do modo de edição
            for i in range(0, len(self.tabela.children), 4):  # Itera a cada linha (4 widgets por linha)
                botao_excluir = self.tabela.children[i]  # Último widget: Botão Excluir
                campo_pacote = self.tabela.children[i + 1]  # Penúltimo widget: Pacote
                campo_nome = self.tabela.children[i + 2]  # Nome
                campo_processo = self.tabela.children[i + 3]  # Nº do Processo

                cliente_id = campo_processo.client_id  # Recuperar ID do cliente associado

                # Atualizar os dados no banco de dados
                self.controlador.banco.executar(
                    "UPDATE clientes SET numero_processo = ?, nome = ?, pacote = ? WHERE id = ?",
                    (campo_processo.text, campo_nome.text, campo_pacote.text, cliente_id)
                )

        self.atualizar_tabela()  # Atualizar a tabela com os dados salvos

    def pesquisar_cliente(self, _):
        """Pesquisa clientes com base no número do processo, nome ou retorna todos."""
        valor = self.campo_pesquisa.text.strip()  # Remove espaços em branco

        # Limpa a tabela antes de exibir os resultados
        self.tabela.clear_widgets()

        if valor:  # Se o campo de pesquisa não está vazio
            if valor.isdigit():
                clientes = self.controlador.pesquisar_cliente('numero_processo', valor)
            else:
                clientes = self.controlador.pesquisar_cliente('nome', valor)
        else:  # Caso o campo de pesquisa esteja vazio, busca todos os clientes
            clientes = self.controlador.pesquisar_cliente('todos', '*')

        if clientes:
            # Exibe os resultados na tabela
            for cliente in clientes:
                self.tabela.add_widget(Label(text=cliente[1], color=(0, 0, 0, 1)))  # Nº do Processo
                self.tabela.add_widget(Label(text=cliente[2], color=(0, 0, 0, 1)))  # Nome
                self.tabela.add_widget(Label(text=cliente[3], color=(0, 0, 0, 1)))  # Pacote
        else:
            # Exibe mensagem se não houver resultados
            self.tabela.add_widget(Label(text="", color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text="Nenhum resultado encontrado.", halign="center", color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text="", color=(0, 0, 0, 1)))

    def ir_para_cadastro(self, _):
        """Abre um pop-up para cadastro de novos clientes."""
        layout_formulario = BoxLayout(orientation='vertical', padding=10, spacing=10)
        campo_num_processo = TextInput(hint_text="Nº do Processo", multiline=False, size_hint_y=None, height=30)
        campo_nome_cliente = TextInput(hint_text="Nome do Cliente", multiline=False, size_hint_y=None, height=30)
        spinner_pacote = TextInput(hint_text="Pacote", multiline=False, size_hint_y=None, height=30)

        def cadastrar_cliente(*args):
            num_processo = campo_num_processo.text
            nome_cliente = campo_nome_cliente.text
            pacote = spinner_pacote.text

            if num_processo and nome_cliente and pacote:
                self.controlador.registrar_cliente(num_processo, nome_cliente, pacote)
                popup_cadastro.dismiss()
                self.atualizar_tabela()
            else:
                Popup(title="Erro", content=Label(text="Preencha todos os campos!"), size_hint=(0.5, 0.5)).open()

        botao_cadastrar = Button(text="Cadastrar", size_hint_y=None, height=40)
        botao_cadastrar.bind(on_press=cadastrar_cliente)

        layout_formulario.add_widget(campo_num_processo)
        layout_formulario.add_widget(campo_nome_cliente)
        layout_formulario.add_widget(spinner_pacote)
        layout_formulario.add_widget(botao_cadastrar)

        popup_cadastro = Popup(title="Cadastro de Cliente", content=layout_formulario, size_hint=(0.6, 0.6))
        popup_cadastro.open()


# Classe gerenciador de telas
class ControleDeClienteApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Tela de Login
        login_screen = LoginScreen(name="login")
        screen_manager.add_widget(login_screen)

        # Tela Principal
        main_screen = MainScreen(name="main")
        screen_manager.add_widget(main_screen)

        return screen_manager


if __name__ == "__main__":
    ControleDeClienteApp().run()
