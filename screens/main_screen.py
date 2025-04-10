# screens/main_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import shutil
import datetime
import os

class MainScreen(Screen):
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Fundo
        with self.layout_principal.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.layout_principal.size, pos=self.layout_principal.pos)
        self.layout_principal.bind(size=self._update_bg, pos=self._update_bg)

        # Título
        titulo = Label(text="MAPA DE CONTROLE", font_size=28, color=(0.2, 0.2, 0.6, 1), size_hint_y=None, height=40)
        self.layout_principal.add_widget(titulo)

        # Barra superior
        barra = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.campo_pesquisa = TextInput(
            hint_text="Pesquisar: Nome ou Nº do Processo",
            size_hint=(0.4, 1)
        )
        botao_pesquisar = Button(text="Pesquisar", size_hint=(0.15, 1))
        botao_pesquisar.bind(on_press=self.pesquisar_cliente)
        botao_cadastrar = Button(text="Cadastrar Cliente", size_hint=(0.15, 1))
        botao_cadastrar.bind(on_press=self.ir_para_cadastro)
        botao_exportar = Button(text="Exportar", size_hint=(0.15, 1))
        botao_exportar.bind(on_press=self.abrir_menu_exportar)
        botao_backup = Button(text="Backup", size_hint=(0.15, 1))
        botao_backup.bind(on_press=self.fazer_backup)
        barra.add_widget(self.campo_pesquisa)
        barra.add_widget(botao_pesquisar)
        barra.add_widget(botao_cadastrar)
        barra.add_widget(botao_exportar)
        barra.add_widget(botao_backup)
        self.layout_principal.add_widget(barra)

        # Cabeçalho da tabela
        cabecalho = BoxLayout(size_hint_y=None, height=30)
        with cabecalho.canvas.before:
            Color(0.6, 0.3, 0.3, 1)
            self.rect_header = Rectangle(size=cabecalho.size, pos=cabecalho.pos)
        cabecalho.bind(size=self._update_header, pos=self._update_header)
        cabecalho.add_widget(Label(text="Nº Processo", color=(1, 1, 1, 1)))
        cabecalho.add_widget(Label(text="Nome", color=(1, 1, 1, 1)))
        cabecalho.add_widget(Label(text="Produtogit add .git add .", color=(1, 1, 1, 1)))
        self.layout_principal.add_widget(cabecalho)

        # Tabela
        self.scroll = ScrollView()
        self.tabela = GridLayout(cols=3, size_hint_y=None, row_default_height=30, spacing=5)
        self.tabela.bind(minimum_height=self.tabela.setter("height"))
        self.scroll.add_widget(self.tabela)
        self.layout_principal.add_widget(self.scroll)

        self.add_widget(self.layout_principal)
        self.atualizar_tabela()

    def _update_bg(self, *args):
        self.rect.size = self.layout_principal.size
        self.rect.pos = self.layout_principal.pos

    def _update_header(self, *args):
        self.rect_header.size = args[0].size
        self.rect_header.pos = args[0].pos

    def atualizar_tabela(self, clientes=None):
        self.tabela.clear_widgets()
        if not clientes:
            clientes = list(reversed(self.controller.buscar_todos_clientes()))
        for cliente in clientes:
            self.tabela.add_widget(Label(text=cliente[1], color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text=cliente[2], color=(0, 0, 0, 1)))
            self.tabela.add_widget(Label(text=cliente[3], color=(0, 0, 0, 1)))

    def pesquisar_cliente(self, _):
        valor = self.campo_pesquisa.text.strip()
        if valor:
            campo = "numero_processo" if valor.isdigit() else "nome"
            clientes = self.controller.pesquisar_cliente(campo, valor)
        else:
            clientes = self.controller.buscar_todos_clientes()
        self.atualizar_tabela(clientes)

    def ir_para_cadastro(self, _):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        campo_processo = TextInput(hint_text="Nº do Processo", multiline=False)
        campo_nome = TextInput(hint_text="Nome do Cliente", multiline=False)
        spinner_pacote = Spinner(
            text="Escolha o Pacote",
            values=["Priza Consumo", "Priza Negócio", "Priza Solidário"]
        )

        def cadastrar_cliente(_):
            num = campo_processo.text.strip()
            nome = campo_nome.text.strip()
            pacote = spinner_pacote.text
            if num and nome and pacote != "Escolha o Pacote":
                sucesso = self.controller.registrar_cliente(num, nome, pacote)
                if sucesso:
                    self.atualizar_tabela()
                    popup.dismiss()
                    self._mostrar_popup("Sucesso", "Cliente cadastrado com sucesso!")
                else:
                    self._mostrar_popup("Erro", "Nº de processo já existe.")
            else:
                self._mostrar_popup("Erro", "Preencha todos os campos.")

        botao = Button(text="Cadastrar", size_hint_y=None, height=40)
        botao.bind(on_press=cadastrar_cliente)

        layout.add_widget(campo_processo)
        layout.add_widget(campo_nome)
        layout.add_widget(spinner_pacote)
        layout.add_widget(botao)

        popup = Popup(title="Cadastro de Cliente", content=layout, size_hint=(0.6, 0.6))
        popup.open()

    def _mostrar_popup(self, titulo, mensagem):
        Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.5, 0.5)).open()

    def abrir_menu_exportar(self, _):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botao_xlsx = Button(text="Exportar para XLSX")
        botao_pdf = Button(text="Exportar para PDF")
        botao_cancelar = Button(text="Cancelar")

        popup = Popup(title="Exportar Dados", content=layout, size_hint=(0.4, 0.4))
        botao_xlsx.bind(on_press=lambda _: (self.exportar_xlsx(), popup.dismiss()))
        botao_pdf.bind(on_press=lambda _: (self.exportar_pdf(), popup.dismiss()))
        botao_cancelar.bind(on_press=lambda _: popup.dismiss())

        layout.add_widget(botao_xlsx)
        layout.add_widget(botao_pdf)
        layout.add_widget(botao_cancelar)
        popup.open()

    def exportar_xlsx(self):
        clientes = self.controller.buscar_todos_clientes()
        wb = Workbook()
        ws = wb.active
        ws.title = "Clientes"
        ws.append(["Nº Processo", "Nome", "Pacote"])
        for c in clientes:
            ws.append([c[1], c[2], c[3]])
        wb.save("clientes_exportados.xlsx")
        self._mostrar_popup("Sucesso", "Dados exportados para clientes_exportados.xlsx")

    def exportar_pdf(self):
        clientes = self.controller.buscar_todos_clientes()
        pdf = SimpleDocTemplate("clientes_exportados.pdf", pagesize=letter)
        data = [["Nº Processo", "Nome", "Pacote"]] + [[c[1], c[2], c[3]] for c in clientes]
        tabela = Table(data)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        pdf.build([tabela])
        self._mostrar_popup("Sucesso", "Dados exportados para clientes_exportados.pdf")

    def fazer_backup(self, _):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        backup_path = os.path.join(backup_dir, f"clientes_{timestamp}.db")
        try:
            shutil.copy("clientes.db", backup_path)
            self._mostrar_popup("Backup", f"Backup criado: {backup_path}")
        except Exception as e:
            self._mostrar_popup("Erro", f"Erro ao criar backup: {e}")
