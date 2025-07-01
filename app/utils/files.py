import base64
import os

from app.utils.constants import Constants


class Files:
    """
        Classe utilitária para trasformação de arquivos.
    """

    @staticmethod
    def create_folder_structure():
        """
            Cria a estrutura de pastas necessárias.

            Esta função cria as pastas especificadas na lista retornada pelo método `lista_pasta` da classe `Constantes`. Se a pasta não existir, ela será criada.
        """
        for constante in Constants().folder_list():
            if not os.path.exists(constante):
                os.makedirs(constante)

    @staticmethod
    def file_to_base64(path_file: str) -> str:
        """
            Converte o conteúdo de um arquivo para uma string em base64.

            Args:
                path_file (str): O caminho do arquivo a ser convertido.

            Returns:
                str: O conteúdo do arquivo em formato base64.
        """
        with open(path_file, "rb") as file:
            content = file.read()
            base64_bytes = base64.b64encode(content)
            base64_string = base64_bytes.decode("utf-8")
            return base64_string

    @staticmethod
    def bytes_to_base64(content_bytes: bytes) -> str:
        """
            Converte um conteúdo em bytes para uma string em base64.

            Args:
                content_bytes (bytes): O conteúdo em bytes a ser convertido.

            Returns:
                str: O conteúdo em formato base64.
        """
        base64_bytes = base64.b64encode(content_bytes)
        base64_string = base64_bytes.decode("utf-8")
        return base64_string

    @staticmethod
    def base64_to_bytes(content_base64: str) -> bytes:
        """
        Converte uma string em base64 para seu conteúdo em bytes.

        Args:
            content_base64 (str): O conteúdo em base64 a ser convertido.

        Returns:
            bytes: O conteúdo decodificado em bytes.
        """
        # Decodifica a string base64 para bytes
        content_bytes = base64.b64decode(content_base64)
        return content_bytes
