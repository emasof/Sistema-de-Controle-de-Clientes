# controller.py
import sqlite3

class Controller:
    def __init__(self, database_path):
        """Inicializa o controlador com o caminho do banco de dados."""
        self.database_path = database_path
        self.conexao = None

    def connect_to_database(self):
        """Estabelece conexão com o banco de dados, se não estiver conectada."""
        if not self.conexao:
            try:
                self.conexao = sqlite3.connect(self.database_path)
                print("Database connection established successfully.")
            except sqlite3.Error as e:
                print(f"Error connecting to database: {e}")
                self.conexao = None

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao:
            self.conexao.close()
            self.conexao = None
            print("Database connection closed.")

    def executar_query(self, query, params=None):
        """
        Executa uma query no banco de dados e retorna os resultados.
        Fecha automaticamente o cursor após a execução.
        """
        if self.conexao is None:
            raise ConnectionError("No database connection established.")
        try:
            cursor = self.conexao.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conexao.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def pesquisar_cliente(self, filtro, campos='*'):
        """
        Pesquisa clientes com base em um filtro e nos campos especificados.
        Retorna todos os registros se o filtro for 'todos'.
        """
        if filtro == 'todos':
            query = f"SELECT {campos} FROM clientes"
            params = None
        else:
            query = f"SELECT {campos} FROM clientes WHERE nome LIKE ?"
            params = (f"%{filtro}%",)
        return self.executar_query(query, params)
