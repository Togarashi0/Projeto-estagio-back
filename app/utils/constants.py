import tempfile


class Constants:
    """
        Classe que define constantes utilizadas na aplicação.

        Attributes:
            TEMP_DIR (str): Diretório temporário do sistema.
            ROOT_FOLDER (str): Diretório raiz dos recursos.
            LOG (str): Diretório dos logs.
    """

    TEMP_DIR = tempfile.gettempdir()
    ROOT_FOLDER = 'resources/'
    SCREENSHOT = f'{ROOT_FOLDER}screenshot/'
    LOG = f'{ROOT_FOLDER}logs/'

    def folder_list(self) -> tuple:
        """
            Retorna uma tupla contendo os diretórios a serem criados.

            Returns:
                tuple: Uma tupla com os diretórios necessários.
        """
        return (self.LOG,)
