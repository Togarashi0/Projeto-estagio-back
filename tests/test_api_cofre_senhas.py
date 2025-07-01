from app.data.api.api_cofre_senhas import ApiCofreSenhas
import logging


class TestApiCofreSenha:
    """
    Classe para testar a funcionalidade da ApiCofreSenhas.
    """

    @staticmethod
    def testar_download_arquivo():
        """
        Testa o método de baixar arquivo da ApiCofreSenhas.
        """
        api = ApiCofreSenhas()
        arquivo_id = "67ad0b667f1219d9d19d82bc"  # Substituir pelo ID real do arquivo

        conteudo_arquivo = api.baixar_arquivo(arquivo_id)

        if conteudo_arquivo:
            caminho_arquivo = "tests/arquivo_baixado.bin"
            with open(caminho_arquivo, "wb") as f:
                f.write(conteudo_arquivo)
            print(f"✅ Arquivo baixado com sucesso: {caminho_arquivo}")
        else:
            print("❌ Falha ao baixar o arquivo. Verifique logs.")

    @staticmethod
    def testar_listagem_credenciais():
        """
        Testa o método de listagem de credenciais da ApiCofreSenhas.
        """
        api = ApiCofreSenhas()
        credenciais = api.buscar_credenciais(projeto="API PROCESOS ENCERRADOS E PAGAMENTOS - ITAU")
        # credenciais = api.buscar_credenciais(nome_portal="SERVICENOW")
        # credenciais = api.buscar_credenciais(projeto="Atualização dos acordos no ServiceNow", nome_portal="SERVICENOW")

        if credenciais:
            print("✅ Credenciais encontradas:")
            for credencial in credenciais:
                print("credencial json: ", credencial)
                print(f"ID: {credencial['id']}")
                print(f"login: {credencial['login']}")
                print(f"senha: {credencial['senha']}")

                # Verifica se 'arquivos' existe e é uma lista
                if "arquivos" in credencial and isinstance(credencial["arquivos"], list):
                    print(f"arquivos: {credencial['arquivos']}")

                    for arquivo in credencial["arquivos"]:
                        if "arquivo_id" in arquivo:
                            print(f"arquivos.arquivo_id: {arquivo['arquivo_id']}")
                else:
                    print("❌ Nenhum arquivo encontrado para esta credencial.")

                # Verifica se 'campos' existe e é uma lista
                if "campos" in credencial and isinstance(credencial["campos"], list):
                    print(f"campos: {credencial['campos']}")

                    for campo in credencial["campos"]:
                        if "campo_id" in campo:
                            print(f"campos.campo_id: {campo['campo_id']}")
                else:
                    print("❌ Nenhum campo encontrado para esta credencial.")
        else:
            print("❌ Nenhuma credencial encontrada. Verifique logs.")

    @staticmethod
    def testar_listagem_e_recuperacao_login_senha():
        """
        Testa o método de listagem de credenciais e recuperação de login e senha da ApiCofreSenhas.
        """
        api = ApiCofreSenhas()
        credenciais = api.buscar_credenciais(projeto="API PROCESOS ENCERRADOS E PAGAMENTOS - ITAU")

        if credenciais:
            print("✅ Credenciais encontradas:")
            for credencial in credenciais:
                print("credencial json: ", credencial)
                login, senha = api.obter_login_senha(credencial)
                print(f"Login: {login}, Senha: {senha}, Id: {credencial['id']}")
        else:
            print("❌ Nenhuma credencial encontrada. Verifique logs.")

    @staticmethod
    def testar_listagem_e_recuperacao_login_senha_por_filtro_login():
        """
        Testa o método de listagem de credenciais e recuperação de login e senha da ApiCofreSenhas filtrando por login.
        """
        api = ApiCofreSenhas()
        login_filtro = "40022.OP93"
        nome_projeto = "API PROCESOS ENCERRADOS E PAGAMENTOS - ITAU"

        logging.info(f"🔍 Buscando credenciais com login: {login_filtro}")

        try:
            resultado = api.obter_login_senha_filtrando_por_login(login_filtro, nome_projeto)
            # resultado = api.obter_login_senha_filtrando_por_login(login="anderson.irigarai@bradesco.com.br", projeto="Atualização dos acordos no ServiceNow", nome_portal="SERVICENOW")

            if not resultado:
                logging.warning("⚠️ Nenhuma credencial encontrada para o login especificado.")
                return

            if isinstance(resultado, tuple) and len(resultado) >= 2:
                login, senha, id = resultado
                print(f"🔑 Login: {login} | 🔒 Senha: {senha} | 🆔 ID: {id}")
                logging.info(f"🔑 Login: {login} | 🔒 Senha: {senha} | 🆔 ID: {id}")
            else:
                print(f"❌ Retorno inesperado da API: {resultado}")
                logging.error(f"❌ Retorno inesperado da API: {resultado}")

        except Exception as e:
            logging.exception(f"🚨 Erro ao buscar credenciais: {e}")

    @staticmethod
    def testar_listagem_e_envio_email_expirado():
        """
        Testa o método de listagem de credenciais e envio de e-mail para credencial expirada da ApiCofreSenhas.
        """
        api = ApiCofreSenhas()
        login_filtro = "40022.OP93"
        nome_projeto = "API PROCESOS ENCERRADOS E PAGAMENTOS - ITAU"

        logging.info(f"🔍 Buscando credenciais com login: {login_filtro}")

        try:
            resultado = api.obter_login_senha_filtrando_por_login(login_filtro, nome_projeto)
            # resultado = api.obter_login_senha_filtrando_por_login(login="anderson.irigarai@bradesco.com.br", projeto="Atualização dos acordos no ServiceNow", nome_portal="SERVICENOW")

            if not resultado:
                logging.warning("⚠️ Nenhuma credencial encontrada para o login especificado.")
                return

            if isinstance(resultado, tuple) and len(resultado) >= 2:
                login, senha, id = resultado
                print(f"🔑 Login: {login} | 🔒 Senha: {senha} | 🆔 ID: {id}")
                logging.info(f"🔑 Login: {login} | 🔒 Senha: {senha} | 🆔 ID: {id}")

                # Enviar e-mail
                resposta = api.enviar_email_credencial_expirada(credencial_ids=[id], nome_automacao="Automação teste API")
                print(f"📧 Resposta da API: {resposta}")
                logging.info(f"📧 Resposta da API: {resposta}")


            else:
                logging.error(f"❌ Retorno inesperado da API: {resultado}")

        except Exception as e:
            logging.exception(f"🚨 Erro ao buscar credenciais: {e}")

    @staticmethod
    def envio_email_expirado():
        """
        Testa o método de listagem de credenciais e envio de e-mail para credencial expirada da ApiCofreSenhas.
        """
        api = ApiCofreSenhas()
        id = ["67af82ba44b2297d39be8087", "67d0982a036fab1838dab8f1"]
        # id = ["67af82ba44b2297d39be8087"]

        try:

            resposta = api.enviar_email_credencial_expirada(credencial_ids=id, nome_automacao="Automação teste API")
            logging.info(f"📧 Resposta da API: {resposta}")

        except Exception as e:
            logging.exception(f"🚨 Erro ao enviar e-mail: {e}")


if __name__ == "__main__":
    # TestApiCofreSenha.testar_download_arquivo()
    # TestApiCofreSenha.testar_listagem_credenciais()
    # TestApiCofreSenha.testar_listagem_e_recuperacao_login_senha()
    # TestApiCofreSenha.testar_listagem_e_recuperacao_login_senha_por_filtro_login()
    # TestApiCofreSenha.testar_listagem_e_envio_email_expirado()
    TestApiCofreSenha.envio_email_expirado()

# import unittest
# import logging
# from app.data.api.api_cofre_senhas import ApiCofreSenhas
#
# class TestApiCofreSenha(unittest.TestCase):
#     """
#     Classe de testes para ApiCofreSenhas.
#     """
#
#     def setUp(self):
#         """Configuração antes de cada teste."""
#         self.api = ApiCofreSenhas()
#
#     def test_download_arquivo(self):
#         """Testa o método de baixar arquivo da ApiCofreSenhas."""
#         arquivo_id = "67ad0b667f1219d9d19d82bc"  # Substituir pelo ID real do arquivo
#         conteudo_arquivo = self.api.baixar_arquivo(arquivo_id)
#
#         self.assertIsNotNone(conteudo_arquivo, "O conteúdo do arquivo não pode ser None")
#
#         caminho_arquivo = "tests/arquivo_baixado.bin"
#         with open(caminho_arquivo, "wb") as f:
#             f.write(conteudo_arquivo)
#
#         logging.info(f"✅ Arquivo baixado com sucesso: {caminho_arquivo}")
#
#     def test_listagem_credenciais(self):
#         """Testa o método de listagem de credenciais da ApiCofreSenhas."""
#         credenciais = self.api.buscar_credenciais("CPF Atualização Automática")
#
#         self.assertIsInstance(credenciais, list, "A resposta deve ser uma lista")
#         self.assertGreater(len(credenciais), 0, "Deve haver pelo menos uma credencial")
#
#         for credencial in credenciais:
#             self.assertIn("id", credencial)
#             self.assertIn("login", credencial)
#             self.assertIn("senha", credencial)
#
#     def test_listagem_e_recuperacao_login_senha(self):
#         """Testa a recuperação de login e senha da ApiCofreSenhas."""
#         credenciais = self.api.buscar_credenciais("CPF Atualização Automática")
#
#         self.assertIsInstance(credenciais, list, "A resposta deve ser uma lista")
#         self.assertGreater(len(credenciais), 0, "Deve haver pelo menos uma credencial")
#
#         for credencial in credenciais:
#             login, senha = self.api.obter_login_senha(credencial)
#             self.assertIsInstance(login, str)
#             self.assertIsInstance(senha, str)
#
#     def test_listagem_e_recuperacao_login_senha_por_filtro_login(self):
#         """Testa a recuperação de credenciais filtrando por login."""
#         login_filtro = "40022.OP93"
#         nome_projeto = "API PROCESOS ENCERRADOS E PAGAMENTOS - ITAU"
#
#         logging.info(f"🔍 Buscando credenciais com login: {login_filtro}")
#         resultado = self.api.obter_login_senha_filtrando_por_login(login_filtro, nome_projeto)
#
#         self.assertIsNotNone(resultado, "Nenhuma credencial encontrada.")
#         self.assertIsInstance(resultado, tuple, "O retorno deve ser uma tupla")
#         self.assertEqual(len(resultado), 2, "A tupla deve conter exatamente dois elementos")
#
#         login, senha = resultado
#         self.assertIsInstance(login, str)
#         self.assertIsInstance(senha, str)
#         logging.info(f"🔑 Login: {login} | 🔒 Senha: {senha}")
#
# if __name__ == "__main__":
#     unittest.main()
