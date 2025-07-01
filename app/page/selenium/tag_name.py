import time
from abc import ABC

from selenium.webdriver.common.by import By


class CssSelectorAbstract(ABC):
    def __init__(self, webbot, wait_d, wait_r):
        self.webbot = webbot
        self.wait_d = wait_d
        self.wait_r = wait_r

    def _existe_tag_name(self, tag_element: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o nome da tag especificado.

        Args:
            tag_element (str): O nome da tag a ser verificada.

        Returns:
            bool: True se pelo menos um elemento com o nome da tag existir, False caso contrário.
        """
        time.sleep(1)
        return len(self.webbot.find_elements(By.TAG_NAME, tag_element)) > 0

    def _existe_class_name(self, class_name: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o nome da classe especificado.

        Args:
            class_name (str): O nome da classe a ser verificada.

        Returns:
            bool: True se pelo menos um elemento com o nome da classe existir, False caso contrário.
        """
        time.sleep(1)
        return len(self.webbot.find_elements(By.CLASS_NAME, class_name)) > 0

    def _existe_id(self, id_element: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o ID especificado.

        Args:
            id_element (str): O ID do elemento a ser verificado.

        Returns:
            bool: True se pelo menos um elemento com o ID existir, False caso contrário.
        """
        time.sleep(1)
        return len(self.webbot.find_elements(By.ID, id_element)) > 0

    def _obter_texto_por_css_selector(self, css_selector: str) -> str:
        """
        Obtém o texto de um elemento identificado pelo seletor CSS.

        Args:
            css_selector (str): O seletor CSS do elemento.

        Returns:
            str: O texto do elemento. Se o elemento não for encontrado, retorna uma string vazia.
        """
        try:
            elemento = self.wait_d.until(lambda driver: driver.find_element(By.CSS_SELECTOR, css_selector))
            return elemento.text
        except Exception:
            return ""

    def _verificar_atributo_por_css_selector(self, css_selector: str, atributo: str, valor: str) -> bool:
        """
        Verifica se um atributo de um elemento identificado pelo seletor CSS corresponde ao valor fornecido.

        Args:
            css_selector (str): O seletor CSS do elemento.
            atributo (str): O nome do atributo a ser verificado.
            valor (str): O valor esperado do atributo.

        Returns:
            bool: True se o valor do atributo corresponder, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(lambda driver: driver.find_element(By.CSS_SELECTOR, css_selector))
            return elemento.get_attribute(atributo) == valor
        except Exception:
            return False

    def _esperar_elemento_visivel_por_css_selector(self, css_selector: str) -> bool:
        """
        Espera até que um elemento identificado pelo seletor CSS se torne visível.

        Args:
            css_selector (str): O seletor CSS do elemento.

        Returns:
            bool: True se o elemento se tornar visível, False caso contrário.
        """
        try:
            self.wait_d.until(lambda driver: driver.find_element(By.CSS_SELECTOR, css_selector).is_displayed())
            return True
        except Exception:
            return False
