# testar_validacao.py
from database import BancoDeDados

def testar_validacao():
    banco = BancoDeDados("clientes.db")
    resultado = banco.validar_credenciais("admin", "1234")
    print(f"Validação de 'admin'/'1234': {resultado}")
    banco.fechar_conexao()

if __name__ == "__main__":
    testar_validacao()