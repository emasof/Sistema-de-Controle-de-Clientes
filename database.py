# database.py
import sqlite3
from bcrypt import hashpw, gensalt, checkpw

class BancoDeDados:
    def __init__(self, nome_banco="clientes.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        self._criar_tabela()
        self._criar_tabela_usuarios()

    def _criar_tabela(self):
        """Cria a tabela de clientes com numero_processo único."""
        # Verifica se a tabela clientes_temp já existe e a remove
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes_temp'")
        if self.cursor.fetchone():
            self.cursor.execute("DROP TABLE clientes_temp")

        # Verifica se a tabela clientes existe e precisa de migração
        self.cursor.execute("PRAGMA table_info(clientes)")
        colunas = self.cursor.fetchall()
        if colunas:  # Se a tabela clientes já existe
            # Verifica se numero_processo já tem UNIQUE
            has_unique = any(col[3] == 1 for col in colunas if col[1] == 'numero_processo')
            if not has_unique:  # Se não tem UNIQUE, faz a migração
                self.cursor.execute("ALTER TABLE clientes RENAME TO clientes_temp")
                self.cursor.execute("""
                CREATE TABLE clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_processo TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    pacote TEXT NOT NULL
                )
                """)
                self.cursor.execute("""
                INSERT INTO clientes (id, numero_processo, nome, pacote)
                SELECT id, numero_processo, nome, pacote FROM clientes_temp
                """)
                self.cursor.execute("DROP TABLE clientes_temp")
        else:
            # Se a tabela não existe, cria diretamente com UNIQUE
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_processo TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                pacote TEXT NOT NULL
            )
            """)
        self.conexao.commit()

    def adicionar_cliente(self, numero_processo, nome, pacote):
        """Adiciona um cliente ao banco de dados."""
        try:
            self.cursor.execute("INSERT INTO clientes (numero_processo, nome, pacote) VALUES (?, ?, ?)",
                                (numero_processo, nome, pacote))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Retorna False se houver duplicata

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

    def _criar_tabela_usuarios(self):
        """Cria a tabela de usuários se ela ainda não existir."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
        """)
        self.conexao.commit()

    def registrar_usuario(self, username, senha):
        """Registra um novo usuário no banco de dados."""
        senha_hash = hashpw(senha.encode('utf-8'), gensalt())
        query = "INSERT INTO usuarios (username, senha_hash) VALUES (?, ?)"
        params = (username, senha_hash)
        self.executar(query, params)

    def validar_credenciais(self, username, senha):
        """Valida as credenciais do usuário."""
        query = "SELECT senha_hash FROM usuarios WHERE username = ?"
        self.cursor.execute(query, (username,))
        resultado = self.cursor.fetchone()

        if resultado:
            senha_hash_armazenada = resultado[0]
            return checkpw(senha.encode('utf-8'), senha_hash_armazenada)
        return False

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self.conexao.close()