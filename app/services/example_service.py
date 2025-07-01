import logging


class ExampleService:
    """
        Serviço para...

        Atributos:
            self.atributo1 (str): String de teste.
    """

    def __init__(self):
        """
            Inicializa o serviço ...
        """
        self.atributo1 = "Sou um teste!! vulgo Hello World!!!"

    def teste(self):
        """
           Metodo teste...
       """
        try:
            return self.atributo1
        except Exception as e:
            logging.error(f"Erro xyz... ERRO: {e}")
            raise e
