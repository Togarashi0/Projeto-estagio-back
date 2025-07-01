from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField


class BaseModel(Document):
    meta = {'abstract': True}

    data_cadastrado = DateTimeField(required=True)
    data_atualizacao = DateTimeField(required=True)

    usuario_insercao: str = StringField()
    usuario_atualizacao: str = StringField()
    usuario_acionamento: str = StringField()

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
