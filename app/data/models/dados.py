from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, DynamicEmbeddedDocument, EmbeddedDocumentField, EmbeddedDocument, ReferenceField

from app.data.models.setor import Setor


class Response(DynamicEmbeddedDocument):
    pass


class Dados_outros(EmbeddedDocument):
    numero_de_patrimonio = StringField(required=True)
    equipamento = StringField()
    setor = StringField()
    unidade = StringField()
    cidade = StringField()
    responsavel = StringField()

    def to_dict(self):
        return {
            'numero_de_patrimonio': self.numero_de_patrimonio,
            'equipamento': self.equipamento,
            'setor': self.setor,
            'unidade': self.unidade,
            'cidade': self.cidade,
            'responsavel': self.responsavel
        }


class Dados(Document):
    id_projeto = ReferenceField(Setor, required=False)

    data_cadastrado = DateTimeField()

    data_atualizacao = DateTimeField(default=None)
    status_proc = StringField(default="ATIVO")
    outros_dados = EmbeddedDocumentField(Dados_outros, required=True)

    meta = {'collection': 'Dados'}

    def save(self, *args, **kwargs):
        """ Garante que data_atualizacao será sempre atualizada antes de salvar. """
        self.data_atualizacao = datetime.now()
        self.data_cadastrado = datetime.now()
        return super().save(*args, **kwargs)

    def update(self, **kwargs):
        """ Atualiza data_atualizacao antes de rodar um update. """
        kwargs["set__data_atualizacao"] = datetime.now()
        return super().update(**kwargs)

    def modify(self, query=None, **update):
        """ Atualiza data_atualizacao antes de modificar diretamente no banco. """
        update["set__data_atualizacao"] = datetime.now()
        return super().modify(query=query, **update)

    def delete(self, signal_kwargs=None, **write_concern):
        """ Atualiza data_atualizacao antes de modificar diretamente no banco. """
        return super().update(status_proc="DELETADO", data_atualizacao=datetime.now())

    def to_dict(self):
        result = {
            '_id': str(self.id),
            'id_projeto': str(self.id_projeto) if self.id_projeto else None,
            'outros_dados': self.outros_dados.to_dict() if self.outros_dados else None,
            'data_cadastrado': self.data_cadastrado,
            'data_atualizacao': self.data_atualizacao if self.data_atualizacao else None,
        }
        return result