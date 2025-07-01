import datetime
from typing import List
import requests
from app.repository.tokens_repository import TokensRepository
from app.utils.data_utils import DataUtils
import os


class CoreSecurity:
    """
    Classe responsável por gerenciar operações de segurança centralizadas.

    Atributos:
        url_email (str): URL da API interna para envio de e-mails.
        token (str): Token de autorização obtido do repositório de tokens.
    """

    def __init__(self):
        """
        Inicializa uma nova instância de CoreSecurity.

        Obtém a URL da API interna para envio de e-mails e o token de autorização necessário.
        """
        self.url_email = f"{os.getenv('URL_API_CORE_SECURITY')}/send_email"
        self.token = TokensRepository().get_token()
        self.url_auth_token = f"{os.getenv('URL_API_CORE_SECURITY')}/chamar_token_google"

    def call_send_email(self, recipients: List, subject, email_body, files: List = None):
        """
        Chama a API interna para enviar um e-mail.

        Args:
            recipients (List[str]): Lista de e-mails dos destinatários.
            subject (str): Assunto do e-mail.
            email_body (str): Corpo do e-mail.
            files (List[str], optional): Lista de caminhos dos arquivos anexados ao e-mail. Default é None.

        Returns:
            str: Resposta da API após o envio do e-mail.

        Raises:
            requests.HTTPError: Se ocorrer um erro ao enviar a solicitação para a API.
        """
        try:
            data = {
                "receiver_email": recipients,
                "subject": subject,
                "body": email_body,
                "arquivos": files
            }
            headers = {'Authorization': 'Bearer ' + self.token}
            response = requests.post(self.url_email, json=data, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f'ERRO AO ENVIAR EMAIL!: {e}')

    def rpa_team_send_error_email(self, bot_name, error, files: List = None):
        """
        Chama a API interna para enviar um e-mail.

        Args:
            bot_name (str): Nome da ferramenta que aparece no assunto do e-mail.
            error (str): Erro que sera concatenado no corpo do e-mail.
            files (List[str], optional): Lista de caminhos dos arquivos anexados ao e-mail. Default é None.

        Returns:
            str: Resposta da API após o envio do e-mail.

        Raises:
            requests.HTTPError: Se ocorrer um erro ao enviar a solicitação para a API.
        """
        try:
            recipients = ["equiperpa@ernestoborges.com.br"]

            email_body = f"""
                               <p>Erro: {error}</p>
                               <br><p>Data: {DataUtils.format_full_date(datetime.datetime.now())}</p>
                               """

            subject = f"ATENÇÃO ERRO AO EXECUTAR O BOT: {bot_name}!"

            data = {
                "receiver_email": recipients,
                "subject": subject,
                "body": email_body,
                "arquivos": files
            }

            headers = {'Authorization': 'Bearer ' + self.token}
            response = requests.post(self.url_email, json=data, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f'ERRO AO ENVIAR EMAIL!: {e}')

    def call_token_google(self, secret_key):
        data = {
            "secret_key": secret_key
        }

        headers = {'Authorization': 'Bearer ' + self.token}

        response = requests.get(
            self.url_auth_token + f'/{secret_key}', json=data, headers=headers)

        response.raise_for_status()

        data = response.json()
        codigo = data.get('codigo')

        return codigo
