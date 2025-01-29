# cliente.py
class Cliente:
    def __init__(self, numero_processo, nome, pacote):
        self.numero_processo = numero_processo
        self.nome = nome
        self.pacote = pacote

    def __str__(self):
        return f"Nº do Processo: {self.numero_processo}, Nome: {self.nome}, Pacote: {self.pacote}"

    # Adicione métodos para salvar clientes ou realizar outras operações
