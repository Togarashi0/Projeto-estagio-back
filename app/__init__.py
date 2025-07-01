import os
import json
import logging.config
from dotenv import load_dotenv
from fastapi import FastAPI
from mongoengine import disconnect, connect
from starlette.middleware.cors import CORSMiddleware

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# TODO: Defina o nome curto do seu projeto para ser usado nas classes e na nomeação de arquivos. Remover este comentário depois.
APP_TITLE: str = "projeto"

# Cria uma instância do FastAPI
# TODO descreva a sua API aqui -  Remover este comentário depois.
app = FastAPI(title="API de Automação de Dados",
              summary="""editar, adicionar, exclir registros""",
              description="""
```Responsáveis: Marcos Dijulian Zellner```""",
              version=os.environ.get("VERSION"),
              contact={
                  "name": "Instituto de Identificação do Paraná",
              },
              license_info={
                  "name": "Copyright © Instituto de Identificação do Paraná - Todos os direitos reservados.",
              },
              openapi_tags=[
                  {
                      "name": "cadastro_dados",
                      "description": "Cadastar dados."
                  }
              ],
              swagger_ui_parameters={
                  "syntaxHighlight.theme": "ascetic",
                  "deepLinking": False,
                  "defaultModelsExpandDepth": -1,
                  "filter": True,
                  "docExpansion": "none"
              })

# Lista de origens permitidas (pode ser ajustada de acordo com suas necessidades)
origins = [
    "http://localhost:4200",
]

# Configuração do middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados mongoengine
host_mongo = os.getenv("MONGO_DB_URL")
disconnect(alias='default')
connect(db=os.getenv('MONGO_DB_NAME'), host=host_mongo)

# Configura o app
app.secret_key = os.getenv('APP_SECRET_KEY')

app.max_request_size = 1000 * 1024 * 1024

from app.utils.files import Files

# Criar a estrutura de pastas necessárias para rodar a aplicação.
Files.create_folder_structure()

try:
    if os.path.exists('logging.json'):
        # Carrega o arquivo de configuração do logging
        with open('logging.json', 'rt') as f:
            config = json.load(f)
        # Configura o logging com base no arquivo de configuração
        logging.config.dictConfig(config)
except Exception as e:
    # Configura o logging com o nível de log INFO como padrão
    logging.basicConfig(level=logging.INFO)

from app.controllers import dados_controller
