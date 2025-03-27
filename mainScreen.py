from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from controller import Controlador
from cliente import Cliente
from login_screen import LoginScreen


class MainScreen(Screen):
    def build(self):
        self.controlador = Controlador()

        # Layout principal
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Adicionando o fundo com canvas
        with self.layout_principal.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Cor de fundo cinza claro
            self.rect = Rectangle(size=self.layout_principal.size, pos=self.layout_principal.pos)

        # Atualiza o fundo quando o layout for redimensionado
        self.layout_principal.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)

        # Layout para o título
        self.layout_titulo = BoxLayout(size_hint_y=None, height=50, orientation='horizontal')
        self.titulo = Label(text="MAPA DE CONTROLE", color=(242 / 255, 81 / 255, 81 / 255, 1), font_size=30, bold=True)
        self.layout_titulo.add_widget(self.titulo)

        self.layout_principal.add_widget(self.layout_titulo)

        # Barra superior com pesquisa e botão de cadastro
        self.barra_superior = BoxLayout(size_hint_y=None, height=40, spacing=10)

        # Ajustando o tamanho do campo de pesquisa
        self.campo_pesquisa = TextInput(hint_text='Pesquisar: Nome ou Nº do Processo', size_hint=(0.7, None), height=30)

        # Ajustando o tamanho dos botões
        self.botao_pesquisar = Button(text="Pesquisar", size_hint=(0.15, None), height=30)
        self.botao_pesquisar.bind(on_press=self.pesquisar_cliente)

        self.botao_cadastrar = Button(text="Cadastrar Cliente", size_hint=(0.15, None), height=30)
        self.botao_cadastrar.bind(on_press=self.ir_para_cadastro)

        self.barra_superior.add_widget(self.campo_pesquisa)
        self.barra_superior.add_widget(self.botao_pesquisar)
        self.barra_superior.add_widget(self.botao_cadastrar)

        self.layout_principal.add_widget(self.barra_superior)

        # Tabela com clientes
        self.scrollview = ScrollView(size_hint=(1, 0.7))  # Ajustando para preencher mais espaço
        self.tabela = GridLayout(cols=3, size_hint_y=None, row_default_height=40, spacing=5)
        self.tabela.bind(minimum_height=self.tabela.setter('height'))

        # Cabeçalho da tabela com fundo colorido
        self.layout_cabecalho = BoxLayout(size_hint_y=None, height=40, orientation='horizontal')

        with self.layout_cabecalho.canvas.before:
            Color(181 / 255, 117 / 255, 117 / 255, 1)  # Cor de fundo rgb(181, 117, 117)
            self.rect_cabecalho = Rectangle(size=self.layout_cabecalho.size, pos=self.layout_cabecalho.pos)

        self.layout_cabecalho.bind(size=self.atualizar_fundo_cabecalho, pos=self.atualizar_fundo_cabecalho)

        # Labels para o cabeçalho
        label_processo = Label(text="Nº do Processo", bold=True, color=(1, 1, 7, 1))
        label_nome = Label(text="Nome", bold=True, color=(1, 1, 7, 1))
        label_pacote = Label(text="Pacote", bold=True, color=(1, 1, 7, 1))

        self.layout_cabecalho.add_widget(label_processo)
        self.layout_cabecalho.add_widget(label_nome)
        self.layout_cabecalho.add_widget(label_pacote)

        # Adicionando o cabeçalho diretamente ao layout_principal
        self.layout_principal.add_widget(self.layout_cabecalho)

        # Adicionando a tabela
        self.scrollview.add_widget(self.tabela)
        self.layout_principal.add_widget(self.scrollview)

        # Carregar clientes iniciais
        self.atualizar_tabela()

        return self.layout_principal

    def atualizar_fundo(self, *args):
        """Atualiza o fundo quando o layout for redimensionado."""
        self.rect.pos = self.layout_principal.pos
        self.rect.size = self.layout_principal.size

    def atualizar_fundo_cabecalho(self, *args):
        """Atualiza o fundo da linha do cabeçalho."""
        self.rect_cabecalho.pos = self.layout_cabecalho.pos
        self.rect_cabecalho.size = self.layout_cabecalho.size

    def atualizar_tabela(self):
        """Atualiza a tabela com os clientes mais recentes."""
        self.tabela.clear_widgets()

        # Busca todos os clientes no banco de dados
        clientes = list(reversed(self.controlador.banco.buscar_clientes()))

        for cliente in clientes:
            numero_processo = cliente[1]  # Segundo elemento da tupla
            nome = cliente[2]  # Terceiro elemento da tupla
            pacote = cliente[3]  # Quarto elemento da tupla

            # Adiciona os dados à tabela
            self.tabela.add_widget(Label(text=numero_processo, color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text=nome, color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text=pacote, color=(0, 0, 0, 1)))

    # Atualizar no ControleDeClienteApp
    def pesquisar_cliente(self, _):
        valor = self.campo_pesquisa.text

        if valor.isdigit():
            clientes = self.controlador.pesquisar_cliente('numero_processo', valor)
        else:
            clientes = self.controlador.pesquisar_cliente('nome', valor)

        self.tabela.clear_widgets()

        if clientes:
            for cliente in clientes:
                self.tabela.add_widget(Label(text=cliente[1], color=(0, 0, 0, 1)))
                self.tabela.add_widget(Label(text=cliente[2], color=(0, 0, 0, 1)))
                self.tabela.add_widget(Label(text=cliente[3], color=(0, 0, 0, 1)))
        else:
            self.tabela.add_widget(Label(text=""))
            self.tabela.add_widget(Label(text="Nenhum resultado encontrado.", halign="center", color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text=""))

    def ir_para_cadastro(self, _):
        """Abre um pop-up de cadastro com campos para preencher dados do cliente."""

        # Criar a caixa de layout para o formulário
        layout_formulario = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campo para o Nº do Processo
        campo_num_processo = TextInput(hint_text="Nº do Processo", multiline=False, size_hint_y=None, height=30)

        # Campo para o Nome do Cliente
        campo_nome_cliente = TextInput(hint_text="Nome do Cliente", multiline=False, size_hint_y=None, height=30)

        # Spinner (caixa de seleção) para os pacotes
        spinner_pacote = Spinner(text='Escolha o Pacote', values=('Priza Consumo', 'Priza Negócio', 'Priza Solidário'),
                                 size_hint_y=None, height=30)

        # Botão de cadastro
        # Atualizar no ControleDeClienteApp
        def cadastrar_cliente(*args):
            num_processo = campo_num_processo.text
            nome_cliente = campo_nome_cliente.text
            pacote = spinner_pacote.text

            if num_processo and nome_cliente and pacote != 'Escolha o Pacote':
                self.controlador.registrar_cliente(num_processo, nome_cliente, pacote)

                # Exibir mensagem de sucesso
                popup_sucesso = Popup(title='Cadastro Concluído',
                                      content=Label(text='Cliente cadastrado com sucesso!'),
                                      size_hint=(0.5, 0.5))
                popup_sucesso.open()

                popup_cadastro.dismiss()

                # Atualizar a tabela
                self.atualizar_tabela()
            else:
                popup_erro = Popup(title='Erro',
                                   content=Label(text='Por favor, preencha todos os campos corretamente.'),
                                   size_hint=(0.5, 0.5))
                popup_erro.open()

        # Layout para o botão de cadastro
        botao_cadastrar = Button(text="Cadastrar", size_hint_y=None, height=40)
        botao_cadastrar.bind(on_press=cadastrar_cliente)

        # Adicionando os campos e o botão ao layout
        layout_formulario.add_widget(campo_num_processo)
        layout_formulario.add_widget(campo_nome_cliente)
        layout_formulario.add_widget(spinner_pacote)
        layout_formulario.add_widget(botao_cadastrar)

        # Criar o pop-up de cadastro
        popup_cadastro = Popup(title='Cadastro de Cliente',
                               content=layout_formulario,
                               size_hint=(0.6, 0.6))
        popup_cadastro.open()


if __name__ == '__main__':
    ControleDeClienteApp().run()
