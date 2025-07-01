from mongoengine import Document, StringField, BooleanField, IntField


class Setor(Document):
    nome_setor = StringField(required=False)


    meta = {'collection': 'Setores', 'strict': False}
