import os
import atexit
import signal
import pymongo
import threading
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException

from app import host_mongo
from app.data.models.processo import Processo

# Define a duração máxima para uma tarefa, após a qual será marcada como finalizada.
MAX_TASK_DURATION = timedelta(hours=28)


class TarefasRepository:
    """
    Repositório para gerenciar tarefas no MongoDB.

    Esta classe permite operações de CRUD (criação, leitura, atualização e deleção)
    em tarefas, manipulando o status e os tempos de execução das tarefas no banco de dados.
    """

    _instance = None
    _handlers_registered = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TarefasRepository, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        """Inicializa uma instância de `TarefasRepository`, conectando-se ao banco MongoDB."""
        self._db = pymongo.MongoClient(host_mongo)
        self._banco = self._db[os.getenv('MONGO_DB_NAME')]
        self._colecao = self._banco["core_security.tarefas"]

        # Registra handlers apenas uma vez
        if not TarefasRepository._handlers_registered:
            self._register_shutdown_handlers()
            TarefasRepository._handlers_registered = True

        self._initialized = True

    def _register_shutdown_handlers(self):
        """Registra handlers para eventos de desligamento (apenas uma vez) """

        # Only register signals in main thread
        if threading.current_thread() is not threading.main_thread():
            return  # Sai se não for a thread principal

        def handle_shutdown(signum=None, frame=None):
            print("Sinal de desligamento recebido, marcando tarefas como interrompidas")
            self._mark_running_tasks_as_interrupted()
            # Garante saída após tratamento
            if signum is not None:
                exit(0)

        # Armazena o handler original para restauração se necessário
        if not hasattr(TarefasRepository, '_original_handlers'):
            TarefasRepository._original_handlers = {
                signal.SIGTERM: signal.getsignal(signal.SIGTERM),
                signal.SIGINT: signal.getsignal(signal.SIGINT)
            }

        # Registra apenas se não estiver registrado
        if signal.getsignal(signal.SIGTERM) != handle_shutdown:
            signal.signal(signal.SIGTERM, handle_shutdown)
        if signal.getsignal(signal.SIGINT) != handle_shutdown:
            signal.signal(signal.SIGINT, handle_shutdown)

        atexit.register(handle_shutdown)

    def _mark_running_tasks_as_interrupted(self):
        """Marca todas as tarefas em execução como interrompidas"""
        Processo.objects(status_proc="INICIADO").update(status="PENDENTE")
        try:
            self._colecao.update_many(
                {"is_running": True},
                {"$set": {
                    "is_running": False,
                    "end_time": datetime.now(),
                    "force_stop": True
                }}
            )
        except Exception as e:
            print(f"Erro ao marcar tarefas como interrompidas: {str(e)}")

    def _cleanup_old_tasks(self):
        """Limpa tarefas antigas que podem ter ficado 'presas'"""
        threshold = datetime.now() - MAX_TASK_DURATION
        self._colecao.update_many(
            {
                "is_running": True,
                "start_time": {"$lt": threshold}
            },
            {"$set": {
                "is_running": False,
                "end_time": datetime.now(),
                "force_stop": True
            }}
        )

    def designado_rodando_em_outra_fila(self, nome_atual: str, designado: str = None) -> bool:
        """
        Verifica se o designado está rodando em outra fila diferente da atual.

        Args:
            nome_atual (str): O nome (task_name) da fila atual.
            designado (str): O designado a ser verificado.

        Returns:
            bool: True se existir outra tarefa em execução para o designado, caso contrário False.
        """
        # Procura por alguma tarefa que esteja rodando (is_running True) para o designado
        # e que não seja a fila atual.
        tarefa = self._colecao.find_one({
            "designado": designado,
            "is_running": True,
            "task_name": {"$ne": nome_atual}
        })
        return tarefa is not None

    def contar_filas_do_designado(self, designado: str) -> int:
        """
        Retorna a quantidade de filas diferentes em que o designado está sendo usado.

        Args:
            designado (str): O designado a ser verificado.

        Returns:
            int: O número de filas distintas onde o designado está rodando.
        """
        # Busca todas as tarefas em execução para o designado, agrupadas por task_name
        filas = self._colecao.distinct("task_name", {
            "designado": designado,
            "is_running": True
        })

        return len(filas)

    def ultimo_uso_usuario(self, usuario: str) -> datetime | None:
        """
        Obtém a data e hora da última vez que o usuário foi utilizado em uma tarefa.

        Args:
            usuario (str): O usuário a ser verificado.

        Returns:
            datetime | None: O horário da última execução ou None se não houver registros.
        """
        tarefa = self._colecao.find_one(
            {"designado": usuario},
            sort=[("start_time", pymongo.DESCENDING)]  # Ordena por start_time do mais recente ao mais antigo
        )
        return tarefa["start_time"] if tarefa else None

    def verificar_finalizado(self, nome: str) -> bool:
        """
        Verifica se a tarefa está no período de funcionamento ou se deve ser finalizada.

        Se o documento tiver a chave "business_hours", utiliza o campo "scheduled_stop"
        para determinar se o horário atual está dentro do período de funcionamento. Caso
        contrário, retorna o valor de "force_stop".

        :param nome: Nome da tarefa.
        :return: True se estiver no período (ou se force_stop for True), False caso contrário.
        :raises ValueError: Se o documento não for encontrado ou campos esperados estiverem ausentes.
        """
        # Recupera o documento uma única vez
        doc = self._colecao.find_one({"task_name": nome})
        if not doc:
            raise ValueError(f"Tarefa '{nome}' não encontrada no banco de dados.")

        def esta_no_periodo(schedule: dict) -> bool:
            """
            Verifica se o horário atual está dentro do período definido em schedule.

            :param schedule: Dicionário com o formato {"start": "HH:MM", "stop": "HH:MM"}.
            :return: True se estiver no período, False caso contrário.
            """
            agora = datetime.now().time()
            hora_inicio = datetime.strptime(schedule["start"], "%H:%M").time()
            hora_parada = datetime.strptime(schedule["stop"], "%H:%M").time()

            # Se o período não cruza a meia-noite
            if hora_inicio < hora_parada:
                return hora_inicio <= agora <= hora_parada

            # Período que cruza a meia-noite (ex: 19:30 a 07:30)
            return agora >= hora_inicio or agora <= hora_parada

        if "business_hours" in doc and doc['business_hours'] is not None:
            schedule = doc.get("scheduled_stop")
            if schedule:
                return esta_no_periodo(schedule)

        # Retorna o valor de 'force_stop', ou False se não estiver definido
        return doc.get("force_stop", True)

    def definir_schedule(self, nome: str, schedule: dict, business_hours: bool):
        self._colecao.update_one(
            {"task_name": nome},
            {"$set": {"business_hours": business_hours, "scheduled_stop": {"start": datetime.now().strftime("%H:%M"), "stop": schedule["stop"]}}}
        )

    def solicitar_interrupcao(self, nome: str) -> bool:
        """Solicita a interrupção de uma tarefa específica"""
        try:
            result = self._colecao.update_one(
                {"task_name": nome},
                {"$set": {"force_stop": True}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao solicitar interrupção: {str(e)}")
            raise

    def verificar_interrupcao(self, nome: str) -> bool:
        """Verifica se há solicitação de interrupção para a tarefa"""
        doc = self._colecao.find_one({"task_name": nome})
        return doc and doc.get("force_stop", False)

    def atualizar_progresso(self, nome: str, progresso: dict):
        """Atualiza o progresso da tarefa"""
        self._colecao.update_one(
            {"task_name": nome},
            {"$set": {"progresso": progresso}}
        )

    def obter_progresso(self, nome: str) -> Optional[dict]:
        """Obtém o progresso atual da tarefa"""
        doc = self._colecao.find_one({"task_name": nome})
        return doc.get("progresso") if doc else None

    def verificar_em_execucao(self, nome: str) -> bool:
        """Verifica se a tarefa está em execução"""
        doc = self._colecao.find_one({"task_name": nome})
        return doc and doc.get("is_running", False)

    def tarefa_recente_concluida(self, nome: str, horas: int = 1) -> bool:
        """Verifica se a tarefa foi concluída recentemente"""
        threshold = datetime.now() - timedelta(hours=horas)
        doc = self._colecao.find_one({
            "task_name": nome,
            "is_running": False,
            "end_time": {"$gt": threshold}
        })
        return doc is not None

    def finalizar_tarefa(self, nome, erro_login: bool = False):
        """
        Finaliza uma tarefa marcando-a como concluída.

        Atualiza o status de uma tarefa no banco de dados, marcando-a como "is_running" False,
        e registrando o horário de término.

        Args:
            nome (str): O nome da tarefa a ser finalizada.
            :param nome:
            :param erro_login:
        """
        self._colecao.update_one(
            {"task_name": nome},
            {"$set": {"is_running": False, "end_time": datetime.now(), "erro_login": erro_login}}
        )

    def atualizar_designado(self, nome, designado=None):
        self._colecao.update_one({"task_name": nome}, {"$set": {'designado': designado}}, upsert=True)

    def inicializar_tarefa(self, nome, designado=None, session_id=None, qtd=None, hora_fim=None, solicitante=None):
        """
        Inicializa uma tarefa marcando-a como em execução.

        Atualiza o status de uma tarefa existente ou cria uma nova entrada no banco de dados.
        A tarefa será marcada como "is_running" com o horário de início atual.

        Args:
            :param solicitante:
            :param hora_fim:
            :param nome:
            :param qtd:
            :param session_id:
            :param designado:
        """
        if (hora_fim is not None):
            self._colecao.update_one({"task_name": nome},
                                     {"$set": {"is_running": True, "erro_login": False, "force_stop": False, "start_time": datetime.now(), 'designado': designado, 'id_driver_session': session_id,
                                               'amount': qtd,
                                               "business_hours": True, "solicitante": solicitante, "scheduled_stop": {"start": datetime.now().strftime("%H:%M"), "stop": hora_fim}}},
                                     upsert=True)
        else:
            self._colecao.update_one({"task_name": nome},
                                     {"$set": {"is_running": True, "erro_login": False, "force_stop": False, "start_time": datetime.now(), 'designado': designado, 'id_driver_session': session_id,
                                               'amount': qtd,
                                               "business_hours": False, "solicitante": solicitante, "scheduled_stop": None}},
                                     upsert=True)

    def disponivel(self, nome):
        """
        Verifica se uma tarefa está disponível para ser executada.

        Se uma tarefa estiver em execução e sua duração exceder `MAX_TASK_DURATION`,
        a tarefa será marcada como finalizada. Caso contrário, uma exceção será levantada
        se a tarefa ainda estiver em execução.

        Args:
            nome (str): O nome da tarefa a ser verificada.

        Raises:
            HTTPException: Se a tarefa estiver em execução e dentro da duração permitida.
        """
        task_status = self._colecao.find_one({"task_name": nome})
        if task_status and task_status.get("is_running"):
            start_time = task_status.get("start_time")
            if start_time and (datetime.now() - start_time) > MAX_TASK_DURATION:
                # Marca a tarefa como finalizada se exceder o tempo máximo permitido.
                self.finalizar_tarefa(nome)
                return True
            else:
                # Lança exceção se a tarefa ainda estiver rodando.
                raise HTTPException(status_code=409, detail="Existe um processo rodando em background!")

    def ativas(self, nome):
        return self._colecao.find({"is_running": True, "task_name": {"$regex": nome, "$options": "i"}})


def escolher_fila_disponivel(nome_fila, hora_fim, quantidade_filas: int = 5) -> str:
    """
    Verifica as 4 (ou quantidade do parametro) filas definidas e retorna a primeira disponível.
    Se nenhuma fila estiver disponível, gera uma exceção HTTP 409.
    """
    repositorio = TarefasRepository()
    # Lista dos nomes de filas a serem verificados.
    for i in range(1, quantidade_filas + 1):
        task_name = nome_fila + str(i)
        try:
            repositorio.disponivel(task_name)
            repositorio.inicializar_tarefa(task_name, hora_fim=hora_fim)
            return task_name
        except HTTPException:
            # Se a fila estiver ocupada, passa para a próxima.
            continue
    # Se todas estiverem ocupadas, lança exceção.
    raise HTTPException(status_code=409, detail="Todas as filas estão em execução.")


def escolher_fila(task_name, hora_fim) -> bool:
    repositorio = TarefasRepository()
    try:
        repositorio.disponivel(task_name)
        repositorio.inicializar_tarefa(task_name, hora_fim=hora_fim)
        return True
    except HTTPException:
        raise HTTPException(status_code=409, detail="Todas as filas estão em execução.")
