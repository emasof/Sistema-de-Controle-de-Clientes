# database.py
import sqlite3
from bcrypt import hashpw, gensalt, checkpw

class BancoDeDados:
    def __init__(self, nome_banco="clientes.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        self._criar_tabelas()

    def _criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_processo TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                pacote TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )
        """)
        self.conexao.commit()

    def adicionar_cliente(self, numero_processo, nome, pacote):
        try:
            self.cursor.execute(
                "INSERT INTO clientes (numero_processo, nome, pacote) VALUES (?, ?, ?)",
                (numero_processo, nome, pacote)
            )
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def buscar_clientes(self, coluna=None, valor=None):
        if coluna not in (None, "numero_processo", "nome", "pacote"):
            raise ValueError("Coluna de busca inválida")
        if coluna and valor:
            self.cursor.execute(
                f"SELECT * FROM clientes WHERE {coluna} LIKE ?",
                (f"%{valor}%",)
            )
        else:
            self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def registrar_usuario(self, username, senha):
        senha_hash = hashpw(senha.encode(), gensalt())
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (username, senha_hash) VALUES (?, ?)",
                (username, senha_hash)
            )
            self.conexao.commit()
        except sqlite3.IntegrityError:
            pass

    def validar_credenciais(self, username, senha):
        self.cursor.execute(
            "SELECT senha_hash FROM usuarios WHERE username = ?",
            (username,)
        )
        resultado = self.cursor.fetchone()
        if resultado:
            return checkpw(senha.encode(), resultado[0])
        return False

    def fechar_conexao(self):
        self.conexao.close()
