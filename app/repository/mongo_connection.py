from datetime import datetime
from typing import List, Dict, Any
import pymongo
from app import host_mongo


class MongoConnection:
    """
    Classe responsável pela conexão e operações com o banco de dados MongoDB.

    Esta classe oferece métodos para inserir dados, gerar relatórios, pesquisar processos e atualizar parâmetros
    em uma coleção específica de um banco de dados MongoDB.
    """

    def __init__(self, db_name, collection_name):
        """
        Inicializa a conexão com o banco de dados MongoDB e configura a coleção.

        Args:
            db_name (str): Nome do banco de dados.
            collection_name (str): Nome da coleção.
        """
        self.client = pymongo.MongoClient(host_mongo)
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = self.client[db_name]

        # Verifica se o banco de dados existe, senão cria
        if db_name not in self.client.list_database_names():
            self.client[db_name]
            print(f"O banco de dados '{db_name}' foi criado.")

        # Verifica se a coleção existe, senão cria
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            print(f"A coleção '{collection_name}' foi criada.")

        self.collection = self.db[collection_name]

    def insert_data(self, data):
        """
            Insere um registro no banco de dados.

            Tem como função fazer o cadastro de um registro no banco de dados.

            Args:
               data (any): linha a ser cadastrada no banco de dados.

            Returns:
                None

            Raises:
                Exception: Se ocorrer um erro ao inserir o dado, uma exceção é levantada com a descrição do erro.
        """
        try:
            self.collection.insert_one(data)
            print("Dado inserido com sucesso!")

        except Exception as e:
            print(f"Erro ao inserir o dado: {data} - ERRO: {e} ")

    def generate_report(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Gera um relatório dos dados cadastrados no banco de dados dentro de um intervalo de datas.

        Args:
            start_date (str): Data inicial no formato 'YYYY-MM-DD'.
            end_date (str): Data final no formato 'YYYY-MM-DD'.

        Returns:
            List[Dict[str, Any]]: Lista de dicionários contendo os dados encontrados no intervalo de datas.
        """
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        results = self.collection.find({
            'data_cadastro_mongo': {'$gte': start_date_obj, '$lte': end_date_obj}
        })
        return list(results)

    def search_by_process_id(self, query=None, count=False):
        """
        Pesquisa no banco de dados com uma query opcional e conta os documentos encontrados se solicitado.

        Args:
            query (Dict[str, Any], opcional): Query de consulta para o banco de dados. Se None, busca todos os documentos.
            count (bool, opcional): Se True, conta o número de documentos encontrados.

        Returns:
            Tuple[int, List[Dict[str, Any]]]: Quantidade de documentos afetados e lista de dados encontrados.
        """
        if query is None:
            found_documents = self.collection.find()
            if count:
                document_count = self.collection.count_documents({})
            return document_count, found_documents
        else:
            found_documents = self.collection.find(query)
            if count:
                document_count = self.collection.count_documents(query)

            return document_count, found_documents

    def search_process(self, query):
        """
        Pesquisa um único documento no banco de dados.

        Args:
            query (Dict[str, Any]): Query de consulta para o banco de dados.

        Returns:
            Dict[str, Any]: Dicionário contendo o resultado da pesquisa. Retorna None se não encontrar nenhum resultado.

        Raises:
            Exception: Se ocorrer um erro ao consultar o banco de dados, uma exceção é levantada com a descrição do erro.
        """
        try:
            result = self.collection.find_one(query)
            if result:
                print(f"Consulta bem-sucedida para a query: {query}")
            else:
                print(f"Nenhum resultado encontrado para a query: {query}")
            return result

        except Exception as e:
            print(f"Erro ao consultar o banco de dados: {e}")
            return None

    def update_parameters(self, query, new_parameter):
        """
        Atualiza parâmetros de documentos no banco de dados.

        Args:
            query (Dict[str, Any]): Query para selecionar os documentos a serem atualizados.
            new_parameter (Dict[str, Any]): Dicionário contendo os novos valores dos parâmetros.

        Returns:
            str: Mensagem indicando o sucesso da operação.
        """
        self.collection.update_many(query, {"$set": new_parameter})
        return "Parâmetros atualizados com sucesso!"
