# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from controller import Controlador
from screens.login_screen import LoginScreen
from screens.main_screen import MainScreen

class PrizaCreditoApp(App):
    def build(self):
        self.controller = Controlador()
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login', controller=self.controller))
        self.sm.add_widget(MainScreen(name='main', controller=self.controller))
        return self.sm

if __name__ == "__main__":
    PrizaCreditoApp().run()
