# verificar_usuarios.py
import sqlite3

def verificar_usuarios():
    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT username, senha_hash FROM usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        for usuario in usuarios:
            print(f"Usuário: {usuario[0]}, Senha Hash: {usuario[1]}")
    else:
        print("Nenhum usuário encontrado na tabela 'usuarios'.")
    conexao.close()

if __name__ == "__main__":
    verificar_usuarios()