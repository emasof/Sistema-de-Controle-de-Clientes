# models.py
from dataclasses import dataclass

@dataclass
class Cliente:
   numero_processo: str
   nome: str
   pacote: str
