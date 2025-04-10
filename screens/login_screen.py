# screens/login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class LoginScreen(Screen):
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.layout.size_hint = (None, None)
        self.layout.size = (400, 450)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)  # Fundo escuro
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Título
        self.layout.add_widget(Label(
            text="Bem-vindo",
            font_size=32,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50
        ))

        # Campo de usuário
        self.username_input = TextInput(
            hint_text="Usuário",
            multiline=False,
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.2, 0.4, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 10]
        )
        self.layout.add_widget(self.username_input)

        # Campo de senha
        self.password_input = TextInput(
            hint_text="Senha",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.2, 0.4, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 10]
        )
        self.layout.add_widget(self.password_input)

        # Botão de login
        login_button = Button(
            text="Entrar",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        login_button.bind(on_press=self.verify_credentials)
        self.layout.add_widget(login_button)

        # Mensagem de erro
        self.message_label = Label(size_hint=(1, None), height=30, color=(1, 0.2, 0.2, 1))
        self.layout.add_widget(self.message_label)

        self.add_widget(self.layout)

        self.password_input.bind(on_text_validate=self.verify_credentials)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def verify_credentials(self, _):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.message_label.text = "Preencha todos os campos."
            return

        if self.controller.validar_login(username, password):
            self.manager.current = "main"
        else:
            self.message_label.text = "Usuário ou senha inválidos."
