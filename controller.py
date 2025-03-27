# controller.py
import sqlite3
from database import BancoDeDados

class Controller:
    def __init__(self, database_path):
        self.database_path = database_path
        self.banco = BancoDeDados(database_path)

    def connect_to_database(self):
        pass

    def close_connection(self):
        self.banco.fechar_conexao()

    def registrar_cliente(self, numero_processo, nome, pacote):
        """Registra um novo cliente e retorna True se bem-sucedido, False se duplicado."""
        return self.banco.adicionar_cliente(numero_processo, nome, pacote)

    def pesquisar_cliente(self, filtro, valor):
        if filtro == 'todos':
            return self.banco.buscar_clientes()
        elif filtro == 'numero_processo':
            return self.banco.buscar_clientes('numero_processo', valor)
        elif filtro == 'nome':
            return self.banco.buscar_clientes('nome', valor)
        return []

    def excluir_cliente(self, numero_processo):
        self.banco.executar("DELETE FROM clientes WHERE numero_processo = ?", (numero_processo,))

    def validar_credenciais(self, username, password):
        return self.banco.validar_credenciais(username, password)