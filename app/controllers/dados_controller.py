import logging
import traceback

from bson import ObjectId
from fastapi import Query, Depends, UploadFile

from app import app
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

from app.controllers import erro_400
from app.data.models.registro_banco import ProcessoFiltroQuery, DadosRequest
from app.services.filtros_service import busca_filtrado
from app.services.manipular_dados import Manipular_dados




@app.post("/cadastrar_dados", status_code=201, tags=["cadastro_dados"], description="API DE CADASTRO DE INFORMAÇÕES.")
def cadastrar_dados(payload: DadosRequest):
    """
    Cria um novo documento em **Dados** ou atualiza o existente,
    usando `numero_de_patrimonio` como chave de unicidade.
    """
    try:
        service = Manipular_dados()
        criado = service.criar_registro(**payload.dict())

        if criado:
            return {
                "mensagem": "Registro criado com sucesso.",
                "criado": True
            }
        # se já existia, o método devolve False
        return {
            "mensagem": "Registro já existia; campos atualizados.",
            "criado": False
        }

    except HTTPException as exc:   # se `criar_registro` já lançar uma HTTPException
        raise exc
    except Exception as exc:
        logging.error("Erro inesperado:\n%s", traceback.format_exc())  # imprime o stack‑trace
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao cadastrar dados."
        ) from exc

@app.get("/buscar/filtro", response_model=dict, status_code=200, tags=["cadastro_dados"], description="Retorna todos elementos do banco filtrados e paginados..")
def busca_calculos_filtrado(filtros: ProcessoFiltroQuery = Depends()):
    try:
        return busca_filtrado(filtros=filtros)
    except Exception as e:
        raise erro_400(f"Método não executado - ERRO: {e}")

@app.delete("/cadastrar_dados/{id}", status_code=200, tags=["cadastro_dados"])
def deletar_dados(id: str):
    """
    Remove um documento de *Dados* a partir do seu _id.
    """
    try:
        service = Manipular_dados()
        excluido = service.deletar_registro(id)

        if excluido:
            return {"mensagem": "Registro excluído com sucesso."}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado."
        )
    except Exception as exc:
        import traceback
        logging.error("Erro inesperado:\n%s", traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar excluir o registro."
        )

