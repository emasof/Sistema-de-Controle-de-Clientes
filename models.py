# models.py
class Cliente:
    def __init__(self, numero_processo: str, nome: str, pacote: str):
        """
        Representa um cliente no sistema.

        :param numero_processo: Número do processo do cliente.
        :param nome: Nome do cliente.
        :param pacote: Pacote do cliente (Priza Consumo, Priza Negócio, Priza Solidário).
        """
        self.numero_processo = numero_processo
        self.nome = nome
        self.pacote = pacote

    @property
    def __repr__(self):
        return f"Cliente(Nº Processo={self.numero_processo}, Nome={self.nome}, Pacote={self.pacote})"
