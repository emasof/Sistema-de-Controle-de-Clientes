from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout Principal
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.layout.size_hint = (None, None)
        self.layout.size = (300, 400)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Background com gradiente
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)  # Fundo escuro
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)

        # Atualizar o fundo quando a janela for redimensionada
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Título
        title = Label(
            text="Bem-vindo",
            font_size=32,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        self.layout.add_widget(title)

        # Campo de Usuário
        self.username_input = TextInput(
            hint_text="Usuário",
            size_hint=(1, 0.2),
            multiline=False,
            padding=(10, 10),
            background_color=(0.2, 0.2, 0.4, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.layout.add_widget(self.username_input)

        # Campo de Senha
        self.password_input = TextInput(
            hint_text="Senha",
            size_hint=(1, 0.2),
            multiline=False,
            password=True,
            padding=(10, 10),
            background_color=(0.2, 0.2, 0.4, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.layout.add_widget(self.password_input)

        # Botão de Login
        login_button = Button(
            text="Login",
            size_hint=(1, 0.2),
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
        )
        login_button.bind(on_press=self.verify_credentials)
        self.layout.add_widget(login_button)

        # Mensagem de erro ou sucesso
        self.message_label = Label(size_hint=(1, 0.2), color=(1, 0.2, 0.2, 1))
        self.layout.add_widget(self.message_label)

        self.add_widget(self.layout)

        # Vincular a tecla "Enter" para a ação de login
        self.password_input.bind(on_text_validate=self.verify_credentials)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def verify_credentials(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        # Credenciais fixas para demonstração
        if username == "admin" and password == "1234":
            self.message_label.text = ""  # Limpa mensagem de erro
            self.manager.current = "cadastro_cliente"  # Troca para a tela de cadastro de clientes
        else:
            self.message_label.text = "Usuário ou senha inválidos."
