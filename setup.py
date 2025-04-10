# setup_app.py
from database import BancoDeDados

def registrar_usuario_inicial():
    banco = BancoDeDados()

    # Dados padrão (você pode pedir input se quiser)
    usuario = "Priza_Admin"
    senha = "priza@clientes"  # Altere depois via interface!

    try:
        banco.registrar_usuario(usuario, senha)
        print(f"✅ Usuário '{usuario}' registrado com sucesso!")
        print("⚠️  Lembre-se de alterar a senha padrão após o primeiro login.")
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
    finally:
        banco.fechar_conexao()

if __name__ == "__main__":
    registrar_usuario_inicial()
