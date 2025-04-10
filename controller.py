# controller.py
from database import BancoDeDados

class Controlador:
    def __init__(self):
        self.banco = BancoDeDados()

    def registrar_cliente(self, numero_processo, nome, pacote):
        return self.banco.adicionar_cliente(numero_processo, nome, pacote)

    def pesquisar_cliente(self, campo, valor):
        return self.banco.buscar_clientes(campo, valor)

    def registrar_usuario(self, usuario, senha):
        self.banco.registrar_usuario(usuario, senha)

    def validar_login(self, usuario, senha):
        return self.banco.validar_credenciais(usuario, senha)

    def buscar_todos_clientes(self):
        return self.banco.buscar_clientes()

    def fechar_conexao(self):
        self.banco.fechar_conexao()
