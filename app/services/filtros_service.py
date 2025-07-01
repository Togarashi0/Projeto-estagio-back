import os
from datetime import datetime
from fastapi import UploadFile, HTTPException

from bson import ObjectId
from mongoengine import Q, disconnect, connect
import logging

from app.controllers import erro_400
from app.data.models.dados import Dados
from app.data.models.registro_banco import ProcessoFiltroQuery
from app.repository.mongo_engine_query import MongoEngineQuery


def busca_filtrado(filtros: ProcessoFiltroQuery):
    """
        Filtra os contatos no banco de dados.

        Args:
            filtros (ProcessFilterQuery): Objeto com os parâmetros de filtragem.

        Retorna:
            dict: Dicionário com dados paginados e contagem total dos processos.
    """
    try:
        # Cria índices para melhorar performance
        Dados.ensure_indexes()

        # Monta query base
        query = Q(status_proc__ne="DELETADO")

        if filtros.numero_de_patrimonio is not None:
            query &= MongoEngineQuery.processar_filtro('outros_dados__numero_de_patrimonio', filtros.numero_de_patrimonio)
        if filtros.responsavel is not None:
            query &= MongoEngineQuery.processar_filtro('outros_dados_responsavel', filtros.responsavel)

        if filtros.ini_data_cadastro is not None and filtros.fim_data_cadastro is not None:
            # Converte as strings de data para objetos datetime
            data_init_dt = datetime.strptime(filtros.ini_data_cadastro, '%Y-%m-%d')
            data_end_dt = datetime.strptime(filtros.fim_data_cadastro, '%Y-%m-%d').replace(hour=23, minute=59, second=59)

            # Adiciona o filtro de intervalo de datas usando $gte e $lte
            query &= Q(data_cadastrado_gte=data_init_dt, data_cadastrado_lte=data_end_dt)

        elif filtros.ini_data_cadastro is not None and filtros.fim_data_cadastro is None:
            query &= Q(data_cadastrado__gte=datetime.strptime(filtros.ini_data_cadastro, '%Y-%m-%d'))

        elif filtros.ini_data_cadastro is None and filtros.fim_data_cadastro is not None:
            data_end_dt = datetime.strptime(filtros.fim_data_cadastro, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            query &= Q(data_cadastrado__lte=data_end_dt)

        # Executa query otimizada
        processos = Dados.objects(query).timeout(False).order_by(filtros.sort)
        total = processos.count()

        if filtros.pageble:
            processos = processos.skip(filtros.skip).limit(filtros.page_size)
            respostas_json = [p.to_dict() for p in processos]

            return {
                'data': respostas_json,
                'page': int(filtros.skip / filtros.page_size) + 1,
                'page_size': filtros.page_size,
                'page_count': total
            }
        else:
            respostas_json = [p.to_dict() for p in processos]
            return {
                'data': respostas_json,
                'page_count': total
            }

    except Exception as e:
        logging.error(f'reportar_contatos_service[busca_filtrado]: {str(e)}')
        raise erro_400(f"Erro ao buscar registros: {str(e)}")