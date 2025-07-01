from typing import Optional
from pydantic import BaseModel, Field

class ProcessoFiltroQuery(BaseModel):
    """
        DTO filtro de consulta para andamentos.

        Atributos:
            pageble (bool): Define se retorna paginável.
            skip (int): Página de resultados.
            page_size (int): Tamanho da página.
            sort (str): Ordenação da página.
            ini_data_cadastro (str): Data Inicial (AAAA-MM-DD).
            fim_data_cadastro (str): Data Final (AAAA-MM-DD).
            id_processo (str): ID do Processo.
            andamento_np (str): Número do Processo.
            status_proc (str): Status do Processo.
            tipo_servico (TipoServico): Tipo de Serviço do Processo.
            tipo_cliente (Client): Tipo de Sistema do Processo.
        """
    pageble: bool = Field(default=True, description="Define se retorna paginável")
    skip: int = Field(default=0, description="Página de resultados")
    page_size: int = Field(default=10, description="Tamanho da página")
    sort: str = Field(default='-data_cadastrado', description="Ordenação da página")
    ini_data_cadastro: Optional[str] = Field(default=None, description="Data Inicial (AAAA-MM-DD)")
    fim_data_cadastro: Optional[str] = Field(default=None, description="Data Final (AAAA-MM-DD)")
    equipamento: Optional[str] = Field(default=None, description="equipamento")
    numero_de_patrimonio: Optional[str] = Field(default=None, description="Número do Patrimonio")
    setor: Optional[str] = Field(default=None, description="Setor")
    unidade: Optional[str] = Field(default=None, description="Unidade")
    cidade: Optional[str] = Field(default=None, description="Cidade")
    responsavel: Optional[str] = Field(default=None, description="Responsavel")

class DadosRequest(BaseModel):
    numero_de_patrimonio: str = Field(..., min_length=1)
    equipamento:    Optional[str] = None
    setor:          Optional[str] = None
    unidade:        Optional[str] = None
    cidade:         Optional[str] = None
    responsavel:    Optional[str] = None