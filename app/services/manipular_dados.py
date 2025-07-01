import logging
from datetime import datetime

from bson import ObjectId
from mongoengine import DoesNotExist

from app.data.models.dados import Dados, Dados_outros
from app.data.models.setor import Setor


class Manipular_dados:

    def __init__(self):
        self.log = None

    def criar_registro(
            self,
            numero_de_patrimonio: str,
            equipamento: str | None = None,
            setor: str | None = None,
            unidade: str | None = None,
            cidade: str | None = None,
            responsavel: str | None = None,
    ) -> bool:
        """
        Cria (ou atualiza) um registro em Dados.

        Returns
        -------
        bool
            True  → novo documento criado ou reativado
            False → documento já existia (apenas atualizado)
        """
        try:
            # Tenta encontrar o registro, mesmo se deletado
            self.log = Dados.objects(outros_dados__numero_de_patrimonio=numero_de_patrimonio).first()

            if self.log:
                atualizacoes = {}
                if equipamento is not None:
                    atualizacoes["set__outros_dados__equipamento"] = equipamento
                if setor is not None:
                    atualizacoes["set__outros_dados__setor"] = setor
                if unidade is not None:
                    atualizacoes["set__outros_dados__unidade"] = unidade
                if cidade is not None:
                    atualizacoes["set__outros_dados__cidade"] = cidade
                if responsavel is not None:
                    atualizacoes["set__outros_dados__responsavel"] = responsavel

                # Se estava excluído, reativa
                if self.log.status_proc == "DELETADO":
                    atualizacoes["set__status_proc"] = "ATIVO"

                if atualizacoes:
                    atualizacoes["set__data_atualizacao"] = datetime.now()
                    self.log.update(**atualizacoes)

                return False  # já existia (reativado ou atualizado)

            # Se não existia, cria novo
            setor_doc = None
            if setor:
                setor_doc = Setor.objects(nome_setor=setor).first()

            if setor and not setor_doc:
                logging.error(f"Setor '{setor}' não encontrado.")
                return False

            self.log = Dados(
                id_projeto=setor_doc,
                status_proc="ATIVO",
                outros_dados=Dados_outros(
                    numero_de_patrimonio=numero_de_patrimonio,
                    equipamento=equipamento,
                    setor=setor,
                    unidade=unidade,
                    cidade=cidade,
                    responsavel=responsavel,
                ),
            )
            self.log.save()
            return True  # novo documento criado

        except Exception as e:
            logging.exception(f"Erro ao criar/atualizar registro: {e}")
            return False

    def deletar_registro(self, id: str) -> bool:
        try:
            registro = Dados.objects.get(id=ObjectId(id))
            registro.delete()
            return True
        except DoesNotExist:
            logging.warning(f"Registro com ID {id} não encontrado para exclusão.")
            return False
        except Exception as e:
            logging.exception(f"Erro ao excluir registro: {e}")
            return False
