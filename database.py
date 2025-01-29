# database.py
import sqlite3


class BancoDeDados:
    def __init__(self, nome_banco="clientes.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        """Cria a tabela de clientes se ela ainda não existir."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_processo TEXT NOT NULL,
            nome TEXT NOT NULL,
            pacote TEXT NOT NULL
        )
        """)
        self.conexao.commit()

    def adicionar_cliente(self, numero_processo, nome, pacote):
        """Adiciona um cliente ao banco de dados."""
        self.cursor.execute("INSERT INTO clientes (numero_processo, nome, pacote) VALUES (?, ?, ?)",
                            (numero_processo, nome, pacote))
        self.conexao.commit()

    def buscar_clientes(self, coluna=None, valor=None):
        """Busca clientes com base em uma coluna e valor."""
        if coluna and valor:
            query = f"SELECT * FROM clientes WHERE {coluna} LIKE ?"
            self.cursor.execute(query, (f"%{valor}%",))
        else:
            self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def executar(self, query, parametros=()):
        """Executa uma consulta SQL no banco de dados."""
        try:
            self.cursor.execute(query, parametros)
            self.conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro ao executar comando SQL: {e}")

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self.conexao.close()
