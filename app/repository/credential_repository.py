import pymongo
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class CredenciaisRepository:
    """
    Repositório para gerenciar credenciais criptografadas armazenadas em um banco de dados MongoDB.
    """

    def __init__(self):
        """
        Inicializa a conexão com o banco de dados MongoDB utilizando variáveis de ambiente.
        """
        self._db = pymongo.MongoClient(os.getenv("MONGO_DB_URL"))
        self._banco = self._db['usuarios']
        self._colecao = self._banco["credenciais"]

    def buscar_credenciais(self, plataforma, responsavel):
        """
        Busca credenciais no banco de dados para a plataforma e responsável fornecidos.

        Args:
            plataforma (str): Nome da plataforma.
            responsavel (str): Nome do responsável.

        Returns:
            tuple: Observação, login descriptografado e senha descriptografada.
        """
        credenciais = self._colecao.find_one({"plataforma": plataforma, "responsavel": responsavel})
        login_decript = _descriptografar(credenciais["login"], credenciais["private_key"], credenciais["salt_key"])
        senha_decript = _descriptografar(credenciais["senha"], credenciais["private_key"], credenciais["salt_key"])
        observacao = credenciais["observacao"]
        return observacao, login_decript, senha_decript

    @property
    def colecao(self):
        """
        Retorna a coleção do MongoDB.

        Returns:
            pymongo.collection.Collection: Coleção MongoDB.
        """
        return self._colecao

    @property
    def banco(self):
        """
        Retorna o banco de dados do MongoDB.

        Returns:
            pymongo.database.Database: Banco de dados MongoDB.
        """
        return self._banco


def __senha_derivar(senha):
    """
    Deriva uma chave a partir de uma senha utilizando PBKDF2 e um salt armazenado no banco de dados.

    Args:
        senha (bytes): Senha em bytes.

    Returns:
        bytes: Chave derivada.
    """
    cr = CredenciaisRepository()
    cr._colecao = cr.banco["cryptography"]
    salt = cr.colecao.find_one()["salt"].encode('utf-8')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=salt, iterations=100000, backend=default_backend())
    return kdf.derive(senha)


def _descriptografar(ciphertext, private_key, salt_key):
    """
    Descriptografa um texto cifrado usando uma chave privada e um salt.

    Args:
        ciphertext (str): Texto cifrado em base64.
        private_key (str): Chave privada em formato PEM.
        salt_key (str): Salt usado para derivar a senha.

    Returns:
        str: Texto descriptografado.
    """
    private_key = serialization.load_pem_private_key(private_key.encode('utf-8'), password=__senha_derivar(salt_key))
    texto_bytes = private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()),
                                                               algorithm=hashes.SHA512(), label=None))
    texto = texto_bytes.decode('utf-8')
    return texto
