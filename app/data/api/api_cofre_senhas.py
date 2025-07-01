import requests
import logging
import os
from typing import List, Optional


class ApiCofreSenhas:
    """
    Classe responsável por gerenciar operações com o cofre de senhas.

    Essa classe abstrai a comunicação com a API interna de cofre de senhas.

    Atributos:
        token (str): Token de autenticação para o cofre de senhas.
        base_url (str): URL base da API do cofre de senhas.
        timeout (tuple): Timeout para conexão e leitura (conexão, leitura).
    """

    USERNAME_ADMIN_COFRE = "eba_admin"

    def __init__(self, token: Optional[str] = None) -> None:
        """
        Inicializa uma nova instância de ApiCofreSenhas.

        Args:
            token (str, opcional): Token de autenticação para a API de cofre de senhas. Se não fornecido, será obtido das variáveis de ambiente.
        """
        self.token = token or os.getenv('BEARER_TOKEN_API_INTERNA')
        self.base_url = os.getenv('URL_API_CORE_SECURITY') + '/cofre_senha'
        self.timeout = (60, 150)  # Timeout de 5 minutos para conexão e leitura

    def _make_request(self, method, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None):
        """
        Método privado para fazer solicitações genéricas à API.

        Args:
            method (function): Método HTTP (requests.get, requests.post, etc.).
            endpoint (str): Endpoint da API.
            params (dict, opcional): Parâmetros da URL.
            json (dict, opcional): Dados JSON para o corpo da solicitação.

        Returns:
            dict: Resposta JSON da API ou None em caso de erro.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = method(url, headers=headers, json=json, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Erro ao fazer a solicitação para {url}: {e}")
            return None

    def buscar_credenciais(self, projeto: Optional[str] = None, credencial_id: Optional[str] = None, nucleo: Optional[str] = None, nome_portal: Optional[str] = None) -> Optional[List[dict]]:
        """
        Busca todas as credenciais filtradas para integração com bots internos.

        Args:
            projeto (Optional[str]): Nome ou ID do projeto ao qual a credencial pertence.
            credencial_id (Optional[str]): ID da credencial.
            nucleo (Optional[str]): Núcleo da credencial.
            nome_portal (Optional[str]): Nome do portal que a credencial é usada.

        Returns:
            list: Lista de credenciais filtradas ou None em caso de erro.
        """
        filtros = {
            "projeto": projeto,
            "credencial_id": credencial_id,
            "nucleo": nucleo,
            "nome_portal": nome_portal
        }
        endpoint = 'credencial/buscar/filtro_integracao_interna'
        response = self._make_request(requests.get, endpoint, params=filtros)
        return response if response else None

    def obter_login_senha(self, credencial: dict) -> tuple[str, str]:
        """
        Obtém o login e a senha de uma credencial.

        Args:
            credencial (dict): Dicionário contendo os dados da credencial.

        Returns:
            tuple[str, str]: Tupla contendo o login e a senha.
        """
        return credencial.get("login"), credencial.get("senha")

    def obter_login_senha_filtrando_por_login(
            self,
            login: str,
            projeto: Optional[str] = None,
            credencial_id: Optional[str] = None,
            nucleo: Optional[str] = None,
            nome_portal: Optional[str] = None
    ) -> Optional[tuple[str, str, str]]:
        """
        Obtém o login e a senha de uma credencial específica filtrando pelo login.

        Args:
            login (str): Login da credencial desejada. (Obrigatório).
            projeto (Optional[str]): Nome ou ID do projeto ao qual a credencial pertence (opcional).
            credencial_id (Optional[str]): ID da credencial (opcional).
            nucleo (Optional[str]): Núcleo da credencial (opcional).
            nome_portal (Optional[str]): Nome do portal onde a credencial é usada (opcional).

        Returns:
            Optional[tuple[str, str, str]]: Tupla contendo (login, senha, id) se encontrada, ou None se não houver correspondência.

        Raises:
            RuntimeError: Se não for possível encontrar a credencial com o login fornecido.
        """
        filtros = {
            "projeto": projeto,
            "credencial_id": credencial_id,
            "nucleo": nucleo,
            "nome_portal": nome_portal
        }
        endpoint = 'credencial/buscar/filtro_integracao_interna'
        response = self._make_request(requests.get, endpoint, params=filtros)

        if response is None:
            logging.error(f"Erro: Não foi possível recuperar credenciais para o projeto  '{projeto}'")
            return None

        for credencial in response:
            if credencial.get("login") == login:
                return credencial.get("login"), credencial.get("senha"), credencial.get("id")

        logging.error(f"Credencial com login '{login}' não encontrada para o projeto '{projeto}'.")
        return None

    def baixar_arquivo(self, arquivo_id: str, username_usuario: str = USERNAME_ADMIN_COFRE) -> Optional[bytes]:
        """
        Realiza o download de um arquivo armazenado no cofre de senhas.

        Args:
            arquivo_id (str): ID do arquivo a ser baixado.
            username_usuario (str): Nome do usuário requisitante.

        Returns:
            bytes: Conteúdo do arquivo em bytes ou None em caso de erro.
        """
        endpoint = f"arquivo/{arquivo_id}"
        params = {"username_usuario": username_usuario}
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=headers, params=params, timeout=self.timeout, stream=True)
            response.raise_for_status()

            # Retorna o conteúdo do arquivo diretamente em bytes
            return response.content
        except requests.RequestException as e:
            logging.error(f"Erro ao baixar o arquivo {arquivo_id}: {e}")
            return None

    def enviar_email_credencial_expirada(self, credencial_ids: List[str], nome_automacao: str) -> dict:
        """
        Faz envio do e-mail para os responsáveis pelas credenciais com as informações e manual em anexo.

        Args:
            credencial_ids (List[str]): Lista contendo os IDs das credenciais expiradas.
            nome_automacao (str): Nome da automação que está solicitando o envio do e-mail.

        Returns:
            dict: Resposta da API após o envio do e-mail.

        Raises:
            requests.HTTPError: Se ocorrer um erro ao enviar a solicitação para a API.
        """
        # Criando o body compatível com EmailCredencialExpiradaDTO
        body = {
            "credencial_ids": credencial_ids,
            "nome_automacao": nome_automacao
        }

        endpoint = 'email/credencial_expirada'
        response = self._make_request(requests.post, endpoint, json=body)  # Envio do JSON compatível com DTO
        return response if response else None

    @staticmethod
    def buscar_por_campo_personalizado(descricao_busca, nome_portal="SERVICENOW"):
        list_json = ApiCofreSenhas().buscar_credenciais(nome_portal=nome_portal)
        for item in list_json:
            for campo in item.get("campos", []):
                if campo.get("descricao") == "nome_responsavel" and campo.get("valor_conteudo") == descricao_busca:
                    return item['login'], item['senha']
        raise RuntimeError("Não foi possível encontrar login desejado.")

    @staticmethod
    def buscar_personalizado_por_campo(descricao_campo: str, valor_campo: str, nome_portal: str, projeto: Optional[str] = None):
        list_inicial = ApiCofreSenhas().buscar_credenciais(nome_portal=nome_portal, projeto=projeto)
        if list_inicial is None:
            raise RuntimeError("Não foi possível recuperar credenciais.")
        list_return = []
        for item in list_inicial:
            for campo in item.get("campos", []):
                if campo.get("descricao") == descricao_campo and campo.get("valor_conteudo") == valor_campo:
                    list_return.append(item)
        if len(list_return) > 0:
            return list_return

        raise RuntimeError("Não foi possível encontrar login desejado.")

    @staticmethod
    def buscar_campo(descricao_campo: str, credencial: dict):
        for campo in credencial.get("campos"):
            if campo.get("descricao") == descricao_campo:
                return campo.get("valor_conteudo")

        raise RuntimeError("Não foi possível encontrar campo desejado.")
