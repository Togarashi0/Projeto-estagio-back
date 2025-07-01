import logging
from fastapi import Depends, APIRouter
from app.services.example_service import ExampleService
from app.data.api.api_core_security import CoreSecurity
from app.controllers import get_token, responses, erro_400

# TODO mude o prefix= "" e tags conforme seu projeto.  Remover este comentário depois.
router = APIRouter(prefix="/teste_base_url", tags=["Teste"])


@router.get("/verificar", responses=responses, response_model=dict, status_code=200,
            tags=["Teste"],
            description="Verificar a disponibilidade da API.")
def check_availability(token: str = Depends(get_token)):
    """
        Verifica a disponibilidade da API.

        Este endpoint é utilizado para verificar se a API está disponível para uso.

        Args:
            token (str): Token de autenticação obtido a partir do cabeçalho Authorization.

        Returns:
            dict: Retorna um dicionário indicando que a API está disponível.
    """
    logging.info("Iniciado enpoint verificar disponibilidade")
    return {"disponível": True}


@router.get("/hello", responses=responses, response_model=dict, status_code=200,
            tags=["Teste"],
            description="Hello World.")
def hello_world(token: str = Depends(get_token)):
    """
        Breve descrição

        Descrição mais detalhada

        Args:
            token (str): Token de autenticação obtido a partir do cabeçalho Authorization.

        Returns:
            dict: Retorna um dicionário.
    """
    try:
        logging.info("Iniciado enpoint...")

        instancia_do_service = ExampleService()
        teste_var = instancia_do_service.teste()

        return {"message": teste_var}
    except Exception as e:
        CoreSecurity.rpa_team_send_error_email(bot_name=app.title, error=str(e))
        raise erro_400(f"metódo não executado - ERRO: {e}")
