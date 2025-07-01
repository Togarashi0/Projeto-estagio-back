import datetime
import logging
import time
from typing import Union
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

from app import APP_TITLE
from app.data.api.api_blob_storage import AzureBlob
from app.data.models.arquivo import Arquivo
from app.page.selenium.class_name import ClassNameAbstract
from app.page.selenium.css_selector import CssSelectorAbstract
from app.page.selenium.id import IdAbstract
from app.page.selenium.keys import KeysAbstract
from app.page.selenium.xpath import XpathAbstract
from app.utils.constants import Constants

WAITING_TIME = 60


def iniciar_driver_prod(projeto_nome: str = None, headless: bool = False):
    """
    Inicializa o WebDriver do Chrome para o ambiente de produção.

    Args:
        projeto_nome (str, optional): Nome do projeto para identificação no Selenoid. Default é "Reportar Contatos do Cliente Mercado Pago".
        headless (bool): Se True, o navegador será iniciado em modo headless (sem interface gráfica). Default é False.

    Returns:
        WebDriver: Instância do WebDriver configurada para o ambiente de produção.

    Raises:
        RuntimeError: Se não for possível criar a conexão com o ChromeDriver após várias tentativas.

    Logs:
        info: Indica o início da inicialização do WebDriver.
        error: Informa sobre erros ao tentar inicializar o WebDriver.
    """
    logging.info("Inicializando chrome webdriver")
    qtd_erros = 0
    while True:
        try:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("window-size=1920x1080")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("prefs",
                                            {"download.default_directory": Constants.TEMP_DIR, "download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled": True})
            options.set_capability("browserName", 'chrome')
            options.set_capability("browserVersion", '112.0')
            options.set_capability("selenoid:options", {"enableVNC": True, "enableVideo": False, "sessionTimeout": "12m", "name": projeto_nome or APP_TITLE})
            driver = webdriver.Remote(command_executor="http://10.67.5.209:4444/wd/hub", options=options)
            driver.maximize_window()
            return driver
        except Exception as e:
            if qtd_erros <= 10:
                time.sleep(50)
                qtd_erros += 1
                logging.error(f"Erro ao buscar o driver no selenoid: {e}")
            else:
                raise RuntimeError(f'ERRO ao criar a conexão com o chrome driver: {e.args}')


def iniciar_driver_local(headless: bool = False):
    """
    Inicializa o WebDriver do Chrome para o ambiente local.

    Returns:
        WebDriver: Instância do WebDriver configurada para o ambiente local.

    Raises:
        RuntimeError: Se não for possível criar a conexão com o ChromeDriver.

    Logs:
        error: Informa sobre erros ao tentar inicializar o WebDriver.
    """
    try:
        options = Options()
        options.add_experimental_option(
            "prefs", {
                "download.default_directory": Constants.TEMP_DIR,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        )
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-infobars")  # Desativa barras de informação
        options.add_argument("--disable-extensions")  # Desativa extensões
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)
    except Exception as e:
        raise RuntimeError(f'ERRO ao criar a conexão com o chrome driver: {e.args}')


@contextmanager
def iniciar_driver_context(projeto: str = "Webdriver - Remoto TESTE"):
    driver = iniciar_driver_prod(projeto)
    try:
        yield driver
    except Exception as e:
        logging.error(f"Erro ao inicializar o WebDriver remoto: {str(e)}")
        raise RuntimeError(f"Erro ao inicializar o WebDriver remoto: {str(e)}")
    finally:
        driver.quit()


@contextmanager
def iniciar_driver_context_local():
    driver = iniciar_driver_local()
    try:
        yield driver
    except Exception as e:
        logging.error(f"Erro ao inicializar o WebDriver local: {str(e)}")
        raise RuntimeError(f"Erro ao inicializar o WebDriver local: {str(e)}")
    finally:
        driver.quit()


@contextmanager
def iniciar_driver_context_selecionado(projeto: str = None, driver_prod=True):
    """
    Inicializa o WebDriver no ambiente correto (local ou remoto) e gerencia seu ciclo de vida.

    Args:
        projeto (str): Nome do projeto (usado apenas se for ambiente de produção).
        driver_prod (bool): Define se será usado o driver remoto (True) ou local (False).

    Yields:
        WebDriver: Instância do WebDriver já configurada.
    """
    try:
        if driver_prod:
            with iniciar_driver_context(projeto) as driver:  # Usa o driver remoto
                yield driver
        else:
            with iniciar_driver_context_local() as driver:  # Usa o driver local
                yield driver
    except Exception as e:
        logging.error(f"Erro ao inicializar o WebDriver: {str(e)}")
        raise RuntimeError(f"Erro ao inicializar o WebDriver: {str(e)}")


class SeleniumAbstract(XpathAbstract, IdAbstract, CssSelectorAbstract, ClassNameAbstract, KeysAbstract):
    """
    Classe abstrata para interações com o Selenium WebDriver.
    Esta classe fornece métodos para interagir com elementos da página, como clicar, enviar texto, verificar a existência de elementos,
    e tirar capturas de tela. Além disso, ela também lida com a configuração do WebDriver e a manipulação de janelas.
    A classe é projetada para ser estendida por outras classes que implementam funcionalidades específicas de automação de testes.

    Atributos:
        - projeto_nome (str): Nome do projeto.
        - webbot (WebDriver): Instância do WebDriver.
        - wait_d (WebDriverWait): Instância do WebDriverWait para espera padrão.
        - wait_r (WebDriverWait): Instância do WebDriverWait para espera rápida.
        - azure_blob (AzureBlob): Instância do AzureBlob para upload de arquivos.
    """

    def __init__(self, webbot: WebDriver, projeto_nome: str = None):
        """
        Inicializa a classe SeleniumAbstract com o WebDriver e o nome do projeto.
        :param webbot:
        :param proejto_nome:
        """
        self.projeto_nome = projeto_nome or APP_TITLE
        self.webbot: WebDriver = webbot
        self.wait_d = WebDriverWait(webbot, WAITING_TIME)
        self.wait_r = WebDriverWait(webbot, 20)
        XpathAbstract.__init__(self, self.webbot, self.wait_d, self.wait_r)
        IdAbstract.__init__(self, self.webbot, self.wait_d, self.wait_r)
        CssSelectorAbstract.__init__(self, self.webbot, self.wait_d, self.wait_r)
        ClassNameAbstract.__init__(self, self.webbot, self.wait_d, self.wait_r)
        KeysAbstract.__init__(self, self.webbot, self.wait_d, self.wait_r)
        self.azure_blob = AzureBlob(container_name="screenshots")

    def _limpar_input_por_id(self, id_element: str):
        self.wait_d.until(presence_of_element_located((By.ID, id_element))).clear()

    def _existe_class_por_id(self, id_element: str, class_html: str):
        time.sleep(1)
        return class_html in self.webbot.find_element(By.ID, id_element).get_attribute("class")

    def _existe_tag_name(self, tag_element: str) -> bool:
        time.sleep(1)
        return len(self.webbot.find_elements(By.TAG_NAME, tag_element)) > 0

    def _existe_id(self, id_element: str) -> bool:
        time.sleep(1)
        return len(self.webbot.find_elements(By.ID, id_element)) > 0

    def _existe_xpath(self, id_element: str) -> bool:
        time.sleep(1)
        return len(self.webbot.find_elements(By.XPATH, id_element)) > 0

    def _existe_css_selector(self, css_element: str) -> bool:
        time.sleep(1)
        return len(self.webbot.find_elements(By.CSS_SELECTOR, css_element)) > 0

    def _existe_css_selector_text(self, css_element: str, texto: str) -> bool:
        time.sleep(1)
        return self._existe_css_selector(css_element) and texto in [text.text for text in self.webbot.find_elements(By.CSS_SELECTOR, css_element)]

    def _verificar_texto_por_id(self, id_element: str, text: str) -> bool:
        time.sleep(1)
        return self.webbot.find_element(By.ID, id_element).text.upper() == text.upper()

    def _acessar_janela_atual(self):
        """
        Acessa a janela do navegador atual.
        """
        janelas = self.webbot.window_handles
        self.webbot.switch_to.window(janelas[-1])

    def _mudar_janela(self, id_element):
        """
        Muda para a janela do navegador especificada pelo índice.

        Args:
            id_element (int): O índice da janela para a qual mudar.
        """
        janelas = self.webbot.window_handles
        self.webbot.switch_to.window(janelas[id_element])

    def _obter_alerta(self) -> Union[Alert, None]:
        """
        Obtém o alerta atual da página.

        Returns:
            Alert: O alerta atual da página.
        """
        try:
            return Alert(self.webbot)
        except NoAlertPresentException:
            return None

    def take_screenshot(self, filename: str):
        """
        Tira uma captura de tela da página atual e salva com o nome de arquivo especificado.

        Args:
            filename (str): O nome do arquivo onde a captura de tela será salva.

        Logs:
            info: Se a captura de tela for salva com sucesso.
            error: Se houver um erro ao salvar a captura de tela.
        """
        try:
            self.webbot.save_screenshot(Constants.SCREENSHOT + filename)
            logging.info(f"Screenshot salvo: {filename}")
        except Exception as e:
            logging.error(f"Erro ao salvar screenshot: {str(e)}")

    def take_screenshot_erros(self):
        try:
            filename = f"{self.projeto_nome}-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
            screenshot = Arquivo(nome_arquivo=filename, extensao="png", categoria="SCREENSHOT", blob_bucket_name="screenshots", blob_connection_string=self.azure_blob.connection_string).save()
            screenshot_bytes = self.webbot.get_screenshot_as_png()
            self.azure_blob.upload_file(filename, screenshot_bytes)
            logging.info(f"Screenshot de erro enviado para o blob com sucesso: {filename}")
            return screenshot
        except Exception as e:
            logging.error(f"Erro ao enviar screenshot de erro para o blob: {str(e)}")

    def enter(self):
        action = ActionChains(self.webbot)
        action.send_keys(Keys.ENTER)
        action.perform()

    def pag_down(self):
        action = ActionChains(self.webbot)
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()

    def set_screen_resolution(self, width=None, height=None):
        """
        Configures the browser dimensions.

        Args:
            width (int): The desired width.
            height (int): The desired height.
        """
        dimensions = (width, height)

        window_size = self.webbot.execute_script("""
            return [window.outerWidth - window.innerWidth + arguments[0],
              window.outerHeight - window.innerHeight + arguments[1]];
            """, *dimensions)
        self.webbot.set_window_size(*window_size)
