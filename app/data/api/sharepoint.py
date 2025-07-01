import base64
import requests
import os


class Sharepoint:
    """
    Classe responsável por interagir com o serviço SharePoint.

    Atributos:
        token (str): Token de autenticação para o SharePoint.
        base_url (str): URL base da API do SharePoint.
        timeout (tuple): Timeout para conexão e leitura (conexão, leitura).
    """

    def __init__(self, token=None) -> None:
        """
        Inicializa uma nova instância de Sharepoint.

        Args:
            token (str, opcional): Token de autenticação para o SharePoint. Se não fornecido, será obtido das variáveis de ambiente.
        """
        self.token = token or os.getenv('BEARER_TOKEN_API_INTERNA')  # pega o token direto no env evitando requisicao ao cofre
        self.base_url = os.getenv('SHAREPOINT_API_URL')
        self.timeout = (60, 300)  # Timeout de 5 minutos para conexão e leitura

    def _make_request(self, method, endpoint, params=None, json=None):
        """
        Método privado para fazer solicitações genéricas.

        Args:
            method (function): Método HTTP (requests.get, requests.post, etc.).
            endpoint (str): Endpoint da API.
            params (dict, opcional): Parâmetros da URL.
            json (dict, opcional): Dados JSON para o corpo da solicitação.

        Returns:
            requests.Response: Objeto de resposta da solicitação.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = method(url, headers=headers,
                              json=json, params=params, timeout=self.timeout)
            response.raise_for_status()  # Lança uma exceção para erros HTTP
            return response
        except requests.RequestException as e:
            print(f"Erro ao fazer a solicitação para {url}: {e}")
            return None

    def upload_base64(self, site_group, folder, arquivo_64, file_name) -> bool:
        """
        Envia um arquivo em formato base64 para uma pasta específica.

        Args:
            site_group (str): Nome do site SharePoint.
            folder (str): Nome da pasta no SharePoint.
            arquivo_64 (str): Conteúdo do arquivo em formato base64.
            file_name (str): Nome do arquivo a ser salvo.

        Returns:
            bool: True se o upload for bem-sucedido, False caso contrário.
        """
        endpoint = 'send_file_base64'
        payload = {"site_group": site_group, "sharepoint_folder": folder, "arquivo_base64": arquivo_64,
                   "file_name": file_name}
        response = self._make_request(requests.post, endpoint, json=payload)
        if response:
            print("Arquivo enviado com sucesso!")
            return True
        else:
            print("Erro ao enviar o arquivo.")
            return False

    def move_file_sharepoint(self, site_group, path_origin, path_destiny, file_name):
        """
        Move um arquivo de uma pasta para outra no SharePoint.

        Args:
            site_group (str): Nome do site SharePoint.
            path_origin (str): Caminho da pasta de origem.
            path_destiny (str): Caminho da pasta de destino.
            file_name (str): Nome do arquivo a ser movido.

        Returns:
            bool: True se a movimentação for bem-sucedida, False caso contrário.
        """
        endpoint = 'move_file'
        json_arquivo = {"site_group": site_group, "path_origin": path_origin, "path_destiny": path_destiny,
                        "file_name": file_name}
        response = self._make_request(method=requests.post, endpoint=endpoint, json=json_arquivo)
        if response:
            print(
                f"Arquivo Movido com Sucesso!\nArquivo: {file_name}\nPasta Origem: {path_origin}\nPasta Destino: {path_destiny}")
            return True
        else:
            print(
                f"*ERRO* ao Mover o Arquivo!\nArquivo: {file_name}\nPasta Origem: {path_origin}\nPasta Destino: {path_destiny}")
            return False

    def search_files_in_folder(self, site: str, folder: str) -> list:
        """
        Pesquisa arquivos em uma pasta específica.

        Args:
            site (str): Nome do site SharePoint.
            folder (str): Nome da pasta no SharePoint.

        Returns:
            list: Lista de nomes de arquivos encontrados na pasta.
        """
        endpoint = 'search_in_folder'
        params = {"site_group": site, "sharepoint_folder": folder}
        response = self._make_request(requests.get, endpoint, params=params)
        if response:
            try:
                files = response.json()[0]['data']['files']
                return [file['name'] for file in files]
            except (KeyError, IndexError) as e:
                print("Erro ao analisar a resposta JSON:", e)
                return []
        else:
            return []

    def search_folder_in_folder(self, site: str, folder: str) -> list:
        """
        Pesquisa subpastas dentro de uma pasta específica no SharePoint.

        Args:
            site (str): Nome do site SharePoint.
            folder (str): Nome da pasta no SharePoint.

        Returns:
            list: Lista de nomes das subpastas encontradas.
        """
        endpoint = 'search_in_folder'
        params = {"site_group": site, "sharepoint_folder": folder}
        response = self._make_request(requests.get, endpoint, params=params)

        if response:
            try:
                dados = response.json()
                return [arquivo['name'] for arquivo in dados[0]['data']['folders']]
            except (KeyError, IndexError) as e:
                print("Erro ao analisar a resposta JSON:", e)
                return []
        else:
            return []

    def download_file_from_folder_64(self, site, folder, file_name):
        """
        Faz download de um arquivo em formato base64 de uma pasta específica.

        Args:
            site (str): Nome do site SharePoint.
            folder (str): Nome da pasta no SharePoint.
            file_name (str): Nome do arquivo a ser baixado.

        Returns:
            str: Conteúdo do arquivo em formato base64, ou None em caso de erro.
        """
        endpoint = 'download_file_from_folder_64'
        params = {"site_group": site,
                  "sharepoint_folder": folder, "file_name": file_name}
        response = self._make_request(requests.get, endpoint, params=params)
        if response:
            try:
                return response.json()[0]['file_64']
            except (KeyError, IndexError) as e:
                print("Erro ao analisar a resposta JSON:", e)
                return None
        else:
            return None

    def get_link(self, path, site_group):
        """
        Obtém o link de acesso para um arquivo no SharePoint.

        Args:
            path (str): Caminho do arquivo.
            site_group (str): Grupo do site no SharePoint.

        Returns:
            str: Link de acesso ao arquivo, ou None em caso de erro.
        """
        endpoint = 'get_link'
        params = {"path": path, "site_group": site_group}
        response = self._make_request(method=requests.get, endpoint=endpoint, params=params)
        if response:
            try:
                return response.json()[0].get("Link de acesso", None)
            except (KeyError, IndexError) as e:
                print("Erro ao obter o link:", e)
                return None
        return None

    def create_folder(self, site: str, folder: str, folder_name: str) -> list:
        """
        Cria uma nova pasta em um diretório específico do SharePoint.

        Args:
            site (str): Nome do site SharePoint.
            folder (str): Caminho da pasta onde a nova pasta será criada.
            folder_name (str): Nome da nova pasta a ser criada.

        Returns:
            list: Resposta JSON da API ou lista vazia em caso de erro.
        """
        endpoint = 'create_folder'
        payload = {"site_group": site, "sharepoint_folder": folder, "folder_name": folder_name}
        response = self._make_request(method=requests.post, endpoint=endpoint, json=payload)
        if response:
            try:
                return response.json()
            except Exception as e:
                print("Erro ao analisar a resposta JSON:", e)
                return []
        return []

    @staticmethod
    def base64_to_file(base64_string, file_name):
        """
        Converte uma string base64 em um arquivo.

        Args:
            base64_string (str): String base64 do arquivo.
            file_name (str): Nome do arquivo a ser salvo.

        Returns:
            str: Caminho do arquivo salvo, ou None em caso de erro.
        """
        try:
            # Diretório para salvar o arquivo
            directory = os.path.join(os.getcwd(), "resources")
            os.makedirs(directory, exist_ok=True)

            # Caminho completo para o arquivo temporário
            file_path = os.path.join(directory, file_name)

            # Decodifica a string base64 e salva o arquivo
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(base64_string))

            return file_path
        except Exception as e:
            print("Ocorreu um erro ao gerar o arquivo:", e)
            return None
