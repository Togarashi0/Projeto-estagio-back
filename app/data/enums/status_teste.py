from enum import Enum


class StatusTeste(Enum):
    """
        Enumeração que representa os tipos de status de um process.
    """
    PENDENTE = (0, "PENDENTE")
    SUCESSO = (1, "SUCESSO")
    ERRO = (2, "ERRO")
    CAMPO_AUSENTE = (3, "CAMPO AUSENTE")

    def __init__(self, id_status, status_name):
        self.id_status = id_status
        self.status_name = status_name

    @classmethod
    def from_id(cls, id_status):
        for status in cls:
            if status.id_status == id_status:
                return status
        raise ValueError(f"Status com id {id_status} não encontrado.")
