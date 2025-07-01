from mongoengine.queryset.visitor import Q


class MongoEngineQuery:

    @staticmethod
    def processar_filtro(campo, filtro):
        if not isinstance(filtro, str):
            filtro = str(filtro)
        partes = filtro.split(',')
        if len(partes) >= 2:
            operador, valor = partes[0], partes[1]
            if operador == 'contains':
                return Q(**{campo + '__icontains': valor})
            elif operador == 'notContains':
                return Q(**{campo + '__not__icontains': valor})
            elif operador == 'equals':
                return Q(**{campo: valor})
        return Q(**{campo + '__icontains': filtro})

    @staticmethod
    def processar_filtro_agregacao(filtro):
        partes = filtro.split(',')
        if len(partes) >= 2:
            operador, valor = partes[0], partes[1]
            if operador == 'contains':
                return {"$regex": valor, "$options": "i"}
            elif operador == 'notContains':
                return {"$not": {"$regex": valor, "$options": "i"}}
            elif operador == 'equals':
                return {"$eq": valor}
            elif operador == 'notEquals':
                return {"$ne": valor}
        return {"$regex": filtro, "$options": "i"}

    @staticmethod
    def processar_filtro_agregacao_num(filtro):
        partes = filtro.split(',')
        if len(partes) >= 2:
            operador, valor = partes[0], partes[1]
            if operador == 'equals':
                return {"$eq": int(valor)}
            elif operador == 'notEquals':
                return {"$ne": int(valor)}
        return {"$regex": filtro, "$options": "i"}
