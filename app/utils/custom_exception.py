class CustomException(Exception):
    """Classe base para exceções relacionadas à manipulação de planilhas."""

    class InvalidColumnsException(Exception):
        """Exceção para quando as colunas esperadas não estão presentes na planilha."""

        def __init__(self, message=None):
            if message is None:
                message = "As colunas são necessárias, mas não foram encontradas."
            super().__init__(message)

    class InvalidFileExtensionException(Exception):
        """Exceção para quando a extensão do arquivo não é suportada."""

        def __init__(self, message=None):
            if message is None:
                message = "Extensão de arquivo não suportada."
            super().__init__(message)

    class EmptyFileException(Exception):
        """Exceção para quando a planilha está vazia."""

        def __init__(self, message=None):
            if message is None:
                message = "A planilha está vazia."
            super().__init__(message)

    class InsertDatabaseException(Exception):
        """Exceção para quando ocorre um erro na inserção de dados no banco."""

        def __init__(self, message=None):
            if message is None:
                message = "Erro ao inserir dado no banco de dados."
            super().__init__(message)

    class FileReadException(Exception):
        """Exceção para quando ocorre um erro na leitura do arquivo."""

        def __init__(self, message=None):
            if message is None:
                message = "Erro ao ler o arquivo Excel."
            super().__init__(message)

    class LoginError(Exception):
        """Exceção para erros gerais de login."""

        def __init__(self, message="Erro durante o login"):
            super().__init__(message)

    class LoginErrorCredencialExpirada(Exception):
        """Exceção para quando as credenciais do usuário estão expiradas."""

        def __init__(self, message="Erro durante o login, credencial expirada."):
            super().__init__(message)

    class MaintenanceError(Exception):
        """Exceção para quando o site está em manutenção."""

        def __init__(self, message="Site em manutenção. Tente novamente mais tarde."):
            super().__init__(message)

    # Outras exceções específicas podem ser adicionadas aqui conforme necessário
