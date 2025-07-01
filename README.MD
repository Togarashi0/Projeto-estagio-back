# Projeto RPA - Início Rápido para Desenvolvimento

### Este projeto foi criado para facilitar o início de novos desenvolvimentos utilizando o nosso framework e as principais bibliotecas criadas pela equipe de RPA. Ele contém todas as pastas e configurações necessárias para você começar a desenvolver rapidamente.

## Desenvolvedores

[Alvaro](https://github.com/alguipires)

## Requisitos

Antes de executar a aplicação, certifique-se de que o seguinte software esteja instalado em seu sistema:

- **Docker ou Docker compose**

### Passos para baixar o projeto
- Baixe o repositório sem incluir a pasta `.git`:
    ````
        git clone --depth=1 https://ernestoborgesms@dev.azure.com/ernestoborgesms/RPA/_git/projeto_base
        rm -rf projeto_base/.git
    ````
- Renomeie a pasta para o nome do seu projeto.

    `mv projeto_base meu_novo_projeto`

- Acesse o diretório do projeto.

    `cd nome-do-projeto`

- Configure o .env **Adicione todas as credenciais do .env**

#### Iniciar desenvolvimento
- Renomeie a Descrição da API e Outros Itens:

Os itens a serem renomeados estão marcados com #TODO no arquivo `__init__.py`.

- Inicialize o Repositório Git

Substitua `seu_repo_aqui` no link pelo nome do repositório que você criou

```
  git init
  git add .
  git commit -m "first commit"
  git branch -M main
  git remote add origin git@ssh.dev.azure.com:v3/ernestoborgesms/RPA/seu_repo_aqui
  git push -u origin main
````

#### Rodar em docker

- Execute o comando para criar a imagem:

`docker build -t nome-img .`

- Execute o comando para iniciar o container e a app:

`docker run -d -p 8000:8000 nome-img uvicorn app:app --host 0.0.0.0 --port 8000`

#### Rodar na maquina com a IDE

- Utilizando o pycharm crie um ambiente virtual para instalação das dependências
- Configure o runner do projeto para fastApi e selecione o `__init__.py` do diretorio `app/`
- Ao executar o projeto estará em execução em sua máquina

### Ambiente de Desenvolvimento

A FastAPI estará em execução no ambiente local, você poderá acessar a documentação do Swagger
em: http://localhost:8000/docs

## Versões

1.0 - Descrição da versão

## Contribuindo com a Equipe

Se você usou o projeto, identificou melhorias ou implementou algo que pode ser útil para futuros projetos, siga os passos abaixo para contribuir:
 - Crie uma Branch `git checkout -b nome-da-sua-branch`
 - Desenvolva
 - Crie uma Pull Request e marque os colegas para avaliar e autorizar o merge.