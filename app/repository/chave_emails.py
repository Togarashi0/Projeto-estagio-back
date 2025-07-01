import pymongo

from app import host_mongo


class ChaveEmailsRepository:

    def __init__(self):
        self._db = pymongo.MongoClient(host_mongo)
        self._banco = self._db['CORE_SECURITY']
        self._colecao = self._banco["chave_emails"]

    def buscar_credenciais(self, nome_ferramenta, tipo):
        filtro = {"nome_ferramenta": nome_ferramenta, "tipo": tipo}
        return self._colecao.find_one(filtro).get('emails')
