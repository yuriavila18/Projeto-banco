from dataclasses import dataclass

@dataclass
class Usuario:
    username: str
    password: str
    nome: str
    cpf: str
    telefone: str