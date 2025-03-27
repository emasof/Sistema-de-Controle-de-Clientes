# setup.py
import sqlite3

from database import BancoDeDados

def registrar_usuario_inicial():
    banco = BancoDeDados("clientes.db")
    try:
        banco.registrar_usuario("admin", "1234")
        print("Usuário 'admin' com senha '1234' registrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Usuário 'admin' já existe no banco de dados.")
    finally:
        banco.fechar_conexao()

if __name__ == "__main__":
    registrar_usuario_inicial()