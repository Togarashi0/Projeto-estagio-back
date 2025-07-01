import time
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable


class XpathAbstract(ABC):
    def __init__(self, webbot, wait_d, wait_r):
        self.webbot = webbot
        self.wait_d = wait_d
        self.wait_r = wait_r

    def _selecionar_option_por_xpath_visible_text(self, xpath_element: str, value_element: str, rapido=False) -> bool:
        """
        Seleciona uma opção de um elemento <select> pelo seu XPath, baseado no texto visível da opção.

        Args:
            xpath_element (str): O XPath do elemento <select>.
            value_element (str): O texto visível da opção a ser selecionada.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.XPATH, xpath_element))).select_by_visible_text(value_element)
            return True
        except Exception:
            return False

    def _preencher_input_por_xpath(self, xpath_element: str, value: str, rapido=False) -> bool:
        """
        Preenche um campo de entrada identificado pelo XPath.

        Args:
            xpath_element (str): O XPath do campo de entrada.
            value (str): O valor a ser inserido no campo.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.XPATH, xpath_element)))
            elemento.clear()
            elemento.send_keys(value)
            return True
        except Exception:
            return False

    def _click_por_xpath(self, xpath_element: str, rapido=False) -> bool:
        """
        Clica em um elemento identificado pelo XPath.

        Args:
            xpath_element (str): O XPath do elemento a ser clicado.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(element_to_be_clickable((By.XPATH, xpath_element))).click()
            return True
        except Exception:
            return False

    def _click_por_xpath_se_existe(self, xpath_element: str, rapido=False) -> bool:
        """
        Clica em um elemento identificado pelo XPath, se ele existir.

        Args:
            xpath_element (str): O XPath do elemento a ser clicado.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(element_to_be_clickable((By.XPATH, xpath_element)))
            elemento.click()
            return True
        except Exception:
            return False

    def _existe_xpath(self, id_element: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o XPath especificado.

        Args:
            id_element (str): O XPath do elemento a ser verificado.

        Returns:
            bool: True se pelo menos um elemento com o XPath existir, False caso contrário.
        """
        time.sleep(1)
        return len(self.webbot.find_elements(By.XPATH, id_element)) > 0

    def _verificar_texto_por_xpath(self, id_element: str, text: str) -> bool:
        """
        Verifica se o texto de um elemento identificado pelo XPath corresponde ao texto fornecido.

        Args:
            id_element (str): O XPath do elemento.
            text (str): O texto a ser verificado.

        Returns:
            bool: True se o texto corresponder, False caso contrário.
        """
        time.sleep(1)
        return self.webbot.find_element(By.XPATH, id_element).text.upper() == text.upper()

    def _verificar_atributo_por_xpath(self, xpath_element: str, atributo: str, valor: str, rapido=False) -> bool:
        """
        Verifica se um atributo de um elemento identificado pelo XPath corresponde ao valor fornecido.

        Args:
            xpath_element (str): O XPath do elemento.
            atributo (str): O nome do atributo a ser verificado.
            valor (str): O valor esperado do atributo.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o valor do atributo corresponder, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.XPATH, xpath_element)))
            return elemento.get_attribute(atributo) == valor
        except Exception:
            return False

    def _esperar_elemento_invisivel_por_xpath(self, xpath_element: str, rapido=False) -> bool:
        """
        Espera até que um elemento identificado pelo XPath se torne invisível.

        Args:
            xpath_element (str): O XPath do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o elemento se tornar invisível, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(lambda driver: not driver.find_element(By.XPATH, xpath_element).is_displayed())
            return True
        except Exception:
            return False

    def _esperar_elemento_visivel_por_xpath(self, xpath_element: str, rapido=False) -> bool:
        """
        Espera até que um elemento identificado pelo XPath se torne visível.

        Args:
            xpath_element (str): O XPath do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o elemento se tornar visível, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.XPATH, xpath_element)))
            return True
        except Exception:
            return False

    def _obter_texto_por_xpath(self, xpath_element: str, rapido=False) -> str:
        """
        Obtém o texto de um elemento identificado pelo XPath.

        Args:
            xpath_element (str): O XPath do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            str: O texto do elemento. Se o elemento não for encontrado, retorna uma string vazia.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.XPATH, xpath_element)))
            return elemento.text
        except Exception:
            return ""

    def _esperar_elemento_estado_por_xpath(self, xpath_element: str, estado: bool, rapido=False) -> bool:
        """
        Espera até que um elemento identificado pelo XPath esteja no estado desejado (visível ou invisível).

        Args:
            xpath_element (str): O XPath do elemento.
            estado (bool): True para esperar o elemento visível, False para invisível.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o elemento estiver no estado desejado, False caso contrário.
        """
        try:
            if estado:
                return self._esperar_elemento_visivel_por_xpath(xpath_element, rapido)
            else:
                return self._esperar_elemento_invisivel_por_xpath(xpath_element, rapido)
        except Exception:
            return False

    def _scroll_para_elemento_por_xpath(self, xpath_element: str) -> bool:
        try:
            elemento = self.webbot.find_element(By.XPATH, xpath_element)
            self.webbot.execute_script("arguments[0].scrollIntoView();", elemento)
            return True
        except Exception:
            return False

    def _verificar_elemento_ativado_por_xpath(self, xpath_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo seletor XPath está ativado.

        Um elemento é considerado ativado se pode ser interagido (clicado, selecionado, etc.).

        Args:
            xpath_element (str): O seletor XPath do elemento a ser verificado.

        Returns:
            bool: True se o elemento estiver ativado, False caso contrário.
        """
        try:
            return self.webbot.find_element(By.XPATH, xpath_element).is_enabled()
        except Exception:
            return False

    def _verificar_elemento_selecionado_por_xpath(self, xpath_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo seletor XPath está selecionado.

        Um elemento é considerado selecionado se estiver marcado (por exemplo, em um checkbox ou radio button).

        Args:
            xpath_element (str): O seletor XPath do elemento a ser verificado.

        Returns:
            bool: True se o elemento estiver selecionado, False caso contrário.
        """
        try:
            return self.webbot.find_element(By.XPATH, xpath_element).is_selected()
        except Exception:
            return False

    def _verificar_texto_contido_por_xpath(self, xpath_element: str, texto: str) -> bool:
        """
        Verifica se o texto fornecido está contido no texto de um elemento identificado pelo seletor XPath.

        O método busca o texto dentro do conteúdo do elemento especificado pelo XPath.

        Args:
            xpath_element (str): O seletor XPath do elemento a ser verificado.
            texto (str): O texto a ser verificado como contido no texto do elemento.

        Returns:
            bool: True se o texto estiver contido, False caso contrário.
        """
        try:
            return texto in self.webbot.find_element(By.XPATH, xpath_element).text
        except Exception:
            return False
