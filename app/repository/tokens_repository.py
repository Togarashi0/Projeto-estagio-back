import os

import pymongo
from app import host_mongo, APP_TITLE


class TokensRepository:
    """
    Classe responsável por gerenciar operações relacionadas a tokens na base de dados MongoDB.

    Atributos:
        _banco (pymongo.database.Database): Instância do banco de dados MongoDB para a coleção de tokens.
        _colecao (pymongo.collection.Collection): Coleção de tokens no banco de dados.
    """

    def __init__(self):
        """
        Inicializa uma nova instância de TokensRepository.

        Conecta-se ao banco de dados MongoDB e define a coleção de tokens.
        """
        _db = pymongo.MongoClient(host_mongo)
        self._banco = _db[os.getenv('MONGO_DB_NAME')]
        self._colecao = self._banco["tokens_api.tokens"]

    def tem_token(self, token) -> bool:
        """
        Verifica se um token específico está presente no banco de dados e está associado à ferramenta 'APP_TITLE'.

        Args:
            token (str): O token a ser verificado.

        Returns:
            bool: True se o token estiver presente e associado à ferramenta 'APP_TITLE', False caso contrário.
        """
        return self._colecao.find_one(
            {"token": token, "ferramenta": {"$elemMatch": {"$eq": APP_TITLE}}}) is not None

    def get_token(self) -> str:
        """
        Obtém o token associado à ferramenta 'APP_TITLE' no banco de dados.
        """
        return self._colecao.find_one({"ferramenta": {"$elemMatch": {"$eq": APP_TITLE}}})["token"]

    def get_token_ferramenta(self, ferramenta) -> str:
        """
        Obtém o token associado a uma ferramenta específica no banco de dados.
        """
        return self._colecao.find_one({"ferramenta": {"$elemMatch": {"$eq": ferramenta}}})["token"]
